# Evidence register (supervisor/marker guide)

| Claim / test | Evidence | What it can demonstrate |
|---|---|---|
| URL and feature logic | `src/feature_extraction.py`, `src/url_validation.py` | Code-level feature/validation implementation |
| LIME condition direction repair | `src/lime_formatting.py`, `tests/test_app_logic.py` | Regression test coverage for inequality formatting |
| Automated tests | `tests/test_app_logic.py` plus user's 25 Oct 2026 terminal screenshot | 14 offline tests passed in local installation; **not a model performance test** |
| TC03 empty URL | `evidence/functional_tests/TC03_empty_URL.png` | Application showed the expected warning in live session |
| TC05 unsupported scheme | `evidence/functional_tests/TC05_unsupported_scheme.png` | Live app rejected `ftp://example.com` |
| TC07 LIME chart/table | `evidence/functional_tests/TC07_LIME_*` | Chart and table had consistent feature labels, signs and inequality direction in a tested case |
| 20-feature model input | `src/feature_extraction.py` and `data/processed/phishing_url_features_v2.csv` | Feature definitions and data schema |
| Reconstructed internal metrics | `evaluation/reproduce_evaluation.py` and `evaluation/reference_results/*` | A new classifier with auditable hold-out predictions |
| Deployed model original training provenance | **Not in supplied artefacts** | Must not be claimed as verified |
| Manual false positives on unfamiliar legitimate URLs | Previously documented 10/28; full trial record not in supplied ZIP | Illustrative, non-representative limitation only |

This is an internal evidence map, **not a history of every report draft**. Align with the corresponding version of the academic report and its figure numbering before final submission.
