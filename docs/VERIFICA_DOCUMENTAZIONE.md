# Verifica di tutta la documentazione

Inventario della documentazione della versione 0.6.0. Il controllo comprende
integrità dei testi di licenza, percorsi, collegamenti e corrispondenza fra
funzionalità descritte, dati e comandi disponibili.

| Documento / avviso | Esito del controllo |
| --- | --- |
| `LICENSE` | Testo originale conservato byte per byte; nessuna sostituzione di licenza o modifica degli avvisi. |
| `LICENSES/CC-BY-SA-4.0.txt` | Testo originale conservato byte per byte; nessuna sostituzione di licenza o modifica degli avvisi. |
| `LICENSES/ISC-libnx.txt` | Testo originale conservato byte per byte; nessuna sostituzione di licenza o modifica degli avvisi. |
| `LICENSES/MIT-original.txt` | Testo originale conservato byte per byte; nessuna sostituzione di licenza o modifica degli avvisi. |
| `LICENSES/NEWLIB.txt` | Avvisi ufficiali newlib 4.6.0; provenienza e integrità registrate. |
| `LICENSES/GPL-3.0-GCC-RUNTIME.txt` | Testo ufficiale GCC per i soli runtime, con eccezione separata. |
| `LICENSES/GCC-RUNTIME-EXCEPTION-3.1.txt` | Eccezione runtime ufficiale riprodotta senza modifiche. |
| `LICENSES/MIT-stb_truetype.txt` | Avviso MIT estratto dall’header vendorizzato, con autore e condizioni. |
| `LICENSES/RUNTIME_SOURCES.json` | Fonti e hash dei nuovi avvisi, verificati dall’audit. |
| `docs/SOFTWARE_NOTICES.txt` | Crediti software e sorgenti della release; incluso nel pacchetto SD. |
| `NOTICE.md` | Avvisi precedenti conservati; aggiunte spiegazione dati esterni e attribuzione tier. |
| `README.md` | Aggiornate installazione, versione, dati e stato delle verifiche; collegamenti ricontrollati. |
| `RELEASE_NOTES.md` | Funzioni della 0.6.0 e note della v0.5.1 identificate per versione, con le prove confermate dall’autore. |
| `catalog/ATTRIBUZIONE.md` | Crediti e fonti storiche conservati; corretti soltanto i riferimenti tecnici alla generazione del catalogo. |
| `catalog/ATTRIBUZIONE_TIER.md` | Fonte intermedia, contributori wiki, commit/hash, selezione della versione e diritti applicabili documentati. |
| `catalog/QUALITY_SOURCE.md` | Fonte e procedura di generazione dei 719 tier; importatore XML documentato come opzione. |
| `docs/BUILD.md` | Allineato a generatori TSV, packaging/ZIP, opzioni GCC per percorsi neutri, controlli dei binari, sorgenti corrispondenti e prove della release. |
| `docs/COMPATIBILITY.md` | Profili di lettura memoria e dei dati, prove Switch confermate dall’autore e procedura di verifica per release. |
| `docs/DATA_FORMAT.md` | Descrive i formati e i limiti effettivi del parser, senza promettere supporti non implementati. |
| `docs/IMPLEMENTATION_STATUS.md` | Funzioni implementate, copertura del catalogo, test automatici e procedura di verifica della release. |
| `docs/PRESERVED_SHA256.json` | Hash fissati dai file originali allegati; usati dall’audit per licenze e testi. |
| `docs/RIEPILOGO_MODIFICHE.md` | Inventario dei file interessati dalla versione 0.6.0 e dei relativi aggiornamenti. |
| `docs/STRUCTURE.md` | Allineato ai parser e alle cartelle runtime/dist; distingue sorgenti e output. |
| `docs/TIER_SETUP.md` | Allineato ai tre file operativi, ai crediti e alle regole per dati assenti o non validi. |
| `docs/VERIFICA_DOCUMENTAZIONE.md` | Questo inventario: controllo dei documenti e delle licenze presenti. |
| `docs/tier_preview.svg` | Verificata la grafica originale; esempio aggiornato al valore del catalogo, senza asset copiati. |
| `third_party/Atmosphere/LIBRARIES_LICENSE` | Testo originale conservato byte per byte; nessuna sostituzione di licenza o modifica degli avvisi. |
| `third_party/Atmosphere/LICENSE` | Testo originale conservato byte per byte; nessuna sostituzione di licenza o modifica degli avvisi. |
| `third_party/README.md` | Ricontrollato e conservato: dipendenze, revisioni, avvisi e adattamenti storici non cambiano. |
| `third_party/Tesla-Template/LICENSE` | Testo originale conservato byte per byte; nessuna sostituzione di licenza o modifica degli avvisi. |
| `third_party/libtesla/LICENSE` | Testo originale conservato byte per byte; nessuna sostituzione di licenza o modifica degli avvisi. |

I collegamenti Markdown relativi dei documenti applicativi vengono verificati
anche da `scripts/audit_publication.py`. I riferimenti alla v0.5.1 rimasti sono
associati a quella release o spiegano la migrazione al formato esterno.
Gli avvisi dentro il codice vendorizzato restano intatti e i file sono controllati
con `third_party/SHA256SUMS.json`.
