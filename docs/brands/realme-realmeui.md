# Debloating Realme (Realme UI)

## Architecture Overview
Realme UI is closely derived from ColorOS, often shipping with additional promotional applications, recommendation modules, and commercial stubs targeted at budget and mid-range devices.

---

## Key Categories Removed

1. **Glance & Lock Screen Magazine (`com.glance.internet`, `com.heytap.pictorial`):**
   - Eliminates lock screen news carousels and commercial ads.
2. **Realme Community (`com.realme.community`):**
   - Promotional forum app with background push notifications.
3. **App Market & Theme Store (`com.heytap.market`, `com.heytap.themestore`):**
   - Removes store recommendations and ad popups.
4. **FinShell Pay (`com.finshell.wallet`):**
   - Pre-installed loan and wallet promotions.

---

## Recommended Execution

```bash
# Safe debloat
./tools/disable.sh lists/realme/realmeui-safe-debloat.txt

# Remove preinstalled commercial bloat
./tools/disable.sh lists/common/facebook-bloat.txt
./tools/disable.sh lists/common/third-party-bloat.txt
```
