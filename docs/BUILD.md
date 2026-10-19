# Compilazione v0.5.1 da sorgenti completi

Requisiti: Windows con shell **devkitPro MSYS** (oppure ambiente devkitPro equivalente), **devkitA64**, **libnx**, **GNU Make**, Bash e Python 3. Non serve clonare libtesla o Atmosphère: nella cartella `third_party/` sono inclusi i sorgenti effettivi di template, libtesla e client dmnt alle revisioni registrate. Il controllo SHA-256 impedisce l'uso accidentale di copie non corrispondenti.

```bash
make host-test
make switch-prepare
make -C switch_build clean
make switch-build
sha256sum switch_build/IsaacHUD.ovl
```

Output: `switch_build/IsaacHUD.ovl`. La cartella `switch_build/` è generata e ignorata da Git; **non modificarne le copie** per cambiare il progetto, modifica solo `native/`, `core/`, `include/`, `scripts/`.

Il contenuto in `third_party/` deriva dalle revisioni `Tesla-Template 241558db2dc009a213d784d291b2547f1f148ef2`, `libtesla e06d42503dd0717253c77734bd46f3c1addc3f9e` e `Atmosphère 36cc9a9f490da37dd1d5f958ee9a256be132cc1d`. Una modifica non invasiva al client dmnt cambia `#include "../service_guard.h"` in `#include "service_guard.h"` al momento della preparazione; `scripts/prepare_hud_runtime.py` crea un header derivato da libtesla con il ciclo `onTick`, senza alterare la copia originale. Non omettere i sorgenti originali e il generatore da un eventuale rilascio binario.

I test `make host-test` verificano la parte logica e i cataloghi, ma **non sostituiscono una build e una prova fisica Switch**. Il file `IsaacHUD.ovl` fornito dall'autore, separato negli asset, ha il suo hash in `RELEASE_NOTES.md`. È la variante testata su console, ottenuta dal binario compilato neutralizzando una stringa di percorso locale, senza cambiare le istruzioni macchina. Non sostituirla con una nuova build non testata. Non è garantito che una compilazione indipendente produca un hash byte-identico, anche a parità di sorgenti, se cambiano le versioni degli strumenti.

Per rigenerare il catalogo:

```bash
python3 scripts/generate_catalog.py
```

Il generatore legge esclusivamente `catalog/id_names.json` e `catalog/it_*.tsv`: le descrizioni inglesi dalla wiki non sono incluse. Fonti e attribuzioni del catalogo sono documentate in `catalog/ATTRIBUZIONE.md` e `NOTICE.md`.

## Neutralizzazione dei percorsi di compilazione

Il normale `make switch-build` non applica la neutralizzazione delle stringhe
di percorso registrate dal compilatore. Per ripetere **solo** il passaggio
di privacy su una nuova build (conservando l'originale), eseguire:

```bash
python3 scripts/neutralize_ovl_build_path.py switch_build/IsaacHUD.ovl out/IsaacHUD.ovl
sha256sum out/IsaacHUD.ovl
strings out/IsaacHUD.ovl | grep -Ei 'Users/|AppData|OneDrive|192\.168\.'
```

L'assenza di risultati da `grep` significa soltanto che non sono state trovate
quelle stringhe. Una build indipendente può avere hash diverso dalla Release;
prima di distribuire un nuovo OVL bisogna ripetere le prove sulla Switch.
Non modificare direttamente l'OVL pubblicato e già testato.
