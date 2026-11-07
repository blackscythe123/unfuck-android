# Claude Assistant Instructions for Unfuck-Android

This document provides operational context, strict execution rules, and workflow commands for Claude Code and Anthropic AI assistants operating within the `unfuck-android` repository or managing connected Android devices via ADB.

---

## 1. Core Principles and Operational Mandates

1. **Safety First:** Read `AGENTS.md` and `SECURITY.md` before executing any device modification or script.
2. **Zero Root & User 0 Isolation:** Never use `su` or remount partitions. Only modify packages in the user context:
   ```bash
   adb shell pm disable-user --user 0 <pkg>
   adb shell pm uninstall -k --user 0 <pkg>
   ```
3. **Untouchable Blacklist:** Never touch packages matching the protected regex:
   ```regex
   ^(android|android\.ext\.(services|shared)|com\.android\.sdksandbox|com\.android\.location\.fused|com\.android\.systemui|com\.android\.shell|com\.android\.phone|com\.android\.dialer|com\.android\.server\.telecom|com\.android\.settings|com\.android\.keyguard|com\.(google\.)?android\.(permissioncontroller|packageinstaller|ext\.services|ext\.shared|modulemetadata)|com\.google\.android\.overlay\.modules.*|com\.android\.providers\.(telephony|media|downloads|settings)|com\.qualcomm\.qti\.telephonyservice|com\.mediatek\.telephony)$
   ```
4. **Mandatory Phase 0 Snapshot:** Always run `.\scripts\01-backup-baseline.ps1` to capture snapshots and back up third-party/developer APKs before executing any removals.
5. **Visual HTML Dashboard Mandate:** Always generate `storage-analyzer.html` using `.\scripts\05-storage-report.ps1` or `python tools/generate_storage_report.py` so the user can inspect disk usage, Code vs Data vs Cache, and recovery tiers visually.
6. **Storage Component Rules:**
   * **App Code (APK):** Binary executable size. Reclaimed only by debloating (`pm disable-user --user 0`).
   * **App User Data:** Private databases, logins, encryption keys. Never wipe with `pm clear` on chat/banking apps. Direct user to in-app storage managers for WhatsApp/Telegram.
   * **App Cache:** Volatile temporary files. Safe to purge at any time via `adb shell pm trim-caches 1000G` with zero loss of logins or chat histories.
7. **Zero-Tracker Objective & Private DNS:** Remove Meta and OEM telemetry daemons. Instruct user to configure Private DNS hostname (`dns.adguard-dns.com`) for system-wide tracker dropping.
8. **Preserve Daily Utilities & Request Consent:** Never disable OEM Notes, Clock/Alarm, Calculator, or Calendar without verifying active user data and asking for explicit user consent.
9. **Stability Verification ("Ensure Nothing Breaks"):** Always inspect `adb logcat -d -b crash` to verify zero system crashes after completing debloat passes.
10. **Zero Emojis & Strict Privacy:** Maintain an objective, professional systems-engineering tone. Never output personal names, emails, real serial numbers, or private package names.

---

## 2. Standard Command Reference

### Connection and Diagnostics
```bash
adb devices -l
adb shell getprop ro.product.manufacturer
adb shell getprop ro.build.version.release
adb shell df -h /data
```

### Phase 0: Baseline Snapshot and APK Preservation
```powershell
.\scripts\01-backup-baseline.ps1
```

### Storage Analysis Dashboard Generation
```powershell
.\scripts\05-storage-report.ps1
# or
python tools/generate_storage_report.py
```

### Phase 1: Brand Debloat
```powershell
.\scripts\02-debloat.ps1 -Brand auto
```
Supported brand flags: `oppo`, `vivo`, `oneplus`, `realme`, `iqoo`, `xiaomi`, `samsung`, `universal`.

### Phase 2: Elimination of Ads, Trackers, and Discover Feed
```bash
# Disable Google Discover Feed on Launcher Minus-One Screen
adb shell pm disable-user --user 0 com.google.android.googlequicksearchbox
adb shell am force-stop com.android.launcher

# System-Wide Private DNS (Settings -> Connection & sharing -> Private DNS):
# dns.adguard-dns.com
```

### Phase 3: Battery and Standby Optimization
```powershell
.\scripts\03-optimize-battery.ps1
```

### Stability and Subsystem Verification
```bash
# Check for system crashes
adb logcat -d -b crash
adb logcat -d -b system -t 500 *:E

# Check battery temperature (e.g., 375 = 37.5 C)
adb shell dumpsys battery | grep temperature

# Check CPU idle load (>95% idle)
adb shell dumpsys cpuinfo | head -n 10
```

### Rollback and Full Restoration
```powershell
.\scripts\04-restore.ps1
```

---

## 3. Empirical Benchmark Context

During production device validation on modern Android 14 hardware, this framework achieved:
* **Storage Reclaimed:** +24.46 GB net storage directly recovered (capacity expanded from 10.90 GB / 10% free to 35.36 GB / 33% free).
* **Package Reduction:** Active package count decreased from 547 down to 474 (73 bloat/telemetry packages safely disabled).
* **RAM De-allocation:** Over 2.0 GB physical RAM freed from background services.
* **Thermals:** Battery temperature stabilized at 37°C–38°C.
* **Stability:** 0 logcat crash events.

---

## 4. Git and Repository Policy

* **Commit Message Format:** Single-line message (`tag: short message`), under 25 words.
* **No AI Trailers:** Never add `Co-Authored-By` or AI attribution trailers.
* **Privacy Verification:** Verify no personal identifiers or real serial numbers are staged before committing.
