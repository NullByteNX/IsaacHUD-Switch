# Sorgenti e licenze delle dipendenze incluse

I file in queste cartelle sono una **snapshot minima del codice corrispondente della build originale**. Non sono checkout Git completi: non servono `.git`, documenti di sviluppo, esempi o test upstream per ricompilare l'OVL. Non sono autorizzati cambiamenti arbitrari in vendoring; gli SHA-256 attesi sono in `SHA256SUMS.json` e sono verificati da `scripts/prepare_switch.sh`.

- `Tesla-Template/Makefile`, `LICENSE` — WerWolv/Tesla Template commit `241558db2dc009a213d784d291b2547f1f148ef2`, GPL-2.0; upstream https://github.com/WerWolv/Tesla-Template .
- `libtesla/include/*`, `LICENSE` — WerWolv/libtesla commit `e06d42503dd0717253c77734bd46f3c1addc3f9e`, GPL-2.0 o successiva; upstream https://github.com/WerWolv/libtesla . Il file `stb_truetype.h` include il proprio avviso MIT/pubblico dominio da conservare.
- `Atmosphere/dmnt/*`, `LICENSE`, `LIBRARIES_LICENSE` — Atmosphère commit `36cc9a9f490da37dd1d5f958ee9a256be132cc1d`, GPL-2.0; upstream https://github.com/Atmosphere-NX/Atmosphere .

`prepare_switch.sh` copia le fonti e adatta **solo** il percorso di un include nel client dmnt. `prepare_hud_runtime.py` applica modifiche testuali deterministiche a un header libtesla per il loop HUD. Il file generato deve mantenere l'header GPL. La compilazione utilizza inoltre devkitPro e libnx. Il sorgente di libnx non è incluso nel repository; il relativo avviso ISC è conservato in `LICENSES/ISC-libnx.txt`.
