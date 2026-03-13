param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [Parameter(Mandatory = $true)]
    [string]$ClaimsFile,

    [switch]$CI
)

$ErrorActionPreference = "Stop"

function Assert-Exists([string]$PathToCheck) {
    if (-not (Test-Path -LiteralPath $PathToCheck)) {
        throw "Missing required file: $PathToCheck"
    }
}

# Resolve repo root:
# ...\Development_Project_Files\Development_Project_Files\Development_Docs\Scripts -> repo root = ..\..\..
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path

Write-Host "Running pre-release checks for v$Version"

# Canonical paths
$CompatFile    = Join-Path $RepoRoot "Development_Project_Files\Development_Docs\Compatibility_and_Version_Mapping.md"
$ManualFile    = Join-Path $RepoRoot "Development_Project_Files\Development_Docs\Development_Manual.md"
$PrimerFile    = Join-Path $RepoRoot "Development_Project_Files\Development_Docs\SOPs\00-Quick_Primer.md"
$ReleaseSop    = Join-Path $RepoRoot "Development_Project_Files\Development_Docs\SOPs\02-Release_Process.md"
$ChecklistFile = Join-Path $RepoRoot "Development_Project_Files\Development_Docs\Checklists\Release_Gate_Checklist.md"
$InstallReadme = Join-Path $RepoRoot "Installation_Files\README.md"

# Claims file may be relative; normalize to absolute
$ClaimsFilePath = if ([System.IO.Path]::IsPathRooted($ClaimsFile)) {
    $ClaimsFile
} else {
    Join-Path $RepoRoot $ClaimsFile
}

# Release notes: support both folder names
$ReleaseNotesA = Join-Path $RepoRoot "Development_Project_Files\Development_Environment\klippy\extras\Release Notes_v$Version.txt"
$ReleaseNotesB = Join-Path $RepoRoot "Development_Project_Files\Development_Environment\klippy\extras\Release Notes_v$Version.txt"
$ReleaseNotes  = if (Test-Path -LiteralPath $ReleaseNotesA) { $ReleaseNotesA } else { $ReleaseNotesB }

# 1) Required files
@(
    $CompatFile,
    $ManualFile,
    $PrimerFile,
    $ReleaseSop,
    $ChecklistFile,
    $InstallReadme,
    $ClaimsFilePath
) | ForEach-Object { Assert-Exists $_ }

Assert-Exists $ReleaseNotes

# 2) Compatibility table contains version
$CompatText = Get-Content -LiteralPath $CompatFile -Raw
if ($CompatText -notmatch [regex]::Escape($Version)) {
    throw "Version '$Version' not found in Compatibility_and_Version_Mapping.md. Update the table before release."
}
Write-Host "Compatibility table check passed."

# 3) Merge conflict markers (strict, avoids false positives from long ===== lines)
Push-Location $RepoRoot
try {
    # Valid conflict marker lines only:
    # <<<<<<< branch
    # =======
    # >>>>>>> branch
    $ConflictPattern = '^(<<<<<<< .+|=======|>>>>>>> .+)$'
    $Conflicts = git --no-pager grep -n -E $ConflictPattern -- . 2>$null

    if ($LASTEXITCODE -eq 0 -and $Conflicts) {
        Write-Host $Conflicts
        throw "Conflict markers detected in repository files."
    }

    # 4) Clean tree (local only)
    if (-not $CI) {
        $Status = git status --porcelain
        if ($Status) {
            throw "Working tree is not clean. Commit/stash changes before release."
        }
    }
}
finally {
    Pop-Location
}

# 5) Release notes contain version
$RnText = Get-Content -LiteralPath $ReleaseNotes -Raw
if ($RnText -notmatch [regex]::Escape($Version)) {
    throw "Version '$Version' not found in release notes file: $ReleaseNotes"
}

# 6) Claims gate
$ClaimsValidator = Join-Path $PSScriptRoot "Validate-ClaimsFile.ps1"
Assert-Exists $ClaimsValidator
& $ClaimsValidator -ClaimsFile $ClaimsFilePath

Write-Host "All pre-release checks passed for v$Version"