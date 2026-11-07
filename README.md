# Unfuck-Android

<p align="center">
  <b>A Systematic, Zero-Root Framework for Debloating, Telemetry Mitigation, and Resource Recovery Across Android Ecosystems.</b><br>
  Verified across ColorOS, Funtouch OS, OriginOS, OxygenOS, Realme UI, HyperOS, MIUI, and One UI.<br>
  <b>Non-Destructive User 0 Isolation · Dual-List Safety Consensus · 100% Mathematically Reversible.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Root-Not%20Required-brightgreen?style=flat-square" alt="No Root">
  <img src="https://img.shields.io/badge/Safety-Dual--List%20Consensus-success?style=flat-square" alt="Dual List Consensus">
  <img src="https://img.shields.io/badge/Reversible-100%25%20User%200-orange?style=flat-square" alt="100% Reversible">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square" alt="Platform Support">
</p>

<p align="center">
  <img src="docs/before-and-after.jpg" alt="Unfuck-Android - Before and After Debloating Comparison" width="850">
</p>

---

> [!CAUTION]
> **DISCLAIMER AND NOTICE OF RISK**
> Modifying Android system packages via ADB involves direct interaction with the Android Package Manager and system services. While this framework operates under strict **User 0 isolation** (preserving system partitions and guaranteeing 100% reversibility), **all scripts and procedures must be executed at your own risk**. The maintainers and contributors assume no liability for device instability, bootloops, data loss, voided warranties, or disruptions to emergency services. Maintain a full baseline backup (**Phase 0**) before executing any modifications.

---

## Abstract and Real-World Benchmark

Modern commercial Android firmware packages come pre-loaded with vendor storefronts, advertisement daemons, diagnostic telemetry loggers, and background analytics hooks that consume significant system resources.

In empirical production testing on Android 14 devices:
* **Starting Storage State:** 10.90 GB available (10% free partition capacity; 547 active packages).
* **Final Post-Debloat State:** 35.36 GB available (33% free partition capacity; 474 active packages).
* **Net Recovered Storage:** **+24.46 GB** reclaimed without factory resetting or altering partition structures.
* **System Metrics:** Zero logcat errors, over 2.0 GB of physical RAM de-allocated from background workers, and device idle CPU capacity maintained above 95%.

---

## Supported Ecosystems and Architectures

<p align="center">
  <img src="docs/brands-lineup.jpg" alt="Supported Android Brands and Operating Systems" width="850">
</p>

| Manufacturer | Operating System | Base Framework | Curated Debloat Profile |
| :--- | :--- | :--- | :--- |
| **Oppo** | ColorOS (5, 6, 7, 11, 12, 13, 14, 15) | OPLUS / HeyTap / NearMe | [`lists/oppo/coloros-safe-debloat.txt`](lists/oppo/coloros-safe-debloat.txt) |
| **vivo** | Funtouch OS (3, 4, 9, 10, 11-15) / OriginOS | BBK Vivo Framework | [`lists/vivo/funtouchos-safe-debloat.txt`](lists/vivo/funtouchos-safe-debloat.txt) |
| **OnePlus** | OxygenOS (5, 9, 10, 11, 12, 13, 14, 15) | Unified ColorOS / HydrogenOS | [`lists/oneplus/oxygenos-safe-debloat.txt`](lists/oneplus/oxygenos-safe-debloat.txt) |
| **Realme** | Realme UI (1.0, 2.0, 3.0, 4.0, 5.0, 6.0) | Unified ColorOS | [`lists/realme/realmeui-safe-debloat.txt`](lists/realme/realmeui-safe-debloat.txt) |
| **iQOO** | Funtouch OS / OriginOS / Monster UI | BBK Vivo Framework | [`lists/iqoo/iqoo-safe-debloat.txt`](lists/iqoo/iqoo-safe-debloat.txt) |
| **Xiaomi / POCO** | MIUI (12, 13, 14) / HyperOS (1.0, 2.0) | Xiaomi Core Framework | [`lists/xiaomi/hyperos-safe-debloat.txt`](lists/xiaomi/hyperos-safe-debloat.txt) |
| **Samsung** | One UI (4, 5, 6, 7) | Samsung One UI Framework | [`lists/samsung/oneui-safe-debloat.txt`](lists/samsung/oneui-safe-debloat.txt) |
| **Universal** | All Android Versions (10 - 15) | Meta & Google Tracking Services | [`lists/universal/tracking-telemetry.txt`](lists/universal/tracking-telemetry.txt) |

---

## Safety Architecture and Dual-List Consensus

<p align="center">
  <img src="docs/feature-privacy-telemetry.jpg" alt="Privacy Shield and Telemetry Mitigation" width="750">
</p>

To guarantee system integrity and prevent bootloops, every package included in this repository is validated against the **Dual-List Consensus Matrix** combining two upstream safety authorities:
1. **[Universal Android Debloater Next Generation (UAD-ng)](https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation)**
2. **[MuntashirAkon Android Debloat List](https://github.com/MuntashirAkon/android-debloat-list)**

### The Consensus Decision Matrix

```text
               ┌──────────────────────────────┐
               │    Package Safety Matrix     │
               └──────────────┬───────────────┘
                              │
             Is package in BOTH safety lists?
             ├── YES ──> Follow the MORE CONSERVATIVE rating
             │           (If either list flags caution, mark Optional)
             │
             └── NO ───> Is it in ONE list?
                         ├── YES ──> Remove ONLY if rated 100% Safe
                         │
                         └── NO ───> DO NOT TOUCH (Zero unverified removals)
```

### Core Package Blacklist Regex
The framework hardcodes a strict regex rejection shield. Any command targeting packages matching this pattern will be aborted immediately:

```regex
^(android|android\.ext\.(services|shared)|com\.android\.sdksandbox|com\.android\.location\.fused|com\.android\.systemui|com\.android\.shell|com\.android\.phone|com\.android\.dialer|com\.android\.server\.telecom|com\.android\.settings|com\.android\.keyguard|com\.(google\.)?android\.(permissioncontroller|packageinstaller|ext\.services|ext\.shared|modulemetadata)|com\.google\.android\.overlay\.modules.*|com\.android\.providers\.(telephony|media|downloads|settings)|com\.qualcomm\.qti\.telephonyservice|com\.mediatek\.telephony)$
```

---

## The Four-Phase Execution Pipeline

```text
[ 1. CONNECT & SNAPSHOT ] ──> [ 2. SAFE DEBLOAT ] ──> [ 3. ADS & DISCOVER ] ──> [ 4. STANDBY OPTIMIZE ]
     Phase 0 Baseline               Consensus Engine       Private DNS & Feed          Doze & Buckets
```

### Phase 0: Baseline Snapshot and APK Preservation
Before modifying any configuration, generate an exact baseline inventory and archive non-Play Store sideloaded packages:
```powershell
.\scripts\01-backup-baseline.ps1
```
* Generates `packages-baseline.txt`, `enabled-baseline.txt`, and `disabled-baseline.txt`.
* Automatically detects third-party developer APKs and pulls them into `backup/apks/`.

### Phase 1: Safe Consensus Debloating
Execute brand-specific debloating using verified lists:
```powershell
.\scripts\02-debloat.ps1 -Brand auto
```
* Targets vendor storefronts (HeyTap Market, V-Appstore, Theme Stores).
* Strips lockscreen ad carousels and clickbait feeds (Pictorial, Lockscreen Poster, Glance).
* Removes background diagnostic loggers (LogKit, CrashBox, OneTrace, DeepThinker).
* Preserves all underlying APKs on `/system` using `--user 0` isolation.

### Phase 2: Elimination of In-App Ads, Meta Trackers, and Discover Feeds
1. **Disable the Minus-One Screen (Google Discover Clickbait Feed):**
   ```powershell
   adb shell pm disable-user --user 0 com.google.android.googlequicksearchbox
   adb shell am force-stop com.android.launcher
   ```
   *Consequence:* Swiping left on the home screen no longer opens the pre-fetched news feed, sponsored articles, or video feeds. The launcher stays strictly on the clean home screen.
2. **System-Wide Ad and Telemetry Blocking (Private DNS):**
   * Navigate to **Settings → Connection & sharing → Private DNS**.
   * Select **Designated / Specified Private DNS**.
   * Set hostname to: `dns.adguard-dns.com`
   * *Consequence:* All network queries targeting known tracking SDKs (Meta Graph, AppsFlyer, DoubleClick) are dropped at the DNS layer over TLS without requiring root or local VPN services.

### Phase 3: Battery and Standby Optimization

<p align="center">
  <img src="docs/feature-battery-ram.jpg" alt="Battery and Standby Optimization Benchmarks" width="750">
</p>

```powershell
.\scripts\03-optimize-battery.ps1
```
1. **Radio Background Scanning Mitigation:** Disables hidden background Wi-Fi and Bluetooth scanning (which continuously pulse hardware radios even when switched off in the quick settings).
2. **Doze Whitelist Scrubbing:** Removes pre-exempted commercial and OEM packages from the Android Doze whitelist (`dumpsys deviceidle whitelist`), ensuring they enter low-power sleep when the screen is locked.
3. **Standby Bucket Restrictions:** Places non-essential background applications into the `RESTRICTED` standby bucket (`45`), cutting background execution while maintaining full responsiveness upon user launch.

---

## Engineering Guidelines: Do's and Don'ts

### Principles to Follow
* **Use Built-In Storage Managers for Messaging Apps:**
  * For apps like WhatsApp or Telegram, never execute `pm clear` over ADB. Instead, use in-app storage managers (**WhatsApp → Settings → Storage and data → Manage storage**) to safely purge gigabytes of forwarded media without endangering personal conversations or images.
* **Purge Heavy Media Caches Directly:**
  * Clean dedicated media cache folders (such as Spotify's storage cache at `/sdcard/Android/data/com.spotify.music/files/spotifycache/Storage`) to reclaim gigabytes without resetting user credentials.
* **Trim Stale App Caches Globally:**
  * Execute `adb shell pm trim-caches 1000G` to safely instruct the package manager to clear stale file caches across all installed applications.

### Anti-Patterns to Avoid
* **Never Delete Proprietary Stock Camera Applications:**
  * Vendors (Oppo, Vivo, Xiaomi, Samsung) bundle proprietary image signal processing (ISP) algorithms directly into their camera software. Removing the stock camera APK degrades hardware imaging capabilities.
* **Never Modify Authentication or Telephony Providers:**
  * Avoid altering packages responsible for SIM negotiation, two-factor authentication, or Emergency Broadcast Services (`com.android.phone`, `com.google.android.apps.authenticator2`, `com.android.cellbroadcastreceiver`).
* **Do Not Misinterpret Linux Process and Thread Counts:**
  * A standard Android 14 environment typically shows 800 to 1,000 Linux processes and 5,000+ threads. Over 99% of these remain in `Interruptible Sleep` (`S` state), drawing 0.0% CPU and zero battery until invoked by a hardware interrupt.
* **Do Not Rely on Blocked Thermal Nodes on MediaTek Architectures:**
  * On modern Android builds with MediaTek Dimensity silicon, raw CPU socket nodes (`/sys/class/thermal/`) are locked behind kernel SELinux rules. Monitor **Battery Temperature** (normally 30°C to 38°C) as the true metric of device thermal state.

---

## Post-Debloat Tool Recommendations

To monitor processes and hardware health post-cleanup:

### 1. TaskManager (by Rohit Kushvaha) + Shizuku
* **Overview:** A lightweight open-source system monitor inspired by Windows Task Manager and GNOME System Monitor (**3.6 MB**).
* **Repository:** [RohitKushvaha01/TaskManager](https://github.com/RohitKushvaha01/TaskManager)
* **Functionality:**
  * Real-time per-core CPU utilization and clock frequencies.
  * RAM usage and ZRAM swap compression tracking.
  * **Process Control:** Navigate to the **Processes** tab to inspect per-app PSS memory and terminate misbehaving background applications on demand.
* **Privilege Layer:** Integrates with **[Shizuku](https://shizuku.rikka.app/)** to obtain non-root ADB shell execution authority (`UID 2000`).

### 2. CPU Info (by Kamil Gurgul)
* **Overview:** An open-source hardware, SoC, and thermal diagnostic utility (**2.6 MB**).
* **Repository:** [kamgurgul/cpu-info](https://github.com/kamgurgul/cpu-info)
* **Functionality:** Inspect real-time battery thermal metrics, ARM Cortex core cluster topology, and Mali/Adreno GPU specifications.

---

## Mathematical State Restoration

To reverse all package removals and return the device to its exact baseline state:
```powershell
.\scripts\04-restore.ps1
```
* Queries `packages-baseline.txt` and `enabled-baseline.txt`.
* Invokes `cmd package install-existing <pkg>` to restore all User 0 uninstalled system packages.
* Re-installs archived custom APKs from `backup/apks/` if necessary.
* Restores the exact original enabled/disabled state for every package.

---

## References and Upstream Acknowledgments

This framework builds upon the collective research and safety classifications of the open-source Android debloating community:

* **[Universal Android Debloater Next Generation (UAD-ng)](https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation):** Cross-manufacturer package safety ratings and community issue tracking.
* **[MuntashirAkon Android Debloat List](https://github.com/MuntashirAkon/android-debloat-list):** Comprehensive package intent documentation and removal classification matrices.
* **[Ankodee/cleanyourphone](https://github.com/Ankodee/cleanyourphone):** OEM brand taxonomy, script paradigms, and BBK/OPLUS architecture references.
* **[RikkaApps/Shizuku](https://shizuku.rikka.app/):** The inter-process communication bridge enabling privileged system API execution without root.
* **[RohitKushvaha01/TaskManager](https://github.com/RohitKushvaha01/TaskManager):** Modern open-source Android process inspection and task termination.
* **[kamgurgul/cpu-info](https://github.com/kamgurgul/cpu-info):** Open-source hardware abstraction layer diagnostic tool.

---

## Documentation and Compliance

* **AI Agent Operating Guidelines:** [AGENTS.md](AGENTS.md)
* **Claude Assistant Reference:** [CLAUDE.md](CLAUDE.md)
* **Security Policy & Core Blacklist:** [SECURITY.md](SECURITY.md)
* **Code of Conduct:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
* **License:** [MIT License](LICENSE)
