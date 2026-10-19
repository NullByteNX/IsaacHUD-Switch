# Organizzazione

- `native/`, `core/`, `include/isaac/`: sorgente applicativo originale v0.5.1, compreso il catalogo compilato.
- `catalog/`: solo identificatori/nomi, testi italiani, origine storica e attribuzione quando applicabile; nessun dataset inglese della wiki.
- `scripts/`: generatori, preparazione della build e neutralizzazione del percorso locale nell'OVL; le modifiche libtesla e dmnt sono riproducibili.
- `third_party/`: sorgente corrispondente delle dipendenze GPL usate, revisioni pin e licenze originali.
- `tests/`: test host isolati senza dump del gioco.
- `docs/`: compilazione, compatibilità e documentazione tecnica.
- `switch_build/`: cartella generata localmente, NON va nel repository Git.

Nell'archivio di consegna, **fuori dal repository**: `RELEASE_ASSETS/IsaacHUD.ovl` con hash e istruzioni di pubblicazione come asset della GitHub Release, non nel controllo versione del codice.
