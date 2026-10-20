# Data access and endpoint definitions

The primary file is `PPD_dataset_v2.csv`, described in the source as a Bangladesh
cohort. The saved loading message reports 800 rows and 51 columns before target
filtering. Rows with nonnumeric or missing PHQ-9 scores are removed. The primary
label is PHQ-9 >=10. EPDS >=13 is evaluated using predictions from the
PHQ-9-trained model, rather than by training an independent EPDS model.

`sr`, PHQ-9 and EPDS score/result columns are removed from predictors. Three
proximal affect fields remain under the default configuration. Set
`drop_proximal_affect` to true and prepare a new notebook to remove them.
The source converts missing EPDS scores to the negative class through its
Boolean comparison; confirm data completeness before interpreting that endpoint.

The optional external file is LTM III national, described as a US cohort. Its
endpoint uses `Depression_Screener_S`: codes 1 and 2 are retained and code 2 is
positive. Only eight demographic/obstetric variables are harmonized. The source
explicitly requires checking one-hot level meanings against the LTM codebook.
Some absent or undecodable external fields pass through `np.where` and become
fixed categories. Inspect mappings and missingness before interpreting transport.

The external evaluation concerns a different endpoint and population, using a
reduced feature set. It does not evaluate direct transfer of the full predictor
model. Data source URLs, complete raw-data codebooks and redistribution terms
are not included in the upload. This package does not grant dataset access.
