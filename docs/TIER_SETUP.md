# Titoli viola e tier — utilizzo e installazione

Il nome viene mostrato in viola `#BB66BB`, la descrizione in bianco, entrambi con
contorno nero. Ai collectible con qualità nota si aggiungono un trattino e uno
scudo dorato originale con numero 0–4. Il badge non viene usato per carte, rune,
pillole o trinket. Per nomi lunghi segue l'ultima riga del titolo, con spazio
riservato; non viene disegnato a una coordinata fissa indipendente dal nome.

## File sulla SD

| Percorso dalla radice SD | Ruolo |
| --- | --- |
| `switch/.overlays/IsaacHUD.ovl` | Programma 0.6.0 compilato |
| `switch/IsaacHUD/catalog_it.tsv` | Nomi, descrizioni e 50 effetti pillole |
| `switch/IsaacHUD/collectible_quality.tsv` | 719 tier dei collectible |

I TSV provengono dalla cartella `runtime/`. `make sdcard-data` prepara il
pacchetto dei cataloghi con directory e crediti. `make release-package OVL=...`
include anche il binario compilato indicato.
Conservare anche `CREDITI.txt` e `licenses/CC-BY-SA-4.0.txt` insieme ai dati.

Non servono XML, Internet o un PC collegato durante il gioco. La HUD carica i
file una volta all'avvio e chiude l'accesso alla SD prima di iniziare il lettore
memoria. Per aggiornare i dati, sostituire i TSV e riaprire l'overlay.

## Assenze e file non validi

- Catalogo assente/non valido: messaggio che invita a copiare i file dati.
- Tabella tier assente/non valida: descrizioni disponibili, badge nascosti.
- ID senza qualità: nessun badge; non viene trasformato in tier 0.
- Dati memoria del gioco non validi: restano i controlli e la rimozione del testo
  della HUD già esistenti.

## Fonte e limiti

I tier usano la snapshot wiki attribuita in
[ATTRIBUZIONE_TIER.md](../catalog/ATTRIBUZIONE_TIER.md). Il profilo è Repentance,
non Repentance+. Infestation 2 vale 3 in questa tabella. La qualità non
calcola le sinergie della run.

La HUD usa il font di sistema Tesla e un badge originale di 22 × 24 pixel
nel framebuffer. Le verifiche della release comprendono leggibilità,
posizionamento e caricamento dei file esterni.

[Anteprima indicativa della grafica](tier_preview.svg) ·
[Compilazione](BUILD.md) · [Formato dati](DATA_FORMAT.md)
