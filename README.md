# PPD-TRUST-MC supplementary package

This package accompanies the uploaded PPD-TRUST-MC notebook. It contains
configuration files, dependency declarations, data specifications, method
metadata and utilities for preparing a configured notebook. Values are taken
from the notebook source. No new model evaluation was performed.

## Contents

- `config/config.json`: canonical manuscript configuration used by the helper.
- `config/config.yaml`: equivalent YAML copy for inspection.
- `config/comparator_parameters.json`: comparator constructor settings with epoch overrides.
- `metadata/`: dataset schema, named-field dictionary, validation protocol,
  architecture model card, source provenance and expected output names.
- `notebooks/PPD_TRUST_MC.ipynb`: original code with saved outputs removed.
- `scripts/prepare_notebook.py`: creates a local-path notebook using the JSON config.
- `scripts/verify_package.py`: checks checksums, JSON and unchanged source cells.
- `scripts/capture_environment.py`: records package versions from the runtime used.
- `requirements.txt` and `environment.yml`: dependency setup.

## Run preparation

Open a terminal in this package directory. Python 3.12 matches the source
notebook metadata. Install dependencies in a dedicated environment:

```bash
python -m venv .venv
# Activate the environment using the command appropriate for your shell.
python -m pip install -r requirements.txt
python scripts/verify_package.py
```

Put the primary CSV in `data/`, and optionally add the external TAB file.
Prepare a notebook with local paths:

```bash
python scripts/prepare_notebook.py --config config/config.json --output notebooks/PPD_TRUST_MC_configured.ipynb
python scripts/capture_environment.py --output runtime_environment.json
jupyter lab notebooks/PPD_TRUST_MC_configured.ipynb
```

Run notebook cells in order. TabPFN authentication and model-license acceptance
follow the notebook's interactive flow. The helper does not store credentials.
CUDA is selected when available; CPU execution uses a TabICL batch size of two.
The manuscript profile uses five outer repeats of five folds and includes
deep comparators, ablations and stress tests, so it requires substantial compute.

## Configuration behavior

The source notebook does not read external JSON or YAML. The preparation helper
inserts JSON settings after the source constants, configures the factory model
parameters, replaces the Colab-specific data-path block and sets the result
directory. Statistical and predictive method bodies are retained. Paths are
resolved against the package root, not the notebook working directory.
Run preparation again after changing `config/config.json`.

YAML is a reference copy and is not loaded by the helper. Changing
`MANUSCRIPT_RUN` alone does not recalculate the explicit derived settings in
JSON. Set repeat counts, bootstrap count, epoch budgets and stress seeds
directly. `TABICL_BATCH_SIZE` is four for CUDA and two for CPU. Parameters in
`comparator_parameters.json` are documentation; comparator settings remain in
the notebook source. Model-factory parameters in `config.json` are applied.

## Evidence boundaries

The architecture uses TabPFN-3 full and stable-core experts plus XGBoost.
The default consensus also includes a counterfactual median contribution.
Calibration is conditional logistic calibration on logits. It is not isotonic
calibration. Learned thresholds, conformal quantiles, fitted weights and raw
datasets are not included. No placeholder model weights or participant arrays
have been created. Tables and figure files are not included.

Refer to `REPRODUCIBILITY.md` before interpreting a rerun and `DATA_ACCESS.md`
for input and harmonization requirements. The source notebook's Stage 20
creates result files after execution; their names are recorded in metadata.
