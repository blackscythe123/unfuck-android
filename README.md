# Unfuck-Android 🚀

<p align="center">
  <b>The definitive, zero-bullshit guide & toolkit to reclaiming battery, RAM, privacy, and 20+ GB of storage from ANY Android phone.</b><br>
  Tested and verified across <b>Oppo</b>, <b>vivo</b>, <b>OnePlus</b>, <b>Realme</b>, <b>iQOO</b>, <b>Xiaomi</b>, and <b>Samsung</b> devices over USB or Wi-Fi.<br>
  <b>Zero Root Required · Nothing Permanently Deleted · 100% Reversible Mathematical Snapshot.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Root-Not%20Required-brightgreen?style=flat-square" alt="No Root">
  <img src="https://img.shields.io/badge/Safety-Dual--List%20Consensus-success?style=flat-square" alt="Dual List Consensus">
  <img src="https://img.shields.io/badge/Reversible-100%25%20User%200-orange?style=flat-square" alt="100% Reversible">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square" alt="Platform Support">
</p>

---

> [!CAUTION]
> ### ⚠️ WARNING: EXECUTE AT YOUR OWN RISK
> Modifying Android system packages via ADB touches low-level operating system controls. While this repository operates under strict **User 0 isolation** (meaning files inside `/system` are never deleted and every change is 100% reversible), **you run these scripts entirely at your own risk**. The authors and contributors accept no responsibility for bricked devices, bootloops, lost data, voided warranties, or broken emergency calls. Always maintain a full mathematical baseline snapshot (**Phase 0**) before modifying anything!

---

## 📊 Proven Real-World Results

In a live production test on an **OPPO Reno8 5G (ColorOS 14 / Android 14)**:
* **Starting Capacity:** `10.90 GB Free` (10% capacity, 90% full, 547 active packages).
* **Final Post-Debloat:** **`35.36 GB Free`** (33% available capacity, 474 active packages).
* **Net Storage Directly Reclaimed:** **`+24.46 GB`** (Available space officially **TRIPLED**!).
* **System Stability:** **0 crashes in logcat**, 2+ GB physical RAM freed, battery temperature cooled to 37°C.
* **Interactive Visual Report:** Interactive before-and-after audit dashboard generated at [`docs/storage-analyzer.md`](docs/storage-analyzer.md).

---

## 📱 Supported Brands & Operating Systems

| Brand | Operating System | Shared Base Architecture | Verified Safe Profile |
| :--- | :--- | :--- | :--- |
| **Oppo** | ColorOS (5, 6, 7, 11, 12, 13, 14, 15) | OPLUS / HeyTap / NearMe | [`lists/oppo/coloros-safe-debloat.txt`](lists/oppo/coloros-safe-debloat.txt) |
| **vivo** | Funtouch OS (3, 4, 9, 10, 11–15) / OriginOS | BBK Vivo | [`lists/vivo/funtouchos-safe-debloat.txt`](lists/vivo/funtouchos-safe-debloat.txt) |
| **OnePlus** | OxygenOS (5, 9, 10, 11, 12, 13, 14, 15) | Unified ColorOS / HydrogenOS | [`lists/oneplus/oxygenos-safe-debloat.txt`](lists/oneplus/oxygenos-safe-debloat.txt) |
| **Realme** | Realme UI (1.0, 2.0, 3.0, 4.0, 5.0, 6.0) | Unified ColorOS | [`lists/realme/realmeui-safe-debloat.txt`](lists/realme/realmeui-safe-debloat.txt) |
| **iQOO** | Funtouch OS / OriginOS / Monster UI | BBK Vivo | [`lists/iqoo/iqoo-safe-debloat.txt`](lists/iqoo/iqoo-safe-debloat.txt) |
| **Xiaomi / POCO**| MIUI (12, 13, 14) / HyperOS (1.0, 2.0) | Xiaomi Core | [`lists/xiaomi/hyperos-safe-debloat.txt`](lists/xiaomi/hyperos-safe-debloat.txt) |
| **Samsung** | One UI (4, 5, 6, 7) | Samsung One UI | [`lists/samsung/oneui-safe-debloat.txt`](lists/samsung/oneui-safe-debloat.txt) |
| **Universal** | All Android Brands (10 - 15) | Meta & Google Daemons | [`lists/universal/tracking-telemetry.txt`](lists/universal/tracking-telemetry.txt) |

---

## 🛠️ The 4-Phase System Unfucking Workflow

```text
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. CONNECT &    │ ──> │ 2. SAFE DEBLOAT  │ ──> │ 3. ADS, TRACKERS│ ──> │ 4. STANDBY &    │
│    SNAPSHOT     │     │    PIPELINE      │     │    & DISCOVER   │     │    DASHBOARD    │
│ (Phase 0 exact) │     │ (Dual-consensus) │     │ (Private DNS)   │     │ (HTML visual)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘     └─────────────────┘
```

### Phase 0: The Mathematical Baseline Snapshot
Before touching a single package, create an exact snapshot of your device and back up any sideloaded developer APKs:
```powershell
.\scripts\01-backup-baseline.ps1
```
* Generates `packages-baseline.txt`, `enabled-baseline.txt`, and `disabled-baseline.txt`.
* Automatically detects non-Play Store sideloaded APKs and backs them up into `backup/apks/`.

### Phase 1: Visual Analytics Dashboard Setup
Launch [`docs/storage-analyzer.md`](docs/storage-analyzer.md) in your browser. This interactive dashboard tracks:
* Baseline storage vs live available storage.
* Net gigabytes reclaimed in real time.
* Interactive category breakdown (App Code, Data, Photos, Cache, Video).
* Audited ledger of every uninstalled, frozen, and protected package.

### Phase 2: Safe Debloat Execution
Run the automated debloat pipeline with your detected brand profile:
```powershell
.\scripts\02-debloat.ps1 -Brand auto
```
* Removes preloaded OEM store bloat (HeyTap Market, V-Appstore, Theme Stores).
* Eliminates lockscreen wallpaper carousels & clickbait ads (Pictorial, Lockscreen Poster, Glance).
* Purges diagnostic loggers & background analytics (LogKit, CrashBox, OneTrace, DeepThinker).
* **Strict Guardrails:** Verifies every package against our untouchable core blacklist (never touches phone dialers, emergency services, settings, or system UI).

### Phase 3: In-App Ads, Meta Trackers & Google Discover Elimination
1. **Kill the Left-Swipe Google Discover Feed:**
   ```powershell
   adb shell pm disable-user --user 0 com.google.android.googlequicksearchbox
   adb shell am force-stop com.android.launcher
   ```
   *Result:* Swiping left on your home screen stops loading clickbait news, sponsored articles, and autoplaying video previews. Your launcher stays strictly on your clean home screen.
2. **System-Wide Ad & Meta Tracker Blocking (Private DNS):**
   * Go to **Settings → Connection & sharing → Private DNS**.
   * Select **Designated Private DNS (or Specified DNS)**.
   * Enter: `dns.adguard-dns.com`
   * *Result:* Every ad request, doubleclick banner, and background Meta/Instagram telemetry ping is filtered over encrypted DNS-over-TLS before reaching your screen.

### Phase 4: Battery & Standby Optimization
```powershell
.\scripts\03-optimize-battery.ps1
```
1. **Kills Hidden Radio Scanning:** Disables background Wi-Fi and Bluetooth scanning (which continuously pulse signals 24/7 even when Wi-Fi and Bluetooth are switched off).
2. **Purges Doze Whitelist:** Removes Facebook and OEM ad services from Android’s battery exemption list so they can no longer hold wake locks when your screen is locked.
3. **Throttles Standby Buckets:** Places non-essential apps into the `RESTRICTED` standby bucket (`45`), cutting off background network usage when in your pocket while keeping them 100% active when opened.

---

## 💡 The "Do's and Don'ts" (Battle-Tested Lessons)

Follow these rules derived directly from real-world debloating experience:

### The DO's ✅
* **DO use WhatsApp's built-in Storage Manager:**
  * Forwarded memes and duplicate videos are usually your phone's largest space hogs.
  * *Never run `pm clear` via ADB on WhatsApp!* Instead, open **WhatsApp → Settings → Storage and data → Manage storage** to safely delete 4–10 GB of forwarded files in 30 seconds with **zero risk** to personal chats or photos.
* **DO clear massive media app caches:**
  * Spotify and Telegram store gigabytes of cached songs and video buffers. Clearing `/sdcard/Android/data/com.spotify.music/files/spotifycache/Storage` can reclaim 3+ GB instantly without logging you out.
* **DO trim system caches safely:**
  * Run `adb shell pm trim-caches 1000G` to instruct Android's package manager to cleanly purge stale application caches across all installed apps.
* **DO understand the 900+ processes & 6,000+ threads in Linux:**
  * Seeing 900 processes in a task monitor is **100% normal on Android**. 99.9% of them are in `Interruptible Sleep` (`S` state), drawing 0% CPU and zero battery until tapped.

### The DON'Ts ❌
* **DON'T touch user sideloaded or developer APKs:**
  * If you have personal APKs, custom portfolio apps, or developer builds, ensure they are strictly whitelisted before running automated scripts.
* **DON'T uninstall stock camera apps:**
  * Phones from Oppo, Vivo, Xiaomi, and Samsung embed proprietary camera ISP hardware tuning inside their stock camera APK. Deleting the stock camera severely degrades photo and video quality.
* **DON'T delete phone dialers or authentication apps:**
  * Never touch Google Authenticator, SIM toolkits, or carrier emergency broadcast receivers (`com.android.phone`, `com.android.cellbroadcastreceiver`).
* **DON'T panic over CPU temperature readings:**
  * On modern Android (12–15) with MediaTek Dimensity or Qualcomm chips, raw CPU socket sensors (`/sys/class/thermal/`) are locked behind kernel SELinux permissions. What actually matters for device health is **Battery Temperature** (normally 30°C–38°C; danger threshold is 45°C+).

---

## 🧰 Post-Debloat Toolkit: The "Windows Task Manager" for Android

To maintain your phone's peak responsiveness:

### 1. TaskManager (by Rohit Kushvaha) + Shizuku
* **What It Is:** An open-source clone of Windows Task Manager / GNOME System Monitor for Android (**only 3.6 MB**).
* **GitHub:** [RohitKushvaha01/TaskManager](https://github.com/RohitKushvaha01/TaskManager)
* **What It Does:**
  * Live CPU utilization & clock frequencies per core.
  * Live RAM usage & ZRAM swap compression meters.
  * **1-Tap Process Killer:** Tap the **Processes** tab, find any memory-hungry app (like Instagram or Facebook), and tap **Kill** to terminate it from RAM immediately.
* **How It Runs Without Root:** Pairs with **[Shizuku](https://shizuku.rikka.app/)** to execute privileged `force-stop` signals using ADB shell permissions directly on-device.

### 2. CPU Info (by Kamil Gurgul)
* **What It Is:** A lightweight, 100% open-source hardware & temperature dashboard (**2.6 MB**).
* **GitHub:** [kamgurgul/cpu-info](https://github.com/kamgurgul/cpu-info)
* **What It Does:** Tap the **Temperature** tab for live battery thermal monitoring, and the **Hardware** tab for SoC architecture, GPU model (Mali / Adreno), and core frequencies.

---

## 🔄 Instant One-Command Rollback

If you ever need to restore any uninstalled or disabled app, or return your phone to its exact starting state:
```powershell
.\scripts\04-restore.ps1
```
* Reinstalls all uninstalled packages using `cmd package install-existing <pkg>`.
* Falls back to installing backed-up APKs from `backup/apks/` for sideloaded apps.
* Re-enables every package back to its exact baseline state.

---

## 📜 Legal, Security & Code of Conduct

* **License:** [MIT License](LICENSE) — Free for personal and commercial use.
* **Security Policy & Core Blacklist:** [SECURITY.md](SECURITY.md) — Protected package regex and vulnerability reporting.
* **Community Guidelines:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Contributor Covenant.

---

<p align="center">
  <i>"Fast phones, zero bloat, zero bullshit."</i>
</p>
