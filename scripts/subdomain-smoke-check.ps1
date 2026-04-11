param(
    [int]$TimeoutSec = 20
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-PageCheck {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][int]$TimeoutSec
    )

    $result = [ordered]@{
        Url = $Url
        Ok = $false
        Status = $null
        FinalUrl = $null
        Html = $null
        Error = $null
    }

    try {
        $resp = Invoke-WebRequest -Uri $Url -Method Get -MaximumRedirection 8 -TimeoutSec $TimeoutSec -UseBasicParsing
        $result.Ok = $true
        $result.Status = [int]$resp.StatusCode
        $result.FinalUrl = $resp.BaseResponse.ResponseUri.AbsoluteUri
        $result.Html = [string]$resp.Content
    }
    catch {
        if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
            $result.Status = [int]$_.Exception.Response.StatusCode
            try {
                $result.FinalUrl = $_.Exception.Response.ResponseUri.AbsoluteUri
            }
            catch {
                $result.FinalUrl = $null
            }
        }
        else {
            $result.Status = 'ERR'
        }
        $result.Error = $_.Exception.Message
    }

    return [pscustomobject]$result
}

function Get-FirstRegexGroup {
    param(
        [string]$InputText,
        [string]$Pattern
    )

    if ([string]::IsNullOrWhiteSpace($InputText)) {
        return $null
    }

    $m = [regex]::Match($InputText, $Pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if ($m.Success -and $m.Groups.Count -gt 1) {
        return $m.Groups[1].Value
    }

    return $null
}

function Add-Check {
    param(
        [Parameter(Mandatory = $true)][System.Collections.ArrayList]$Target,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Type,
        [Parameter(Mandatory = $true)][string]$Url,
        [int]$ExpectedStatus,
        [string]$ExpectedPrefix,
        [string]$ExpectedHost,
        [string]$ExpectedNeedle
    )

    $item = [ordered]@{
        Name = $Name
        Type = $Type
        Url = $Url
    }

    if ($PSBoundParameters.ContainsKey('ExpectedStatus')) { $item.ExpectedStatus = $ExpectedStatus }
    if ($PSBoundParameters.ContainsKey('ExpectedPrefix')) { $item.ExpectedPrefix = $ExpectedPrefix }
    if ($PSBoundParameters.ContainsKey('ExpectedHost')) { $item.ExpectedHost = $ExpectedHost }
    if ($PSBoundParameters.ContainsKey('ExpectedNeedle')) { $item.ExpectedNeedle = $ExpectedNeedle }

    [void]$Target.Add([pscustomobject]$item)
}

function Add-StoreChecks {
    param(
        [Parameter(Mandatory = $true)][System.Collections.ArrayList]$Target,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$StoreHost,
        [switch]$HasDownload,
        [switch]$HasBaseHref
    )

    $rootUrl = "https://$StoreHost/"
    $feedbackUrl = "https://$StoreHost/canal-feedback.html"
    $wikiUrl = "https://$StoreHost/wiki/index.html"

    if ($HasBaseHref) {
        Add-Check -Target $Target -Name "$Name root base host" -Type 'base-host' -Url $rootUrl -ExpectedHost $StoreHost
    }

    if ($HasDownload) {
        $downloadUrl = "https://$StoreHost/download.html"
        Add-Check -Target $Target -Name "$Name download 200" -Type 'status' -Url $downloadUrl -ExpectedStatus 200
        if ($HasBaseHref) {
            Add-Check -Target $Target -Name "$Name download base host" -Type 'base-host' -Url $downloadUrl -ExpectedHost $StoreHost
        }
    }

    Add-Check -Target $Target -Name "$Name feedback 200" -Type 'status' -Url $feedbackUrl -ExpectedStatus 200
    if ($HasBaseHref) {
        Add-Check -Target $Target -Name "$Name feedback base host" -Type 'base-host' -Url $feedbackUrl -ExpectedHost $StoreHost
    }

    Add-Check -Target $Target -Name "$Name wiki 200" -Type 'status' -Url $wikiUrl -ExpectedStatus 200
    Add-Check -Target $Target -Name "$Name wiki links canonical wiki" -Type 'contains' -Url $wikiUrl -ExpectedNeedle 'https://wiki.caracore.com.br/index.html'
}

$checks = [System.Collections.ArrayList]@(
    [pscustomobject]@{ Name = 'matrix root 200'; Type = 'status'; Url = 'https://www.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'tools root 200'; Type = 'status'; Url = 'https://tools.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'retro root 200'; Type = 'status'; Url = 'https://retro.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'personal root 200'; Type = 'status'; Url = 'https://personal.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'wiki root 200'; Type = 'status'; Url = 'https://wiki.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'pdv root 200'; Type = 'status'; Url = 'https://pdv.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'cso root 200'; Type = 'status'; Url = 'https://cso.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'hub root 200'; Type = 'status'; Url = 'https://hub.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'seed root 200'; Type = 'status'; Url = 'https://seed.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'oidc root 200'; Type = 'status'; Url = 'https://oidc.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'area51 root 200'; Type = 'status'; Url = 'https://area51.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'ru root 200'; Type = 'status'; Url = 'https://ru.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'ete root 200'; Type = 'status'; Url = 'https://ete.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'circuito root 200'; Type = 'status'; Url = 'https://circuito.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'ink root 200'; Type = 'status'; Url = 'https://ink.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'mkt root 200'; Type = 'status'; Url = 'https://mkt.caracore.com.br/'; ExpectedStatus = 200 },
    [pscustomobject]@{ Name = 'retro articles redirect'; Type = 'redirect'; Url = 'https://retro.caracore.com.br/articles.html'; ExpectedPrefix = 'https://retro.caracore.com.br/' },
    [pscustomobject]@{ Name = 'personal articles redirect'; Type = 'redirect'; Url = 'https://personal.caracore.com.br/articles.html'; ExpectedPrefix = 'https://personal.caracore.com.br/' },
    [pscustomobject]@{ Name = 'retro article canonical/og host'; Type = 'meta-host'; Url = 'https://retro.caracore.com.br/articles/2026_04_04_article_79.html'; ExpectedHost = 'retro.caracore.com.br' },
    [pscustomobject]@{ Name = 'personal article canonical/og host'; Type = 'meta-host'; Url = 'https://personal.caracore.com.br/articles/2026_04_03_alem_da_lente_os_limites_da_automacao_visual.html'; ExpectedHost = 'personal.caracore.com.br' },
    [pscustomobject]@{ Name = 'wiki root og:url host'; Type = 'meta-host-og-only'; Url = 'https://wiki.caracore.com.br/'; ExpectedHost = 'wiki.caracore.com.br' }
)

Add-StoreChecks -Target $checks -Name 'pdv' -StoreHost 'pdv.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'cso' -StoreHost 'cso.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'hub' -StoreHost 'hub.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'seed' -StoreHost 'seed.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'oidc' -StoreHost 'oidc.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'area51' -StoreHost 'area51.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'ru' -StoreHost 'ru.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'ete' -StoreHost 'ete.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'circuito' -StoreHost 'circuito.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'ink' -StoreHost 'ink.caracore.com.br' -HasDownload -HasBaseHref
Add-StoreChecks -Target $checks -Name 'mkt' -StoreHost 'mkt.caracore.com.br'

$cache = @{}
$report = @()

foreach ($check in $checks) {
    if (-not $cache.ContainsKey($check.Url)) {
        $cache[$check.Url] = Invoke-PageCheck -Url $check.Url -TimeoutSec $TimeoutSec
    }

    $page = $cache[$check.Url]
    $pass = $false
    $detail = ''

    switch ($check.Type) {
        'status' {
            $pass = ($page.Status -eq $check.ExpectedStatus)
            $detail = "expected=$($check.ExpectedStatus); got=$($page.Status)"
        }

        'redirect' {
            $metaTarget = Get-FirstRegexGroup -InputText $page.Html -Pattern '<meta[^>]+http-equiv=["'']refresh["''][^>]+content=["''][^"'']*url\s*=\s*([^"'']+)["'']'
            $httpRedirectOk = ($null -ne $page.FinalUrl) -and ($page.FinalUrl -ne $check.Url) -and $page.FinalUrl.StartsWith($check.ExpectedPrefix)
            $metaRedirectOk = ($null -ne $metaTarget) -and ($metaTarget.StartsWith('/') -or $metaTarget.StartsWith($check.ExpectedPrefix))

            $pass = ($page.Status -eq 200) -and ($httpRedirectOk -or $metaRedirectOk)
            $detail = "expected-prefix=$($check.ExpectedPrefix); final=$($page.FinalUrl); meta-target=$metaTarget; status=$($page.Status)"
        }

        'meta-host' {
            $canonical = Get-FirstRegexGroup -InputText $page.Html -Pattern '<link[^>]+rel=["'']canonical["''][^>]+href=["'']([^"'']+)["'']'
            $ogUrl = Get-FirstRegexGroup -InputText $page.Html -Pattern '<meta[^>]+property=["'']og:url["''][^>]+content=["'']([^"'']+)["'']'

            $canonHost = $null
            $ogHost = $null

            if ($canonical) { $canonHost = ([Uri]$canonical).Host }
            if ($ogUrl) { $ogHost = ([Uri]$ogUrl).Host }

            $pass = ($canonHost -eq $check.ExpectedHost) -and ($ogHost -eq $check.ExpectedHost)
            $detail = "expected-host=$($check.ExpectedHost); canonical-host=$canonHost; og-host=$ogHost"
        }

        'meta-host-og-only' {
            $ogUrl = Get-FirstRegexGroup -InputText $page.Html -Pattern '<meta[^>]+property=["'']og:url["''][^>]+content=["'']([^"'']+)["'']'
            $ogHost = $null
            if ($ogUrl) { $ogHost = ([Uri]$ogUrl).Host }

            $pass = ($ogHost -eq $check.ExpectedHost)
            $detail = "expected-host=$($check.ExpectedHost); og-host=$ogHost"
        }

        'base-host' {
            $baseHref = Get-FirstRegexGroup -InputText $page.Html -Pattern '<base[^>]+href=["'']([^"'']+)["'']'
            $baseHost = $null
            if ($baseHref) { $baseHost = ([Uri]$baseHref).Host }

            $pass = ($baseHost -eq $check.ExpectedHost)
            $detail = "expected-host=$($check.ExpectedHost); base-host=$baseHost"
        }

        'contains' {
            $pass = ($null -ne $page.Html) -and $page.Html.Contains($check.ExpectedNeedle)
            $detail = "expected-needle=$($check.ExpectedNeedle)"
        }

        default {
            throw "Unknown check type: $($check.Type)"
        }
    }

    if (-not $pass -and $page.Error) {
        $detail = "$detail; error=$($page.Error)"
    }

    $report += [pscustomobject]@{
        Result = if ($pass) { 'PASS' } else { 'FAIL' }
        Check = $check.Name
        Url = $check.Url
        Status = $page.Status
        FinalUrl = $page.FinalUrl
        Detail = $detail
    }
}

$report | Sort-Object Result, Check | Format-Table -AutoSize | Out-String -Width 380 | Write-Output

$total = $report.Count
$passed = ($report | Where-Object { $_.Result -eq 'PASS' }).Count
$failed = $total - $passed

Write-Output "Summary: total=$total; pass=$passed; fail=$failed"

if ($failed -gt 0) {
    exit 1
}

exit 0
