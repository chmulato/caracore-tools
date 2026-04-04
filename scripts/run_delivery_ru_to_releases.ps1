param(
    [switch]$DryRun,
    [switch]$NoPush
)

$ErrorActionPreference = "Stop"
$sync = Join-Path $PSScriptRoot "sync_delivery_site_to_releases_docs.ps1"
$params = @{
  DeliveryPath = "D:\dev\caracore-site\delivery\ru"
  ReleasesRepoPath = "D:\dev\caracore-ru-releases"
  CommitMessage = "site: sync delivery/ru para docs/"
}
if ($DryRun.IsPresent) { $params.DryRun = $true }
if ($NoPush.IsPresent) { $params.NoPush = $true }

& $sync @params
