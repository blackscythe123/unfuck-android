#!/usr/bin/env bash
# ==============================================================================
# CleanYourPhone - Reversible Package Restoration Script (Bash)
# Restores / re-enables packages previously disabled or uninstalled for user 0.
#
# Usage:
#   tools/restore.sh lists/oppo/coloros-safe-debloat.txt
#   tools/restore.sh restore_last_session.sh
# ==============================================================================

set -euo pipefail

TARGET="${1:?Usage: restore.sh <package-list.txt or session-restore.sh>}"

if [ ! -f "$TARGET" ]; then
  echo "Error: Target file not found: $TARGET" >&2
  exit 1
fi

if [[ "$TARGET" =~ \.sh$ ]]; then
  echo "[*] Executing session restore script $TARGET..."
  bash "$TARGET"
  exit 0
fi

# Extract package names
PKGS=$(awk 'NR==1{sub(/^\xef\xbb\xbf/,"")} {sub(/\r$/,""); print}' "$TARGET" \
  | grep -vE '^\s*(#|$)' | sed -E 's/[[:space:]]+#.*$//' | awk '{print $1}')

TOTAL=$(printf '%s\n' "$PKGS" | wc -l | tr -d ' ')
CURRENT=0
RESTORED=0

echo "[*] Restoring $TOTAL packages from $TARGET..."

while IFS= read -r pkg; do
  [ -z "$pkg" ] && continue
  CURRENT=$((CURRENT + 1))

  # Universal restoration across Android 5.0 through Android 15
  adb shell pm enable "$pkg" >/dev/null 2>&1 || true
  adb shell pm unhide "$pkg" >/dev/null 2>&1 || true

  # Re-install for user 0 if uninstalled (try modern cmd, then legacy pm)
  OUT=$(adb shell cmd package install-existing "$pkg" 2>&1 || adb shell pm install-existing "$pkg" 2>&1 || true)
  if [[ "$OUT" =~ "installed for user" ]] || [[ "$OUT" =~ "Package" ]]; then
    echo "[$CURRENT/$TOTAL] Restored: $pkg"
    RESTORED=$((RESTORED + 1))
  else
    echo "[$CURRENT/$TOTAL] Re-enabled: $pkg"
    RESTORED=$((RESTORED + 1))
  fi

done <<< "$PKGS"

# Ensure stock OEM launchers are re-enabled if disabled
for stock in com.oppo.launcher com.coloros.home com.oneplus.launcher com.realme.launcher com.bbk.launcher2 com.vivo.launcher; do
  adb shell pm enable "$stock" >/dev/null 2>&1 || true
done

echo "=========================================================="
echo " Restoration complete. Total packages processed: $RESTORED"
echo "=========================================================="
