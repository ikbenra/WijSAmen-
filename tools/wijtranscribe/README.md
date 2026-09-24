# WijTranscribe

Offline batch-transcriptie in Termux, gebouwd rond `whisper.cpp` en FFmpeg.

## Doel

Na een apparaatwissel hoeft alleen Termux te worden geïnstalleerd en de installer opnieuw te worden uitgevoerd. De installer regelt dependencies, bouwt `whisper.cpp`, haalt een meertalig model op en installeert het commando `wijtranscribe`.

## Installatie

Vanuit deze map:

```bash
chmod +x install.sh
./install.sh
```

Wanneer deze map in een publieke GitHub-repository staat kan installatie met één regel:

```bash
pkg install -y curl && curl -fsSL RAW_INSTALL_URL | bash
```

> De huidige WijSAmen-repository is privé. Een anonieme raw-GitHub one-liner werkt daarom pas wanneer dit pakket in een publieke repo staat of de repository publiek wordt gemaakt.

## Gebruik

```bash
wijtranscribe ~/storage/downloads/funghi
```

Resultaat:

- per bronbestand een `.txt`
- per bronbestand een `.srt`
- `ALL_TRANSCRIPTS.txt` met alles achter elkaar

Andere voorbeelden:

```bash
wijtranscribe opname.mp3 --lang nl
wijtranscribe ~/storage/downloads/audio --output ~/storage/downloads/project-tekst
wijtranscribe doctor
wijtranscribe model small
wijtranscribe update
```

## Modellen

Standaard wordt het meertalige `base`-model gebruikt. Een ander model kan later worden geïnstalleerd met bijvoorbeeld:

```bash
wijtranscribe model small
```

Grotere modellen vragen meer opslag, RAM en rekentijd.

## Ontwerp

- volledig lokale transcriptie na installatie/modeldownload
- bronaudio blijft lokaal
- tijdelijke WAV-bestanden worden automatisch verwijderd
- bestand- of mapinvoer
- automatische taalherkenning standaard
- herstelcontrole via `wijtranscribe doctor`
- reproduceerbaar op een nieuwe Termux-installatie
