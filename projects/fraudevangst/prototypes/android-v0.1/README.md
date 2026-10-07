# WijSAmen FraudeVangst v0.1

Een snelle lokale capture-app voor verdachte telefoongesprekken. Doel: preventie en analyse, niet identificatie of bestraffing.

## Wat één tik doet

- start een foreground-capture;
- probeert de luidsprekerroute te kiezen;
- probeert microfoonaudio lokaal als `.m4a` op te slaan in `Music/WijSAmenFraude`;
- geeft start/stop-events aan Termux via `com.termux.RUN_COMMAND`;
- Termux maakt lokaal een case-map met telecom/connectiviteits-snapshots via `rish`/ADB, Bridge-status en een `wsb observe` indien aanwezig;
- na STOP: SHA-256, `wijtranscribe --no-timestamps`, en een simpele semantische fraude-indicatoranalyse;
- niets wordt automatisch geüpload.

## Belangrijke Android-beperking

Een gewone third-party app op recente Android-versies kan **niet betrouwbaar beide kanten van een cellulair telefoongesprek opnemen**. Shizuku/shell geeft niet automatisch de signature/privileged permissie `CAPTURE_AUDIO_OUTPUT`. Deze v0.1 probeert daarom de speaker + microfoonroute. Op sommige toestellen kan Android tijdens een gewone telefoonoproep de microfoon voor deze app stil houden. Metadata/Bridge/Termux-capture blijft dan wel bruikbaar. Een latere versie kan een tweede toestel of ondersteunde native call-recorder als audio-bron gebruiken.

## Eenmalig op de telefoon

1. Clone of update de WijSAmen-repository en checkout deze projectbranch.
2. Ga in Termux naar `projects/fraudevangst/prototypes/android-v0.1`.
3. Installeer de Termux-kant:
   ```bash
   bash termux/install_termux_side.sh
   ```
4. Bouw de APK met GitHub Actions (`Build FraudeVangst APK`) of met een aanwezige Gradle + Android SDK.
5. Installeer de debug-APK en geef microfoon/notificatie-toestemming.
6. Voeg eventueel de Quick Settings-tegel **FraudeVangst** toe.

## Gebruik

Bij een verdachte call: tik **FraudeVangst**. De app start direct zodra permissions al gegeven zijn. Stop met **STOP + VERWERK** of via de notificatie/Quick Settings-tegel.

Case-output verschijnt onder:

```text
~/storage/downloads/WijSAmenFraude/YYYYMMDD_HHMMSS/
```

Verwachte bestanden zijn o.a. `telecom.txt`, `connectivity.txt`, `bridge-scene.json`, `wsb-observe.txt`, audio, `audio.sha256`, `transcript.txt` en `analysis.json`.
