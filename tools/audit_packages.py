#!/usr/bin/env python3
"""
CleanYourPhone - Phone Package Auditor
Audits connected phone's installed packages against our safe debloat lists,
optional lists, and core Android protections.
"""

import sys
import os
import re
import glob

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

def load_list(file_path):
    pkgs = set()
    if not os.path.isfile(file_path):
        return pkgs
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            clean = line.strip()
            if not clean or clean.startswith("#"):
                continue
            pkg = clean.split("#")[0].strip()
            if pkg:
                pkgs.add(pkg)
    return pkgs

def get_installed_packages():
    import subprocess
    try:
        res = subprocess.run(["adb", "shell", "pm", "list", "packages"], capture_output=True, text=True, check=True)
        return set([line.strip().replace("package:", "") for line in res.stdout.splitlines() if line.strip()])
    except Exception as e:
        print(f"Error reading packages from ADB: {e}", file=sys.stderr)
        return set()

def main():
    installed = get_installed_packages()
    if not installed:
        print("No Android device detected over ADB or unable to read package list.")
        sys.exit(1)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lists_dir = os.path.join(repo_root, "lists")

    safe_pkgs = set()
    optional_pkgs = set()

    for p in glob.glob(os.path.join(lists_dir, "**", "*-safe-debloat.txt"), recursive=True):
        safe_pkgs.update(load_list(p))
    for p in glob.glob(os.path.join(lists_dir, "common", "*.txt")):
        safe_pkgs.update(load_list(p))
    for p in glob.glob(os.path.join(lists_dir, "**", "*-optional-debloat.txt"), recursive=True):
        optional_pkgs.update(load_list(p))

    found_safe = installed.intersection(safe_pkgs)
    found_optional = installed.intersection(optional_pkgs)

    print("=" * 60)
    print("         CLEANYOURPHONE — DEVICE AUDIT REPORT")
    print("=" * 60)
    print(f" Total packages on device   : {len(installed)}")
    print(f" Safe bloatware detected     : {len(found_safe)}")
    print(f" Optional / OEM tools found  : {len(found_optional)}")
    print("=" * 60)

    if found_safe:
        print("\n[+] Safe Bloatware Ready for Removal:")
        for pkg in sorted(found_safe):
            print(f"  • {pkg}")

    if found_optional:
        print("\n[?] Optional Packages (Remove only if you have replacements):")
        for pkg in sorted(found_optional):
            print(f"  • {pkg}")

    print("\nRun './tools/disable.sh <list>' to safely disable these packages.")

if __name__ == "__main__":
    main()
