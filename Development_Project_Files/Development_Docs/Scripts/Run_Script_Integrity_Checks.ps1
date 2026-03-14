param(
    [string]$RepoRoot,
    [switch]$Apply,
    [switch]$FailOnFindings
)

$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
    param([string]$ProvidedRoot)

    if ($ProvidedRoot) {
        if (-not (Test-Path -LiteralPath $ProvidedRoot)) {
            throw "RepoRoot not found: $ProvidedRoot"
        }
        return (Resolve-Path -LiteralPath $ProvidedRoot).Path
    }

    $gitRoot = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -eq 0 -and $gitRoot) {
        return $gitRoot.Trim()
    }

    return (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
}

function Write-Log {
    param(
        [string]$Message,
        [string]$LogFile
    )
    Write-Host $Message
    Add-Content -LiteralPath $LogFile -Value $Message -Encoding UTF8
}

function Get-LineNumber {
    param(
        [string]$Text,
        [int]$Index
    )
    if ($Index -le 0) { return 1 }
    return ([regex]::Matches($Text.Substring(0, $Index), "`n")).Count + 1
}

function Get-LineText {
    param(
        [string]$Text,
        [int]$LineNumber
    )
    $lines = $Text -split "`r?`n"
    if ($LineNumber -lt 1 -or $LineNumber -gt $lines.Count) { return "" }
    return $lines[$LineNumber - 1].Trim()
}

$RepoRoot = Resolve-RepoRoot -ProvidedRoot $RepoRoot

$VerificationDir = Join-Path $RepoRoot "Development_Project_Files\Development_Docs\Verification"
if (-not (Test-Path -LiteralPath $VerificationDir)) {
    New-Item -ItemType Directory -Path $VerificationDir -Force | Out-Null
}

$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$LogFile = Join-Path $VerificationDir "Script_Integrity_Findings_$Timestamp.txt"

# Regex-based migration rules (targeted)
$Rules = @(
    @{
        Name        = "Old pre-release script name"
        Pattern     = '\bpre_release_checks\.ps1\b'
        Replacement = 'Invoke-PreReleaseGate.ps1'
    },
    @{
        Name        = "Old claims script name"
        Pattern     = '\bverify_claims\.ps1\b'
        Replacement = 'Validate-ClaimsFile.ps1'
    },
    @{
        Name        = "Old docs root path (slash)"
        Pattern     = '(?<!Development_Project_Files/)Development_Docs/'
        Replacement = 'Development_Project_Files/Development_Docs/'
    },
    @{
        Name        = "Old docs root path (backslash)"
        Pattern     = '(?<!Development_Project_Files\\)Development_Docs\\'
        Replacement = 'Development_Project_Files\Development_Docs\'
    },
    @{
        Name        = "Old env folder (slash)"
        Pattern     = 'Development_Project_Files/Dev_Environment/'
        Replacement = 'Development_Project_Files/Development_Environment/'
    },
    @{
        Name        = "Old env folder (backslash)"
        Pattern     = 'Development_Project_Files\\Dev_Environment\\'
        Replacement = 'Development_Project_Files\Development_Environment\'
    }
)

@(
    "Script Integrity Check Findings"
    "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    "RepoRoot : $RepoRoot"
    "Apply    : $Apply"
    "FailOnFindings: $FailOnFindings"
    "------------------------------------------------------------"
) | Set-Content -LiteralPath $LogFile -Encoding UTF8

$Findings = New-Object System.Collections.Generic.List[object]
$ChangedFiles = New-Object System.Collections.Generic.List[string]

try {
    $Targets = Get-ChildItem -LiteralPath $RepoRoot -Recurse -File -Include *.ps1,*.md,*.txt,*.yml,*.yaml |
        Where-Object {
            $_.FullName -notmatch '\\\.git\\' -and
            $_.FullName -notmatch '\\ci_build\\' -and
            $_.FullName -notmatch '\\Development_Project_Files\\Development_Docs\\Verification\\Script_Integrity_Findings_.*\.txt$' -and
            $_.Name -ne 'Run_Script_Integrity_Checks.ps1' -and
            $_.Length -lt 2MB
        }

    foreach ($File in $Targets) {
        $Original = Get-Content -LiteralPath $File.FullName -Raw
        $Updated = $Original
        $FileChanged = $false

        foreach ($Rule in $Rules) {
            $ruleMatches = [regex]::Matches($Updated, $Rule.Pattern)
            if ($ruleMatches.Count -eq 0) { continue }

            foreach ($m in $ruleMatches) {
                $lineNum = Get-LineNumber -Text $Updated -Index $m.Index
                $lineTxt = Get-LineText -Text $Updated -LineNumber $lineNum
                $Findings.Add([pscustomobject]@{
                    File    = $File.FullName.Replace($RepoRoot, ".")
                    Line    = $lineNum
                    Rule    = $Rule.Name
                    Found   = $m.Value
                    Replace = $Rule.Replacement
                    Excerpt = $lineTxt
                })
            }

            if ($Apply) {
                $Updated = [regex]::Replace($Updated, $Rule.Pattern, $Rule.Replacement)
                $FileChanged = $true
            }
        }

        if ($Apply -and $FileChanged -and $Updated -ne $Original) {
            Set-Content -LiteralPath $File.FullName -Value $Updated -Encoding UTF8 -NoNewline
            $ChangedFiles.Add($File.FullName.Replace($RepoRoot, "."))
        }
    }

    if ($Findings.Count -eq 0) {
        Write-Log -Message "No stale references found." -LogFile $LogFile
        Write-Log -Message "------------------------------------------------------------" -LogFile $LogFile
        Write-Log -Message "LogFile : $LogFile" -LogFile $LogFile
        exit 0
    }

    Write-Log -Message "Summary by rule:" -LogFile $LogFile
    foreach ($g in ($Findings | Group-Object Rule | Sort-Object Name)) {
        Write-Log -Message (" - {0}: {1} hit(s)" -f $g.Name, $g.Count) -LogFile $LogFile
    }

    Write-Log -Message "" -LogFile $LogFile
    Write-Log -Message "Detailed findings:" -LogFile $LogFile
    Write-Log -Message "Format: <file>:<line> | <rule> | found='<token>' -> new='<replacement>'" -LogFile $LogFile
    foreach ($f in ($Findings | Sort-Object File, Line, Rule)) {
        Write-Log -Message ("{0}:{1} | {2} | found='{3}' -> new='{4}'" -f $f.File, $f.Line, $f.Rule, $f.Found, $f.Replace) -LogFile $LogFile
        Write-Log -Message ("    {0}" -f $f.Excerpt) -LogFile $LogFile
    }

    if ($Apply) {
        Write-Log -Message "" -LogFile $LogFile
        Write-Log -Message "Applied fixes to $($ChangedFiles.Count) file(s):" -LogFile $LogFile
        foreach ($c in ($ChangedFiles | Sort-Object)) {
            Write-Log -Message " - $c" -LogFile $LogFile
        }
        Write-Log -Message "Review changes with: git diff" -LogFile $LogFile
    }
    else {
        Write-Log -Message "" -LogFile $LogFile
        Write-Log -Message "Dry run only. Re-run with -Apply to fix." -LogFile $LogFile
    }

    Write-Log -Message "------------------------------------------------------------" -LogFile $LogFile
    Write-Log -Message "LogFile : $LogFile" -LogFile $LogFile

    if ($FailOnFindings) { exit 2 } else { exit 0 }
}
catch {
    Write-Log -Message "ERROR: $($_.Exception.Message)" -LogFile $LogFile
    Write-Log -Message "------------------------------------------------------------" -LogFile $LogFile
    Write-Log -Message "LogFile : $LogFile" -LogFile $LogFile
    throw
}