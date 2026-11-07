# Common Bloatware & Telemetry

Across all Android manufacturers, device shipments frequently include pre-installed
third-party applications, telemetry frameworks, and carrier software.

---

## 1. Facebook Ecosystem
- **Packages:** `com.facebook.katana`, `com.facebook.system`, `com.facebook.appmanager`, `com.facebook.services`
- **Why remove:** The `com.facebook.system` and `com.facebook.appmanager` packages are privileged background services capable of silently updating and installing Facebook partner apps without opening Google Play Store.

## 2. Commercial Streaming & Shopping
- **Packages:** `com.netflix.partner.activation`, `com.amazon.mShop.android.shopping`, `com.amazon.appmanager`
- **Why remove:** Partner activation stubs consume storage and query activation endpoints periodically.

## 3. Short Video & Content Aggregators
- **Packages:** `com.glance.internet`, `in.mohalla.sharechat`, `in.mohalla.video`, `com.eterno.shortvideos`
- **Why remove:** In-feed sponsored content designed to monopolize screen-time.

---

## Recommended Execution

```bash
./tools/disable.sh lists/common/facebook-bloat.txt
./tools/disable.sh lists/common/third-party-bloat.txt
./tools/disable.sh lists/common/carrier-bloat.txt
```
