# About Unfuck-Android

`unfuck-android` is an open-source systems engineering project dedicated to restoring device speed, recovering storage capacity, and eliminating background telemetry across commercial Android smartphones without requiring root privileges.

---

## The Problem: Modern Android Firmware Bloat

Commercial Android smartphones across major original equipment manufacturers (OEMs) ship with hundreds of pre-installed vendor packages. These bundled applications fall into distinct categories:

1. **Vendor Storefronts and Monetization Platforms:** Duplicate app stores, theme stores, and coin ecosystems designed to push recurring promotional notifications.
2. **Lockscreen Ad Services:** Lockscreen magazines (such as Pictorial, Lockscreen Poster, and Glance) that continuously fetch high-resolution sponsored imagery and video advertisements over cellular data.
3. **Minus-One Screen Feeds:** Pre-fetched news and clickbait feeds (e.g., Google Discover) that consume CPU cycles and RAM on home screen swipe.
4. **Diagnostic & Telemetry Loggers:** Deep vendor tracking engines (ROM statistics, DCS logging, CrashBox, LogKit, and OneTrace) that continuously record device events and transmit telemetry.
5. **Pre-exempted Background Daemons:** Commercial social and analytics packages pre-whitelisted to bypass standard Android Doze battery sleep states.

The standard internet advice to "just factory reset" only resets the phone to the exact same bloated state while erasing all user accounts. Rooting the phone breaks Android Play Integrity, prevents the use of banking and enterprise applications, and permanently voids hardware warranties.

---

## The Architectural Solution

`unfuck-android` provides a disciplined, non-destructive alternative built on the Android Package Manager's low-level architecture:

### 1. Non-Destructive User 0 Isolation
Modern Android architecture supports multi-user profiles. When a package is uninstalled using:
```bash
pm uninstall -k --user 0 <package>
```
or disabled using:
```bash
pm disable-user --user 0 <package>
```
the application binary remains untouched in the read-only `/system` or `/vendor` partition. The operating system kernel treats the application as nonexistent exclusively for the primary user profile (`User 0`). 

* Zero RAM is allocated.
* Zero background processes or threads are spawned.
* Zero network sockets are opened to telemetry endpoints.
* DM-verity cryptographic partition integrity is 100% preserved.
* Official Over-The-Air (OTA) firmware updates install normally.
* Every change is instantly reversible via `cmd package install-existing <package>`.

### 2. Dual-List Consensus Safety Model
Rather than relying on arbitrary heuristics, every package listed in this project is audited against two independent community authorities:
* **Universal Android Debloater Next Generation (UAD-ng)**
* **MuntashirAkon Android Debloat List**

If either list indicates that an application has dependencies or requires caution, it is moved to an optional category or protected by a hardcoded fail-safe regex blacklist.

### 3. Encrypted Platform-Level Telemetry Mitigation
To stop tracking SDKs from embedded apps without rooting or running battery-intensive local VPN slots, the framework directs traffic through encrypted Private DNS over TLS (`dns.adguard-dns.com`), dropping advertisement and analytics queries before connection establishment.

---

## Maintainer and Community

* **Maintainer:** Project maintained by `@blackscythe123`.
* **Repository:** [https://github.com/blackscythe123/unfuck-android](https://github.com/blackscythe123/unfuck-android)
* **License:** [MIT License](LICENSE)
* **Contributions:** Community issue submissions, pull requests, and verified package list additions are welcome following the guidelines in [SECURITY.md](SECURITY.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
