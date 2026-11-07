<#
.SYNOPSIS
    CleanYourPhone - Reversible Package Restoration Script for Windows PowerShell
.DESCRIPTION
    Restores / re-enables packages previously disabled or uninstalled for user 0.
.EXAMPLE
    .\tools\restore.ps1 -Target "lists\oppo\coloros-safe-debloat.txt"
    .\tools\restore.ps1 -Target "restore_last_session.ps1"
#>

param (
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Target
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -Path $Target)) {
    Write-Error "Error: Target file not found: $Target"
    exit 1
}

if ($Target.EndsWith(".ps1")) {
    Write-Host "[*] Executing session restore script $Target..." -ForegroundColor Cyan
    & $Target
    exit 0
}

$rawLines = Get-Content -Path $Target -Encoding UTF8
$pkgs = @()
foreach ($line in $rawLines) {
    $clean = $line.Trim()
    if ($clean.StartsWith("#") -or [string]::IsNullOrWhiteSpace($clean)) {
        continue
    }
    $pkgName = ($clean -split "#")[0].Trim()
    if ($pkgName) {
        $pkgs += $pkgName
    }
}

$total = $pkgs.Count
$current = 0
$restored = 0

Write-Host "[*] Restoring $total packages from $Target..." -ForegroundColor Cyan

foreach ($pkg in $pkgs) {
    $current++
    # Universal re-enable (modern enable & legacy unhide)
    adb shell pm enable $pkg 2>$null | Out-Null
    adb shell pm unhide $pkg 2>$null | Out-Null

    # Reinstall for user 0 (try modern cmd, fallback to legacy pm)
    $out = adb shell cmd package install-existing $pkg 2>&1
    if ($out -notmatch "installed for user" -and $out -notmatch "Package") {
        $out = adb shell pm install-existing $pkg 2>&1
    }

    if ($out -match "installed for user" -or $out -match "Package") {
        Write-Host "[$current/$total] Restored: $pkg" -ForegroundColor Green
    } else {
        Write-Host "[$current/$total] Re-enabled: $pkg" -ForegroundColor Green
    }
    $restored++
}

# Ensure stock OEM launchers are re-enabled if disabled
$stockList = @("com.oppo.launcher", "com.coloros.home", "com.oneplus.launcher", "com.realme.launcher", "com.bbk.launcher2", "com.vivo.launcher")
foreach ($stock in $stockList) {
    adb shell pm enable $stock | Out-Null
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Restoration complete. Total packages processed: $restored" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
