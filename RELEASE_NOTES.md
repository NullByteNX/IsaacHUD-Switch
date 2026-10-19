# Isaac HUD v0.5.1 — note di pubblicazione

Release unica della HUD per **The Binding of Isaac: Repentance** su Nintendo Switch, con overlay Tesla e descrizioni in italiano. Include le ultime correzioni a 223 descrizioni italiane, già presenti nel catalogo della release v0.5.1.

## Funzioni
- HUD trasparente che legge in sola lettura la memoria tramite Atmosphère `dmnt`.
- 719 collectible, 188 trinket, 97 carte/rune e 50 effetti di pillole nel catalogo italiano.
- Attivazione manuale da Tesla dopo l'avvio della console; testo automatico vicino all'oggetto.
- Tenere premuti contemporaneamente `+` e `−` per almeno circa un secondo (o qualche secondo) per tornare a Tesla Menu **finché l'overlay è ancora attivo**. Se è stato terminato, riaprire Tesla con la combinazione configurata e riavviare l'overlay.

## Compatibilità verificata dall'autore
- Title ID: `01009CD0167E2000`
- Build ID, primi 8 byte: `BDB0590D4BA00019`
- L'autore ha confermato il funzionamento sulla console anche del preciso `IsaacHUD.ovl` della Release, dopo la neutralizzazione della stringa del percorso locale di compilazione.

## Identificazione asset
- File: `IsaacHUD.ovl`
- Byte: `417848`
- SHA-256: `eb0f2bee733e6e0e414fe5c3463fbb05f1383e79ac3e2c9a1691f2802df6a4fe`
- L'eseguibile proviene dalla compilazione originale con devkitPro. Dopo la compilazione è stata **neutralizzata un'unica stringa ASCII contenente un percorso locale** associato a `stb_truetype.h`, sostituendola con `libs/libtesla/include/stb_truetype.h` e riempimento nullo. Sono rimaste invariate dimensione del file e istruzioni macchina. Il binario così corretto è stato provato dall'autore su Switch.
- I sorgenti applicativi e le dipendenze utilizzate sono inclusi nel repository. Lo script `scripts/neutralize_ovl_build_path.py` documenta e riproduce la neutralizzazione del percorso senza contenere riferimenti al PC dell'autore; una ricompilazione indipendente può comunque produrre un hash diverso.

## Importante
Licenze e attribuzioni sono documentate in `LICENSE`, `LICENSES/`, `NOTICE.md`, `catalog/ATTRIBUZIONE.md` e `third_party/`.

**Pulizia repository:** i dataset inglesi estratti dalla wiki non sono inclusi. Le descrizioni visualizzate dall'OVL non sono state cambiate durante la pulizia; nel binario è stata neutralizzata unicamente la stringa del percorso di compilazione. Le fonti e le attribuzioni del catalogo sono documentate in `catalog/ATTRIBUZIONE.md`.
