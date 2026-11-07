# Debloating vivo (Funtouch OS / OriginOS)

## Architecture Overview
vivo devices feature Funtouch OS (Global markets) or OriginOS (China).
Bloatware resides in `com.vivo.*` and `com.bbk.*` namespaces.

---

## Key Categories Removed

1. **V-Appstore (`com.vivo.appstore`):**
   - Disables aggressive notifications prompting updates and trending game installations.
2. **Lockscreen Poster (`com.vivo.magazine`):**
   - Stops unwanted lock screen wallpapers and commercial news feeds.
3. **Jovi Assistant & HiBoard (`com.vivo.assistant`, `com.vivo.hiboard`):**
   - Disables the minus-one discovery feed and voice prompt background listener.
4. **vivo Browser (`com.vivo.browser`):**
   - Replaced with privacy-focused browsers like Firefox or Brave.
5. **vivo Daemon & Push Service (`com.vivo.daemonService`, `com.vivo.pushservice`):**
   - Eliminates diagnostic logging and background ad delivery channels.

---

## Recommended Execution

```bash
# Safe debloat for Funtouch OS
./tools/disable.sh lists/vivo/funtouchos-safe-debloat.txt

# Or for OriginOS
./tools/disable.sh lists/vivo/originos-safe-debloat.txt

# Remove preinstalled commercial bloat
./tools/disable.sh lists/common/facebook-bloat.txt
./tools/disable.sh lists/common/third-party-bloat.txt
```
