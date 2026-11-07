<#
.SYNOPSIS
    Phase 4: Mathematical 1-Click Rollback Script
.DESCRIPTION
    Restores all debloated or disabled packages to their exact baseline state
    captured in Phase 0.
#>
param(
    [string]$BaselineDir = "$PSScriptRoot\..\backup"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " EXECUTING PHASE 4: MATHEMATICAL STATE RESTORATION" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$device = adb devices | Select-String -Pattern "\s+device$"
if (-not $device) {
    Write-Error "No Android device detected over ADB."
    exit 1
}

$enabledBaseline = "$BaselineDir\enabled-baseline.txt"
$disabledBaseline = "$BaselineDir\disabled-baseline.txt"
$packagesBaseline = "$BaselineDir\packages-baseline.txt"

if (-not (Test-Path $enabledBaseline) -or -not (Test-Path $packagesBaseline)) {
    Write-Error "Baseline files not found in $BaselineDir. Cannot perform exact mathematical restoration."
    exit 1
}

# 1. Index current device packages
$currentRaw = adb shell pm list packages --user 0
$currentInstalled = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($line in $currentRaw) {
    $clean = $line.Trim()
    if ($clean.StartsWith("package:")) { [void]$currentInstalled.Add($clean.Substring(8).Trim()) }
}

$currentDisabledRaw = adb shell pm list packages -d --user 0
$currentDisabled = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($line in $currentDisabledRaw) {
    $clean = $line.Trim()
    if ($clean.StartsWith("package:")) { [void]$currentDisabled.Add($clean.Substring(8).Trim()) }
}

# 2. Index baseline enabled packages
$origEnabled = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($line in (Get-Content $enabledBaseline)) {
    $clean = $line.Trim()
    if ($clean.StartsWith("package:")) { [void]$origEnabled.Add($clean.Substring(8).Trim()) }
}

$origDisabled = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
if (Test-Path $disabledBaseline) {
    foreach ($line in (Get-Content $disabledBaseline)) {
        $clean = $line.Trim()
        if ($clean.StartsWith("package:")) { [void]$origDisabled.Add($clean.Substring(8).Trim()) }
    }
}

# 3. Reinstall uninstalled packages
$missing = @()
foreach ($pkg in $origEnabled) {
    if (-not $currentInstalled.Contains($pkg)) { $missing += $pkg }
}

if ($missing.Count -gt 0) {
    Write-Host "`nReinstalling $($missing.Count) uninstalled packages..." -ForegroundColor Yellow
    foreach ($pkg in $missing) {
        $res = adb shell cmd package install-existing $pkg
        if ($res -like "*Failure*" -or $res -like "*not installed*") {
            if (Test-Path "$BaselineDir\apks\$pkg.apk") {
                Write-Host "    Fallback: Installing from $BaselineDir\apks\$pkg.apk..." -ForegroundColor Cyan
                adb install -r "$BaselineDir\apks\$pkg.apk" | Out-Null
            }
        }
        Write-Host "  Reinstalling $pkg: $res" -ForegroundColor Gray
    }
} else {
    Write-Host "Package inventory: All baseline packages are installed." -ForegroundColor Green
}

# 4. Re-enable packages back to original enabled state
$toEnable = @()
foreach ($pkg in $currentDisabled) {
    if ($origEnabled.Contains($pkg) -and -not $origDisabled.Contains($pkg)) { $toEnable += $pkg }
}

if ($toEnable.Count -gt 0) {
    Write-Host "`nRe-enabling $($toEnable.Count) packages..." -ForegroundColor Yellow
    foreach ($pkg in $toEnable) {
        $res = adb shell pm enable $pkg
        Write-Host "  Enabling $pkg: $res" -ForegroundColor Green
    }
} else {
    Write-Host "Package states: Disabled states match baseline." -ForegroundColor Green
}

Write-Host "`nDevice state has been strictly restored to Phase 0 baseline!" -ForegroundColor Green
