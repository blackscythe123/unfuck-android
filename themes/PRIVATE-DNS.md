# Private DNS: System-Wide Ad & Tracker Blocking (Zero Apps)

Android 9+ includes native support for **DNS-over-TLS (Private DNS)**.
By setting a Private DNS hostname, you block ads, malicious domains, and OEM telemetry across
all apps and web browsers — with **zero background apps, zero battery consumption, and zero VPN profile overhead**.

---

## How to Set It Up

1. Open **Settings** on your phone.
2. Go to **Network & Internet (or Connection & Sharing)**.
3. Tap on **Private DNS**.
4. Select **Designated Private DNS (or Private DNS provider hostname)**.
5. Enter one of the trusted privacy hostnames below and tap **Save**.

---

## Recommended DNS Hostnames

### 1. NextDNS (Recommended — Custom Control)
- **Hostname:** `<your-id>.dns.nextdns.io`
- **Why:** Lets you create a free custom profile with custom blocklists (OISD, AdGuard Mobile, OEM telemetry blockers).
- **Website:** [nextdns.io](https://nextdns.io)

### 2. AdGuard DNS (Default Ad Blocking)
- **Hostname:** `dns.adguard-dns.com`
- **Why:** Standard, battle-tested system-wide ad and tracker blocker. No signup required.

### 3. Mullvad DNS (Strict Privacy)
- **Hostname:** `adblock.doh.mullvad.net`
- **Why:** Operated by privacy-first Mullvad VPN with zero query logging and built-in ad/tracker blocking.

### 4. Control D
- **Hostname:** `p2.freedns.controld.com`
- **Why:** High performance, blocks ads and tracking domains with low latency.
