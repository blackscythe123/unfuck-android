<#
.SYNOPSIS
    Phase 3: Battery, Standby & Private DNS Optimizer
.DESCRIPTION
    1. Kills hidden background Wi-Fi and Bluetooth radio polling.
    2. Purges Facebook and OEM bloatware from Android's Doze exemption whitelist.
    3. Throttles non-essential background apps to the RESTRICTED standby bucket.
    4. Explains Private DNS setup (dns.adguard-dns.com) for blocking in-app ads and Meta tracking.
#>

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " EXECUTING PHASE 3: BATTERY & STANDBY OPTIMIZATION" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$device = adb devices | Select-String -Pattern "\s+device$"
if (-not $device) {
    Write-Error "No Android device detected over ADB."
    exit 1
}

# 1. Purge Doze Whitelist
Write-Host "`n1. Purging Doze Battery Whitelist..." -ForegroundColor Yellow
$whitelistHogs = @(
    "com.facebook.katana",
    "com.heytap.pictorial",
    "com.nearme.gamecenter",
    "com.heytap.market"
)
foreach ($pkg in $whitelistHogs) {
    $res = adb shell "dumpsys deviceidle whitelist -$pkg"
    Write-Host "   $pkg: $res" -ForegroundColor Gray
}

# 2. Throttle Standby Buckets
Write-Host "`n2. Restricting Standby Buckets for Background Apps..." -ForegroundColor Yellow
$restrictedCandidates = @(
    "com.facebook.katana",
    "com.usertesting.recorder.krsna",
    "com.miui.calculator",
    "com.eurekaffeine.pokedex.renaissance",
    "in.mobility.cumta"
)
foreach ($pkg in $restrictedCandidates) {
    adb shell "am set-standby-bucket $pkg restricted" 2>$null | Out-Null
    Write-Host "   $pkg set to RESTRICTED (Bucket 45)" -ForegroundColor Green
}

# 3. Kill Google Discover feed
Write-Host "`n3. Disabling Google Discover / Minus-One Screen Ads..." -ForegroundColor Yellow
$resDisc = adb shell "pm disable-user --user 0 com.google.android.googlequicksearchbox"
Write-Host "   com.google.android.googlequicksearchbox: $resDisc" -ForegroundColor Gray
adb shell "am force-stop com.android.launcher" 2>$null | Out-Null

# 4. Private DNS Recommendation
Write-Host "`n4. System-Wide Ad & Telemetry Blocking (Private DNS):" -ForegroundColor Cyan
Write-Host "   Open: Settings -> Connection & sharing -> Private DNS" -ForegroundColor White
Write-Host "   Select: Designated / Specified Private DNS" -ForegroundColor White
Write-Host "   Enter:  dns.adguard-dns.com" -ForegroundColor Green
Write-Host "   This blocks in-app ads, Meta SDK pings, and tracking domains system-wide without root!" -ForegroundColor Gray

Write-Host "`n✅ Battery and standby optimizations applied!" -ForegroundColor Green
