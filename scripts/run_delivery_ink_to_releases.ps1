param(
    [switch]$DryRun,
    [switch]$NoPush
)

$ErrorActionPreference = "Stop"
$sync = Join-Path $PSScriptRoot "sync_delivery_site_to_releases_docs.ps1"
$params = @{
  DeliveryPath = "D:\dev\caracore-site\delivery\ink"
  ReleasesRepoPath = "D:\dev\caracore-ink-releases"
  CommitMessage = "site: sync delivery/ink para docs/"
}
if ($DryRun.IsPresent) { $params.DryRun = $true }
if ($NoPush.IsPresent) { $params.NoPush = $true }

& $sync @params
