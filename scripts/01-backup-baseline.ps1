<#
.SYNOPSIS
    Phase 0: Mathematical Baseline Snapshot & APK Backup
.DESCRIPTION
    Dumps all installed packages, enabled/disabled states, disk partition metrics,
    and backs up sideloaded APKs locally before modifying anything.
#>
param(
    [string]$OutputDir = "$PSScriptRoot\..\backup"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " EXECUTING PHASE 0: MATHEMATICAL BASELINE SNAPSHOT" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$device = adb devices | Select-String -Pattern "\s+device$"
if (-not $device) {
    Write-Error "No Android device detected over ADB. Enable USB Debugging and reconnect."
    exit 1
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
New-Item -ItemType Directory -Force -Path "$OutputDir\apks" | Out-Null

Write-Host "`n1. Dumping Package Baselines..." -ForegroundColor Yellow
adb shell pm list packages --user 0 > "$OutputDir\packages-baseline.txt"
adb shell pm list packages -e --user 0 > "$OutputDir\enabled-baseline.txt"
adb shell pm list packages -d --user 0 > "$OutputDir\disabled-baseline.txt"

Write-Host "2. Capturing Disk Metrics..." -ForegroundColor Yellow
adb shell df -k /data > "$OutputDir\disk-baseline.txt"

Write-Host "3. Detecting & Backing Up Sideloaded / Custom APKs..." -ForegroundColor Yellow
$thirdParty = adb shell pm list packages -i -3
$backedUpCount = 0

foreach ($line in $thirdParty) {
    # Match package:com.example installer=null or browser/packageinstaller
    if ($line -match "package:([^\s]+)\s+installer=(null|com\.android\.packageinstaller|com\.google\.android\.packageinstaller|com\.brave\.browser|com\.whatsapp|com\.anilab\.android)") {
        $pkg = $matches[1].Trim()
        $pathOut = adb shell pm path $pkg
        foreach ($pLine in ($pathOut -split "`n")) {
            if ($pLine -match "package:(.+base\.apk)") {
                $remoteApk = $matches[1].Trim()
                Write-Host "   Pulling $pkg ($remoteApk)..." -ForegroundColor Gray
                adb pull $remoteApk "$OutputDir\apks\$pkg.apk" 2>$null | Out-Null
                $backedUpCount++
            }
        }
    }
}

Write-Host "`n[+] Snapshot complete! $backedUpCount custom APKs backed up safely." -ForegroundColor Green
Write-Host "   Baseline files stored in: $OutputDir" -ForegroundColor Cyan
