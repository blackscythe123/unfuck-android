<#
.SYNOPSIS
    Generates an interactive, standalone HTML storage analyzer and recovery dashboard.

.DESCRIPTION
    Queries `adb shell dumpsys diskstats`, extracts partition metrics, separates App Code,
    User Data, and App Cache, and produces an interactive visual report.

.EXAMPLE
    .\scripts\05-storage-report.ps1
#>

[CmdletBinding()]
param()

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$ToolPath = Join-Path $RepoRoot "tools\generate_storage_report.py"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Android Storage Architecture & Recovery Advisor" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

if (-not (Test-Path $ToolPath)) {
    Write-Error "Storage report generator tool not found at $ToolPath"
    exit 1
}

python $ToolPath

Write-Host "`n[+] Dashboard generated at: storage-analyzer.html" -ForegroundColor Green
