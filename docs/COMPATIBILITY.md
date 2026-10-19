# Compatibilità e limiti documentati

## Profilo supportato

- Gioco: *The Binding of Isaac: Repentance* per Switch.
- Title ID: `01009CD0167E2000`.
- Prefisso Build ID (8 byte): `BDB0590D4BA00019`. Non è il Build ID completo di 32 byte.
- Ambiente dei test documentati: HOS `18.1.0`, Atmosphère `1.7.1`, overlay Tesla operativo.

Il progetto utilizza indirizzi ricavati dalle basi di processo correnti, **non** gli indirizzi assoluti di registrazioni diagnostiche. Offset e firme di codice sono specifici della build identificata. Nessuna compatibilità garantita con diverse edizioni, aggiornamenti, Repentance+, altri Title ID/Build ID o configurazioni non testate.

## Funzionalità e verifiche

- HUD trasparente e lettura sola locale: comportamento di base confermato nelle versioni di sviluppo provate su Switch.
- Lettura di collectible e trinket: evidenze PC e conferme native storiche.
- Carte, rune e pillole: implementazione presente; l'autore conferma il funzionamento del binario distribuito nella build dichiarata, senza una matrice pubblica dei test per ogni oggetto o pillola.
- Solo descrizioni italiane; nessuna localizzazione inglese dell'interfaccia.
- Più player, sinergie complete, blind, inventario generale, effetti di pillole trasformati/giganti/dorate e auto-avvio: non supportati o non validati.
- Riattivazione dopo `Exit Game → Continue`, HOME/sleep: comportamento da verificare secondo la configurazione; con overlay ancora attivo si può tornare a Tesla premendo `+` e `−`.

Se i metadati, la build, le firme o le due acquisizioni risultano incoerenti, la HUD omette il dato invece di presentare un elemento ormai non attuale.
