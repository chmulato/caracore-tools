param(
    [ValidateSet("list", "calendar", "validate", "run")]
    [string]$Action = "list",

    [string]$App,

    [switch]$DryRun,

    [string[]]$ExtraArgs
)

$ErrorActionPreference = "Stop"

$MapPath = Join-Path $PSScriptRoot "ecosystem-delivery-map.json"
if (-not (Test-Path $MapPath)) {
    throw "Mapa de delivery nao encontrado: $MapPath"
}

$Items = Get-Content -Path $MapPath -Raw -Encoding UTF8 | ConvertFrom-Json

function Get-TokenStatus {
    param([object]$Item)

    if (-not $Item.requiredTokens -or $Item.requiredTokens.Count -eq 0) {
        return "n/a"
    }

    foreach ($tokenName in $Item.requiredTokens) {
        if (Get-ChildItem "Env:$tokenName" -ErrorAction SilentlyContinue) {
            return "ok:$tokenName"
        }
    }

    return "missing"
}

function Resolve-CommandFile {
    param([object]$Item)

    if (-not $Item.commandPath) { return $null }
    return Join-Path $Item.repoPath $Item.commandPath
}

function Get-RoadmapDateValue {
    param([string]$RoadmapDate)

    if ([string]::IsNullOrWhiteSpace($RoadmapDate)) {
        return [datetime]::MaxValue
    }

    try {
        return [datetime]$RoadmapDate
    }
    catch {
        return [datetime]::MaxValue
    }
}

function Show-Items {
    param([object[]]$Rows)

    $Rows |
        Sort-Object -Property @{ Expression = { Get-RoadmapDateValue $_.roadmapDate } }, app |
        Select-Object app, displayName, category, roadmapStatus, roadmapDate,
            @{ Name = "mode"; Expression = { if ([string]::IsNullOrWhiteSpace($_.commandPath)) { "manual" } else { "auto" } } },
            @{ Name = "token"; Expression = { Get-TokenStatus $_ } } |
        Format-Table -AutoSize
}

switch ($Action) {
    "list" {
        Show-Items -Rows $Items
        Write-Host "\nDica: use -Action run -App <id> [-DryRun] para executar um delivery especifico."
        break
    }

    "calendar" {
        Show-Items -Rows $Items
        break
    }

    "validate" {
        $report = foreach ($item in $Items) {
            $cmd = Resolve-CommandFile -Item $item
            [pscustomobject]@{
                app = $item.app
                repoPathExists = Test-Path $item.repoPath
                commandExists = if ($cmd) { Test-Path $cmd } else { $false }
                mode = if ([string]::IsNullOrWhiteSpace($item.commandPath)) { "manual" } else { "auto" }
                token = Get-TokenStatus -Item $item
                notes = $item.notes
            }
        }

        $report | Format-Table -AutoSize
        break
    }

    "run" {
        if ([string]::IsNullOrWhiteSpace($App)) {
            throw "Informe -App com o id do produto (ex: pdv, oidc, seed, area51)."
        }

        $item = $Items | Where-Object { $_.app -ieq $App } | Select-Object -First 1
        if (-not $item) {
            throw "App '$App' nao encontrada no mapa. Rode com -Action list para ver ids validos."
        }

        if ([string]::IsNullOrWhiteSpace($item.commandPath)) {
            throw "App '$App' esta em modo manual (sem comando cadastrado)."
        }

        if (-not (Test-Path $item.repoPath)) {
            throw "Repositorio nao encontrado: $($item.repoPath)"
        }

        $cmdFile = Resolve-CommandFile -Item $item
        if (-not (Test-Path $cmdFile)) {
            throw "Comando nao encontrado: $cmdFile"
        }

        $tokenStatus = Get-TokenStatus -Item $item
        if ($tokenStatus -eq "missing") {
            Write-Warning "Nenhum token do conjunto requerido foi encontrado para '$($item.app)'."
            Write-Warning "Tokens aceitos: $($item.requiredTokens -join ', ')"
            if (-not $DryRun) {
                throw "Abortei execucao por falta de token. Rode com -DryRun para simulacao."
            }
            Write-Host "DryRun sem token: simulacao concluida sem invocar o script legado."
            return
        }

        $invocationArgs = @()
        if ($ExtraArgs) {
            $invocationArgs += $ExtraArgs
        }

        if ($DryRun -and $item.supportsDryRun -and -not [string]::IsNullOrWhiteSpace($item.dryRunArg)) {
            if (-not ($invocationArgs -contains $item.dryRunArg)) {
                $invocationArgs += $item.dryRunArg
            }
        }

        Write-Host "App: $($item.displayName) [$($item.app)]"
        Write-Host "Repo: $($item.repoPath)"
        Write-Host "Comando: $cmdFile"
        Write-Host "Token: $tokenStatus"
        Write-Host "DryRun: $DryRun"
        if ($invocationArgs.Count -gt 0) {
            Write-Host "Args: $($invocationArgs -join ' ')"
        }

        Push-Location $item.repoPath
        try {
            if ($item.commandType -ieq "ps1") {
                & $cmdFile @invocationArgs
            } elseif ($item.commandType -ieq "python") {
                python $cmdFile @invocationArgs
            } else {
                throw "Tipo de comando nao suportado: $($item.commandType)"
            }

            if ($LASTEXITCODE -ne 0) {
                throw "Falha no delivery '$($item.app)' (exit code $LASTEXITCODE)."
            }
        }
        finally {
            Pop-Location
        }

        break
    }
}
