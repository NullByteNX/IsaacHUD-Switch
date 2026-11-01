# Tier dei collectible — attribuzione e selezione della versione

La tabella `collectible_quality.tsv` contiene esclusivamente **719 coppie ID e
qualità 0–4**. Il file distribuito sulla SD è `runtime/collectible_quality.tsv`.
Carte, rune, pillole e trinket non sono inclusi. Nessun testo descrittivo, quote,
HTML, icona o font della fonte è copiato nel dataset dei tier.

## Fonte e contributori

- Fonte primaria dei dati: [Items, The Binding of Isaac: Rebirth Wiki](https://bindingofisaacrebirth.wiki.gg/wiki/Items).
- Autori: [contributori della wiki, cronologia Items](https://bindingofisaacrebirth.wiki.gg/index.php?title=Items&action=history).
- [Politica di copyright della wiki](https://bindingofisaacrebirth.wiki.gg/wiki/The_Binding_of_Isaac_Rebirth_Wiki:Copyrights).
- Esportazione intermedia: [binding-of-isaac-oracle di lubna-ishaq](https://github.com/lubna-ishaq/binding-of-isaac-oracle).
- Snapshot usata: commit `0026f8343069f689582176cf7b061743ea7decb6`, file
  [items.generated.json](https://github.com/lubna-ishaq/binding-of-isaac-oracle/blob/0026f8343069f689582176cf7b061743ea7decb6/frontend/src/data/items.generated.json).
- Avviso sulla provenienza/licenza dei dati del progetto intermedio:
  [SOURCES.md, revisione fissata](https://github.com/lubna-ishaq/binding-of-isaac-oracle/blob/5845596d8038c924871979a439b6d5e3ac588cc9/SOURCES.md).
- Data di acquisizione per questa modifica: **1 novembre 2026**.
- SHA-256 della snapshot intermedia:
  `fd4cd09b981b41e5543331ce7f175b0dadc7d49968f0c2d48543fb6e2e982c54`.

La snapshot usata è identificata dal commit, dal percorso e dallo SHA-256
riportati sopra. I collegamenti alla pagina originale e alla sua cronologia
identificano la fonte e i contributori della wiki.

## Selezione per Repentance

La snapshot scelta conserva `qualityRaw`, anche per le **143 righe con due
valori**. Per questa esatta snapshot si seleziona il primo valore, riferito a
Repentance, e non il successivo riferito a Repentance+. Il campo `quality` della
stessa snapshot coincide con il primo valore per tutti i 719 record. La snapshot
successiva del progetto intermedio filtra invece i valori vecchi e conserva
Repentance+: **non sostituire l'URL fissato con `main`**.

Controlli di versione riscontrati sulle pagine della wiki:

| ID | Oggetto | Repentance usato | Repentance+ escluso |
| --- | --- | --- | --- |
| 706 | [Abyss](https://bindingofisaacrebirth.wiki.gg/wiki/Abyss) | 4 | 3 |
| 562 | [Rock Bottom](https://bindingofisaacrebirth.wiki.gg/wiki/Rock_Bottom) | 3 | 4 |
| 292 | [Satanic Bible](https://bindingofisaacrebirth.wiki.gg/wiki/Satanic_Bible) | 4 | 3 |

Riferimento ulteriore: [cambiamenti di qualità in V1.9.7.4](https://bindingofisaacrebirth.wiki.gg/wiki/V1.9.7.4).
[Infestation 2](https://bindingofisaacrebirth.wiki.gg/wiki/Infestation_2), ID 234,
vale 3 nella snapshot selezionata. Il profilo dei valori segue la fonte
Repentance documentata; la compatibilità della lettura memoria è descritta in
[COMPATIBILITY.md](../docs/COMPATIBILITY.md).

## Licenza e modifiche

Per i diritti applicabili al dataset derivato dalla wiki si mantiene **CC BY-SA
4.0**. [Testo completo invariato](../LICENSES/CC-BY-SA-4.0.txt);
[licenza online](https://creativecommons.org/licenses/by-sa/4.0/).

Modifiche: estrazione dei soli `gameId`/qualità, selezione del profilo Repentance,
esclusione di tutti gli altri campi, ordinamento per ID e conversione in TSV.
La tabella generata mantiene il riferimento ai contributori. I diritti sui
contenuti del gioco restano dei rispettivi titolari. Il codice dell’importatore
di Isaac HUD è originale e distinto dal dataset attribuito alla wiki.

Il programma conserva i propri avvisi software e legge la tabella come dato
esterno. Il badge è un disegno originale realizzato nel codice del progetto.

Riproduzione: [QUALITY_SOURCE.md](QUALITY_SOURCE.md).
