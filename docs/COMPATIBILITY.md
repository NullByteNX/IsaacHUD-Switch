# Compatibilità e limiti

## Profilo di lettura memoria

- Gioco: The Binding of Isaac: Repentance per Nintendo Switch.
- Title ID: `01009CD0167E2000`.
- Prefisso Build ID (8 byte): `BDB0590D4BA00019`, non il Build ID completo.

Offset, firme, campionamento e lettura in sola lettura del gioco non vengono
cambiati in questa modifica. Il profilo è specifico del Title ID e del
prefisso Build ID indicati sopra.

## Verifiche su Nintendo Switch

L’autore ha confermato il funzionamento su Nintendo Switch dell’OVL v0.5.1,
con HOS 18.1.0 e Atmosphère 1.7.1. Le relative informazioni e l’hash sono
conservati nelle note della v0.5.1 in [RELEASE_NOTES.md](../RELEASE_NOTES.md).

Le informazioni di compatibilità di ciascuna release sono associate alla
versione del programma, all’hash del binario e alla configurazione utilizzata.
La procedura di verifica comprende anche caricamento SD, colori e badge.

## Cataloghi e tier

La nuova versione richiede `switch/IsaacHUD/catalog_it.tsv`; il file dei tier è
separato. Catalogo invalido: messaggio e nessun catalogo parziale. Tier invalido
o mancante: descrizioni disponibili senza badge. I file vengono letti una volta,
prima dell'avvio del worker; durante il gioco restano in memoria e la SD è chiusa.

I 719 tier sono il profilo Repentance selezionato dalla snapshot wiki attribuita.
La fonte della tabella e la selezione dei valori sono documentate in
[ATTRIBUZIONE_TIER.md](../catalog/ATTRIBUZIONE_TIER.md). Il profilo dei dati
è distinto dal profilo di lettura memoria. I tier si applicano ai soli collectible.

## Ambito funzionale

- Una selezione descritta alla volta, pensata per un singolo giocatore.
- Pillole non identificate: il colore non rivela l’effetto. Il supporto riguarda
  gli effetti base identificati e le varianti gestite dal lettore.
- La HUD descrive gli oggetti riconosciuti dal lettore. Sinergie complete,
  inventario, multiplayer e gestione generale della Curse of the Blind
  restano fuori dall’ambito di questa versione.
- La qualità non stima l'utilità dell'oggetto per la run corrente.
- Nessun avvio automatico al boot. HOME/sospensione possono richiedere una
  riattivazione; il ritorno a Tesla usa la gestione `+` e `−` già esistente.
- Snapshot del gioco incoerenti/fallite eliminano la presentazione; non vengono
  mantenuti indefinitamente gli ultimi dati buoni.

La procedura di prova su Switch comprende avvio con dati completi,
file assenti o errati, un collectible per ogni qualità, titoli lunghi, carte,
pillole, trinket, raccolta/reroll degli oggetti e chiusura/riapertura della HUD.
