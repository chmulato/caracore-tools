param(
    [string]$DocsPath = (Join-Path $PSScriptRoot '..\docs'),
    [switch]$ReportOnly
)

$resolvedDocsPath = (Resolve-Path $DocsPath).Path

$allowedExtensions = @(
    '.html',
    '.css',
    '.js',
    '.png',
    '.jpg',
    '.jpeg',
    '.gif',
    '.svg',
    '.webp',
    '.ico',
    '.avif',
    '.woff',
    '.woff2',
    '.ttf',
    '.otf',
    '.eot',
    '.map'
)

$allowedFileNames = @(
    'CNAME',
    '.gitkeep',
    'feed.xml'
)

$files = Get-ChildItem -Path $resolvedDocsPath -Recurse -File
$violations = @(
    $files | Where-Object {
        $extension = $_.Extension.ToLowerInvariant()
        $name = $_.Name
        ($allowedFileNames -notcontains $name) -and ($allowedExtensions -notcontains $extension)
    }
)

Write-Host "DOCS_PATH=$resolvedDocsPath"
Write-Host "FILES_TOTAL=$($files.Count)"
Write-Host "VIOLATIONS_TOTAL=$($violations.Count)"

if ($violations.Count -gt 0) {
    Write-Host ''
    Write-Host 'Violacoes por extensao:'
    $violations |
        Group-Object { if ([string]::IsNullOrWhiteSpace($_.Extension)) { '[sem-extensao]' } else { $_.Extension.ToLowerInvariant() } } |
        Sort-Object -Property @{ Expression = 'Count'; Descending = $true }, @{ Expression = 'Name'; Descending = $false } |
        ForEach-Object {
            Write-Host ('  {0,4}  {1}' -f $_.Count, $_.Name)
        }

    Write-Host ''
    Write-Host 'Diretorios com mais violacoes:'
    $violations |
        Group-Object DirectoryName |
        Sort-Object -Property @{ Expression = 'Count'; Descending = $true }, @{ Expression = 'Name'; Descending = $false } |
        Select-Object -First 15 |
        ForEach-Object {
            Write-Host ('  {0,4}  {1}' -f $_.Count, $_.Name)
        }

    Write-Host ''
    Write-Host 'Arquivos bloqueados:'
    $violations |
        Sort-Object FullName |
        ForEach-Object {
            Write-Host ('  - ' + $_.FullName)
        }

    if (-not $ReportOnly) {
        throw 'Docs contem artefatos publicados fora do padrao HTML-only.'
    }
}

Write-Host ''
Write-Host 'STATUS=OK'