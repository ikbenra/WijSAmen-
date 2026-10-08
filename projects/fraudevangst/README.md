# WijSAmen FraudeVangst

## Doel

Een lokale, snelle anti-fraudehulp voor verdachte telefoongesprekken. Het project probeert **de fraudehandeling minder effectief te maken**, niet bellers te identificeren, te volgen of te straffen.

De eerste toepassing is een Android/Termux-prototype op de Samsung A52s: één tik start lokale vastlegging van beschikbare audio en technische context; na stoppen wordt de opname lokaal getranscribeerd en op herkenbare fraude-indicatoren onderzocht.

## Huidige fase

**Prototype v0.1 — capturepad en Android-beperkingen valideren.**

De software is nog geen betrouwbare call-recorder en geen automatische fraudeclassificator. Op moderne Android-versies kan een gewone app niet zonder meer beide kanten van een cellulair gesprek opnemen. De v0.1 gebruikt daarom, waar Android het toestaat, luidspreker + microfoon en verzamelt daarnaast lokale context via Termux/Shizuku/Device Bridge.

## Architectuur

```text
Telefoongesprek
      |
      v
Android Quick Settings-tegel / app
      |
      +--> lokale MediaRecorder-capture
      |
      +--> Termux RUN_COMMAND-event
                |
                +--> rish/ADB snapshots
                +--> Device Bridge observatie
                +--> SHA-256
                +--> wijtranscribe --no-timestamps
                +--> lokale patroonanalyse
```

Prototypebron:

- [`prototypes/android-v0.1/`](prototypes/android-v0.1/)

## Privacy- en veiligheidsgrens

- niets wordt automatisch geüpload;
- caller-ID wordt niet als betrouwbare identiteit behandeld;
- transcript/patroonscore is geen bewijs van schuld;
- geen actieve tegenaanval, contactname, tracking of verstoring van de beller;
- ruwe opnamen, telefoonnummers en transcripties horen **niet** in deze repository;
- verzamelen is begrensd tot wat nodig is voor preventie en technische validatie.

## Bewijsplan v0.1

1. Bouwt de APK reproduceerbaar met Java 17 / Android SDK 35?
2. Start en stopt de Quick Settings-tegel betrouwbaar op de A52s?
3. Ontstaat bij een onschuldig testgesprek een bruikbare lokale audiofile?
4. Komen de Termux-events en snapshots in dezelfde case-map terecht?
5. Levert `wijtranscribe --no-timestamps` een transcript op?
6. Geeft de patroonanalyse alleen signalen weer en geen identiteitsclaim?

## Stop/go

**GO naar v0.2** als capture, case-correlatie en lokale verwerking stabiel werken.  
**STOP/REDESIGN** als Android de audio tijdens een gesprek structureel blokkeert; dan wordt de audiobron vervangen zonder bevoegdheden kunstmatig te verruimen.
