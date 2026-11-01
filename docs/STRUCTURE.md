# Organizzazione 0.6.0

| Percorso | Contenuto |
| --- | --- |
| `native/` | Overlay Tesla, avvio del caricamento SD e lettore memoria |
| `core/` | Campionamento del gioco, invariato rispetto alla base |
| `include/isaac/catalog.hpp` | Parser dei cataloghi esterni e indici in memoria |
| `include/isaac/quality.hpp` | Ricerca della qualità solo per variant 100 |
| `include/isaac/hud_style.hpp` | Colori e scudo numerato originali |
| `include/isaac/hud_layout.hpp` | Wrapping e spazio riservato al badge |
| `catalog/` | Sorgenti dei testi, tabella numerica, attribuzioni e provenienza |
| `runtime/` | I due TSV da installare, generati e verificabili offline |
| `scripts/` | Generatori, importatori, preparazione Switch, packaging e audit |
| `third_party/` | Dipendenze GPL vendorizzate, con hash e licenze invariati |
| `tests/` | Test host e fixture sintetiche; nessun dump del gioco |
| `docs/` | Build, formato dati, limiti, verifica documenti e riepilogo modifiche |
| `LICENSE`, `LICENSES/` | Testi originali conservati; avvisi runtime e loro provenienza |

I cataloghi sono conservati nei due TSV sotto `runtime/`. Dopo il caricamento
dalla SD il programma usa vettori ordinati, immutabili durante la sessione,
e ricerca binaria.

## Directory generate

- `out/`: eseguibili dei test host.
- `switch_build/`: copie per la compilazione Switch e relativo OVL.
- `dist/sdcard/`: albero da copiare sulla SD, con o senza OVL secondo il comando.

Queste tre directory sono escluse da Git. `make sdcard-data` prepara il
pacchetto dei cataloghi; `make release-package OVL=...` prepara il pacchetto
operativo con il binario indicato. Le note di ciascuna release riportano
gli identificativi del relativo eseguibile.
