#!/usr/bin/env bash
# Read-only source backup: never force-push, delete refs or alter source.
set -Eeuo pipefail
if [[ $# -ne 2 ]]; then echo "Usage: bash backup.sh REPO_URL OUTPUT_DIR" >&2; exit 2; fi
repo="$1"; out="$2"
mkdir -p "$out"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
git clone --mirror "$repo" "$tmp/source.git"
git -C "$tmp/source.git" fsck --full --no-reflogs
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
bundle="$out/wijsamen-$stamp.bundle"
git -C "$tmp/source.git" bundle create "$bundle" --all
git bundle verify "$bundle" >/dev/null
# Independently prove bundle is restorable; do not merely trust bundle verify.
git clone --mirror "$bundle" "$tmp/restore.git"
git -C "$tmp/restore.git" fsck --full --no-reflogs
git -C "$tmp/source.git" show-ref | LC_ALL=C sort > "$tmp/original.refs"
git -C "$tmp/restore.git" show-ref | LC_ALL=C sort > "$tmp/restored.refs"
diff -u "$tmp/original.refs" "$tmp/restored.refs"
sha256sum "$bundle" > "$bundle.sha256"
printf 'RESTORE_VERIFIED bundle=%s\n' "$bundle"
# Important: GitHub pull-request refs, LFS, releases, issues, wiki, secrets and external state are NOT covered.
