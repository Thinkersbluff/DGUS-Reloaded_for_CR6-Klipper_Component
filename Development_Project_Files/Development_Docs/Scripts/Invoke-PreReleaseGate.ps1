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
# Scripts folder is at: <root>\Development_Project_Files\Development_Docs\Scripts
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

# Release notes
$ReleaseNotes = Join-Path $RepoRoot "Development_Project_Files\Development_Environment\klippy\extras\Release Notes_v$Version.txt"

# 1) Required files
@(
    $CompatFile,
    $ManualFile,
    $PrimerFile,
    $ReleaseSop,
    $ChecklistFile,
    $InstallReadme,
    $ClaimsFilePath,
    $ReleaseNotes
) | ForEach-Object { Assert-Exists $_ }

# 2) Compatibility table contains version
$CompatText = Get-Content -LiteralPath $CompatFile -Raw
if ($CompatText -notmatch [regex]::Escape($Version)) {
    throw "Version '$Version' not found in Compatibility_and_Version_Mapping.md. Update the table before release."
}
Write-Host "Compatibility table check passed."

# 3) Merge conflict markers
# git grep exits 0 = matches found (bad), 1 = no matches (good), >1 = error
Push-Location $RepoRoot
try {
    $ConflictPattern = '^(<<<<<<< .+|=======|>>>>>>> .+)$'
    $Conflicts = git --no-pager grep -n -E $ConflictPattern -- . 2>$null
    $grepExit = $LASTEXITCODE

    if ($grepExit -gt 1) {
        throw "git grep failed with exit code $grepExit"
    }
    if ($grepExit -eq 0 -and $Conflicts) {
        Write-Host $Conflicts
        throw "Conflict markers detected in repository files."
    }
    Write-Host "Conflict marker check passed."

    # 4) Clean working tree (local only, skip in CI)
    if (-not $CI) {
        $Status = git status --porcelain
        if ($Status) {
            throw "Working tree is not clean. Commit or stash changes before release."
        }
        Write-Host "Working tree check passed."
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
Write-Host "Release notes check passed."

# 6) Claims validation
$ClaimsValidator = Join-Path $PSScriptRoot "Validate-ClaimsFile.ps1"
Assert-Exists $ClaimsValidator
& $ClaimsValidator -ClaimsFile $ClaimsFilePath
$claimsExit = $LASTEXITCODE
if ($claimsExit -ne 0) {
    throw "Claims validation failed with exit code $claimsExit"
}

Write-Host "All pre-release checks passed for v$Version"
exit 0