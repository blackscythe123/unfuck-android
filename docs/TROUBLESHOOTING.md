# Troubleshooting & FAQ

Encountering an issue while connecting or debloating? Here are tested solutions.

---

## 1. ADB Connection Issues

### `adb devices` shows nothing
- **Fix:**
  1. Ensure **USB Debugging** is toggled ON under `Settings > Developer Options`.
  2. If using a cable, try another USB cable or a different USB port on your PC (prefer USB 2.0 or direct motherboard ports).
  3. Ensure USB Mode is set to **File Transfer / MTP** rather than "Charge only".
  4. On Oppo/Realme, enable **Disable Permission Monitoring** if available under Developer Options.

### `device unauthorized`
- **Fix:**
  - Unlock your phone screen.
  - A pop-up dialog will ask: *"Allow USB debugging from this computer?"*.
  - Check **Always allow from this computer** and tap **Allow**.

### Wireless Debugging disconnects
- Android rotates the pairing port each time Wireless Debugging is toggled. Check `Settings > Developer Options > Wireless Debugging` to see the current port number.

---

## 2. Package Management Errors

### `Failure [DELETE_FAILED_INTERNAL_ERROR]`
- **Cause:**
  - Modern ColorOS and Realme UI prevent `pm uninstall` on certain packages without root.
- **Solution:**
  - Use `pm disable-user --user 0 <pkg>`. This achieves the exact same result: 0 RAM, 0 CPU usage, no background services, and the app icon is removed.
  - `disable.sh` and `disable.ps1` handle this fallback automatically.

### `SecurityException: Permission Denial`
- **Cause:**
  - On vivo (Funtouch OS / OriginOS 14), BBK security policies block modifying certain protected system packages via standard ADB.
- **Solution:**
  - Under Developer Options, look for **USB Debugging (Security settings)** or **Verify apps over USB** and toggle it appropriately.
  - If a package is hard-locked by vivo, skip it.

---

## 3. Post-Debloat Fixes

### "I accidentally disabled an app I need. How do I get it back?"
- **Solution:**
  - If you know the package name:
    ```bash
    adb shell pm enable <package.name>
    adb shell cmd package install-existing <package.name>
    ```
  - Or run the automatic rollback script generated during your session:
    ```bash
    # Linux / macOS
    ./restore_last_session.sh

    # Windows PowerShell
    .\restore_last_session.ps1
    ```

### "Can I still receive OTA system updates?"
- **Yes.**
  - Because debloating via ADB only uninstalls or disables apps for **User 0**, the `/system` partition is untouched and dm-verity cryptographic checksums remain valid. Official over-the-air updates will install normally.
