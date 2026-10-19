#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
bash scripts/prepare_switch.sh
python3 scripts/prepare_hud_runtime.py switch_build/libs/libtesla/include/tesla.hpp switch_build/include/isaac/tesla_hud.hpp
printf '%s\n' 'HUD runtime: codice libtesla adattato con onTick e gestione input, generato a build time.' >> switch_build/DEPENDENCY_REVISIONS.txt
echo 'Pronto: make switch-build; output switch_build/IsaacHUD.ovl'
