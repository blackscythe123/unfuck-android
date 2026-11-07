#!/usr/bin/env python3
"""
CleanYourPhone - Package List & Pre-flight Validator
Verifies debloat lists for syntax errors, CRLF/BOM contamination,
and ensures zero core packages are in the list.
"""

import sys
import os
import re

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

PACKAGE_SYNTAX_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z0-9_]+)+$")

def check_list(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return False

    with open(file_path, "rb") as f:
        content = f.read()

    # Check for UTF-8 BOM
    if content.startswith(b"\xef\xbb\xbf"):
        print(f"Warning: {file_path} contains UTF-8 BOM. Normalizing...")
        content = content[3:]

    text = content.decode("utf-8", errors="replace")
    lines = text.splitlines()

    packages = []
    has_crlf = b"\r\n" in content
    if has_crlf:
        print(f"Notice: {file_path} contains Windows CRLF line endings (normalized during run).")

    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        # Extract package name (strip trailing inline comments)
        pkg = line.split("#")[0].strip()
        if not pkg:
            continue

        # Check valid package name syntax
        if not PACKAGE_SYNTAX_REGEX.match(pkg):
            print(f"Error [{file_path}:{idx}]: Invalid package name syntax: '{pkg}'", file=sys.stderr)
            return False

        # Guard against critical core packages
        if CORE_PACKAGE_REGEX.match(pkg):
            print(f"CRITICAL ERROR [{file_path}:{idx}]: Protected core package found: '{pkg}'", file=sys.stderr)
            print("Disabling this package can cause bootloops or broken emergency calling.", file=sys.stderr)
            return False

        packages.append(pkg)

    if not packages:
        print(f"Warning: {file_path} contains no active packages (all commented or empty).")
        return True

    duplicates = set([x for x in packages if packages.count(x) > 1])
    if duplicates:
        print(f"Warning: Duplicate packages found in {file_path}: {', '.join(duplicates)}")

    print(f"[OK] {file_path}: {len(packages)} valid safe packages passed checks.")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/check.py <path_to_list.txt> [more_lists...]")
        sys.exit(1)

    all_passed = True
    for list_path in sys.argv[1:]:
        passed = check_list(list_path)
        if not passed:
            all_passed = False

    if not all_passed:
        sys.exit(1)
    print("\nAll package lists verified successfully.")

if __name__ == "__main__":
    main()
