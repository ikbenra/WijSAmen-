# WijSAmen Weather Nowcast

Eerste werkende kern voor een gratis, lokale **0–3 uur neerslag-nowcast** op Android/Termux.

De [Evidence Passport](EVIDENCE_PASSPORT.md) scheidt aanwezige code, bronfeiten, nog onbewezen uitvoering, privacygrenzen en de goedkoopste falsifieerbare validatiecyclus.

## Eerste mijlpaal

De eerste mijlpaal is bewust kleiner dan een volledige weerapp:

> Een telefoon kan zonder handmatige databewerking een actuele KNMI-file ophalen, een 0–180 minutenforecast voor één locatie produceren en het resultaat lokaal als JSONL loggen.

**Android Studio komt pas daarna.** Eerst moet de forecastkern op een echte telefoon bewezen werken.

## Snelste validatie op de telefoon

Na installatie:

```bash
cd ~/WijSAmen-/weather-nowcast
bash validate_live.sh
```

`validate_live.sh` doet twee dingen:

1. draait de synthetische coretests;
2. draait `python nowcast.py --validate-live`, dat GPS gebruikt, de actuele NetCDF-structuur toont, +0 t/m +180 minuten controleert en alleen `LIVE VALIDATION: PASS` toont wanneer ook een JSONL-snapshot is geschreven.

Voor de live-validatie is naast het Termux-pakket `termux-api` ook de **Android-app Termux:API** nodig, met locatiepermissie.

## Termux: eerste installatie

```bash
pkg install git
cd ~
git clone https://github.com/ikbenra/WijSAmen-.git
cd WijSAmen-/weather-nowcast
bash termux_setup.sh
```

Daarna is de voorkeursroute:

```bash
bash validate_live.sh
```

Losse opdrachten blijven beschikbaar.

Met Termux GPS:

```bash
python nowcast.py --gps --hours 3
```

Met een expliciete locatie:

```bash
python nowcast.py --lat 52.1561 --lon 5.3878 --hours 3
```

Actuele KNMI NetCDF-structuur inspecteren:

```bash
python nowcast.py --lat 52.1561 --lon 5.3878 --diagnose
```

## Wat v0.2 doet

- haalt automatisch het nieuwste KNMI seamless probability-bestand op;
- gebruikt KNMI's `created desc` sortering om de nieuwste file te kiezen;
- registreert bestandsnaam, KNMI-created/last-modified metadata, bronouderdom en eventuele `X-KNMI-Deprecation` melding;
- kiest het dichtstbijzijnde rasterpunt;
- leidt de horizon af uit de **werkelijke tijdas** in het NetCDF-bestand in plaats van een vast aantal regels aan te nemen;
- vereist bij de milestonevalidatie dekking t/m **+180 minuten**;
- toont neerslagkansen per drempel;
- bewaart iedere voorspelling als JSONL in `logs/forecast_history.jsonl`;
- ondersteunt `termux-location` via Termux:API;
- faalt expliciet wanneer `--gps` gevraagd is maar geen GPS-locatie beschikbaar is, in plaats van stil op de defaultlocatie verder te gaan;
- gebruikt de door KNMI gepubliceerde anonieme Open Data API-key (geldig t/m 1 augustus 2027), met `KNMI_API_KEY` als override.

## Waarom logging vanaf dag 1

We willen niet alleen een app bouwen maar aantoonbaar leren wanneer de forecast goed of slecht is. Iedere snapshot bewaart daarom bronmetadata, locatiebron, rasterpunt, lead time en de voorspelde kansen. Exacte GPS-logs blijven lokaal en `logs/` staat in `.gitignore`.

De volgende meetstap is om iedere uitgegeven forecast te koppelen aan onafhankelijke RTCOR-5m-radarwaarnemingen. Daarna kunnen we per lead time en drempel Brier score, reliability en regen-start/stopfout berekenen.

## Volgende stappen

1. `bash validate_live.sh` op een echte Android/Termux-installatie laten eindigen met `LIVE VALIDATION: PASS`.
2. Werkelijke `nl_rdr_data_rtcor_5m`-waarnemingen automatisch naast iedere voorspelling bewaren.
3. Brier score, reliability en timingfout berekenen.
4. Ensembleleden toevoegen voor mediaan en onzekerheidsband van intensiteit.
5. Bewolking/satelliet en zonkans toevoegen.
6. Kern achter een eenvoudige lokale JSON-interface zetten.
7. Android Studio UI bouwen op dezelfde bewezen kern.

## Bron / licentie

Weerdata: KNMI Data Platform, CC BY 4.0. Vermeld KNMI als databron bij afgeleide producten.
