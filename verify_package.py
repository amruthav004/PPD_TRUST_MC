"""Check immutable package files and clean notebook source hashes."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
for item in manifest['files']:
    p=ROOT/item['path']
    if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
        raise SystemExit(f'Checksum mismatch: {p}')
for p in ROOT.rglob('*.json'):
    json.loads(p.read_text(encoding='utf-8'))
cfg=json.loads((ROOT/'config/config.json').read_text(encoding='utf-8'))
assert cfg['globals']['TABPFN_CORE_ESTIMATORS']==cfg['model_parameters']['core_estimators']
nb=json.loads((ROOT/'notebooks/PPD_TRUST_MC.ipynb').read_text(encoding='utf-8'))
hashes=manifest['clean_source_sha256_by_cell']
for i,c in enumerate(nb['cells']):
    source=''.join(c['source'])
    assert hashlib.sha256(source.encode()).hexdigest()==hashes[str(i)], f'Source changed: cell {i}'
    if c['cell_type']=='code':
        assert not c['outputs'] and c['execution_count'] is None
        ast.parse('\n'.join(x for x in source.splitlines() if not x.startswith('%')))
print(f"PASS: {len(manifest['files'])} file checksums, JSON documents and {len(nb['cells'])} source cells.")
print('This structural check does not execute model training.')
