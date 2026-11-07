# Claude Assistant Instructions for Unfuck-Android

This document provides operational context and strict execution rules for Claude Code and Anthropic AI assistants operating within the `unfuck-android` repository or managing connected Android devices via ADB.

---

## 1. Core Principles

1. **Safety First:** Read `AGENTS.md` and `SECURITY.md` before executing any device modification or script.
2. **Zero Root & User 0 Isolation:** Never use `su` or remount partitions. Only modify packages in the user context:
   ```bash
   adb shell pm disable-user --user 0 <pkg>
   adb shell pm uninstall -k --user 0 <pkg>
   ```
3. **Blacklist Enforcement:** Never touch packages matching the protected regex:
   ```regex
   ^(android|android\.ext\.(services|shared)|com\.android\.sdksandbox|com\.android\.location\.fused|com\.android\.systemui|com\.android\.shell|com\.android\.phone|com\.android\.dialer|com\.android\.server\.telecom|com\.android\.settings|com\.android\.keyguard|com\.(google\.)?android\.(permissioncontroller|packageinstaller|ext\.services|ext\.shared|modulemetadata)|com\.google\.android\.overlay\.modules.*|com\.android\.providers\.(telephony|media|downloads|settings)|com\.qualcomm\.qti\.telephonyservice|com\.mediatek\.telephony)$
   ```
4. **Mandatory Phase 0:** Never execute removals without first creating the baseline snapshots (`packages-baseline.txt`, `enabled-baseline.txt`) and backing up third-party/developer APKs.
5. **No `pm clear` on Messaging Apps:** Never wipe user data on WhatsApp, Telegram, Signal, or communication apps. Guide the user to in-app storage managers instead.
6. **Zero Emojis:** Maintain a strict, professional, systems-engineering tone across all documentation and commit messages.
7. **Absolute Privacy:** Never record, commit, or push personal names, emails, device serial numbers, or private application identifiers.

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

### Phase 1: Brand Debloat
```powershell
.\scripts\02-debloat.ps1 -Brand auto
```
Supported brand flags: `oppo`, `vivo`, `oneplus`, `realme`, `iqoo`, `xiaomi`, `samsung`, `universal`.

### Phase 2: Ads and Discover Feed Mitigation
```bash
# Disable Google Discover Feed on Launcher Minus-One Screen
adb shell pm disable-user --user 0 com.google.android.googlequicksearchbox
adb shell am force-stop com.android.launcher

# Advise User to Set Private DNS Hostname:
# dns.adguard-dns.com
```

### Phase 3: Battery and Standby Optimization
```powershell
.\scripts\03-optimize-battery.ps1
```

### System Health and Stability Verification
```bash
# Check battery temperature (e.g. 375 = 37.5 C)
adb shell dumpsys battery | grep temperature

# Verify crash logcat
adb logcat -d -b crash
```

### Rollback and Full Restoration
```powershell
.\scripts\04-restore.ps1
```

---

## 3. Git and Repository Policy

* **Commit Message Format:** Single-line message (`tag: short message`), under 25 words.
* **No AI Trailers:** Never add `Co-Authored-By`, assistant names, or AI attribution tags to commit messages or PR descriptions.
* **Privacy Verification:** Verify no personal names, emails, or device serials are staged before committing:
  ```bash
  git diff --cached
  ```
