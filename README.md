# Isaac HUD — Nintendo Switch

**0.6.0 · cataloghi esterni · Repentance · descrizioni italiane**

Overlay Tesla non ufficiale: mostra nome, descrizione e, per i soli collectible,
qualità 0–4 quando Isaac si avvicina. Titoli viola, descrizioni bianche, contorno
nero e badge dorato originale preceduto da un trattino. Carte, rune, pillole e
trinket non ricevono tier.

Il progetto comprende il programma e i cataloghi da installare sulla SD.
I pacchetti di release includono i file operativi; dai sorgenti è possibile
compilare il programma seguendo [BUILD.md](docs/BUILD.md).

## Installazione della nuova versione

Usare il pacchetto di release 0.6.0 oppure compilare il programma dai sorgenti.
Copiare la cartella `switch` del pacchetto nella radice della SD. I tre file
operativi sono:

| Percorso sulla SD | Contenuto |
| --- | --- |
| `switch/.overlays/IsaacHUD.ovl` | Programma 0.6.0 compilato |
| `switch/IsaacHUD/catalog_it.tsv` | Nomi e descrizioni, comprese le pillole |
| `switch/IsaacHUD/collectible_quality.tsv` | 719 coppie ID/qualità dei collectible |

`CREDITI.txt`, `SOFTWARE_NOTICES.txt`, `NOTICE.md` e `licenses/` accompagnano
il pacchetto: comprendono le attribuzioni dei dati, gli avvisi software e i
riferimenti ai sorgenti corrispondenti. I due TSV sono sotto `runtime/` nei sorgenti.
`make sdcard-data` prepara i cataloghi in `dist/sdcard/`.
`make release-package OVL=/percorso/IsaacHUD.ovl` include anche il binario indicato.

Il formato dei cataloghi esterni è supportato dalla versione 0.6.0.
Se il catalogo è assente o non valido, la HUD mostra un messaggio.
Un file dei tier assente o non valido lascia funzionare le descrizioni senza badge.
Non servono Internet, XML del gioco o configurazioni manuali sulla console.

## Utilizzo

Avviare il gioco, aprire Tesla Menu e selezionare Isaac HUD. La combinazione
abituale di Tesla è L + freccia giù + pressione dello stick destro (R3), salvo
configurazioni diverse. L'overlay non si avvia automaticamente al boot.

Avvicinandosi a un oggetto compare il testo; allontanandosi scompare. I comandi
del gioco restano disponibili. Tenere premuti `+` e `−` per circa un secondo
(o qualche secondo) consente di tornare a Tesla Menu finché l'overlay è attivo.
Dopo HOME/sospensione può essere necessaria una riattivazione. I cataloghi vengono
letti all'avvio della HUD: riaprirla dopo aver sostituito i dati.

## Dati e compatibilità

719 collectible, 188 trinket, 97 carte/rune e 50 effetti base di pillole. Nomi e
descrizioni sono quelli già presenti nella v0.5.1, senza riscritture. Per le pillole
restano le precedenti regole di identificazione: il colore non rivela l'effetto.

Il profilo di lettura memoria resta quello della v0.5.1:

- Gioco: The Binding of Isaac: Repentance per Switch, **non Repentance+**.
- Title ID: `01009CD0167E2000`.
- Prefisso Build ID di 8 byte: `BDB0590D4BA00019`.

I tier provengono da una snapshot della wiki con selezione dei valori Repentance.
Sono un indicatore generale del gioco, non una valutazione delle sinergie correnti.
Il profilo dei valori e la loro provenienza sono documentati separatamente
dal profilo di lettura memoria della console. Infestation 2 ha qualità **3**
nel catalogo selezionato. Dettagli: [provenienza tier](catalog/QUALITY_SOURCE.md)
e [compatibilità](docs/COMPATIBILITY.md).

## Compilazione e verifica

Servono devkitPro/devkitA64/libnx per Switch, GNU Make, Bash e Python 3. I test
host usano un compilatore C++20. Le dipendenze vendorizzate non cambiano.

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

Il risultato compilato è `switch_build/IsaacHUD.ovl`; il pacchetto SD è sotto
`dist/sdcard/`. La build usa percorsi neutri nei riferimenti ai sorgenti;
compilazione e packaging controllano i binari per rilevare percorsi locali.
Per ogni release si associano al binario il relativo hash,
le informazioni di compatibilità e il sorgente corrispondente.
I dati si rigenerano offline; solo la reimportazione esplicita della snapshot wiki
richiede una sorgente locale o un download. Istruzioni complete: [BUILD.md](docs/BUILD.md).

## Licenze e attribuzioni

- Programma e componenti GPL: [LICENSE](LICENSE), [NOTICE.md](NOTICE.md), [third_party](third_party/README.md).
- Avviso MIT originale conservato: [MIT-original.txt](LICENSES/MIT-original.txt).
- Descrizioni: [catalog/ATTRIBUZIONE.md](catalog/ATTRIBUZIONE.md), CC BY-SA 4.0 per i contenuti derivati dalla wiki.
- Tier: [catalog/ATTRIBUZIONE_TIER.md](catalog/ATTRIBUZIONE_TIER.md), CC BY-SA 4.0 per i diritti applicabili al dataset.
- Testo CC invariato: [CC-BY-SA-4.0.txt](LICENSES/CC-BY-SA-4.0.txt).

Il codice e i dati sono identificati dalle rispettive licenze e attribuzioni.
I diritti sui contenuti del gioco restano dei rispettivi titolari. Il badge è
un disegno originale realizzato nel codice del progetto.

Progetto indipendente e non approvato da Nintendo, Nicalis, dagli autori del gioco,
dalla wiki o da EID. Non sono inclusi gioco, ROM, firmware, chiavi, dump o asset
proprietari estratti. Restano i limiti su sinergie, co-op, inventario e varianti
non supportate descritti in [COMPATIBILITY.md](docs/COMPATIBILITY.md).

[Note di versione](RELEASE_NOTES.md) · [Formato dati](docs/DATA_FORMAT.md) ·
[Riepilogo per file](docs/RIEPILOGO_MODIFICHE.md)
