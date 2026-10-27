# Evaluation results — provenance and interpretation

## Sources of the figures

1. `results/recorded_original_metrics.csv` contains values present in the original project ZIP. The code and hold-out predictions underlying this file were **not supplied**, so treat it as historical self-recorded evidence, not a verified test of the shipped model.
2. `evaluation/reproduce_evaluation.py` and `evaluation/reference_results/` describe an **independently retrained** classifier. The script read `data/processed/phishing_url_features_v2.csv` and did **not** load or execute the uploaded pickle model.
3. A different project figure (47,142-case confusion matrix and approximately 99.80% accuracy) was present in the earlier working material. It appears to be a *different experimental setup*, so it was deliberately not bundled as if it belonged to the 6,100-case reconstruction.
4. The two original `.ipynb` notebook entries in the uploaded archive were **empty (0 bytes)**. They are omitted here; the reconstruction is **not** their restoration.

## Previously reproduced new-model results

| Metric | Independent reconstruction |
|---|---:|
| Cleaned, unique-feature examples | 30,500 |
| Class counts (0 = phishing / 1 = legitimate) | 29,634 / 866 |
| Stratified training / testing | 24,400 / 6,100 |
| Accuracy | 0.9993442623 |
| Balanced accuracy | 0.9996625612 |
| Phishing-class F1 | 0.9996624473 |
| ROC–AUC (phishing positive) | 0.9998342064 |
| Errors | 4 |

Confusion matrix (actual rows, predicted columns, class order `[0,1]`):

```text
                 Predicted 0   Predicted 1
Actual 0            5923             4
Actual 1               0           173
```

**Interpretation:** This internal feature-pattern-level stratified holdout remains dataset-specific; it is not a chronological split, website-domain-separated holdout, independent source dataset or deployment evaluation. The exceptionally rare legitimate examples after cleaning make distribution shift a serious limitation. Some unfamiliar legitimate URLs were misclassified during purposive manual testing, which must not be hidden or presented as a representative measurement.

**Critical limitation:** The source (recorded original model metrics) and new-model reconstruction *happen to be numerically consistent* but this does not prove the deployed model is identical or establish original training provenance. A marker would need the original training code, metadata and model artefact generation evidence to confirm that stronger claim.

## Running the reconstruction

```sh
python evaluation/reproduce_evaluation.py --input data/processed/phishing_url_features_v2.csv --output evaluation/generated
```

This writes new holdout predictions, metrics and charts to `evaluation/generated/`, separate from the preserved reference outputs. Dependence versions may affect exact determinism. Do not alter or overwrite the original `reference_results`.
