# Debloating OnePlus (OxygenOS)

## Architecture Overview
Since OxygenOS 12, OnePlus devices share their core codebase with ColorOS. While retaining OnePlus branding (`net.oneplus.*`), modern OxygenOS sets incorporate the OPLUS/HeyTap service architecture.

---

## Key Categories Removed

1. **OnePlus Membership & Forums (`net.oneplus.forums`, `net.oneplus.membership`):**
   - Red Cable Club push notifications and marketing banners.
2. **OnePlus Scout / Global Search (`com.oneplus.sound.quicksearchbox`):**
   - The universal search overlay that queries online services on home screen gestures.
3. **OEM LogKit (`com.oem.oemlogkit`, `com.oneplus.diagnostics`):**
   - Diagnostics daemon that tracks device status and uploads telemetry.
4. **HeyTap Services (`com.heytap.usercenter`, `com.heytap.market`):**
   - Cloud synchronization and store stubs present on unified firmware builds.

---

## Recommended Execution

```bash
# Recommended safe debloat
./tools/disable.sh lists/oneplus/oxygenos-safe-debloat.txt

# Remove preinstalled commercial bloat
./tools/disable.sh lists/common/facebook-bloat.txt
./tools/disable.sh lists/common/third-party-bloat.txt
```
