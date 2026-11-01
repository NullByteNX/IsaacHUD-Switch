# Compilazione e pacchetto 0.6.0

Servono devkitPro con devkitA64/libnx, GNU Make, Bash e Python 3. Per i test host
serve un compilatore C++20, ad esempio `g++`. Le dipendenze effettive
sono vendorizzate sotto `third_party/`, con revisioni e hash invariati. La build
ordinaria e la rigenerazione dei dati sono offline.

Nella shell devkitPro MSYS2 su Windows, il compilatore per i test host si installa
con `pacman -S --needed gcc`. Il pacchetto comprende anche `g++`.

Dalla radice del repository:

```sh
make data
make host-test
make publication-audit
make switch-prepare
python3 tests/test_hud_runtime.py
make -C switch_build clean
make switch-build
make release-package OVL=switch_build/IsaacHUD.ovl
```

Output compilato: `switch_build/IsaacHUD.ovl`. Pacchetto SD: `dist/sdcard/`.
Le directory `switch_build/`, `out/` e `dist/` sono generate e ignorate da Git.
Modificare i sorgenti in `native/`, `core/`, `include/isaac/`, `scripts/`, `catalog/`.
Non correggere direttamente le copie sotto `switch_build/`.

## Generazione e packaging dei dati

`scripts/generate_catalog.py` legge `catalog/id_names.json` e i quattro
`catalog/it_*.tsv`, e produce `runtime/catalog_it.tsv` conservando i testi.
`scripts/generate_quality.py` produce `runtime/collectible_quality.tsv` dai dati e
dalla provenienza locali. I due vecchi header di tabelle compilate sono rimossi.

```sh
make sdcard-data
```

Questo comando prepara il pacchetto dei cataloghi, dei crediti e della licenza
CC sotto `dist/sdcard/`, insieme agli avvisi software e alle licenze dei componenti. La modalità dati aggiorna la directory generata con
i soli componenti previsti per questo tipo di pacchetto.

`make release-package OVL=...` richiede un OVL esistente, non vuoto, e una tabella
completa di 719 tier con provenienza. Il parametro `OVL` indica il binario
compilato dai sorgenti della release da includere nel pacchetto.

Per creare lo ZIP installabile, dopo `make release-package`:

```sh
mkdir -p out
python3 -m zipfile -c out/IsaacHUD-0.6.0-SD.zip dist/sdcard/switch dist/sdcard/LEGGIMI.txt dist/sdcard/SHA256SUMS.json
```

Lo ZIP ha `switch/` alla radice, inclusa la sottocartella `.overlays`. Estrarne
il contenuto nella radice della SD, unendo la cartella `switch` e sostituendo
i file di IsaacHUD. Crediti e licenza dei dati accompagnano i tre file operativi.

La reimportazione wiki è separata ed esplicita:
[QUALITY_SOURCE.md](../catalog/QUALITY_SOURCE.md). Non scarica dati durante `make data`.

## Sorgenti corrispondenti e avvisi

Le revisioni restano Tesla-Template `241558db2dc009a213d784d291b2547f1f148ef2`,
libtesla `e06d42503dd0717253c77734bd46f3c1addc3f9e` e Atmosphère
`36cc9a9f490da37dd1d5f958ee9a256be132cc1d`. Gli script riproducono l'adattamento
storico del percorso include dmnt e il runtime HUD libtesla; non alterano il
vendoring. I relativi avvisi di modifica storici restano validi per quelle
trasformazioni. libnx/devkitPro restano requisiti esterni.

Con un rilascio binario distribuire il sorgente completo corrispondente,
dipendenze modificate, generatori, istruzioni, crediti e licenze applicabili.
Conservare i file di dati e le loro attribuzioni separatamente dal software.
Il packaging copia anche GPL-2.0, MIT, ISC, i testi relativi ai runtime GCC/newlib
e gli avvisi `SOFTWARE_NOTICES.txt` e `NOTICE.md`. Il sorgente corrispondente
va pubblicato con il tag `v0.6.0` e reso disponibile nella stessa release, anche
come allegato `IsaacHUD-Switch.zip`. Questi avvisi accompagnano il binario;
le licenze originali e i dati non vengono riscritti.

## Percorsi di build e prove console

La compilazione host e quella Switch applicano `-ffile-prefix-map` ai percorsi
del progetto, della home e del SDK. Lo script [build_privacy.py](../scripts/build_privacy.py)
genera le opzioni includendo le notazioni MSYS e Windows quando `cygpath` è
disponibile. I riferimenti nei macro `__FILE__`, `__BASE_FILE__` e nelle
informazioni di debug vengono sostituiti con percorsi neutri. Le opzioni del
compilatore non vengono registrate nei file oggetto.

`make switch-build` controlla l'ELF e l'OVL risultanti. Anche il packaging
controlla l'OVL prima di modificare la cartella SD. Il controllo cerca prefissi
locali della macchina corrente e forme comuni di percorsi assoluti, nelle
stringhe UTF-8 e UTF-16. Sono riconosciuti separatamente tre prefissi dei
percorsi di origine delle librerie precompilate devkitA64/newlib, libnx e
libgcc, elencati in `PREBUILT_SDK_PATHS` nello script: appartengono al sistema
che ha costruito il SDK e possono rimanere nei binari. I prefissi della
macchina corrente restano sempre vietati, anche se coincidessero con uno di
quelli del SDK. Ogni altro percorso locale rilevato blocca il controllo senza
modificare il binario. Per ripetere il controllo su un file:

```sh
python3 scripts/build_privacy.py check switch_build/IsaacHUD.ovl
sha256sum switch_build/IsaacHUD.ovl
```

Quando si applica questo aggiornamento a una cartella già compilata, eseguire
`make switch-prepare` e `make -C switch_build clean` prima di ricompilare, per
non riutilizzare file oggetto precedenti. Lo script storico
`neutralize_ovl_build_path.py` rimane disponibile per la singola stringa nota;
la procedura corrente usa le opzioni di compilazione e il controllo completo
del file, senza riscrivere stringhe dentro l'eseguibile.

L'aggiornamento delle sole eccezioni del controllo per le librerie precompilate
non richiede di ricompilare: ripetere il controllo sui file ELF/OVL esistenti e
poi il packaging. La rimappatura dei prefissi agisce sui sorgenti compilati
localmente, non sulle librerie già compilate del SDK.

Calcolare l’hash sul binario finale destinato alla distribuzione e associarlo
alla release corrispondente. Gli identificativi e le prove della v0.5.1 sono
conservati in [RELEASE_NOTES.md](../RELEASE_NOTES.md).

I test host verificano logica, cataloghi, errori, wrapping e chiamate di disegno
con primitive simulate. La procedura di verifica su Switch comprende lettura SD,
memoria, colori, leggibilità, transizioni e ritorno a Tesla. I risultati sono
associati alla versione e all’hash del binario nelle note di release.
