#!/usr/bin/env sh
# check-update.sh — compare the installed VERSION against upstream main.
#
# Prints one of:
#   up-to-date                      local VERSION matches upstream
#   update-notified                 newer version exists but was already
#                                   surfaced to the user in the last 24h
#   UPDATE AVAILABLE: installed=X latest=Y
#
# Exit is always 0 — never let the update check break a task. Network
# failure prints "no-info" and exits silently.
set -eu

DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
LOCAL=$(cat "$DIR/VERSION" 2>/dev/null || echo unknown)
STATE="$HOME/.cache/atelier/update-check"

UPDATE=$(curl -sf -m 4 https://raw.githubusercontent.com/adamramadhn/atelier/main/skills/atelier/VERSION 2>/dev/null || true)
[ -n "$UPDATE" ] || { echo no-info; exit 0; }

if [ "$UPDATE" = "$LOCAL" ]; then
  echo up-to-date
  exit 0
fi

# state file: "<notified-version>|<epoch>"
SAW=""
NOTIFIED_AT=0
if [ -f "$STATE" ]; then
  SAW=$(cut -d'|' -f1 "$STATE")
  NOTIFIED_AT=$(cut -d'|' -f2 "$STATE")
fi
NOW=$(date +%s)
if [ "$SAW" = "$UPDATE" ] && [ "$((NOW - NOTIFIED_AT))" -lt 86400 ]; then
  echo update-notified
  exit 0
fi

mkdir -p "$(dirname "$STATE")"
echo "$UPDATE|$NOW" > "$STATE"
echo "UPDATE AVAILABLE: installed=$LOCAL latest=$UPDATE"
