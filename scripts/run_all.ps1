<#
.SYNOPSIS
    一键重建：抓取 + 规范化。
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot

& (Join-Path $PSScriptRoot 'fetch_ingredients.ps1') -Root $root
python (Join-Path $PSScriptRoot 'build_dataset.py')
if ($LASTEXITCODE -ne 0) { throw "build_dataset.py 失败（exit $LASTEXITCODE）" }

Write-Host ''
Write-Host "完成。看这几份:" -ForegroundColor Green
Write-Host "  $root\README.md"
Write-Host "  $root\data\tags.md"
Write-Host "  $root\data\ingredients.csv"
