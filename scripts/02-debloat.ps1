<#
.SYNOPSIS
    Phase 2: Universal Safe Android Debloater
.DESCRIPTION
    Safely disables or uninstalls OEM bloatware, tracking telemetry, and ad services
    using brand-specific verified consensus lists under User 0 isolation.
#>
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("oppo", "oneplus", "realme", "vivo", "iqoo", "xiaomi", "samsung", "auto")]
    [string]$Brand = "auto",
    
    [switch]$IncludeOptional = $false
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " EXECUTING PHASE 2: SAFE ANDROID DEBLOAT PIPELINE" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Detect connected device
$device = adb devices | Select-String -Pattern "\s+device$"
if (-not $device) {
    Write-Error "No Android device detected over ADB. Enable USB Debugging and reconnect."
    exit 1
}

# 2. Auto-detect manufacturer brand if requested
if ($Brand -eq "auto") {
    $rawBrand = (adb shell getprop ro.product.brand).Trim().ToLower()
    $rawManufacturer = (adb shell getprop ro.product.manufacturer).Trim().ToLower()
    Write-Host "Detected device brand: $rawBrand ($rawManufacturer)" -ForegroundColor Yellow

    if ($rawBrand -match "oppo" -or $rawManufacturer -match "oppo") { $Brand = "oppo" }
    elseif ($rawBrand -match "oneplus" -or $rawManufacturer -match "oneplus") { $Brand = "oneplus" }
    elseif ($rawBrand -match "realme" -or $rawManufacturer -match "realme") { $Brand = "realme" }
    elseif ($rawBrand -match "vivo" -or $rawManufacturer -match "vivo") { $Brand = "vivo" }
    elseif ($rawBrand -match "iqoo") { $Brand = "iqoo" }
    elseif ($rawBrand -match "xiaomi" -or $rawBrand -match "redmi" -or $rawBrand -match "poco") { $Brand = "xiaomi" }
    elseif ($rawBrand -match "samsung") { $Brand = "samsung" }
    else {
        Write-Warning "Brand could not be auto-matched. Defaulting to 'oppo' profile."
        $Brand = "oppo"
    }
}

Write-Host "Active Target Profile: $Brand" -ForegroundColor Cyan

# 3. Locate debloat lists
$listDir = "$PSScriptRoot\..\lists"
$safeList = "$listDir\$Brand\$Brand-safe-debloat.txt"
$commonList = "$listDir\common\third-party-bloat.txt"
$telemetryList = "$listDir\common\google-telemetry-safe.txt"
$facebookList = "$listDir\common\facebook-bloat.txt"

$targetLists = @($safeList, $commonList, $telemetryList, $facebookList)
if ($IncludeOptional) {
    $optList = "$listDir\$Brand\$Brand-optional-debloat.txt"
    if (Test-Path $optList) { $targetLists += $optList }
}

# 4. Read installed packages
$installedRaw = adb shell pm list packages --user 0
$installedSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($line in $installedRaw) {
    $clean = $line.Trim()
    if ($clean.StartsWith("package:")) { [void]$installedSet.Add($clean.Substring(8).Trim()) }
}

# 5. Core package safety regex
$coreRegex = "^(android|android\.ext\.(services|shared)|com\.android\.sdksandbox|com\.android\.location\.fused|com\.android\.systemui|com\.android\.shell|com\.android\.phone|com\.android\.dialer|com\.android\.server\.telecom|com\.android\.settings|com\.android\.keyguard|com\.(google\.)?android\.(permissioncontroller|packageinstaller|ext\.services|ext\.shared|modulemetadata)|com\.google\.android\.overlay\.modules.*|com\.android\.providers\.(telephony|media|downloads|settings)|com\.qualcomm\.qti\.telephonyservice|com\.mediatek\.telephony)$"

$processed = 0
$skipped = 0

foreach ($lFile in $targetLists) {
    if (-not (Test-Path $lFile)) { continue }
    Write-Host "`nProcessing: $(Split-Path $lFile -Leaf)" -ForegroundColor Yellow

    foreach ($pkg in (Get-Content $lFile)) {
        $p = $pkg.Trim()
        if (-not $p -or $p.StartsWith("#")) { continue }

        # Safety Check: Never touch core packages
        if ($p -match $coreRegex) {
            Write-Warning "  [SAFETY SHIELD] Refusing to touch core package: $p"
            continue
        }

        if ($installedSet.Contains($p)) {
            Write-Host -NoNewline "  Uninstalling $p... "
            $res = adb shell pm uninstall -k --user 0 $p
            if ($res -like "*Success*") {
                Write-Host "Success" -ForegroundColor Green
                $processed++
            } else {
                # Fallback to disable-user
                Write-Host -NoNewline "Retrying with disable-user... "
                $res2 = adb shell pm disable-user --user 0 $p
                Write-Host "$res2" -ForegroundColor Gray
                $processed++
            }
        } else {
            $skipped++
        }
    }
}

Write-Host "`n✅ Debloat complete! $processed packages removed/disabled ($skipped skipped / not on device)." -ForegroundColor Green
