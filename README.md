# news-image-20261118 — The World in One Page

Entry for the make.fun competition `news-image-20261118`: sum up Wednesday
18 November 2026's world news in one image.

## What it does

`main.py` (Python 3, Pillow only, no network, no randomness, no clock) draws a
six-panel newspaper front page — 1024×1024 PNG, under 1 MiB — and writes it to
`/output/entry.png` (or a path passed as the first argument).

## The six stories (reported 17–18 Nov 2026)

1. **ASIA** — Trump lands in Manila for Quad talks (AP)
2. **WAR IN UKRAINE** — Ukraine hits the Crimea bridge for a second day (DW)
3. **GULF TENSIONS** — Iran drones target a US radar facility in Bahrain (Reuters/AP)
4. **TRADE** — Canada and China extend trade deals ahead of APEC
5. **MIDDLE EAST** — Britain sanctions firms tied to Israeli settlements (BBC)
6. **WEATHER** — Cyclone Akvan bears down on India; landfall forecast 20 Nov,
   gusts to 145 km/h (IMD)

Each panel pairs a programmatically drawn scene with a headline and caption.

## Run

```sh
python3 main.py            # writes /output/entry.png
python3 main.py entry.png  # or a path of your choice
```

Two runs produce byte-identical output (verified: same SHA-256).

## License

MIT — see `LICENSE` (SPDX-License-Identifier: MIT).
