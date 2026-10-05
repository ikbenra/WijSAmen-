#!/usr/bin/env bash
set -Eeuo pipefail

VERSION="${VERSION:-0.1.1}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
DIST="$ROOT/dist"
STAGE="$ROOT/.build/wijsamen-output-share"

rm -rf "$STAGE"
mkdir -p   "$STAGE/DEBIAN"   "$STAGE/data/data/com.termux/files/usr/bin"   "$STAGE/data/data/com.termux/files/usr/share/doc/wijsamen-output-share"   "$DIST"

cat > "$STAGE/DEBIAN/control" <<EOF
Package: wijsamen-output-share
Version: $VERSION
Architecture: all
Maintainer: WijSAmen
Depends: bash, coreutils, python, termux-tools, util-linux
Recommends: termux-api
Description: WijSAmen helper to capture and share the latest complete Termux output
 Creates readable and raw copies of the newest logged Termux session and opens
 Android sharing in one command. Designed to work with the existing
 ~/ai/termux-output/current.log convention and wsb-session logs.
EOF

cat > "$STAGE/DEBIAN/postinst" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -e
echo
echo "WijSAmen Output Share geïnstalleerd."
echo "Start logging:     wso session"
echo "Deel met ChatGPT:  wso chatgpt"
echo "Status:            wso status"
echo
exit 0
EOF
chmod 755 "$STAGE/DEBIAN/postinst"

install -m 755 "$ROOT/wso" "$STAGE/data/data/com.termux/files/usr/bin/wso"

for name in share chatgpt status session export; do
  cat > "$STAGE/data/data/com.termux/files/usr/bin/wso-$name" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec /data/data/com.termux/files/usr/bin/wso $name "\$@"
EOF
  chmod 755 "$STAGE/data/data/com.termux/files/usr/bin/wso-$name"
done

cat > "$STAGE/data/data/com.termux/files/usr/share/doc/wijsamen-output-share/README.txt" <<'EOF'
WijSAmen Output Share

Belangrijkste commando's:
  wso session
  wso chatgpt
  wso share
  wso export
  wso status

De Android-route gebruikt een zichtbare share-intent. Het pakket probeert niet
blind een specifiek bestaand ChatGPT-gesprek te adresseren.
EOF

OUT="$DIST/wijsamen-output-share_${VERSION}_all.deb"
dpkg-deb --build --root-owner-group "$STAGE" "$OUT"
echo "$OUT"
