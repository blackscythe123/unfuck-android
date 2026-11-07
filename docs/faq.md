# Frequently Asked Questions (FAQ)

### 1. Does debloating void my phone's warranty?
**No.** Debloating via ADB does not unlock the bootloader, alter the `/boot` or `/recovery` partitions, or trip any hardware fuses (like Samsung Knox). It is completely recognized as standard Android user configuration.

### 2. Does this break banking and UPI apps (Google Pay, PhonePe, Paytm)?
**No.** Because the bootloader remains locked and the device is not rooted, Google Play Integrity and SafetyNet pass with flying colors. All banking apps continue working seamlessly.

### 3. Will I still receive Android OS and security updates?
**Yes.** Standard over-the-air (OTA) updates download and install normally. System partitions remain intact.
*Note:* A major Android OS upgrade (e.g. from Android 14 to Android 15) may re-install or re-enable some OEM bloatware. You can simply re-run CleanYourPhone after the update.

### 4. What is the difference between disabling and uninstalling?
- **Disabling (`pm disable-user --user 0`):** Freezes the application completely. It consumes 0 bytes of RAM, 0% CPU, and is hidden from app drawers and launchers.
- **Uninstalling (`pm uninstall -k --user 0`):** Removes the package from the active user environment. The APK remains stored in the read-only `/system` partition and can be brought back instantly with `cmd package install-existing`.
Both achieve identical privacy, speed, and battery benefits.

### 5. What if I make a mistake?
Run `./restore_last_session.sh` (or `.\restore_last_session.ps1` on Windows) to immediately reverse every modification made in that session.
