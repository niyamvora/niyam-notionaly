#!/usr/bin/env bash
# Install every folder containing a SKILL.md into the Codex skills directory.
# Skills may nest (notion/infographic/); each installs flat under its own name,
# and a nested skill is stripped from its parent's copy so nothing ships twice.
# Portable to the bash 3.2 that ships with macOS — no mapfile.
set -euo pipefail
cd "$(dirname "$0")"
DEST="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$DEST"

SKILLS=$(find . -name SKILL.md -not -path "./.git/*" | sed 's|/SKILL.md$||; s|^\./||' | sort)

for dir in $SKILLS; do
  name=$(sed -n 's/^name: *//p' "$dir/SKILL.md" | head -1 | tr -d '"')
  if [ -z "$name" ]; then echo "skip $dir: no name in SKILL.md" >&2; continue; fi
  rm -rf "${DEST:?}/$name"
  cp -R "$dir" "$DEST/$name"
  # strip any nested skill that came along with the parent
  for other in $SKILLS; do
    case "$other" in
      "$dir"/*) rm -rf "$DEST/$name/${other#"$dir"/}" ;;
    esac
  done
  find "$DEST/$name" -name ".DS_Store" -delete
  echo "installed $name  <-  $dir"
done
echo "Restart Codex to pick up changes."
