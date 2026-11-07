# Restoring Removed & Disabled Packages

CleanYourPhone guarantees complete reversibility. Because changes operate exclusively on **User 0**, the original APK files are never deleted from your phone's read-only system partitions.

---

## Method 1: Instant Single-Session Rollback

Whenever you run `tools/disable.sh` or `tools/disable.ps1`, a dedicated undo script is generated.

### On Linux / macOS:
```bash
./restore_last_session.sh
```

### On Windows PowerShell:
```powershell
.\restore_last_session.ps1
```

---

## Method 2: Restore an Entire Brand List

If you want to re-enable everything listed in a specific brand file:

### On Linux / macOS:
```bash
tools/restore.sh lists/oppo/coloros-safe-debloat.txt
```

### On Windows PowerShell:
```powershell
.\tools\restore.ps1 -Target "lists\oppo\coloros-safe-debloat.txt"
```

---

## Method 3: Restoring an Individual App by Hand

If you only want to bring back a single package (e.g. `com.heytap.themestore`):

1. **Re-enable the package:**
   ```bash
   adb shell pm enable com.heytap.themestore
   ```
2. **Reinstall for User 0 (if uninstalled):**
   ```bash
   adb shell cmd package install-existing com.heytap.themestore
   ```
3. The app icon will immediately reappear in your app drawer without needing a reboot!

---

## Method 4: Complete Factory Reset (Nuclear Option)

If you ever wish to return the phone to 100% factory state, performing a standard factory reset via:
`Settings > System > Reset options > Erase all data (factory reset)`
will recreate User 0 from the system image, restoring every factory package.
