# Debloating Oppo (ColorOS)

## Architecture Overview
ColorOS serves as the foundation for the broader OPLUS ecosystem (powering Oppo, Realme, and modern OnePlus).
Bloatware packages primarily occupy the `com.heytap.*`, `com.coloros.*`, `com.oppo.*`, and `com.oplus.*` namespaces.

### Legacy ColorOS (ColorOS 5, 6 & 7) vs Modern ColorOS (11–15)
* **ColorOS 5 (Android 7.1 / 8.1) & ColorOS 6 (Android 9):** Shipped before the unified HeyTap rebrand. Packages used `com.oppo.*`, `com.coloros.*`, and `com.nearme.*` (e.g. `com.oppo.market`, `com.coloros.cloud`, `com.coloros.securepay`, `com.oppo.community`, `com.coloros.smartdrive`).
* **ColorOS 7 & 11–15 (Android 10–15):** Modern HeyTap & Oplus unified ecosystem (`com.heytap.market`, `com.oplus.games`, `com.heytap.mcs`).
* **Universal Script Handling:** CleanYourPhone automatically detects your OS build (`ro.build.version.opporom`), using legacy-compatible fallback chains (`pm disable-user` → `pm disable` → `pm hide`).

---

## Key Categories Removed

1. **HeyTap App Market (`com.heytap.market`):**
   - Replaced by Google Play Store or F-Droid.
   - Eliminates spammy push notifications promoting sponsored utility tools.
2. **Lock Screen Pictorial (`com.heytap.pictorial`):**
   - Eliminates dynamic lockscreen wallpaper clickbait and commercial ads.
3. **Global Search (`com.heytap.quicksearchbox`):**
   - Disables the intrusive swipe-down search bar on the home screen.
4. **FinShell Pay & Wallet (`com.finshell.wallet`):**
   - Pre-installed loan, insurance, and financial marketing services.
5. **LogKit & DeepThinker (`com.oplus.logkit`, `com.oplus.deepthinker`):**
   - Telemetry collection daemons that track app usage sequences and upload crash metrics.

---

## Recommended Execution

```bash
# Recommended safe debloat
./tools/disable.sh lists/oppo/coloros-safe-debloat.txt

# Remove preinstalled commercial bloat
./tools/disable.sh lists/common/facebook-bloat.txt
./tools/disable.sh lists/common/third-party-bloat.txt
```
