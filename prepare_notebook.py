"""Create a configured notebook without executing training or importing models."""
import argparse
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config', default='config/config.json')
    ap.add_argument('--output', default='notebooks/PPD_TRUST_MC_configured.ipynb')
    args = ap.parse_args()
    cp = Path(args.config)
    cp = cp if cp.is_absolute() else ROOT / cp
    cfg = json.loads(cp.read_text(encoding='utf-8'))
    nb = json.loads((ROOT / 'notebooks/PPD_TRUST_MC.ipynb').read_text(encoding='utf-8'))
    g = cfg['globals']
    for key in ['OUTER_FOLDS','OUTER_REPEATS','INNER_FOLDS','META_FOLDS','N_BOOT']:
        if type(g[key]) is not int or g[key] < (2 if 'FOLDS' in key else 1):
            raise ValueError(f'Invalid {key}')
    for key in ['alpha_negative','alpha_positive']:
        if not 0 < cfg['model_parameters'][key] < 1:
            raise ValueError(f'Invalid {key}')
    def path(value):
        p = Path(value).expanduser()
        return str(p.resolve() if p.is_absolute() else (ROOT / p).resolve())
    s = ''.join(nb['cells'][2]['source'])
    start = s.index('# Results + checkpoints on Google Drive')
    end = s.index('MANUSCRIPT_RUN = True',start)
    s = s[:start] + 'RESULT_DIR = Path(' + repr(path(cfg['output']['result_dir'])) + ')\nRESULT_DIR.mkdir(parents=True, exist_ok=True)\n\n' + s[end:]
    pos = s.index('from getpass import getpass')
    overrides = '\n# Supplementary configuration overrides\n'
    for key,value in g.items():
        if not key.isidentifier() or not key.isupper():
            raise ValueError(f'Invalid configuration variable: {key}')
        overrides += f'{key} = {value!r}\n'
    overrides += "TABICL_BATCH_SIZE = TABICL_BATCH_SIZE if DEVICE == 'cuda' else 2\n"
    overrides += "np.random.seed(RANDOM_STATE)\nrandom.seed(RANDOM_STATE)\ntorch.manual_seed(RANDOM_STATE)\nif torch.cuda.is_available():\n    torch.cuda.manual_seed_all(RANDOM_STATE)\n\n"
    s=s[:pos]+overrides+s[pos:]
    nb['cells'][2]['source']=s.splitlines(keepends=True)
    s=''.join(nb['cells'][4]['source'])
    start=s.index("if not Path('/content/gdrive/MyDrive').exists():")
    end=s.index('df = pd.read_csv(PRIMARY_PATH',start)
    replacement = (
        'PRIMARY_PATH = Path(' + repr(path(cfg['data']['primary_csv'])) + ')\n'
        'NATIONAL_PATH = Path(' + repr(path(cfg['data']['external_tab'])) + ')\n'
        'if not PRIMARY_PATH.is_file():\n    raise FileNotFoundError(str(PRIMARY_PATH))\n'
        'if not NATIONAL_PATH.is_file():\n    NATIONAL_PATH = None\n\n'
    )
    nb['cells'][4]['source']=(s[:start]+replacement+s[end:]).splitlines(keepends=True)
    s=''.join(nb['cells'][6]['source'])
    s=s.replace('DROP_PROXIMAL_AFFECT = False',f"DROP_PROXIMAL_AFFECT = {cfg['drop_proximal_affect']!r}")
    nb['cells'][6]['source']=s.splitlines(keepends=True)
    s=''.join(nb['cells'][14]['source'])
    anchor='    parameters.update(kwargs)'
    if anchor not in s: raise RuntimeError('Factory anchor missing')
    s=s.replace(anchor,'    parameters.update('+repr(cfg['model_parameters'])+')\n'+anchor,1)
    # Keep the caller's seed; factory is also used by repeated evaluations.
    s=s.replace(anchor,"    parameters['random_state'] = rs\n"+anchor,1)
    nb['cells'][14]['source']=s.splitlines(keepends=True)
    nb['metadata']['supplementary_config']=cfg
    for cell in nb['cells']:
        if cell['cell_type']=='code':
            code=''.join(cell['source'])
            ast.parse('\n'.join(line for line in code.splitlines() if not line.startswith('%')))
    output=Path(args.output)
    output=output if output.is_absolute() else ROOT/output
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(nb,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Prepared {output}')
    print('Training was not executed. Open this notebook and run cells in order.')

if __name__=='__main__': main()
