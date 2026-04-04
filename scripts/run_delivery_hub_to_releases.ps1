param(
    [string]$Tag,
    [switch]$Clobber,
    [switch]$DryRun,
    [string]$Dir,
    [string]$War
)

$ErrorActionPreference = "Stop"
$script = "D:\\dev\\caracore-hub\\scripts\\delivery_war_hub_to_releases.py"
if (-not (Test-Path $script)) { throw "Script nao encontrado: $script" }

$args = @()
if ($Tag) { $args += "--tag"; $args += $Tag }
if ($Clobber) { $args += "--clobber" }
if ($DryRun) { $args += "--dry-run" }
if ($Dir) { $args += "--dir"; $args += $Dir }
if ($War) { $args += "--war"; $args += $War }

python $script @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
