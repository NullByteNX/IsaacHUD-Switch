# Catalogo italiano — crediti, fonti e modifiche

Le brevi descrizioni italiane in `it_*.tsv` sintetizzano **effetti, condizioni e valori numerici di gameplay**. Molte formulazioni sono state tradotte, rielaborate o corrette a partire da informazioni consultate sulla [The Binding of Isaac: Rebirth Wiki](https://bindingofisaacrebirth.wiki.gg/).

I testi del catalogo derivati da contenuti della wiki sono attribuiti ai relativi contributori e distribuiti secondo la licenza **CC BY-SA 4.0**. Le modifiche sono descritte nella sezione seguente. Testo della licenza: [`../LICENSES/CC-BY-SA-4.0.txt`](../LICENSES/CC-BY-SA-4.0.txt).

## Fonti e cronologie consultate durante lo sviluppo

- [Items, revisione 268993](https://bindingofisaacrebirth.wiki.gg/wiki/Items?oldid=268993) — [autori e modifiche](https://bindingofisaacrebirth.wiki.gg/index.php?title=Items&action=history)
- [Trinkets, revisione 261412](https://bindingofisaacrebirth.wiki.gg/wiki/Trinkets?oldid=261412) — [autori e modifiche](https://bindingofisaacrebirth.wiki.gg/index.php?title=Trinkets&action=history)
- [Cards and Runes, revisione 259738](https://bindingofisaacrebirth.wiki.gg/wiki/Cards_and_Runes?oldid=259738) — [autori e modifiche](https://bindingofisaacrebirth.wiki.gg/index.php?title=Cards_and_Runes&action=history)
- [Pills, revisione 270111](https://bindingofisaacrebirth.wiki.gg/wiki/Pills?oldid=270111) — [autori e modifiche](https://bindingofisaacrebirth.wiki.gg/index.php?title=Pills&action=history)
- [XV - The Devil?, revisione 258528](https://bindingofisaacrebirth.wiki.gg/wiki/XV_-_The_Devil%3F?oldid=258528) — [autori e modifiche](https://bindingofisaacrebirth.wiki.gg/index.php?title=XV_-_The_Devil%3F&action=history)

## Modifiche apportate

Dati selezionati per **Repentance** (non Repentance+), identificati per Variant e ID, e riassunti in italiano con stile funzionale. Sono state riformulate o corrette ulteriormente 223 descrizioni nella revisione testuale successiva, incorporata nella release pubblica **v0.5.1**. Non sono incluse le descrizioni inglesi estratte, HTML della wiki, copie di articoli o file grafici del gioco.

Il repository contiene soltanto `id_names.json` (identificatori e nomi degli oggetti del gioco), `it_*.tsv` (riassunti in italiano) e `include/isaac/catalog_data.hpp` (dati C++ generati). `scripts/generate_catalog.py` opera esclusivamente su questi file, senza rete e senza scaricare la wiki.

I diritti sul gioco, i suoi nomi, loghi e asset restano dei rispettivi titolari. Il progetto è indipendente e non affiliato a Nintendo o agli autori del gioco. [External Item Descriptions (EID)](https://github.com/wofsauge/External-Item-Descriptions) è soltanto un riferimento concettuale: non sono distribuiti i suoi file Lua o asset.
