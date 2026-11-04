# WijSAmen SaldoSnoetje v0.1

Lokale Termux-proefversie voor **zelf gekopieerde** saldo-tekst. Android beperkt achtergrondklembordtoegang; dit is nog geen automatische schermlezer.

Installeer Termux en de compatibele Termux:API Android-app. Download de map, voer `bash install.sh` uit en start `~/bin/saldosnoetje`.

Kopieer `Saldo: € 12,34` en daarna `Saldo: € 13,34`. De eerste waarneming is stil; daarna trilt de telefoon of speelt een eigen `happy.mp3` / `sad.mp3` uit `~/.saldosnoetje/`.

Er worden geen screenshots, rekeningnummers of klembordteksten verstuurd. Alleen het laatst herkende bedrag wordt lokaal bewaard. Vergelijk voorlopig slechts één rekening. Stop met Ctrl+C.
