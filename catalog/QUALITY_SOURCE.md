# Provenienza operativa della tabella qualità

Stato del pacchetto: **719/719 collectible**, profilo wiki Repentance, senza i
valori specifici di Repentance+. L’attribuzione è in
[ATTRIBUZIONE_TIER.md](ATTRIBUZIONE_TIER.md). Il registro
`quality_source.json` documenta fonte, profilo e copertura della tabella.

La fonte effettiva è una snapshot attribuita della wiki esportata nel progetto
binding-of-isaac-oracle. Si usano soltanto le coppie numeriche. L'importazione
accetta esclusivamente la revisione fissata e controlla il suo SHA-256: un export
attuale di Repentance+ non viene accettato silenziosamente.

## Reimportazione esplicita

Dalla radice del repository, con una copia locale della snapshot tenuta fuori
dal repository:

```sh
python3 scripts/import_wiki_quality.py --input /percorso/items.generated.json
```

Oppure richiedendo esplicitamente il download della revisione fissata:

```sh
python3 scripts/import_wiki_quality.py --download
```

Il download viene tenuto in memoria: il JSON con descrizioni inglesi e riferimenti
a immagini non viene incluso nel repository o nel pacchetto. Non vengono
scaricate le immagini. Commit, URL e hash sono nel registro e nell'attribuzione.

## Generazione ordinaria, offline

```sh
python3 scripts/generate_quality.py
python3 scripts/generate_quality.py --check
```

Il generatore legge solo `catalog/collectible_quality.tsv` e il registro locale,
poi produce `runtime/collectible_quality.tsv`. Non crea un header C++ e non
consulta la rete. Valida ID noti, duplicati, intervallo 0–4 e corrispondenza della
copertura con il registro. Una qualità zero esplicita è distinta da un valore
mancante.

## Importazione alternativa da metadati locali

`scripts/import_quality.py` rimane uno strumento opzionale per chi possiede XML
locali della versione corretta; non è richiesto dalla distribuzione normale.
Importa solo `quality`, non `craftquality`, e ignora i trinket. Per impostazione
predefinita richiede 719 valori; `--allow-partial` rende esplicita un'eccezione.
Gli XML non vengono copiati nel repository. Se si sostituisce la fonte wiki con
un’altra fonte, mantenere allineati il registro, i riferimenti alla fonte
e le relative attribuzioni.

I valori sintetici dei test sono fixture, non dati di gioco. Non vengono
inseriti nei file runtime distribuiti.
