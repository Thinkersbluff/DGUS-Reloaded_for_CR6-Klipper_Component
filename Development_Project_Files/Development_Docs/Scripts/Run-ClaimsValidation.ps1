param(
    [string]$ClaimsFile,
    [switch]$Draft
)

$ErrorActionPreference = "Stop"

$validator = Join-Path $PSScriptRoot "Validate-ClaimsFile.ps1"
if (-not (Test-Path -LiteralPath $validator)) { throw "Validator not found: $validator" }

if (-not $ClaimsFile) {
    $ClaimsFile = Get-ChildItem (Join-Path $PSScriptRoot "..\Verification") -Filter "Claims_v*.md" -File |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1 -ExpandProperty FullName
}
if (-not $ClaimsFile) { throw "No Claims_v*.md found in Verification." }

$claims = (Resolve-Path -LiteralPath $ClaimsFile).Path
$verificationDir = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\Verification")).Path
$stamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$logFile = Join-Path $verificationDir "ClaimsCheck_$stamp.txt"

$exitCode = 0
Start-Transcript -Path $logFile -Force | Out-Null
try {
    Write-Host "Claims file: $claims"
    Write-Host "Mode: $(if ($Draft) { 'DRAFT' } else { 'STRICT' })"
    if ($Draft) { & $validator -ClaimsFile $claims -AllowPlaceholders }
    else { & $validator -ClaimsFile $claims }
    Write-Host "PASS"
}
catch {
    $exitCode = 1
    Write-Host "FAIL"
    Write-Host $_.Exception.Message
}
finally {
    Write-Host "Log file: $logFile"
    Stop-Transcript | Out-Null
}
exit $exitCode