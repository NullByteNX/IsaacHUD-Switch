# Implementazione e verifiche della versione 0.6.0

La versione 0.6.0 estende la base v0.5.1 del commit
`105c07a1c1d6a8adb8ae3354ddb4df5ce08fd84b` con i cataloghi esterni e i tier.

## Funzioni completate

- Titoli viola, descrizioni bianche, contorno nero e badge numerato originale.
- Badge esclusivamente sui collectible e gestione dei titoli lunghi.
- Catalogo e tier esterni, caricati dalla SD prima dell'avvio del worker.
- 1004 nomi/descrizioni e 50 effetti pillole esportati senza riscritture.
- 719 tier dal profilo Repentance di una snapshot wiki attribuita; selezione di
  143 righe con valori differenti per versione.
- Lettori con limiti e rifiuto di duplicati, namespace errati e input non valido;
  un file dei tier mancante non elimina le descrizioni.
- Generazione offline, packaging SD e audit di dati, documenti e integrità.
- Opzioni di compilazione per percorsi neutri e controllo dei binari prima
  dell'inclusione nel pacchetto SD.
- Testi di licenza, nomi e quattro TSV descrittivi originali conservati byte per byte.

## Verifiche eseguite sul computer

- `make host-test`: sette eseguibili C++ e test Python superati.
- 70 controlli specifici su caricamento cataloghi, errori, assenze e recupero.
- Cinque test sull'importatore XML opzionale e quattro sulla selezione wiki.
- 4016 scenari del vero `HudGui`, con font/display simulati, su due larghezze:
  catalogo effettivo e fixture sintetica. Nessun font Nintendo viene emulato.
- Tre test sul packaging: crediti, licenze software/dati e avvisi, hash, binario di prova sintetico,
  gestione dell’output dati, directory generate e rifiuto dei percorsi locali.
- Cinque test sui percorsi di build: Windows/MSYS, UTF-8/UTF-16, percorsi SD,
  riconoscimento dei percorsi dei SDK precompilati senza eccezioni per la
  macchina corrente, e neutralizzazione di macro e debug con il compilatore host.
- `python3 tests/test_hud_runtime.py`: cinque scenari del runtime/controlli con
  primitive Switch simulate, usando i cataloghi esterni.

L'audit finale verifica i generatori, le dipendenze e gli hash dei nove file
conservati indicati in `PRESERVED_SHA256.json`, i collegamenti relativi dei
Markdown e l'assenza degli header con tabelle incorporate.

## Verifiche su Switch per la release

L’autore ha confermato le prove su Nintendo Switch del binario v0.5.1;
configurazione e hash sono riportati nelle relative note di release.

Per ogni release, la documentazione delle prove associa versione, hash del
binario e configurazione console ai risultati. La procedura comprende memoria,
prestazioni, lettura SD, disegno, oggetti di ogni qualità, titoli lunghi e
riapertura dell’overlay. Il profilo dei tier è documentato dalla relativa fonte.

Riferimenti: [COMPATIBILITY.md](COMPATIBILITY.md) e
[RELEASE_NOTES.md](../RELEASE_NOTES.md).
