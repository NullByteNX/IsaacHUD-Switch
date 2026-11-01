
# Attribution, third-party code and rights

## Software licenses

The original project archive includes an **MIT License** notice (preserved at `LICENSES/MIT-original.txt`). The application is built using **GPL version 2** code, including:

- [libtesla](https://github.com/WerWolv/libtesla) — WerWolv and contributors, GPL-2.0.
- [Tesla-Template](https://github.com/WerWolv/Tesla-Template) — WerWolv and contributors, GPL-2.0.
- [Atmosphère `dmntcht` client](https://github.com/Atmosphere-NX/Atmosphere/tree/master/libraries/libstratosphere/source/dmnt) — Atmosphère-NX contributors, GPL-2.0.

The GPL-2.0 text appears in root `LICENSE`; upstream sources and their license texts are vendored under `third_party/` at exact pinned revisions. The build scripts also preserve and reproduce the necessary adaptation steps. When distributing a linked `.ovl`, comply with the GPL-2.0 requirements for the complete corresponding buildable source, including the relevant modifications and build instructions, alongside the original MIT notice where applicable. Dependency sources, revisions and license notices are documented in `third_party/`.

## Catalog texts

Italian catalog descriptions include summaries, translations and reworkings based on information from wiki contributors. Attribution, source revisions, contributor histories and CC BY-SA 4.0 licensing details for wiki-derived texts are documented in `catalog/ATTRIBUZIONE.md`. The CC BY-SA 4.0 attribution concerns the applicable catalog texts, not third-party game graphics, music or software. License text: `LICENSES/CC-BY-SA-4.0.txt`.

## Game and community attribution

- *The Binding of Isaac: Repentance* — rights held by its respective creators and publishers.
- Nintendo, Nintendo Switch — Nintendo's respective trademarks and rights.
- [External Item Descriptions (EID)](https://github.com/wofsauge/External-Item-Descriptions) — a community project that inspired the presentation idea; this is **not a port** of EID's Lua and its assets are not bundled.
- [devkitPro](https://devkitpro.org/) — development toolchain used for compilation.
- [libnx](https://github.com/switchbrew/libnx) — Nintendo Switch library linked using `-lnx`. Copyright 2017-2018 libnx Authors. ISC License. Full license notice: `LICENSES/ISC-libnx.txt`.

This is an unofficial fan project, not affiliated with or endorsed by Nintendo, the game's authors/publisher, wiki.gg or EID contributors. No game dumps, decryption keys, firmware images or extracted game assets are provided.

## External runtime catalogs (0.6.0)

The program reads names/descriptions from `runtime/catalog_it.tsv` and collectible
qualities from `runtime/collectible_quality.tsv`, installed under
`sd:/switch/IsaacHUD/`. These data are not compiled into the OVL. The existing
catalog text attribution above is retained, and the descriptions are unchanged.

Quality data are a minimal ID/quality extraction from a pinned wiki-derived
snapshot. Where dataset rights apply, they are distributed under CC BY-SA 4.0;
source, selection of Repentance values, contributors and provenance are recorded
in `catalog/ATTRIBUZIONE_TIER.md` and `catalog/quality_source.json`. Rights in
third-party game content remain with their respective holders. Attribution is
carried into the SD package as `CREDITI.txt`, with
the unmodified CC license in `licenses/CC-BY-SA-4.0.txt`.

## Compiler runtime and binary package notices

The binary package carries the software notices and license texts alongside
its runtime catalogs, including the original GPL-2.0, MIT and ISC notices.
`docs/SOFTWARE_NOTICES.txt` identifies components and the matching release
source. newlib's collected notices and GCC's GPLv3 runtime terms with the
GCC Runtime Library Exception 3.1 are included under `LICENSES/`; they apply to
the respective runtime components and do not replace the application's GPL-2.0
license. `stb_truetype` uses its supplied MIT alternative. Notice sources and
hashes are recorded in `LICENSES/RUNTIME_SOURCES.json`. These files are copied
into `switch/IsaacHUD/licenses/` when preparing an SD package.

The numbered shield is original procedural artwork implemented in this project.
Original software license notices and third-party revisions are retained.
Software and runtime data carry their respective notices and attributions.
