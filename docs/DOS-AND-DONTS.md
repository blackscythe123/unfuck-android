# Do's and Don'ts of Smartphone Debloating

Follow these golden rules to avoid bricking your phone, losing contacts, or breaking essential services.

---

## The DO's

- **DO keep a full backup before changing anything.**
  - CleanYourPhone scripts create an automatic backup in `backups/`, but verify that your contacts, photos, and messages are backed up to cloud or PC.
- **DO prefer disabling over uninstalling.**
  - `pm disable-user --user 0` freezes the application completely without altering the system partition. It is 100% reversible.
- **DO reboot and test your phone after debloating.**
  - Verify that calls, SMS, camera, biometrics (fingerprint/face), and Google Play Store work properly.
- **DO verify your phone's battery level.**
  - Ensure your phone is at least 30% charged before running ADB scripts.
- **DO turn off USB Debugging when you're finished.**
  - Leaving ADB open poses a security hazard on public Wi-Fi networks.

---

## The DON'Ts

- **DON'T ever delete core Android packages.**
  - Never touch `com.android.systemui`, `com.android.phone`, `packageinstaller`, or `permissioncontroller`.
- **DON'T debloat while driving or needing emergency services.**
  - Always debloat in a relaxed environment with access to a computer in case a restore is needed.
- **DON'T disable both your stock launcher and custom launcher at the same time.**
  - If you disable the stock OEM launcher (`com.oppo.launcher`, `com.vivo.launcher`), make sure you have installed a third-party launcher (like Lawnchair or Niagara) and tested it first!
- **DON'T remove stock camera apps if you care about photo quality.**
  - Oppo and vivo use proprietary ISP camera tuning pipelines inside their stock camera apps. Third-party cameras won't produce the same image quality.
- **DON'T panic if an app won't uninstall.**
  - Android 14/15 firmware prevents certain OEM packages from being uninstalled. CleanYourPhone automatically falls back to disabling them.
