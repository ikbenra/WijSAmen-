#!/data/data/com.termux/files/usr/bin/bash
set -eu
pkg install -y python termux-api
mkdir -p "$HOME/.saldosnoetje" "$HOME/bin"
cp "$(dirname "$0")/saldosnoetje.py" "$HOME/.saldosnoetje/saldosnoetje.py"
printf '#!/data/data/com.termux/files/usr/bin/bash\nexec python "$HOME/.saldosnoetje/saldosnoetje.py"\n' > "$HOME/bin/saldosnoetje"
chmod +x "$HOME/bin/saldosnoetje"
echo 'Start met ~/bin/saldosnoetje; installeer ook de Android-app Termux:API.'
