param(
    [switch]$DryRun,
    [switch]$NoPush
)

$ErrorActionPreference = "Stop"
$sync = Join-Path $PSScriptRoot "sync_delivery_site_to_releases_docs.ps1"
$params = @{
  DeliveryPath = "D:\dev\caracore-site\delivery\cso"
  ReleasesRepoPath = "D:\dev\caracore-cso-releases"
  CommitMessage = "site: sync delivery/cso para docs/"
}
if ($DryRun.IsPresent) { $params.DryRun = $true }
if ($NoPush.IsPresent) { $params.NoPush = $true }

& $sync @params
