<#
.SYNOPSIS
    抓取 Wynncraft 物品图鉴（https://wynncraft.com/help/item-guide）中的全部 Ingredient。

.DESCRIPTION
    图鉴页面本身是 Nuxt 客户端渲染，HTML 里没有数据；页面实际调用的是
        POST https://api.wynncraft.com/v3/item/search?page=N   body: {"type":["ingredient"]}
    本脚本正是复用这个接口（与网页完全同源），把 49 页结果合并成一个 JSON。

    输出:
        raw/ingredients_raw.json   分页合并后的原始响应（不做任何改写）
        raw/item_metadata.json     筛选元数据（type/tier/identifications 全表）
        raw/fetch_log.txt          抓取日志（时间、页数、条数）
#>
[CmdletBinding()]
param(
    [string]$Root       = (Split-Path -Parent $PSScriptRoot),
    [int]   $PageSize   = 20,
    [int]   $DelayMs    = 250,
    [int]   $Retry      = 4
)

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'

$rawDir = Join-Path $Root 'raw'
New-Item -ItemType Directory -Force -Path $rawDir | Out-Null

$apiSearch   = 'https://api.wynncraft.com/v3/item/search'
$apiMetadata = 'https://api.wynncraft.com/v3/item/metadata'
$body        = '{"type":["ingredient"]}'

function Invoke-WynnApi {
    param([string]$Uri, [string]$Method = 'Get', [string]$Body)
    for ($i = 1; $i -le $Retry; $i++) {
        try {
            if ($Method -eq 'Post') {
                return Invoke-RestMethod -Uri $Uri -Method Post -ContentType 'application/json' `
                                         -Body $Body -TimeoutSec 60
            }
            return Invoke-RestMethod -Uri $Uri -Method Get -TimeoutSec 60
        }
        catch {
            if ($i -eq $Retry) { throw "请求失败 $Uri : $($_.Exception.Message)" }
            Start-Sleep -Milliseconds (500 * $i)
        }
    }
}

$startedAt = Get-Date
Write-Host "[1/3] 读取筛选元数据 ..."
$meta = Invoke-WynnApi -Uri $apiMetadata
$meta | ConvertTo-Json -Depth 20 | Set-Content -Path (Join-Path $rawDir 'item_metadata.json') -Encoding UTF8

Write-Host "[2/3] 抓取第 1 页以确定总页数 ..."
$first = Invoke-WynnApi -Uri "$apiSearch`?page=1" -Method Post -Body $body
$expected = [int]$first.controller.count
$pages    = [int]$first.controller.pages
Write-Host "       共 $expected 条 / $pages 页"

$items = New-Object System.Collections.ArrayList
foreach ($it in $first.results) { [void]$items.Add($it) }

for ($p = 2; $p -le $pages; $p++) {
    $r = Invoke-WynnApi -Uri "$apiSearch`?page=$p" -Method Post -Body $body
    foreach ($it in $r.results) { [void]$items.Add($it) }
    if ($p % 10 -eq 0 -or $p -eq $pages) { Write-Host "       第 $p/$pages 页，累计 $($items.Count)/$expected" }
    Start-Sleep -Milliseconds $DelayMs
}

if ($items.Count -ne $expected) {
    Write-Warning "条数不一致: 实际 $($items.Count)，接口声明 $expected"
}

$merged = [ordered]@{
    source     = 'POST https://api.wynncraft.com/v3/item/search  body: {"type":["ingredient"]}'
    page_size  = $PageSize
    pages      = $pages
    count      = $items.Count
    fetched_at = (Get-Date).ToString('o')
    items      = $items
}
$merged | ConvertTo-Json -Depth 20 -Compress | Set-Content -Path (Join-Path $rawDir 'ingredients_raw.json') -Encoding UTF8

$log = @(
    "fetched_at : $($startedAt.ToString('o'))"
    "finished_at : $((Get-Date).ToString('o'))"
    "endpoint   : $apiSearch"
    "pages      : $pages"
    "count      : $($items.Count) (expect $expected)"
    "page_size  : $PageSize"
)
$log | Set-Content -Path (Join-Path $rawDir 'fetch_log.txt') -Encoding UTF8

Write-Host "[3/3] 完成 -> raw/ingredients_raw.json ($($items.Count) 条)"
