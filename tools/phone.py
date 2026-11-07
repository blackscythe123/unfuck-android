#!/usr/bin/env python3
"""
CleanYourPhone - Phone ADB Manager & Inspector
Supports USB ADB and Android 11+ Wireless Debugging.
Works across Oppo, OnePlus, Realme, vivo, and iQOO devices.
"""

import sys
import os
import subprocess
import re
import json
import argparse
from datetime import datetime

# Blacklist of critical core packages that must never be modified
CORE_PACKAGE_REGEX = re.compile(
    r"^(android|android\.ext\.(services|shared)|com\.android\.sdksandbox|"
    r"com\.android\.location\.fused|com\.android\.systemui|com\.android\.shell|"
    r"com\.android\.phone|com\.android\.dialer|com\.android\.server\.telecom|"
    r"com\.android\.settings|com\.android\.keyguard|"
    r"com\.(google\.)?android\.(permissioncontroller|packageinstaller|ext\.services|ext\.shared|modulemetadata)|"
    r"com\.google\.android\.overlay\.modules.*|"
    r"com\.android\.providers\.(telephony|media|downloads|settings)|"
    r"com\.qualcomm\.qti\.telephonyservice|com\.mediatek\.telephony)$",
    re.IGNORECASE
)

def run_adb(cmd_args, capture=True, check=False):
    """Run an adb command using subprocess."""
    full_cmd = ["adb"] + cmd_args
    try:
        if capture:
            res = subprocess.run(full_cmd, capture_output=True, text=True, check=check, encoding="utf-8", errors="replace")
            return res.stdout.strip()
        else:
            res = subprocess.run(full_cmd, check=check)
            return res.returncode
    except FileNotFoundError:
        print("Error: 'adb' command not found. Please install Android Platform Tools and add adb to your PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        if capture:
            return e.stdout.strip() if e.stdout else ""
        return e.returncode

def get_device_info():
    """Retrieve brand, model, Android version, battery, and RAM info."""
    devices = run_adb(["devices"]).splitlines()
    attached = [line.split()[0] for line in devices[1:] if line.strip() and not line.startswith("*") and "device" in line]
    if not attached:
        return None

    brand = run_adb(["shell", "getprop", "ro.product.brand"]).strip().capitalize()
    model = run_adb(["shell", "getprop", "ro.product.model"]).strip()
    manufacturer = run_adb(["shell", "getprop", "ro.product.manufacturer"]).strip().capitalize()
    android_ver = run_adb(["shell", "getprop", "ro.build.version.release"]).strip()
    sdk_ver = run_adb(["shell", "getprop", "ro.build.version.sdk"]).strip()
    security_patch = run_adb(["shell", "getprop", "ro.build.version.security_patch"]).strip()
    
    # Universal multi-OS detection (ColorOS 5+, Funtouch 3+, OxygenOS 5+, Realme UI 1+)
    os_flavor = run_adb(["shell", "getprop", "ro.build.version.opporom"]).strip()
    if os_flavor:
        os_flavor = f"ColorOS {os_flavor}"
    if not os_flavor:
        v_ver = run_adb(["shell", "getprop", "ro.vivo.os.version"]).strip()
        if v_ver:
            os_flavor = f"Funtouch/OriginOS {v_ver}"
    if not os_flavor:
        o_ver = run_adb(["shell", "getprop", "ro.oxygen.version"]).strip()
        if o_ver:
            os_flavor = f"OxygenOS {o_ver}"
    if not os_flavor:
        r_ver = run_adb(["shell", "getprop", "ro.build.version.realmeui"]).strip()
        if r_ver:
            os_flavor = f"Realme UI {r_ver}"
    if not os_flavor:
        os_flavor = run_adb(["shell", "getprop", "ro.rom.version"]).strip()

    # Battery
    battery_dump = run_adb(["shell", "dumpsys", "battery"])
    level_match = re.search(r"level:\s*(\d+)", battery_dump)
    battery_level = level_match.group(1) + "%" if level_match else "Unknown"

    return {
        "device_id": attached[0],
        "brand": brand,
        "manufacturer": manufacturer,
        "model": model,
        "android_version": android_ver,
        "sdk_version": sdk_ver,
        "security_patch": security_patch,
        "os_flavor": os_flavor if os_flavor else "Generic/AOSP",
        "battery_level": battery_level
    }

def print_device_banner(info):
    """Print a clean summary banner of the connected device."""
    print("=" * 60)
    print("           CLEAN YOUR PHONE — DEVICE STATUS")
    print("=" * 60)
    print(f" Device ID       : {info['device_id']}")
    print(f" Brand / Maker   : {info['brand']} ({info['manufacturer']})")
    print(f" Model           : {info['model']}")
    print(f" Android OS      : Version {info['android_version']}")
    print(f" Security Patch  : {info['security_patch']}")
    print(f" OS Flavor/Build : {info['os_flavor']}")
    print(f" Battery Level   : {info['battery_level']}")
    print("=" * 60)

def backup_device(backup_dir="backup"):
    """Create a complete backup of packages and properties before debloating."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = os.path.join(backup_dir, f"backup_{timestamp}")
    os.makedirs(target_dir, exist_ok=True)

    print(f"[*] Creating full pre-debloat backup in '{target_dir}'...")

    # Save installed packages
    pkgs = run_adb(["shell", "pm", "list", "packages", "-f"])
    with open(os.path.join(target_dir, "installed_packages.txt"), "w", encoding="utf-8") as f:
        f.write(pkgs)

    # Save disabled packages
    disabled = run_adb(["shell", "pm", "list", "packages", "-d"])
    with open(os.path.join(target_dir, "disabled_packages.txt"), "w", encoding="utf-8") as f:
        f.write(disabled)

    # Save getprop
    props = run_adb(["shell", "getprop"])
    with open(os.path.join(target_dir, "getprop.txt"), "w", encoding="utf-8") as f:
        f.write(props)

    # Generate instant restore script for this device
    restore_sh = os.path.join(target_dir, "restore_all.sh")
    with open(restore_sh, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/usr/bin/env bash\n# Restore script generated during backup\n")
        f.write('echo "Restoring packages..."\n')
        for line in pkgs.splitlines():
            if "=" in line:
                pkg_name = line.split("=")[-1].strip()
                f.write(f"adb shell cmd package install-existing {pkg_name} 2>/dev/null || adb shell pm install-existing {pkg_name} 2>/dev/null || adb shell pm enable {pkg_name} 2>/dev/null || adb shell pm unhide {pkg_name} 2>/dev/null || true\n")
        f.write('echo "Restore complete."\n')

    restore_ps1 = os.path.join(target_dir, "restore_all.ps1")
    with open(restore_ps1, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("# PowerShell Restore script generated during backup\n")
        f.write('Write-Host "Restoring packages..." -ForegroundColor Cyan\n')
        for line in pkgs.splitlines():
            if "=" in line:
                pkg_name = line.split("=")[-1].strip()
                f.write(f"adb shell cmd package install-existing {pkg_name} 2>`$null | Out-Null; adb shell pm install-existing {pkg_name} 2>`$null | Out-Null; adb shell pm enable {pkg_name} 2>`$null | Out-Null; adb shell pm unhide {pkg_name} 2>`$null | Out-Null\n")
        f.write('Write-Host "Restore complete." -ForegroundColor Green\n')

    print(f"[+] Backup completed successfully. {len(pkgs.splitlines())} packages recorded.")
    print(f"[+] Safety restore scripts created at:\n    - {restore_sh}\n    - {restore_ps1}")
    return target_dir

def main():
    parser = argparse.ArgumentParser(description="CleanYourPhone Phone Manager CLI")
    parser.add_argument("--info", action="store_true", help="Display connected device hardware and OS info")
    parser.add_argument("--backup", action="store_true", help="Backup installed packages and system properties")
    parser.add_argument("--list-installed", action="store_true", help="List all installed user and system packages")
    parser.add_argument("--list-disabled", action="store_true", help="List currently disabled packages")
    parser.add_argument("--reboot", action="store_true", help="Safely reboot the connected phone")
    args = parser.parse_args()

    info = get_device_info()
    if not info:
        print("No Android device detected over ADB.")
        print("Ensure USB Debugging or Wireless Debugging is enabled in Developer Options.")
        sys.exit(1)

    if args.info or len(sys.argv) == 1:
        print_device_banner(info)

    if args.backup:
        backup_device()

    if args.list_installed:
        pkgs = run_adb(["shell", "pm", "list", "packages"])
        print(pkgs)

    if args.list_disabled:
        disabled = run_adb(["shell", "pm", "list", "packages", "-d"])
        if disabled:
            print(disabled)
        else:
            print("No packages are currently disabled on this device.")

    if args.reboot:
        print("[*] Rebooting device...")
        run_adb(["reboot"])

if __name__ == "__main__":
    main()
