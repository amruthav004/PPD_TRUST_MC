# Reproducibility notes

## Source and execution

The clean notebook retains every source cell from the uploaded file. Saved
output images, logs, execution counts and widget state have been removed.
The uploaded file's SHA-256 and original cell execution metadata are recorded
in `metadata/notebook_provenance.json`. Later analysis/export cells have no
saved outputs in the upload; their presence in code is not evidence of completion.
This supplementary package was checked structurally. Training, authentication,
model downloads and complete notebook execution were not repeated.

## Dependencies and runtime

Python 3.12, GPU acceleration and Colab T4 appear in source metadata.
`tabpfn>=8.1,<9` is the only explicit installation version range in the source.
Other requirements are unpinned because their original runtime versions are
not recorded. This is not an exact environment lockfile. Capture versions after
installation using the included utility. The tabicl checkpoint name is pinned
in configuration. GPU availability, library changes and numerical behavior can
change outputs even when random seeds agree.

## Validation details

Five repeats of stratified five-fold outer evaluation produce participant-level
averaged OOF probabilities. Inner expert fitting uses three folds; calibration
uses five meta folds. Bootstrap intervals resample participants within class.
The paired comparison adjusts empirical AUPRC p-values with Holm's method.
Reliability sensitivity and coverage settings are selection targets, not
established achieved values. The selection routine has explicit fallback rules.

The source builds class-conditional quantiles from inner OOF probabilities
used elsewhere during model selection. A separate untouched split-conformal
calibration set is not constructed. Nominal alpha values must not be reported
as evidence of achieved coverage. Empirical coverage requires the actual run.

The reported threshold metrics use an additional cross-fit of participant-
averaged OOF probabilities. This differs from `PPDTrustMC.predict`, which uses
an internal Youden threshold. Do not mix the two threshold definitions.

## Checkpoints and modifications

Use a new result directory after changing data values, endpoints or methods.
The source CV cache signature includes model parameters, dimensions, column
names and positive count, but not a complete hash of data values. Comparator
exceptions are logged; jobs enter the source `done` set even after failure.
Inspect errors and OOF counts before treating a run as complete.

Some constants, including PHQ2_CUTOFF and EARLY_MONTH_MIN/MAX, are retained
from the source but do not implement a primary-cohort restriction in Stage 2.
The external harmonization block fills medians before its internal five-fold
reference evaluation. The package preserves this behavior and does not add
further claims about leakage control. See DATA_ACCESS.md for endpoint and
harmonization constraints.

## Scope of configuration utility

The prepared notebook changes configuration loading and path handling, not
the source method bodies. The verification script checks clean-source hashes
and package checksums. It does not establish predictive reproducibility or
test all third-party library API combinations. Baseline constructors remain
source-defined. No raw data, predictions or trained arrays are fabricated.
