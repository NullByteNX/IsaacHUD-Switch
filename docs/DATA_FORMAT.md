# Formato dei cataloghi esterni

Encoding UTF-8, colonne separate da TAB, commenti con `#`, righe LF o CRLF.
I formati v1 sono specifici del catalogo Repentance attuale, non un contratto per
mod arbitrarie o Repentance+. I file si caricano all'avvio; sostituirli richiede
riaprire l'overlay. Nessun accesso in scrittura o download sulla console.

## catalog_it.tsv

Prima riga obbligatoria: `# isaac-hud-catalog-v1`.

| Tipo | Colonne, nell'ordine |
| --- | --- |
| `D` | tipo, variant, ID, nome, descrizione |
| `P` | tipo, 70, ID effetto, nome, descrizione normale, descrizione gigante |

Sono richieste 1004 righe D: 719 variant 100, 97 variant 300 e 188 variant 350,
ordinate per variant e ID, senza duplicati. Seguono 50 effetti pillola con ID
0–49. Il numero della pillola qui è un **effetto**, non il colore della capsula.
Il testo gigante è conservato anche dove la HUD attuale non ne applica tutte le
varianti; non si ampliano le regole di identificazione della v0.5.1.

Nei campi testuali backslash, TAB, LF e CR sono rappresentati dagli escape
`\\`, `\t`, `\n`, `\r`; gli altri escape sono rifiutati. Il caricatore controlla
formato, categorie, conteggi, ordine, limiti degli ID, duplicati e dimensioni:
file massimo 1 MiB, riga massima 16384 byte, nome 256 byte e testi 4096 byte.
Un errore rifiuta l'intero catalogo ed elimina i dati precedenti, senza usare un
caricamento parziale. L'errore viene mostrato nella HUD.

## collectible_quality.tsv

Prima riga obbligatoria: `# isaac-hud-quality-v1`.
Due colonne: ID collectible e qualità intera 0–4. Righe ordinate, ID unici e già
presenti nel catalogo dei collectible. Nessun variant o nome viene duplicato.
La tabella distribuita ha 719 righe numeriche. Un file parziale valido può
mostrare solo le qualità presenti; un file errato viene interamente scartato.

Zero è una qualità valida. Un dato mancante non è zero e non produce un badge.
Anche se il numero coincide con l'ID di una carta, pillola o trinket, la qualità
non viene applicata a quelle categorie.

## Codice e dati

Gli schemi e i parser sono codice; i record del catalogo e dei tier sono dati
esterni con le attribuzioni descritte in `catalog/`. Nessun generatore produce
più un header C++ contenente nomi, descrizioni o qualità. Il file sorgente
`catalog/collectible_quality.tsv` è un input del generatore, non va copiato sulla
SD al posto del corrispondente `runtime/collectible_quality.tsv`, che contiene
l'intestazione di formato obbligatoria.
