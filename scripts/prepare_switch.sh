#!/usr/bin/env bash
# Vendored, commit-pinned GPL source. Creates files only inside generated switch_build/.
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$project_dir"
if [[ -z "${DEVKITPRO:-}" || ! -f "$DEVKITPRO/libnx/switch_rules" ]]; then
    echo 'Serve devkitPro/devkitA64/libnx (usa la shell devkitPro MSYS).' >&2
    exit 1
fi
command -v python3 >/dev/null
for input in third_party/SHA256SUMS.json third_party/Tesla-Template/Makefile third_party/libtesla/include/tesla.hpp third_party/libtesla/include/stb_truetype.h third_party/Atmosphere/dmnt/dmntcht.os.horizon.c; do
    test -f "$input" || { echo "Sorgente richiesto mancante: $input" >&2; exit 1; }
done
python3 - <<'PY_VERIFY'
import hashlib,json,pathlib
m=json.loads(pathlib.Path('third_party/SHA256SUMS.json').read_text(encoding='utf-8'))
for name,expected in m['files'].items():
    content=pathlib.Path(name).read_bytes()
    if hashlib.sha256(content).hexdigest()!=expected:
        raise SystemExit('Sorgente vendorizzato cambiato: '+name)
print('Sorgenti GPL e revisioni verificati.')
PY_VERIFY
if [[ -e switch_build && ! -f switch_build/.isaac_hud_generated ]]; then
    echo 'Cartella switch_build preesistente e non generata da questo progetto: non sovrascrivo.' >&2
    exit 1
fi
mkdir -p switch_build/source switch_build/include/isaac switch_build/libs/libtesla/include
: > switch_build/.isaac_hud_generated
cp third_party/Tesla-Template/Makefile switch_build/Makefile
cp third_party/Tesla-Template/LICENSE switch_build/LICENSE
cp third_party/libtesla/include/tesla.hpp third_party/libtesla/include/stb_truetype.h switch_build/libs/libtesla/include/
cp third_party/libtesla/LICENSE switch_build/libs/libtesla/LICENSE
cp include/isaac/core.hpp include/isaac/descriptions.hpp include/isaac/catalog_data.hpp include/isaac/pills.hpp include/isaac/hud.hpp include/isaac/hud_layout.hpp include/isaac/hud_controls.hpp switch_build/include/isaac/
cp core/core.cpp switch_build/source/isaac_core.cpp
cp native/hud_main.cpp switch_build/source/main.cpp
cp native/dmnt_memory.cpp switch_build/source/dmnt_memory.cpp
cp native/dmnt_memory.hpp switch_build/include/dmnt_memory.hpp
cp third_party/Atmosphere/dmnt/dmntcht.os.horizon.c switch_build/source/dmntcht.c
cp third_party/Atmosphere/dmnt/dmntcht.h switch_build/include/dmntcht.h
cp third_party/Atmosphere/dmnt/service_guard.h switch_build/include/service_guard.h
python3 - <<'PY_PATCH'
from pathlib import Path
import re
p=Path('switch_build/source/dmntcht.c')
s=p.read_text(encoding='utf-8')
needle='#include "../service_guard.h"'
assert s.count(needle)==1, 'Include del client dmnt inatteso'
patched = s.replace(needle, '#include "service_guard.h"')
notice = (
    '// Modified from Atmosphere for Isaac HUD v0.5.1 '
    '(2026-10-19): service_guard.h include path adapted '
    'for local build.\n'
    '// Original copyright and license notices retained below.\n'
)
p.write_text(notice + patched, encoding='utf-8')
p=Path('switch_build/Makefile');s=p.read_text(encoding='utf-8')
for field,value in [('TARGET','IsaacHUD'),('APP_TITLE','Isaac HUD Automatico'),('APP_VERSION','0.5.1')]:
    s,n=re.subn(r'(?m)^'+field+r'\s*:?=.*$',field+' := '+value,s)
    if n!=1:raise SystemExit('Template incompatibile: '+field)
s,n=re.subn(r'(?m)^CXXFLAGS\s*:=.*$', 'CXXFLAGS := $(CFLAGS) -std=gnu++20 -fexceptions',s)
if n!=1:raise SystemExit('Template incompatibile: CXXFLAGS')
p.write_text(s,encoding='utf-8')
PY_PATCH
cat > switch_build/DEPENDENCY_REVISIONS.txt <<'EOF'
Tesla-Template: 241558db2dc009a213d784d291b2547f1f148ef2
libtesla: e06d42503dd0717253c77734bd46f3c1addc3f9e
Atmosphere: 36cc9a9f490da37dd1d5f958ee9a256be132cc1d
Materiale vendorizzato, hashes: third_party/SHA256SUMS.json
Modifica dmnt: solo relocation di #include service_guard.h
HUD runtime adattato separatamente tramite scripts/prepare_hud_runtime.py
EOF
echo 'Preparazione dei sorgenti Switch completata.'
