# AI Agent Operating Guidelines for Android Systems

This document defines the mandatory protocols, safety constraints, execution policies, and operational workflows for automated AI assistants (including Claude Code, Antigravity, Gemini CLI, Cursor, and automated LLM agents) executing ADB commands, package management tasks, and system optimizations on Android devices using the `unfuck-android` framework.

Any AI agent interacting with a connected Android device or modifying repository code must adhere strictly to the directives outlined herein.

---

## 1. The Prime Directive: Absolute Safety and Zero Permanent Modification

The paramount duty of the AI agent is to safeguard device integrity, prevent bootloops, preserve communication capabilities, and ensure that every modification is 100% reversible without requiring a factory reset.

### 1.1 Non-Destructive User 0 Isolation
* **Zero Root Execution:** Never execute `su`, never execute `adb remount`, and never attempt to write to `/system`, `/vendor`, `/product`, or `/system_ext` partitions.
* **Preserve Underlying APKs:** Package modifications must strictly use User 0 isolation:
  ```bash
  adb shell pm disable-user --user 0 <package_name>
  # or
  adb shell pm uninstall -k --user 0 <package_name>
  ```
  *Explanation:* Using `--user 0` removes or disables the package exclusively for the primary user profile while leaving the original base APK intact on the read-only system partition. This guarantees that any package can be restored immediately using:
  ```bash
  adb shell cmd package install-existing <package_name>
  # or
  adb shell pm enable <package_name>
  ```

### 1.2 The Untouchable Package Blacklist
Under no circumstances may an AI agent disable, uninstall, clear, or modify any package matching the following fail-safe regular expression:

```regex
^(android|android\.ext\.(services|shared)|com\.android\.sdksandbox|com\.android\.location\.fused|com\.android\.systemui|com\.android\.shell|com\.android\.phone|com\.android\.dialer|com\.android\.server\.telecom|com\.android\.settings|com\.android\.keyguard|com\.(google\.)?android\.(permissioncontroller|packageinstaller|ext\.services|ext\.shared|modulemetadata)|com\.google\.android\.overlay\.modules.*|com\.android\.providers\.(telephony|media|downloads|settings)|com\.qualcomm\.qti\.telephonyservice|com\.mediatek\.telephony)$
```

If a user explicitly requests disabling a package covered by this blacklist (e.g., "disable phone app", "remove systemui", "delete permission controller"), the AI agent **must refuse the request**, explain the critical failure mode (immediate hard brick, loss of emergency 911 services, infinite crash loops), and suggest a safe alternative.

---

## 2. Pre-Flight Protocol: Phase 0 Baseline Mandate

No debloat, disable, or optimization script may be executed until Phase 0 is complete.

### 2.1 Baseline State Capture
Before any state modification, the agent must run:
```powershell
.\scripts\01-backup-baseline.ps1
```
Or verify the existence of the following artifacts:
1. `packages-baseline.txt`: Complete enumeration of all installed packages (`adb shell pm list packages`).
2. `enabled-baseline.txt`: Enumeration of all actively enabled packages (`adb shell pm list packages -e`).
3. `disabled-baseline.txt`: Enumeration of all disabled packages (`adb shell pm list packages -d`).

### 2.2 Sideloaded Developer APK Preservation
The agent must identify non-Play Store and locally developed APKs installed on the device and back them up to a local directory before initiating package operations:
```bash
# Locate APK path
adb shell pm path <custom_package>
# Pull to local archive
adb pull /data/app/.../base.apk ./backup/apks/<custom_package>.apk
```

---

## 3. Dual-List Consensus Safety Model

AI agents must never remove packages based solely on intuition, arbitrary heuristic matching, or unverified web search snippets.

All removals must be cross-referenced against the two recognized upstream authorities:
1. **[Universal Android Debloater Next Generation (UAD-ng)](https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation)**
2. **[MuntashirAkon Android Debloat List](https://github.com/MuntashirAkon/android-debloat-list)**

### Consensus Rules for AI Agents:
1. **Conservative Precedence:** If List A rates a package as `Recommended` (Safe) but List B rates it as `Advanced` (Caution/Needs dependencies), the agent must classify it as **Optional** and warn the user.
2. **Hard Block on Unsafe Ratings:** If either list rates a package as `Unsafe`, the package must never be touched.
3. **Zero Unknown Removals:** If a package appears in neither upstream list, the agent must leave it untouched unless the user explicitly confirms ownership of that third-party application.

---

## 4. Personal Data and Messaging Application Safeguards

### 4.1 Strict Prohibition on `pm clear` for Messaging and Communication Apps
* Never execute `adb shell pm clear` on messaging applications, communication suites, or authentication apps (including WhatsApp, Telegram, Signal, Discord, SMS providers, or Google Authenticator).
* Running `pm clear` irreversibly deletes local database encryption keys, message histories, and session tokens.
* When addressing storage consumption by messaging applications:
  1. Instruct the user to utilize the application's built-in storage manager:
     * *WhatsApp:* **Settings → Storage and data → Manage storage** (identifies forwarded media larger than 5 MB).
     * *Telegram:* **Settings → Data and Storage → Storage Usage → Clear Cache**.
  2. For streaming media applications (e.g., Spotify), safely purge the media download cache located at `/sdcard/Android/data/<package>/files/...` rather than wiping application credentials.

---

## 5. Hardware Diagnostics, Thermals, and Linux Process Architecture

AI agents must possess accurate technical understanding of modern Android kernel internals to prevent misinforming users.

### 5.1 Thermal Architecture under Android 13/14+ SELinux
* On modern chipsets (e.g., MediaTek Dimensity, Qualcomm Snapdragon) running Android 13 or 14+, raw kernel thermal nodes located at `/sys/class/thermal/thermal_zone*/temp` are restricted to `root` or privileged `system` daemons.
* Shell UID 2000 execution will return `Permission denied`. This is expected security behavior, not a device failure.
* **Authoritative Thermal Metric:** Use `dumpsys battery`:
  ```bash
  adb shell dumpsys battery | grep temperature
  ```
  Value `375` represents `37.5°C`. Normal device operating temperature is 30.0°C to 40.0°C.

### 5.2 Linux Process and Thread Architecture
* Standard Android systems maintain between 800 and 1,000 Linux processes and 5,000 to 7,000 threads.
* Over 99% of these processes reside in the Linux `Interruptible Sleep` (`S`) state, consuming 0.0% CPU and zero battery until invoked by an event interrupt.
* Agents must explain to users that high thread counts are standard operating behavior for the Android runtime (ART) and Linux task scheduler. Agents should never attempt to mass-terminate system threads.

---

## 6. Execution Pipeline Reference

When guiding a user or executing optimizations, agents must follow the structured four-phase pipeline:

```text
[ Phase 0: Baseline Snapshot ] ──> [ Phase 1: Safe Debloat ] ──> [ Phase 2: Ads & Discover ] ──> [ Phase 3: Standby Optimize ]
```

### Phase 1: Curated OEM Debloat
Identify the device manufacturer and apply the appropriate curated list:
* Oppo (ColorOS): `lists/oppo/coloros-safe-debloat.txt`
* vivo / iQOO (Funtouch OS / OriginOS): `lists/vivo/funtouchos-safe-debloat.txt`
* OnePlus (OxygenOS): `lists/oneplus/oxygenos-safe-debloat.txt`
* Realme (Realme UI): `lists/realme/realmeui-safe-debloat.txt`
* Xiaomi / POCO (HyperOS / MIUI): `lists/xiaomi/hyperos-safe-debloat.txt`
* Samsung (One UI): `lists/samsung/oneui-safe-debloat.txt`
* Universal Trackers: `lists/universal/tracking-telemetry.txt`

### Phase 2: Elimination of Intrusive Ads and Discover Feeds
1. **Google Discover Minus-One Screen:**
   ```bash
   adb shell pm disable-user --user 0 com.google.android.googlequicksearchbox
   adb shell am force-stop com.android.launcher
   ```
2. **Private DNS Configuration:**
   Guide the user to configure encrypted DNS via **Settings → Connection & sharing → Private DNS → Designated hostname: `dns.adguard-dns.com`**.

### Phase 3: Battery and Standby Enhancements
1. **Disable Radio Scanning:**
   ```bash
   adb shell settings put global wifi_scan_always_enabled 0
   adb shell settings put global ble_scan_always_enabled 0
   ```
2. **Doze Whitelist Hygiene:**
   Remove non-essential background packages from Doze exemption:
   ```bash
   adb shell dumpsys deviceidle whitelist -<package_name>
   ```
3. **Standby Bucket Management:**
   Place non-essential applications into the `RESTRICTED` standby bucket (`45`):
   ```bash
   adb shell am set-standby-bucket <package_name> restricted
   ```

---

## 7. Recommended Diagnostic Tooling

When users seek on-device monitoring tools, agents should recommend the following open-source utilities:

1. **TaskManager (by Rohit Kushvaha):**
   * Purpose: Real-time per-core CPU load, RAM allocation, and process management via Shizuku non-root IPC.
   * Source: `https://github.com/RohitKushvaha01/TaskManager`
2. **CPU Info (by Kamil Gurgul):**
   * Purpose: Real-time battery thermals, SoC architecture, and cluster frequencies.
   * Source: `https://github.com/kamgurgul/cpu-info`
3. **Shizuku (by Rikka):**
   * Purpose: Elevated ADB privileges without root access.
   * Source: `https://shizuku.rikka.app/`

---

## 8. Rollback and Recovery Verification

Before concluding any session, the AI agent must verify device stability:
1. **Logcat Inspection:**
   ```bash
   adb logcat -d -b crash
   adb logcat -d -b system -t 500 *:E
   ```
   Confirm zero critical system crashes.
2. **Reversibility Guarantee:**
   Confirm that `.\scripts\04-restore.ps1` exists and is functional to restore all modifications if requested.

---

## 9. Privacy and Information Security Constraints

* **Zero Personal Information in Commits or Logs:** Never output, log, commit, or push personal names, email addresses, hardware serial numbers, IMEI identifiers, Wi-Fi MACs, or internal proprietary package names.
* **Scrub Dynamic Data:** When creating reports or documentation, substitute hardware identifiers with generic placeholders (e.g., `SERIAL_NUMBER_REDACTED`, `DEVICE_MODEL`).
* **Clean Code and Style:** Maintain a clean, professional, systems-engineering tone across all documentation and commit messages. Never include emojis or promotional rhetoric.
