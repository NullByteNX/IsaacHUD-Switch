#!/usr/bin/env python3
"""Check repository contents, catalog structure and dependency checksums."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
prohibited=['catalog/wiki_repentance.json','catalog/catalog_it.json']
for item in prohibited:
    assert not (root/item).exists(), f"Unwanted wiki dataset present: {item}"
index=json.loads((root/'catalog/id_names.json').read_text(encoding='utf-8'))
assert len(index['entries'])==1004 and len(index['pills'])==50
for kind in ('entries','pills'):
    for e in index[kind]:
        assert set(e)==({'id','name','variant'} if kind=='entries' else {'id','name'}),f"Unexpected fields in {kind}"
for rel in ['catalog/ATTRIBUZIONE.md','LICENSES/CC-BY-SA-4.0.txt','LICENSES/ISC-libnx.txt','NOTICE.md','LICENSE','third_party/SHA256SUMS.json']:
    assert (root/rel).is_file(),f"Missing required repository file: {rel}"
checks=json.loads((root/'third_party/SHA256SUMS.json').read_text(encoding='utf-8'))['files']
for rel, expected in checks.items():
    assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==expected,f"Dependency changed: {rel}"
print('Repository technical checks: PASS')
