param(
    [Parameter(Mandatory = $true)]
    [string]$ClaimsFile,

    [switch]$AllowPlaceholders
)

$ErrorActionPreference = "Stop"

function Test-Checked([string]$Mark) {
    return $Mark -match '^[xX]$'
}

function Get-UrlFromText([string]$Text) {
    if (-not $Text) { return $null }

    $md = [regex]::Match($Text, '\((https?://[^)\s]+)\)')
    if ($md.Success) { return $md.Groups[1].Value }

    $raw = [regex]::Match($Text, '(https?://\S+)')
    if ($raw.Success) { return $raw.Groups[1].Value.TrimEnd(')', '.', ',') }

    return $null
}

function Test-PlaceholderValue([string]$Text) {
    if (-not $Text) { return $true }
    $t = $Text.Trim()
    if ($t -match '^(NA|N/A|`?NA`?)$') { return $true }
    if ($t -match '<[A-Z0-9_]+>') { return $true }
    return $false
}

if (-not (Test-Path -LiteralPath $ClaimsFile)) {
    throw "Claims file not found: $ClaimsFile"
}

$content = Get-Content -LiteralPath $ClaimsFile -Raw
if (-not $content) {
    throw "Claims file is empty: $ClaimsFile"
}

$blocks = [regex]::Split($content, '(?m)(?=^##\s+Claim\s+\d+:)') | Where-Object { $_ -match '^##\s+Claim\s+\d+:' }
if ($blocks.Count -eq 0) {
    throw "No claim sections found. Expected headings like: '## Claim N: ...'"
}

$errors = New-Object System.Collections.Generic.List[string]

$requiredValidationItems = @(
    "Pre-fix behavior documented",
    "Post-fix test steps documented",
    "Confirmed correct operation on Dev SE",
    "Result confirms claim"
)

$impactQuestions = @(
    "Breaks previous DWIN-t5uid1 interface contract?",
    "Breaks previous Klipper-t5uid1 interface contract?",
    "Breaks previous Klipper-mcu interface contract?",
    "Impacts printer_data?",
    "Changes the back-end?",
    "Changes the front-end?"
)

foreach ($block in $blocks) {
    $header = [regex]::Match($block, '(?m)^##\s+Claim\s+(\d+):\s*(.+)$')
    if (-not $header.Success) {
        $errors.Add("Malformed claim heading.")
        continue
    }

    $claimNo = $header.Groups[1].Value

    foreach ($item in $requiredValidationItems) {
        $pat = '(?mi)^\s*-\s*\[(?<m>[ xX])\]\s*' + [regex]::Escape($item) + '\s*$'
        $m = [regex]::Match($block, $pat)
        if (-not $m.Success) {
            $errors.Add("Claim ${claimNo}: missing validation checkbox '$item'.")
            continue
        }
        if (-not (Test-Checked $m.Groups['m'].Value)) {
            $errors.Add("Claim ${claimNo}: validation item not checked '$item'.")
        }
    }

    $issueLine  = [regex]::Match($block, '(?mi)^\s*-\s*Issue:\s*(?<v>.+)$')
    $commitLine = [regex]::Match($block, '(?mi)^\s*-\s*Fix commit\(s\):\s*(?<v>.+)$')

    if (-not $issueLine.Success) {
        $errors.Add("Claim ${claimNo}: missing 'Issue:' evidence line.")
    }
    if (-not $commitLine.Success) {
        $errors.Add("Claim ${claimNo}: missing 'Fix commit(s):' evidence line.")
    }

    if ($issueLine.Success -and -not $AllowPlaceholders) {
        $issueVal = $issueLine.Groups['v'].Value.Trim()
        $issueUrl = Get-UrlFromText $issueVal
        if ((Test-PlaceholderValue $issueVal) -or -not $issueUrl) {
            $errors.Add("Claim ${claimNo}: Issue evidence must contain a real URL.")
        }
    }

    if ($commitLine.Success -and -not $AllowPlaceholders) {
        $commitVal = $commitLine.Groups['v'].Value.Trim()
        $commitUrl = Get-UrlFromText $commitVal
        if ((Test-PlaceholderValue $commitVal) -or -not $commitUrl) {
            $errors.Add("Claim ${claimNo}: Fix commit evidence must contain a real URL.")
        }
    }

    foreach ($q in $impactQuestions) {
        $qEsc = [regex]::Escape($q)
        $pat = '(?mis)^\s*-\s*' + $qEsc + '\s*$\s*^\s*-\s*\[(?<yes>[ xX])\]\s*Yes\s*$\s*^\s*-\s*\[(?<no>[ xX])\]\s*No\s*$'
        $m = [regex]::Match($block, $pat)
        if (-not $m.Success) {
            $errors.Add("Claim ${claimNo}: malformed or missing Yes/No pair for '$q'.")
            continue
        }

        $yesChecked = Test-Checked $m.Groups['yes'].Value
        $noChecked  = Test-Checked $m.Groups['no'].Value

        if (($yesChecked -and $noChecked) -or (-not $yesChecked -and -not $noChecked)) {
            $errors.Add("Claim ${claimNo}: '$q' must have exactly one of Yes/No checked.")
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Host "Claims validation failed:`n" -ForegroundColor Red
    $errors | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    throw "Claims file validation failed with $($errors.Count) issue(s)."
}

Write-Host "Claims validation passed: $ClaimsFile"