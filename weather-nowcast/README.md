# WijSAmen Weather Nowcast

Eerste werkende kern voor een gratis, lokale **0–3 uur neerslag-nowcast** op Android/Termux.

## Waarom deze bron

De kern gebruikt KNMI `seamless_precipitation_ensemble_forecast_probabilities/1.0`: een 1×1 km probabilistische neerslagverwachting met stappen van 5 minuten tot 6 uur vooruit. De eerste appversie toont maximaal 3 uur.

De voorspelling bevat kansen op overschrijding van neerslagdrempels. Dat is nuttiger dan één schijnbaar exact getal: bij buien wil je weten *hoe zeker* regen en zwaardere regen zijn.

## Termux: eerste installatie

```bash
pkg install git
cd ~
git clone https://github.com/ikbenra/WijSAmen-.git
cd WijSAmen-/weather-nowcast
bash termux_setup.sh
```

Als Termux:API en de `termux-location` opdracht beschikbaar zijn:

```bash
python nowcast.py --gps --hours 3
```

Zonder GPS-koppeling:

```bash
python nowcast.py --lat 52.1561 --lon 5.3878 --hours 3
```

Alleen om de actuele KNMI NetCDF-structuur te inspecteren:

```bash
python nowcast.py --lat 52.1561 --lon 5.3878 --diagnose
```

## Wat v0.1 al doet

- haalt automatisch het nieuwste KNMI seamless probability-bestand op;
- kiest het dichtstbijzijnde 1 km-rasterpunt;
- toont de komende 3 uur in stappen van 5 minuten;
- bewaart iedere voorspelling als JSONL in `logs/forecast_history.jsonl`;
- ondersteunt `termux-location` indien geïnstalleerd;
- gebruikt de door KNMI gepubliceerde anonieme Open Data API-key (geldig t/m 1 augustus 2027), met `KNMI_API_KEY` als override.

## Waarom logging vanaf dag 1

We willen niet alleen een app bouwen maar aantoonbaar leren wanneer de forecast goed of slecht is. De opgeslagen snapshots worden later tegen echte radarwaarnemingen gelegd. Daarna kunnen we per lead time, weertype en lokale situatie kalibreren.

## Volgende stappen

1. v0.1 op een echte telefoon en actuele KNMI-file valideren.
2. Werkelijke RTCOR-5m radarwaarden automatisch naast iedere voorspelling bewaren.
3. Brier score, reliability en timingfout berekenen.
4. Ensembleleden toevoegen voor mediaan en onzekerheidsband van intensiteit.
5. Bewolking/satelliet en zonkans toevoegen.
6. Kern achter een eenvoudige lokale JSON-interface zetten.
7. Android Studio UI bouwen op dezelfde kern.

## Bron / licentie

Weerdata: KNMI Data Platform, CC BY 4.0. Vermeld KNMI als databron bij afgeleide producten.
