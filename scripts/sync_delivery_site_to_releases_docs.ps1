param(
    [Parameter(Mandatory = $true)]
    [string]$DeliveryPath,

    [Parameter(Mandatory = $true)]
    [string]$ReleasesRepoPath,

    [string]$CommitMessage,

    [switch]$DryRun,

    [switch]$NoPush
)

$ErrorActionPreference = "Stop"

$delivery = (Resolve-Path $DeliveryPath).Path
$releases = (Resolve-Path $ReleasesRepoPath).Path
$docs = Join-Path $releases "docs"

if (-not (Test-Path (Join-Path $releases ".git"))) {
    throw "Repositorio de releases sem .git: $releases"
}

if (-not (Test-Path $docs)) {
    New-Item -ItemType Directory -Path $docs -Force | Out-Null
}

$leaf = Split-Path $delivery -Leaf
if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
    $CommitMessage = "site: sync delivery/$leaf para docs/"
}

$entries = Get-ChildItem -LiteralPath $delivery -Force

Write-Host "Fonte: $delivery"
Write-Host "Destino: $docs"
Write-Host "DryRun: $DryRun"

foreach ($entry in $entries) {
    if ($entry.Name -eq ".git") { continue }

    $dest = Join-Path $docs $entry.Name
    if ($DryRun) {
        Write-Host "[dry-run] Copiar $($entry.FullName) -> $dest"
        continue
    }

    Copy-Item -LiteralPath $entry.FullName -Destination $dest -Recurse -Force
}

Push-Location $releases
try {
    git add docs

    if ($DryRun) {
        git status --short
        return
    }

    git diff --cached --quiet 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Nenhuma alteracao para commit em $releases"
        return
    }

    git commit -m $CommitMessage

    if ($NoPush) {
        Write-Host "Commit criado com -NoPush."
        return
    }

    git push origin HEAD
    Write-Host "Sync concluido e enviado para origin."
}
finally {
    Pop-Location
}
