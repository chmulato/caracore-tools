param(
    [string]$Tag,
    [switch]$Clobber,
    [switch]$DryRun,
    [string]$Dir
)

$ErrorActionPreference = "Stop"
$script = "D:\\dev\\caracore-circuito\\scripts\\script_delivery_circuito_ferradura_to_releases.py"
if (-not (Test-Path $script)) { throw "Script nao encontrado: $script" }

$args = @()
if ($Tag) { $args += "--tag"; $args += $Tag }
if ($Clobber) { $args += "--clobber" }
if ($DryRun) { $args += "--dry-run" }
if ($Dir) { $args += "--dir"; $args += $Dir }

python $script @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
