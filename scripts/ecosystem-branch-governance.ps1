param(
    [ValidateSet("status", "align")]
    [string]$Action = "status",

    [string]$App,

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$CatalogPath = Join-Path $PSScriptRoot "ecosystem-governance-catalog.json"
if (-not (Test-Path $CatalogPath)) {
    throw "Catalogo de governanca nao encontrado: $CatalogPath"
}

$Catalog = Get-Content -Path $CatalogPath -Raw -Encoding UTF8 | ConvertFrom-Json

function Get-BranchState {
    param([string]$RepoPath)

    if (-not (Test-Path $RepoPath)) {
        return [pscustomobject]@{ exists = $false; branch = ""; dirty = $null }
    }

    if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
        return [pscustomobject]@{ exists = $true; branch = ""; dirty = $null }
    }

    $branch = (git -C $RepoPath rev-parse --abbrev-ref HEAD 2>$null)
    $dirty = @(git -C $RepoPath status --porcelain 2>$null).Count

    return [pscustomobject]@{
        exists = $true
        branch = $branch
        dirty = $dirty
    }
}

function Get-Rows {
    param([object[]]$Items)

    $rows = foreach ($item in $Items) {
        $src = Get-BranchState -RepoPath $item.sourceRepoPath
        $rel = Get-BranchState -RepoPath $item.releaseRepoPath

        $srcTarget = if ($item.sourceBranchTarget) { $item.sourceBranchTarget } else { $src.branch }
        $relTarget = if ($item.releaseBranchTarget) { $item.releaseBranchTarget } else { $rel.branch }

        [pscustomobject]@{
            app = $item.app
            sourceBranch = $src.branch
            sourceTarget = $srcTarget
            sourceDirty = $src.dirty
            sourceAligned = ($src.branch -eq $srcTarget)
            releaseBranch = $rel.branch
            releaseTarget = $relTarget
            releaseDirty = $rel.dirty
            releaseAligned = ($rel.branch -eq $relTarget)
        }
    }

    return $rows
}

$items = $Catalog
if ($App) {
    $items = $Catalog | Where-Object { $_.app -ieq $App }
    if (-not $items -or $items.Count -eq 0) {
        throw "App '$App' nao encontrada no catalogo."
    }
}

$rows = Get-Rows -Items $items

switch ($Action) {
    "status" {
        $rows |
            Select-Object app, sourceBranch, sourceTarget, sourceAligned, sourceDirty, releaseBranch, releaseTarget, releaseAligned, releaseDirty |
            Format-Table -AutoSize
        break
    }

    "align" {
        foreach ($item in $items) {
            $src = Get-BranchState -RepoPath $item.sourceRepoPath
            $rel = Get-BranchState -RepoPath $item.releaseRepoPath

            $srcTarget = if ($item.sourceBranchTarget) { $item.sourceBranchTarget } else { $src.branch }
            $relTarget = if ($item.releaseBranchTarget) { $item.releaseBranchTarget } else { $rel.branch }

            if ($src.exists -and $src.branch -ne $srcTarget) {
                if ($src.dirty -gt 0) {
                    Write-Warning "[$($item.app)] source repo sujo ($($item.sourceRepoPath)); nao vou trocar branch."
                }
                else {
                    Write-Host "[$($item.app)] source: $($src.branch) -> $srcTarget"
                    if (-not $DryRun) {
                        git -C $item.sourceRepoPath checkout $srcTarget | Out-Host
                    }
                }
            }

            if ($rel.exists -and $rel.branch -ne $relTarget) {
                if ($rel.dirty -gt 0) {
                    Write-Warning "[$($item.app)] release repo sujo ($($item.releaseRepoPath)); nao vou trocar branch."
                }
                else {
                    Write-Host "[$($item.app)] release: $($rel.branch) -> $relTarget"
                    if (-not $DryRun) {
                        git -C $item.releaseRepoPath checkout $relTarget | Out-Host
                    }
                }
            }
        }

        Write-Host "\nEstado apos alinhamento:"
        (Get-Rows -Items $items) |
            Select-Object app, sourceBranch, sourceTarget, sourceAligned, sourceDirty, releaseBranch, releaseTarget, releaseAligned, releaseDirty |
            Format-Table -AutoSize
        break
    }
}
