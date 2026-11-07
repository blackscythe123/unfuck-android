# Wireless ADB Pairing Guide (No Cable Required)

Android 11 and newer (ColorOS 11+, OxygenOS 11+, Realme UI 2+, Funtouch OS 11+, OriginOS)
supports native **Wireless Debugging** over Wi-Fi without needing a USB cable.

---

## Prerequisites
- Your computer and phone must be connected to the **same Wi-Fi network**.
- Android version **11 or newer**.

---

## Step-by-Step Instructions

### Step 1: Enable Developer Options
1. On your phone, go to **Settings > About Device (or About Phone)**.
2. Tap on **Version** or **Build Number** 7 times until you see the message:
   `"You are now in Developer mode!"`

### Step 2: Enable Wireless Debugging
1. Go to **Settings > System Settings (or Additional Settings) > Developer Options**.
2. Scroll down and toggle **Wireless debugging** to **ON**.
3. Tap **Allow** when prompted to allow wireless debugging on your Wi-Fi network.

### Step 3: Pair with Your Computer
1. Tap directly on the words **"Wireless debugging"** (not just the toggle).
2. Tap **"Pair device with pairing code"**.
3. You will see a dialog displaying:
   - **Wi-Fi pairing code** (a 6-digit number, e.g. `123456`)
   - **IP address & Port** (e.g. `192.168.1.45:37123`)

4. On your computer terminal, run:
   ```bash
   adb pair 192.168.1.45:37123
   ```
5. Enter the 6-digit pairing code when prompted.
   You will see: `Successfully paired to 192.168.1.45:37123 [guid=...]`

### Step 4: Connect to the Phone
1. Look back at the main Wireless debugging screen on your phone.
2. Note the **IP address & Port** shown under **"IP address & Port"** (note: this port is different from the pairing port, e.g. `192.168.1.45:41899`).
3. Connect from your computer terminal:
   ```bash
   adb connect 192.168.1.45:41899
   ```
4. Confirm connection:
   ```bash
   adb devices
   ```
   You will see:
   ```text
   List of devices attached
   192.168.1.45:41899    device
   ```

You are now ready to run CleanYourPhone wirelessly!
