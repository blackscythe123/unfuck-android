# Debloating iQOO (Funtouch OS / OriginOS)

## Architecture Overview
iQOO is vivo's gaming-centric sub-brand. Devices run specialized builds of Funtouch OS or OriginOS, incorporating gaming overlay services (`com.vivo.gamecube`), iQOO logging daemons (`com.bbk.iqoo.logsystem`), and diagnostic tools alongside standard vivo services.

---

## Key Categories Removed

1. **V-Appstore & Theme Store (`com.vivo.appstore`, `com.bbk.theme`):**
   - Eliminates store ads and push notifications.
2. **Lockscreen Poster (`com.vivo.magazine`):**
   - Disables sponsored lock screen cards.
3. **iQOO Log System & Daemons (`com.bbk.iqoo.logsystem`, `com.vivo.daemonService`):**
   - Silences persistent background loggers.
4. **Jovi Assistant (`com.vivo.assistant`):**
   - Disables redundant voice and smart scene assistants.

---

## Recommended Execution

```bash
# Safe debloat for iQOO
./tools/disable.sh lists/iqoo/iqoo-safe-debloat.txt

# Remove preinstalled commercial bloat
./tools/disable.sh lists/common/facebook-bloat.txt
./tools/disable.sh lists/common/third-party-bloat.txt
```
