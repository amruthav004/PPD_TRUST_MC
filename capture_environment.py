"""Record installed runtime versions without training or importing model packages."""
import argparse
import importlib.metadata as metadata
import json
import platform
from pathlib import Path

PACKAGES=['numpy','pandas','scipy','scikit-learn','torch','matplotlib','tabpfn',
          'tabicl','xgboost','pytorch-tabnet','shap','statsmodels','ipython',
          'jupyterlab','nbformat','nbclient','ipykernel']
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',default='runtime_environment.json')
args=ap.parse_args()
versions={}
for name in PACKAGES:
    try: versions[name]=metadata.version(name)
    except metadata.PackageNotFoundError: versions[name]=None
result={'python':platform.python_version(),'platform':platform.platform(),
        'packages':versions,'note':'Captured from the invoking runtime, not the uploaded notebook runtime.'}
p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(f'Wrote {p}')
