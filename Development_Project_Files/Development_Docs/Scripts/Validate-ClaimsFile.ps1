param(
    [Parameter(Mandatory = $true)]
    [string]$ClaimsFile,
    [switch]$AllowPlaceholders
)

$ErrorActionPreference = "Stop"

function Test-Checked([string]$m) { $m -match '^[xX]$' }

function Get-Urls([string]$text) {
    if (-not $text) { return @() }
    $urlMatches = [regex]::Matches($text, 'https?://[^\s\)`>]+')
    $urls = @()
    foreach ($u in $urlMatches) { $urls += $u.Value.TrimEnd(')', '.', ',') }
    return $urls
}

function Get-Section([string]$text, [string]$heading) {
    $m = [regex]::Match($text, "(?ms)^\s*###\s*$heading\s*$" + '(?:\r?\n)' + "(?<b>.*?)(?=^\s*###\s+|\Z)")
    if ($m.Success) { return $m.Groups['b'].Value }
    return $null
}

function Get-QuestionBlock([string]$impact, [string]$q) {
    $e = [regex]::Escape($q)
    $m = [regex]::Match($impact, "(?ms)^\s*-\s*$e\s*$" + '(?:\r?\n)' + "(?<b>.*?)(?=^\s*-\s*[^\r\n]+\?\s*$|\Z)")
    if ($m.Success) { return $m.Groups['b'].Value }
    return $null
}

function Get-YesNo([string]$qb) {
    $yes = [regex]::Match($qb, '(?mi)^\s*-\s*\[(?<m>[ xX])\]\s*Yes\s*$')
    $no  = [regex]::Match($qb, '(?mi)^\s*-\s*\[(?<m>[ xX])\]\s*No\s*$')
    if (-not $yes.Success -or -not $no.Success) { return @{Valid=$false;State=$null} }
    $yc = Test-Checked $yes.Groups['m'].Value
    $nc = Test-Checked $no.Groups['m'].Value
    if (($yc -and $nc) -or (-not $yc -and -not $nc)) { return @{Valid=$false;State=$null} }
    return @{Valid=$true;State=($(if ($yc) {"Yes"} else {"No"}))}
}

if (-not (Test-Path -LiteralPath $ClaimsFile)) { throw "Claims file not found: $ClaimsFile" }
$content = Get-Content -LiteralPath $ClaimsFile -Raw
$claims = [regex]::Split($content, '(?m)(?=^##\s+Claim\s+\d+:)') | Where-Object { $_ -match '^##\s+Claim\s+\d+:' }
if ($claims.Count -eq 0) { throw "No claim sections found." }

$errors = New-Object System.Collections.Generic.List[string]

$requiredChecks = @(
    "Pre-fix behavior documented",
    "Post-fix test steps documented",
    "Confirmed correct operation on Dev SE",
    "Result confirms claim"
)

$impactQuestions = @(
    "Impacts printer_data?",
    "Changes t5uid1 extras?",
    "Changes klipper.bin?",
    "Changes klipper/src?",
    "Changes DWIN_SET?"
)

$componentQuestions = @(
    "Impacts printer_data?",
    "Changes t5uid1 extras?",
    "Changes klipper.bin?",
    "Changes klipper/src?",
    "Changes DWIN_SET?"
)

foreach ($c in $claims) {
    $h = [regex]::Match($c, '(?m)^##\s+Claim\s+(\d+):')
    $n = if ($h.Success) { $h.Groups[1].Value } else { "?" }

    foreach ($item in $requiredChecks) {
        $m = [regex]::Match($c, '(?mi)^\s*-\s*\[(?<x>[ xX])\]\s*' + [regex]::Escape($item) + '\s*$')
        if (-not $m.Success) { $errors.Add("Claim ${n}: missing '$item'."); continue }
        if (-not (Test-Checked $m.Groups['x'].Value)) { $errors.Add("Claim ${n}: unchecked '$item'.") }
    }

    $issue = [regex]::Match($c, '(?mi)^\s*-\s*Issue:\s*(?<v>.+)$')
    if (-not $issue.Success) { $errors.Add("Claim ${n}: missing Issue line.") }
    elseif (-not $AllowPlaceholders) {
        if ((Get-Urls $issue.Groups['v'].Value).Count -eq 0) { $errors.Add("Claim ${n}: Issue must include URL.") }
    }

    $impact = Get-Section $c 'Impact classification'
    if (-not $impact) { $errors.Add("Claim ${n}: missing Impact classification."); continue }

    $states = @{}
    foreach ($q in $impactQuestions) {
        $qb = Get-QuestionBlock $impact $q
        if (-not $qb) { $errors.Add("Claim ${n}: missing '$q'."); continue }
        $yn = Get-YesNo $qb
        if (-not $yn.Valid) { $errors.Add("Claim ${n}: '$q' must have exactly one of Yes/No checked."); continue }
        $states[$q] = @{State=$yn.State;Block=$qb}
    }

    foreach ($cq in $componentQuestions) {
        if ($states.ContainsKey($cq) -and $states[$cq].State -eq "Yes") {
            $qb = $states[$cq].Block
            if ($qb -notmatch '(?mi)^\s*-\s*Fix commit\(s\):') {
                $errors.Add("Claim ${n}: '$cq' is Yes but missing 'Fix commit(s):' label.")
                continue
            }
            if ((Get-Urls $qb).Count -eq 0) {
                $errors.Add("Claim ${n}: '$cq' is Yes but no fix commit URL found.")
            }
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Host "Claims validation failed:`n" -ForegroundColor Red
    $errors | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    throw "Claims file validation failed with $($errors.Count) issue(s)."
}

Write-Host "Claims validation passed: $ClaimsFile"