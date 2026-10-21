#!/usr/bin/env sh
# install.sh — install or update the `atelier` skill into a skills directory.
#
#   sh install.sh                      # default target: ~/.claude/skills
#   sh install.sh ~/.agents/skills     # custom target dir
#
# Safe to re-run: pulls latest main and rsyncs skills/atelier in place.
set -eu

REPO="https://github.com/adamramadhn/atelier.git"
SKILL="skills/atelier"
CACHE="${ATELIER_CACHE:-$HOME/.cache/atelier}"
TARGET="${1:-$HOME/.claude/skills}"
DEST="$TARGET/atelier"

# 1. Fetch/refresh the repo copy
if [ -d "$CACHE/.git" ]; then
  git -C "$CACHE" fetch -q origin main
  git -C "$CACHE" reset -q --hard origin/main
else
  git clone --depth 1 -q "$REPO" "$CACHE"
fi

# 2. Sync skill folder in place (keeps installed path stable)
mkdir -p "$TARGET"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$CACHE/$SKILL/" "$DEST/"
else
  rm -rf "$DEST"
  cp -R "$CACHE/$SKILL" "$DEST"
fi

echo "installed/updated: $DEST"
head -5 "$DEST/SKILL.md" 2>/dev/null | grep -i version || true
