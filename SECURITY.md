# Security Policy & Critical Safety Rules

> [!CAUTION]
> ### DISCLAIMER AND WARNING: USE AT YOUR OWN RISK
> Modifying Android system packages via ADB involves low-level operating system controls. While our debloat lists and scripts are strictly curated against dual-list safety consensus and operate under **User 0 isolation** (meaning `/system` is never permanently modified and changes are 100% reversible), **you execute these operations entirely at your own discretion and risk**. The author and contributors are not responsible for bricked devices, bootloops, data loss, voided warranties, or malfunctioning emergency services. Always maintain a full mathematical baseline snapshot (Phase 0) before executing any debloat operations.

---

## 1. Protected Core Packages (The Untouchable Blacklist)

The `unfuck-android` suite strictly refuses to disable or modify any package matching this fail-safe regex blacklist:

```regex
^(android|android\.ext\.(services|shared)|com\.android\.sdksandbox|com\.android\.location\.fused|com\.android\.systemui|com\.android\.shell|com\.android\.phone|com\.android\.dialer|com\.android\.server\.telecom|com\.android\.settings|com\.android\.keyguard|com\.(google\.)?android\.(permissioncontroller|packageinstaller|ext\.services|ext\.shared|modulemetadata)|com\.google\.android\.overlay\.modules.*|com\.android\.providers\.(telephony|media|downloads|settings)|com\.qualcomm\.qti\.telephonyservice|com\.mediatek\.telephony)$
```

### Critical Packages Explained

| Package | Purpose | Disabling Consequence |
| :--- | :--- | :--- |
| `android` | Android OS Core Framework | **Immediate bootloop / hard brick** |
| `com.android.systemui` | Status bar, navigation bar, recent apps, notifications | Infinite crash loop; screen goes black |
| `com.android.phone` / `telephony` | Cellular modem, radio interface, SIM stack | Loss of cellular connection, **no 911/emergency calls** |
| `permissioncontroller` | Grants/revokes runtime app permissions | All apps crash immediately when asking for permissions |
| `packageinstaller` | Allows APK installation and updates | Cannot install, update, or sideload any app |
| `com.android.keyguard` | PIN, password, pattern, fingerprint lockscreen | Cannot unlock phone |
| `com.android.settings` | System settings app | Settings crashes; cannot access Wi-Fi, Bluetooth, or Display |

---

## 2. Safety Rules & Rating Consensus

`unfuck-android` cross-references every package against two recognized safety authorities:
1. **[Universal Android Debloater Next Generation (UAD-ng)](https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation)**
2. **[MuntashirAkon Android Debloat List](https://github.com/MuntashirAkon/android-debloat-list)**

### The Consensus Decision Matrix

```text
               ┌──────────────────────────────┐
               │    Package Safety Matrix     │
               └──────────────┬───────────────┘
                              │
             Is package in BOTH safety lists?
             ├── YES ──> Follow the MORE CAUTIOUS rating
             │           (If either says Advanced, move to Optional)
             │
             └── NO ───> Is it in ONE list?
                         ├── YES ──> Remove ONLY if rated 100% SAFE
                         │
                         └── NO ───> LEAVE IT ALONE (0 unknown removals)
```

1. **Conservative Override:** If List A rates a package "Recommended" (Safe) but List B rates it "Advanced" (Needs caution), `unfuck-android` moves it to the Optional list and warns the user. If either list rates it "Unsafe", it is permanently blacklisted.
2. **Zero Unknown Removals:** If a package appears in neither list, it is left completely untouched.
3. **User 0 Isolation:** All removals are executed using `pm disable-user --user 0` or `pm uninstall -k --user 0`.
   * The actual APK remains preserved in `/system` or `/vendor`.
   * No root access is ever required.
   * Any app can be restored instantly via `cmd package install-existing <pkg>` or `pm enable <pkg>`.

---

## 3. ADB & Network Hygiene

When connecting your phone via ADB:

* **Turn off USB / Wireless Debugging** immediately after completing your debloat session.
* Leaving Network ADB (port 5555) open on public or shared Wi-Fi networks exposes your device shell to unauthorized LAN connections.
* Revoke USB debugging authorizations in `Developer Options` when you are finished.

---

## 4. Reporting Security Vulnerabilities

If you discover a package in our safe lists that causes a bootloop, prevents emergency calls, breaks Play Integrity, or leads to system instability:

1. Open an issue with the tag `[SAFETY CRITICAL]`.
2. Include the phone brand, model, OS build (`ro.build.display.id`), and logcat output if available.
3. The package will be pulled immediately from default safe lists into the protected blacklist.
