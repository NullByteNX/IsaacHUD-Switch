# Riepilogo completo delle modifiche — 0.6.0

La tabella elenca i file interessati dalla versione 0.6.0, sviluppata dalla
base v0.5.1 del commit `105c07a1c1d6a8adb8ae3354ddb4df5ce08fd84b`.
Sono compresi i file sorgente, i dati runtime e la documentazione;
`out/`, `switch_build/` e `dist/` sono output generati, non sorgenti modificati.

I testi delle licenze sono invariati. I quattro TSV descrittivi e l'indice dei
nomi sono identici agli originali. Crediti storici e note v0.5.1 sono conservati;
la documentazione descrive il formato esterno e i comandi della versione 0.6.0.

| File | Stato | Modifica effettuata |
| --- | --- | --- |
| `.gitignore` | Modificato | Esclude anche dist/, directory generata dei pacchetti SD. |
| `LICENSES/NEWLIB.txt` | Aggiunto | Avvisi raccolti di newlib 4.6.0, riprodotti dalla fonte ufficiale. |
| `LICENSES/GPL-3.0-GCC-RUNTIME.txt` | Aggiunto | Testo GPLv3 relativo ai componenti runtime GCC; non cambia la licenza dell’applicazione. |
| `LICENSES/GCC-RUNTIME-EXCEPTION-3.1.txt` | Aggiunto | Eccezione ufficiale per le librerie runtime GCC. |
| `LICENSES/MIT-stb_truetype.txt` | Aggiunto | Riproduce l’alternativa MIT presente nell’header vendorizzato, con copyright Sean Barrett. |
| `LICENSES/RUNTIME_SOURCES.json` | Aggiunto | Fonti e hash dei quattro avvisi runtime aggiunti. |
| `docs/SOFTWARE_NOTICES.txt` | Aggiunto | Crediti software, avvisi runtime e riferimento al sorgente della release; copiato anche sulla SD. |
| `Makefile` | Modificato | Aggiunge generazione dati, test dei parser/tier/packaging, opzioni per neutralizzare i percorsi e controllo ELF/OVL; target SD e release. |
| `NOTICE.md` | Modificato | Conserva gli avvisi software e del catalogo; aggiunge dati runtime esterni, attribuzione tier e badge originale. |
| `README.md` | Modificato | Versione, installazione dei tre file operativi, dati, build con ricompilazione pulita e controlli dei percorsi; attribuzioni e identificativi per release. |
| `RELEASE_NOTES.md` | Modificato | Funzioni, percorsi di build neutri e migrazione 0.6.0; note della v0.5.1 con identificativi del binario e prove confermate dall’autore. |
| `catalog/ATTRIBUZIONE.md` | Modificato | Conserva crediti, revisioni e licenza dei testi; aggiorna soltanto la descrizione tecnica del catalogo esterno e dei file. |
| `catalog/ATTRIBUZIONE_TIER.md` | Aggiunto | Documenta contributori, snapshot fissata, hash, selezione Repentance, modifiche e CC BY-SA 4.0 per i diritti applicabili. |
| `catalog/QUALITY_SOURCE.md` | Aggiunto | Spiega fonte effettiva, riproduzione offline, download esplicito e importatore XML solo opzionale. |
| `catalog/collectible_quality.tsv` | Aggiunto | Aggiunge le 719 coppie ID/qualità selezionate per Repentance, senza nomi, descrizioni o asset della fonte. |
| `catalog/quality_source.json` | Aggiunto | Registra origine, commit, hash, copertura, 143 righe con valori per versione e limiti della verifica sulla build Switch. |
| `docs/BUILD.md` | Modificato | Aggiorna generatori, pacchetto dati/OVL, ZIP per SD, prerequisiti MSYS2, neutralizzazione e controllo dei percorsi, sorgenti corrispondenti e prove. |
| `docs/COMPATIBILITY.md` | Modificato | Profili di compatibilità, cataloghi SD, ambito funzionale e verifica delle release. |
| `docs/DATA_FORMAT.md` | Aggiunto | Specifica intestazioni TSV, colonne D/P, escape, limiti, ordinamento, qualità zero e gestione degli errori. |
| `docs/IMPLEMENTATION_STATUS.md` | Aggiunto | Riepiloga funzioni, copertura, test automatici inclusi percorsi di build e packaging, e procedura di prova su Switch per release. |
| `docs/PRESERVED_SHA256.json` | Aggiunto | Fissa gli hash originali di quattro file di licenza e cinque file di nomi/testi per controllare che restino identici. |
| `docs/RIEPILOGO_MODIFICHE.md` | Aggiunto | Tabella completa per file aggiunto, modificato o rimosso, con criteri di confronto e file conservati. |
| `docs/STRUCTURE.md` | Modificato | Descrive parser, runtime/, cataloghi esterni e directory generate; elimina la descrizione del catalogo compilato come attuale. |
| `docs/TIER_SETUP.md` | Aggiunto | Descrive installazione SD, badge, avvio, gestione file mancanti, fonte wiki e anteprima; non richiede più XML. |
| `docs/VERIFICA_DOCUMENTAZIONE.md` | Aggiunto | Inventario del controllo di ogni documento e avviso di licenza, con esito e motivazione. |
| `docs/tier_preview.svg` | Aggiunto | Anteprima originale di titoli viola e badge; esempio Infestation 2 aggiornato a 3 come nel catalogo selezionato. |
| `include/isaac/catalog.hpp` | Aggiunto | Lettori originali dei due TSV, validazione e dati in memoria; nessuna tabella di testi o tier incorporata. |
| `include/isaac/catalog_data.hpp` | Rimosso | Elimina il precedente header con nomi e descrizioni compilati nell’OVL. |
| `include/isaac/collectible_quality_data.hpp` | Rimosso | Tabella dei tier gestita tramite il TSV runtime esterno. |
| `include/isaac/descriptions.hpp` | Modificato | Usa il catalogo caricato dalla SD; aggiunge la qualità opzionale alla presentazione senza cambiare le regole delle pillole. |
| `include/isaac/hud_layout.hpp` | Modificato | Riserva spazio al suffisso trattino/badge dopo l’ultima riga del titolo; gestisce larghezze ridotte. |
| `include/isaac/hud_style.hpp` | Aggiunto | Colori separati e disegno procedurale originale dello scudo con cifre 0–4. |
| `include/isaac/quality.hpp` | Aggiunto | Ricerca binaria dei tier caricati, limitata ai collectible e con assenza distinta dalla qualità zero. |
| `native/hud_main.cpp` | Modificato | Carica i dati dalla SD prima del worker; chiude la SD; mostra errori del catalogo e disegna titolo viola e tier. |
| `runtime/catalog_it.tsv` | Aggiunto | Catalogo SD generato: 1004 oggetti e 50 effetti pillola, con gli stessi nomi e testi sorgente della v0.5.1. |
| `runtime/collectible_quality.tsv` | Aggiunto | Tabella SD generata con intestazione v1, attribuzione e 719 tier; non è un header C++. |
| `scripts/audit_publication.py` | Modificato | Verifica dati generati, file conservati, dipendenze, assenza dei vecchi header e link relativi della documentazione. |
| `scripts/build_privacy.py` | Aggiunto | Genera opzioni GCC con prefissi neutri MSYS/Windows; controlla i binari UTF-8/UTF-16 e riconosce i prefissi dei SDK precompilati, senza eccezioni per la macchina corrente. |
| `scripts/generate_catalog.py` | Modificato | Esporta TSV esterno invece dell’header C++; aggiunge escape e modalità --check senza cambiare i testi. |
| `scripts/generate_quality.py` | Aggiunto | Genera e verifica il TSV runtime con copertura e provenienza; non genera più codice con tabelle. |
| `scripts/import_quality.py` | Aggiunto | Importatore XML locale opzionale, con namespace separati e output TSV esterno; nessun XML copiato nel repo. |
| `scripts/import_wiki_quality.py` | Aggiunto | Importatore originale della snapshot CC fissata: controllo hash, selezione versione e conservazione dei soli ID/qualità. |
| `scripts/package_sd.py` | Aggiunto | Prepara cartelle SD, crediti, avvisi software, licenze di programma/dati/runtime e hash; controlla i percorsi dell’OVL prima di scrivere. |
| `scripts/prepare_switch.sh` | Modificato | Copia parser e stile, rimuove header obsoleti, imposta versione 0.6.0 e opzioni GCC per percorsi neutri nelle unità C/C++. |
| `tests/isaac_test_fixture.py` | Aggiunto | Genera qualità sintetiche esclusivamente per i test; non contiene una seconda tabella di gioco. |
| `tests/test_build_privacy.py` | Aggiunto | Verifica riconoscimento dei percorsi, varianti MSYS/Windows e neutralizzazione reale di macro e debug con il compilatore host. |
| `tests/test_catalog.cpp` | Modificato | Carica il catalogo esterno prima di verificare copertura, lookup e riservatezza delle pillole. |
| `tests/test_catalog_setup.hpp` | Aggiunto | Configurazione comune dei test C++ con caricamento dei TSV host. |
| `tests/test_descriptions.cpp` | Modificato | Carica i dati esterni mantenendo i controlli di nomi, descrizioni e namespace. |
| `tests/test_hud.cpp` | Modificato | Esegue i controlli di prossimità e presentazione con il catalogo caricato dal file. |
| `tests/test_hud_render.py` | Aggiunto | Prova la vera classe HudGui su 4016 scenari con display/font simulati e dati esterni. |
| `tests/test_hud_runtime.py` | Modificato | Adatta la simulazione del runtime/overlay all’avvio con dati esterni; conserva i cinque scenari dei comandi. |
| `tests/test_package_sd.py` | Aggiunto | Prova cartelle, crediti/licenza, hash, rimozione OVL residuo e rifiuto di input non validi o percorsi locali senza modificare il pacchetto. |
| `tests/test_quality.cpp` | Aggiunto | Verifica lookup, esclusione delle altre categorie, wrapping e disegno delle cinque cifre. |
| `tests/test_quality_import.py` | Aggiunto | Verifica l’importatore XML, qualità zero, override e copertura, usando fixture sintetiche non distribuite come dati reali. |
| `tests/test_runtime_catalog.cpp` | Aggiunto | 70 controlli su formati, escape, duplicati, limiti, file mancanti e cancellazione dei dati precedenti. |
| `tests/test_wiki_quality.py` | Aggiunto | Verifica selezione del primo valore Repentance, rifiuto di snapshot non fissate e provenienza della tabella reale. |

## File conservati

`LICENSE`, `LICENSES/CC-BY-SA-4.0.txt`, `LICENSES/MIT-original.txt`,
`LICENSES/ISC-libnx.txt`, `catalog/id_names.json`, `catalog/it_collectibles.tsv`,
`catalog/it_trinkets.tsv`, `catalog/it_cards.tsv` e `catalog/it_pills.tsv` sono
verificati mediante gli hash originali in `PRESERVED_SHA256.json`. Il vendoring
`third_party/` e i suoi avvisi non sono stati modificati.

## Distribuzione

Il pacchetto operativo comprende `IsaacHUD.ovl`, i due cataloghi esterni,
i crediti e la licenza dei dati. I generatori e le istruzioni consentono di
preparare il pacchetto dai sorgenti. Versione, hash e risultati delle prove
sono associati al relativo binario nelle note di release.
