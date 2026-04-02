param(
    [string]$RootPath = "d:\dev",
    [switch]$Fix
)

$ErrorActionPreference = "Stop"

$repoDirs = Get-ChildItem -Path $RootPath -Directory |
    Where-Object { $_.Name -like "caracore-*" -or $_.Name -like "circuito*" }

$readmes = foreach ($repo in $repoDirs) {
    $readme = Join-Path $repo.FullName "README.md"
    if (Test-Path $readme) { $readme }
}

if (-not $readmes) {
    Write-Host "No README.md files found in target repositories."
    exit 0
}

# Mojibake markers typically produced by UTF-8 text decoded as CP1252/Latin1.
# Match suspicious lead bytes followed by CP1252 continuation range.
$mojibakePattern = '\u00C3[\u0080-\u00BF]|\u00C2[\u0080-\u00BF]|\u00E2[\u0080-\u00BF]{1,2}|\uFFFD'
$cp1252 = [Text.Encoding]::GetEncoding(1252)
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$issues = @()

foreach ($file in $readmes) {
    $raw = Get-Content -Path $file -Raw -Encoding UTF8
    $matchesBefore = [regex]::Matches($raw, $mojibakePattern).Count

    if ($matchesBefore -le 0) {
        continue
    }

    $fixed = [Text.Encoding]::UTF8.GetString($cp1252.GetBytes($raw))
    $matchesAfter = [regex]::Matches($fixed, $mojibakePattern).Count

    $changed = $false
    if ($Fix -and $matchesAfter -lt $matchesBefore) {
        [IO.File]::WriteAllText($file, $fixed, $utf8NoBom)
        $changed = $true
    }

    $issues += [pscustomobject]@{
        File = $file
        MarkersBefore = $matchesBefore
        MarkersAfter = $matchesAfter
        Fixed = $changed
    }
}

if (-not $issues) {
    Write-Host "Encoding check passed: no mojibake markers found."
    exit 0
}

Write-Host "Potential encoding issues:" -ForegroundColor Yellow
$issues | Sort-Object File | Format-Table -AutoSize

$remaining = @(
    if ($Fix) {
        $issues | Where-Object { -not $_.Fixed }
    }
    else {
        $issues
    }
)

if ($remaining.Count -gt 0) {
    Write-Host "Encoding check failed. Remaining files with potential issues: $($remaining.Count)" -ForegroundColor Red
    exit 1
}

if ($Fix) {
    Write-Host "Encoding check passed after auto-fix." -ForegroundColor Green
}
else {
    Write-Host "Encoding check passed." -ForegroundColor Green
}
exit 0
