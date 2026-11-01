# Isaac HUD 0.6.0 — cataloghi esterni e tier

La versione 0.6.0 introduce i cataloghi esterni e la visualizzazione della
qualità dei collectible. I nomi e i testi descrittivi mantengono il contenuto
della v0.5.1.

## Cambiamenti

- Titoli viola, testo descrittivo bianco e contorno nero.
- Badge dorato originale 0–4 preceduto da un trattino, solo per collectible.
- Catalogo dei nomi/descrizioni e tabella tier esterni all'OVL, letti all'avvio.
- Testi e nomi della v0.5.1 conservati; regole di identificazione pillole invariate.
- 719 tier dal profilo Repentance della snapshot wiki attribuita; 143 righe con
  due valori vengono selezionate per versione, senza usare i valori Repentance+.
- Cataloghi validati per formato, limiti, ordine, duplicati e namespace; file
  tier mancante/errato: descrizioni disponibili senza badge.
- Preparazione offline della struttura SD, avvisi software e dati, licenze dei
  componenti e registrazione degli hash del contenuto.
- Percorsi neutri nei riferimenti compilati ai sorgenti e nei dati di debug;
  controllo dei percorsi locali nei binari prima del packaging.
- Rimozione dei vecchi header contenenti il catalogo e la tabella compilati.

## Migrazione dalla v0.5.1

Installare il nuovo OVL e i due TSV nei percorsi descritti nel README. Conservare
crediti e licenza CC nel pacchetto. Il formato esterno richiede il programma
0.6.0. Ogni release è identificata dal proprio binario e relativo hash.

## Documentazione e diritti

I testi di `LICENSE` e `LICENSES/*` e le dipendenze vendorizzate non cambiano.
Aggiornati i riferimenti tecnici; crediti storici delle descrizioni conservati.
Aggiunta un'attribuzione distinta per i tier. Il riepilogo completo dei file è in
[docs/RIEPILOGO_MODIFICHE.md](docs/RIEPILOGO_MODIFICHE.md).

---

Le note seguenti descrivono la **v0.5.1**, con il relativo binario, hash e
verifiche confermate dall’autore.

# Isaac HUD v0.5.1 — note di pubblicazione

Release v0.5.1 della HUD per **The Binding of Isaac: Repentance** su Nintendo Switch, con overlay Tesla e descrizioni in italiano. Il catalogo comprende una revisione testuale di 223 descrizioni italiane.

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

**Contenuto del repository:** il catalogo comprende i nomi e i testi italiani visualizzati dalla HUD. Fonti e attribuzioni sono documentate in `catalog/ATTRIBUZIONE.md`. La normalizzazione del percorso di compilazione nel binario conserva il contenuto delle descrizioni.
