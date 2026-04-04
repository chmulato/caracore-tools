param(
    [ValidateSet("dashboard", "roadmap", "gate", "report")]
    [string]$Action = "dashboard",

    [string]$App,

    [int]$WindowDays = 120,

    [switch]$Strict
)

$ErrorActionPreference = "Stop"

$CatalogPath = Join-Path $PSScriptRoot "ecosystem-governance-catalog.json"
$DeliveryMapPath = Join-Path $PSScriptRoot "ecosystem-delivery-map.json"

if (-not (Test-Path $CatalogPath)) { throw "Catalogo nao encontrado: $CatalogPath" }
if (-not (Test-Path $DeliveryMapPath)) { throw "Mapa de delivery nao encontrado: $DeliveryMapPath" }

$Catalog = Get-Content -Path $CatalogPath -Raw -Encoding UTF8 | ConvertFrom-Json
$DeliveryMap = Get-Content -Path $DeliveryMapPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Today = (Get-Date).Date

function Get-DeliveryConfig {
    param([string]$AppId)
    return $DeliveryMap | Where-Object { $_.app -ieq $AppId } | Select-Object -First 1
}

function Get-TokenStatus {
    param([object]$DeliveryCfg)

    if (-not $DeliveryCfg -or -not $DeliveryCfg.requiredTokens -or $DeliveryCfg.requiredTokens.Count -eq 0) {
        return "n/a"
    }

    foreach ($name in $DeliveryCfg.requiredTokens) {
        if (Get-ChildItem "Env:$name" -ErrorAction SilentlyContinue) {
            return "ok:$name"
        }
    }

    return "missing"
}

function Get-RoadmapDate {
    param([string]$DateText)

    if ([string]::IsNullOrWhiteSpace($DateText)) {
        return $null
    }

    try {
        return ([datetime]$DateText).Date
    }
    catch {
        return $null
    }
}

function Get-RepoState {
    param([string]$Path)

    $exists = Test-Path $Path
    if (-not $exists) {
        return [pscustomobject]@{
            exists = $false
            isGit = $false
            dirty = $null
            branch = ""
            path = $Path
        }
    }

    $gitDir = Join-Path $Path ".git"
    if (-not (Test-Path $gitDir)) {
        return [pscustomobject]@{
            exists = $true
            isGit = $false
            dirty = $null
            branch = ""
            path = $Path
        }
    }

    $branch = ""
    $dirtyCount = 0

    try {
        $branch = (git -C $Path rev-parse --abbrev-ref HEAD 2>$null)
        $statusLines = @(git -C $Path status --porcelain 2>$null)
        $dirtyCount = $statusLines.Count
    }
    catch {
        $branch = ""
        $dirtyCount = 0
    }

    return [pscustomobject]@{
        exists = $true
        isGit = $true
        dirty = $dirtyCount
        branch = $branch
        path = $Path
    }
}

function Find-GitRoot {
    param([string]$StartPath)

    $p = Resolve-Path $StartPath -ErrorAction SilentlyContinue
    if (-not $p) { return $null }

    $current = $p.Path
    while ($current) {
        if (Test-Path (Join-Path $current ".git")) {
            return $current
        }
        $parent = Split-Path $current -Parent
        if (-not $parent -or $parent -eq $current) { break }
        $current = $parent
    }

    return $null
}

function Get-ForbiddenMatrixChanges {
    param([object]$Item)

    if (-not $Item.forbidBinaryDeliveryInMatrix -or -not $Item.matrixForbiddenPaths) {
        return @()
    }

    $gitRoot = Find-GitRoot -StartPath $Item.matrixDeliveryPath
    if (-not $gitRoot) {
        return @()
    }

    $changes = @()
    foreach ($relPath in $Item.matrixForbiddenPaths) {
        $path = $relPath.Replace('/', '\\')
        $status = @(git -C $gitRoot status --porcelain -- $path 2>$null)
        if ($status.Count -gt 0) {
            $changes += $relPath
        }
    }

    return $changes
}

function Get-AppSnapshot {
    param([object]$Item)

    $delivery = Get-DeliveryConfig -AppId $Item.app
    $token = Get-TokenStatus -DeliveryCfg $delivery
    $roadmapDate = Get-RoadmapDate -DateText $Item.roadmapDate
    $daysTo = $null
    if ($roadmapDate) {
        $daysTo = [int](($roadmapDate - $Today).TotalDays)
    }

    $source = Get-RepoState -Path $Item.sourceRepoPath
    $release = Get-RepoState -Path $Item.releaseRepoPath
    $matrixExists = Test-Path $Item.matrixDeliveryPath
    $releaseDocsExists = Test-Path (Join-Path $Item.releaseRepoPath $Item.releaseDocsPath)
    $forbiddenMatrixChanges = Get-ForbiddenMatrixChanges -Item $Item
    $releaseRepoLeaf = Split-Path $Item.releaseRepoPath -Leaf
    $usesDedicatedReleasesRepo = $releaseRepoLeaf -like "*-releases"

    $commandExists = $false
    if ($delivery -and $delivery.commandPath -and $delivery.repoPath) {
        $commandExists = Test-Path (Join-Path $delivery.repoPath $delivery.commandPath)
    }

    return [pscustomobject]@{
        app = $Item.app
        displayName = $Item.displayName
        category = $Item.category
        roadmapStatus = $Item.roadmapStatus
        roadmapDate = $Item.roadmapDate
        daysToRoadmap = $daysTo
        commandExists = $commandExists
        token = $token
        matrixExists = $matrixExists
        releaseDocsExists = $releaseDocsExists
        releaseRepoLeaf = $releaseRepoLeaf
        usesDedicatedReleasesRepo = $usesDedicatedReleasesRepo
        releaseChannelPolicy = $Item.releaseChannelPolicy
        forbiddenMatrixChanges = $forbiddenMatrixChanges
        officialReleaseRepo = $Item.officialReleaseRepo
        sourceDirty = $source.dirty
        releaseDirty = $release.dirty
        sourceBranch = $source.branch
        releaseBranch = $release.branch
    }
}

function Build-GateResult {
    param([object]$Snapshot)

    $checks = @()

    $checks += [pscustomobject]@{
        name = "Seguranca"
        status = if ($Snapshot.token -eq "missing") { "BLOQUEADO" } else { "APROVADO" }
        detail = if ($Snapshot.token -eq "missing") { "Token de delivery ausente para comando configurado." } else { "Token disponivel ou nao aplicavel." }
        critical = $true
    }

    $checks += [pscustomobject]@{
        name = "Consistencia Delivery-Matriz-Loja"
        status = if ($Snapshot.matrixExists -and $Snapshot.releaseDocsExists) { "APROVADO" } else { "BLOQUEADO" }
        detail = if ($Snapshot.matrixExists -and $Snapshot.releaseDocsExists) { "Paths de matriz e docs da loja encontrados." } else { "Path ausente em matriz ou docs da loja." }
        critical = $true
    }

    $checks += [pscustomobject]@{
        name = "Automacao"
        status = if ($Snapshot.commandExists) { "APROVADO" } else { "BLOQUEADO" }
        detail = if ($Snapshot.commandExists) { "Comando de delivery encontrado no ecossistema." } else { "Comando de delivery nao encontrado." }
        critical = $true
    }

    $checks += [pscustomobject]@{
        name = "Canal Oficial de Release"
        status = if ($Snapshot.usesDedicatedReleasesRepo) { "APROVADO" } else { "BLOQUEADO" }
        detail = if ($Snapshot.usesDedicatedReleasesRepo) {
            "Repositorio de release dedicado confirmado: " + $Snapshot.releaseRepoLeaf
        } else {
            "Repositorio de release fora do padrao *-releases: " + $Snapshot.releaseRepoLeaf
        }
        critical = $true
    }

    $hasForbiddenMatrixChanges = ($Snapshot.forbiddenMatrixChanges -and $Snapshot.forbiddenMatrixChanges.Count -gt 0)
    $checks += [pscustomobject]@{
        name = "Politica de Artefato na Matriz"
        status = if ($hasForbiddenMatrixChanges) { "BLOQUEADO" } else { "APROVADO" }
        detail = if ($hasForbiddenMatrixChanges) {
            "Arquivos de artefato alterados na matriz: " + ($Snapshot.forbiddenMatrixChanges -join ", ") + ". Publique binarios apenas na loja oficial: " + $Snapshot.officialReleaseRepo
        } else {
            "Matriz sem alteracoes de artefatos proibidos para este app."
        }
        critical = $true
    }

    $dirtyOk = (($Snapshot.sourceDirty -eq 0) -and ($Snapshot.releaseDirty -eq 0))
    $checks += [pscustomobject]@{
        name = "Integridade Git"
        status = if ($dirtyOk) { "APROVADO" } else { "APROVADO COM RESSALVAS" }
        detail = if ($dirtyOk) { "Repositorios fonte e release limpos." } else { "Alteracoes locais detectadas em fonte ou release." }
        critical = $false
    }

    $criticalFailed = @($checks | Where-Object { $_.critical -and $_.status -eq "BLOQUEADO" }).Count
    $highWarnings = @($checks | Where-Object { -not $_.critical -and $_.status -ne "APROVADO" }).Count

    $overall = "APROVADO"
    if ($criticalFailed -gt 0) {
        $overall = "BLOQUEADO"
    }
    elseif ($highWarnings -gt 0) {
        $overall = "APROVADO COM RESSALVAS"
    }

    return [pscustomobject]@{
        app = $Snapshot.app
        displayName = $Snapshot.displayName
        overall = $overall
        checks = $checks
        snapshot = $Snapshot
    }
}

function Write-GateMarkdown {
    param([object]$Gate)

    $reportsDir = Join-Path (Split-Path $PSScriptRoot -Parent) "docs\governance-reports"
    if (-not (Test-Path $reportsDir)) {
        New-Item -ItemType Directory -Path $reportsDir -Force | Out-Null
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $file = Join-Path $reportsDir ("GATE_" + $Gate.app + "_" + $timestamp + ".md")

    $lines = @()
    $lines += "# Gate de Governanca - " + $Gate.displayName
    $lines += ""
    $lines += "Data: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $lines += "Status final: **" + $Gate.overall + "**"
    $lines += ""
    $lines += "## Snapshot"
    $lines += "- App: " + $Gate.snapshot.app
    $lines += "- Roadmap status: " + $Gate.snapshot.roadmapStatus
    $lines += "- Roadmap date: " + $Gate.snapshot.roadmapDate
    $lines += "- Token: " + $Gate.snapshot.token
    $lines += "- Command exists: " + $Gate.snapshot.commandExists
    $lines += "- Matrix exists: " + $Gate.snapshot.matrixExists
    $lines += "- Release docs exists: " + $Gate.snapshot.releaseDocsExists
    $lines += "- Release channel policy: " + $Gate.snapshot.releaseChannelPolicy
    $lines += "- Release repo leaf: " + $Gate.snapshot.releaseRepoLeaf
    $lines += "- Uses dedicated -releases repo: " + $Gate.snapshot.usesDedicatedReleasesRepo
    if ($Gate.snapshot.forbiddenMatrixChanges -and $Gate.snapshot.forbiddenMatrixChanges.Count -gt 0) {
        $lines += "- Forbidden matrix changes: " + ($Gate.snapshot.forbiddenMatrixChanges -join ", ")
    } else {
        $lines += "- Forbidden matrix changes: none"
    }
    if ($Gate.snapshot.officialReleaseRepo) {
        $lines += "- Official release repo: " + $Gate.snapshot.officialReleaseRepo
    }
    $lines += "- Source dirty files: " + $Gate.snapshot.sourceDirty
    $lines += "- Release dirty files: " + $Gate.snapshot.releaseDirty
    $lines += ""
    $lines += "## Checks"

    foreach ($c in $Gate.checks) {
        $lines += "- " + $c.name + ": " + $c.status + " - " + $c.detail
    }

    Set-Content -Path $file -Value ($lines -join "`r`n") -Encoding UTF8
    return $file
}

function Get-Snapshots {
    $rows = foreach ($item in $Catalog) {
        Get-AppSnapshot -Item $item
    }
    return $rows
}

switch ($Action) {
    "dashboard" {
        $rows = Get-Snapshots
        $rows |
            Sort-Object -Property @{ Expression = { if ($_.daysToRoadmap -eq $null) { 99999 } else { $_.daysToRoadmap } } }, app |
            Select-Object app, roadmapStatus, roadmapDate, daysToRoadmap, token, commandExists, matrixExists, releaseDocsExists, sourceDirty, releaseDirty |
            Format-Table -AutoSize
        break
    }

    "roadmap" {
        $rows = Get-Snapshots |
            Where-Object { $_.roadmapDate -and $_.daysToRoadmap -ne $null -and $_.daysToRoadmap -le $WindowDays }

        if (-not $rows -or $rows.Count -eq 0) {
            Write-Host "Nenhum marco de roadmap nos proximos $WindowDays dias."
            break
        }

        $rows |
            Sort-Object -Property daysToRoadmap |
            Select-Object app, displayName, roadmapStatus, roadmapDate, daysToRoadmap |
            Format-Table -AutoSize
        break
    }

    "gate" {
        if ([string]::IsNullOrWhiteSpace($App)) {
            throw "Use -App para executar gate de uma aplicacao especifica."
        }

        $snapshot = Get-Snapshots | Where-Object { $_.app -ieq $App } | Select-Object -First 1
        if (-not $snapshot) {
            throw "App '$App' nao encontrada no catalogo de governanca."
        }

        $gate = Build-GateResult -Snapshot $snapshot

        $gate.checks | Select-Object name, status, detail | Format-Table -AutoSize
        Write-Host "\nStatus final: $($gate.overall)"

        if ($Strict -and $gate.overall -ne "APROVADO") {
            throw "Gate em modo estrito bloqueou a publicacao para '$App'."
        }

        break
    }

    "report" {
        if ([string]::IsNullOrWhiteSpace($App)) {
            throw "Use -App para gerar o relatorio de gate."
        }

        $snapshot = Get-Snapshots | Where-Object { $_.app -ieq $App } | Select-Object -First 1
        if (-not $snapshot) {
            throw "App '$App' nao encontrada no catalogo de governanca."
        }

        $gate = Build-GateResult -Snapshot $snapshot
        $file = Write-GateMarkdown -Gate $gate

        Write-Host "Relatorio gerado: $file"
        Write-Host "Status final: $($gate.overall)"

        if ($Strict -and $gate.overall -ne "APROVADO") {
            throw "Gate em modo estrito bloqueou a publicacao para '$App'."
        }

        break
    }
}
