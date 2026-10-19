# Isaac HUD — Nintendo Switch

**v0.5.1 · Overlay Tesla per *The Binding of Isaac: Repentance* · Descrizioni in italiano**

Isaac HUD è un overlay non ufficiale per Nintendo Switch che mostra il nome di un oggetto e una breve descrizione del suo effetto quando Isaac gli si avvicina. Funziona con **Atmosphère**, **Tesla Menu** e un overlay loader compatibile, senza PC o connessione di rete durante il gioco.

> **Stato della release:** l'autore ha installato e verificato il funzionamento di `IsaacHUD.ovl` sulla build del gioco indicata sotto. Il file pubblicato è stato ottenuto dall'OVL compilato con devkitPro dai sorgenti del progetto; **dopo la compilazione è stata sostituita soltanto una stringa contenente un percorso locale di build**, con un percorso generico. La modifica non ha alterato le istruzioni macchina né la dimensione del file. Anche l'OVL con questa correzione è stato provato dall'autore sulla console. Non è garantita la compatibilità con altre build.

## Funzionalità

- Descrizioni di **collectible** e **trinket** a terra.
- Descrizioni di **carte e rune**.
- Informazioni sulle **pillole normali già identificate**, quando i dati letti sono sufficienti; quelle sconosciute mostrano `???`.
- Testo trasparente che appare vicino all'oggetto e scompare allontanandosi.
- Comandi del gioco utilizzabili mentre la HUD è visibile.
- Lettura locale **in sola lettura** della memoria del gioco tramite il servizio `dmnt` di Atmosphère.

Il catalogo comprende **719 collectible, 188 trinket, 97 carte/rune e 50 effetti base di pillole**. Le descrizioni e l'interfaccia sono in **italiano**; i nomi degli oggetti restano generalmente quelli inglesi del gioco. Non sono supportate tutte le sinergie, le modifiche agli effetti delle pillole, le statistiche dell'inventario o le modalità multigiocatore.

## Requisiti e compatibilità

- Una Nintendo Switch con [Atmosphère](https://github.com/Atmosphere-NX/Atmosphere) configurato.
- [Tesla Menu](https://github.com/WerWolv/Tesla-Menu) e relativo overlay loader installati e funzionanti.
- Una copia legittimamente ottenuta di *The Binding of Isaac: Repentance*.
- **Title ID:** `01009CD0167E2000`.
- **Build ID:** prefisso di 8 byte `BDB0590D4BA00019` (non il Build ID completo).

Le prove documentate sono state condotte con **HOS 18.1.0** e **Atmosphère 1.7.1**. Questo non garantisce compatibilità con altre versioni del sistema, altre edizioni del gioco o aggiornamenti successivi. Per maggiori dettagli, consulta [Compatibilità e limitazioni](docs/COMPATIBILITY.md).

## Installazione

1. Scarica `IsaacHUD.ovl` dalla sezione **Releases** del repository (versione `v0.5.1`) oppure compila i sorgenti seguendo [BUILD.md](docs/BUILD.md).
2. Copia il file in `sd:/switch/.overlays/IsaacHUD.ovl` sulla scheda SD della console.
3. Assicurati che Tesla Menu (`ovlmenu.ovl`) e il relativo loader siano già installati: **non sono inclusi** in questa release.
4. Avvia la console con Atmosphère e apri il gioco.
5. **Apri Tesla Menu e seleziona Isaac HUD** per attivarlo. L'overlay non si avvia automaticamente all'accensione della console.

## Utilizzo e riattivazione

Apri Tesla Menu usando la combinazione configurata sul tuo sistema. Quella comunemente utilizzata è **L + freccia giù + pressione dello stick destro (R3)**. Seleziona **IsaacHUD / Isaac HUD Automatico**.

Una volta attivato, avvicinati a un oggetto a terra. Il nome e la descrizione italiana compaiono automaticamente quando l'oggetto viene riconosciuto ed è abbastanza vicino; scompaiono quando ti allontani.

**Se esci dal gioco o la HUD non riappare**, puoi tenere premuti **`+` e `−` contemporaneamente per qualche secondo** (soglia prevista dal codice: circa un secondo) per tornare a Tesla Menu e richiamare Isaac HUD, **purché l'overlay sia ancora in esecuzione**. Se è stato chiuso completamente, apri nuovamente Tesla con la sua combinazione abituale. I due tasti possono anche attivare le rispettive azioni all'interno del gioco.

Dopo HOME, sospensione o altri cambiamenti di stato potrebbe essere necessario riattivare la HUD. La combinazione configurata in Tesla può inoltre servire per nascondere o mostrare la HUD durante una sessione attiva.

## File binario della Release

Il file `IsaacHUD.ovl` pubblicato nella Release **non è byte-identico all'OVL appena compilato**: è stata applicata **una sola correzione successiva alla compilazione** per eliminare dalla stringa associata a `stb_truetype.h` un percorso assoluto del PC usato per la build. La stringa ora contiene il percorso generico `libs/libtesla/include/stb_truetype.h`, seguito dal riempimento necessario a mantenere il layout binario.

- **File:** `IsaacHUD.ovl`
- **Dimensione:** `417848` byte
- **SHA-256 della versione pubblicabile e testata:**

```text
eb0f2bee733e6e0e414fe5c3463fbb05f1383e79ac3e2c9a1691f2802df6a4fe
```

La correzione riguarda esclusivamente una stringa di percorso, non il codice macchina. La build standard dai sorgenti può produrre un hash diverso, anche a parità di funzionalità: il file della Release è la variante con il percorso neutralizzato, **testata dall'autore sulla console**. L'hash permette di identificare il file esatto; non certifica da solo sicurezza o compatibilità.

## Compilazione dai sorgenti

Sono necessari **devkitPro**, **devkitA64/libnx**, GNU Make, Bash e Python 3. La cartella `third_party/` include i sorgenti necessari delle dipendenze utilizzate, con revisioni e licenze documentate. Dalla shell devkitPro MSYS, nella cartella principale del repository:

```bash
make host-test
make switch-prepare
make -C switch_build clean
make switch-build
```

Il risultato della compilazione è `switch_build/IsaacHUD.ovl`. Questa compilazione **non applica automaticamente la correzione della stringa** descritta sopra. Per riprodurla su una build nuova si può usare `scripts/neutralize_ovl_build_path.py` (istruzioni in `docs/BUILD.md`); il nuovo binario va comunque verificato sulla console prima della distribuzione. Per informazioni sul processo di build e sulle dipendenze consulta [docs/BUILD.md](docs/BUILD.md).

## Licenze e attribuzioni

- Il programma include componenti **GPL-2.0**, tra cui libtesla, Tesla Template e il client `dmnt` di Atmosphère. La distribuzione del file `.ovl` deve rispettare i requisiti GPL-2.0 per la disponibilità del codice sorgente corrispondente, delle modifiche e delle istruzioni di compilazione. Vedi [LICENSE](LICENSE), [NOTICE.md](NOTICE.md) e [third_party/](third_party/).
- Il testo della licenza **MIT** presente nell'archivio originale del progetto è conservato in [LICENSES/MIT-original.txt](LICENSES/MIT-original.txt).
- Le descrizioni italiane riassumono effetti e meccaniche di gioco. Fonti, contributori, modifiche e informazioni sulla licenza **CC BY-SA 4.0** sono documentati in [catalog/ATTRIBUZIONE.md](catalog/ATTRIBUZIONE.md) e [LICENSES/CC-BY-SA-4.0.txt](LICENSES/CC-BY-SA-4.0.txt).
- *The Binding of Isaac*, Nintendo, Nintendo Switch ed *External Item Descriptions* appartengono ai rispettivi titolari. Isaac HUD **non è affiliato né approvato** da Nintendo, dagli autori del gioco, dalla wiki o dai creatori di EID; non è un port del codice Lua di EID.

Questo repository **non distribuisce il gioco, ROM, asset proprietari estratti, firmware, chiavi di cifratura o dump**. Per gli obblighi e i crediti dei componenti di terzi, leggi [NOTICE.md](NOTICE.md).

## Limiti noti

La HUD è pensata per la build indicata; altre edizioni, aggiornamenti e configurazioni non sono garantiti. Gli effetti delle pillole sconosciute o modificati da altri elementi del gioco potrebbero non essere descritti. In caso di dati incoerenti la HUD può non mostrare alcun testo; le letture non sono atomiche. L'avvio automatico al boot non è implementato.

Consulta [RELEASE_NOTES.md](RELEASE_NOTES.md) per le note della versione 0.5.1.
