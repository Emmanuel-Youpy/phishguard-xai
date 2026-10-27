# PhishGuard XAI — MSc project artefact (repository candidate)

**Project:** An Explainable Machine Learning Framework for Phishing URL Detection  
**Application:** PhishGuard XAI (Streamlit / Python)  
**Module:** UFCF9Y-60-M, UWE Bristol  
**Build assembled:** 27 October 2026

## What this package does

An interactive research prototype accepts an HTTP/HTTPS URL, extracts 20 lexical features, applies a **saved Histogram-Based Gradient Boosting** phishing URL classifier and displays model predictions, probability values and **SHAP/LIME** feature explanations. The two classes are **0 = phishing** and **1 = legitimate**.

The application analyses URL text; it does **not** establish that a site is safe, does not inspect web content and is **not a production security service**. A prediction or explanation is not proof of a URL's true status.

## File map

```text
app/                         Streamlit application, styling
src/                         Lexical feature extraction, validation, LIME formatting
models/                      Saved inference model and feature-column order
data/processed/               20-feature CSV used for SHAP/LIME background and evaluation
 tests/                       14 offline regression tests
evaluation/                   Independent, reproducible evaluation script and saved evidence
results/                      Originally recorded metrics (not reattributed to the deployed model)
evidence/functional_tests/   Cropped live application screenshots and status matrix
docs/                         Provenance, data rights, submission and evidence guides
```

## Windows setup and launch

1. Download/extract this package into a separate folder (do **not** overwrite the backup of your original project).
2. Open the extracted folder in VS Code and open Terminal → New Terminal.
3. Create a virtual environment and install dependencies:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `py -3.14` is not available, use a compatible installed Python version, e.g. `python -m venv .venv`, and check dependency support. The user's functioning environment was **Python 3.14.6**; these dependencies were recorded from the user's earlier project ZIP.

4. Run the 14 offline tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_app_logic.py -v
```

5. Start the application:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app\app.py
```

Then open the local address Streamlit displays, usually `http://localhost:8501`. Python packages and port availability depend on your machine. The `app/` directory is the live implementation; redundant `app2/` was **not** distributed.

## Independent evaluation reconstruction

The original two notebooks provided with the project ZIP were **0-byte empty files**, so this package deliberately does not pretend they are usable training evidence. An independently written reconstruction is provided instead:

```powershell
.\.venv\Scripts\python.exe evaluation\reproduce_evaluation.py --input data\processed\phishing_url_features_v2.csv --output evaluation\generated
```

This script trains a **new** classifier using a documented procedure: deduplicate by 20 lexical-feature patterns, discard patterns with conflicting labels, 80:20 stratified split (`random_state=42`), class-weighted Histogram-Based Gradient Boosting. The 30,500-row modelling dataset is *extremely imbalanced* (29,634 phishing, 866 legitimate). Previously reproduced hold-out accuracy was **0.999344**, over **6,100** test patterns with **4** errors; see `evaluation/reference_results/` for original output and `docs/EVALUATION_PROVENANCE.md` for crucial limitations.

**Do not attribute these reconstructed scores to the shipped inference pickle unless model provenance is established.** An unrelated supplied 47,142-case confusion matrix was not reconciled with this experiment and has intentionally been omitted from this coherent repository candidate.

## What was tested

The user supplied VS Code evidence showing **14/14 regression tests passed** (25 October 2026). Subsequent live screenshots (26 October 2026) support **TC03**, **TC05** and the LIME **display/formatting** check **TC07**. These tests do **not** validate the deployed model's predictive quality on new data. See `evidence/functional_tests/test_status_summary.csv` and `docs/EVIDENCE_INDEX.md`.

## Key research limitations

- The modelling dataset is highly class-imbalanced *after feature-pattern cleaning*; internal accuracy is not a guarantee of reliable real-world phishing detection.
- A previous *small and purposively chosen* check classified only 10/28 legitimate URL examples correctly. Its complete underlying record was not included in the originally supplied ZIP; it is not a representative external performance measure.
- SHAP and LIME are explanations of model behaviour, not proof of correct prediction or causal importance.
- The deployed pickle's original training notebook and exact lineage remain unavailable in the supplied materials.

## Source, safety and sharing

The application and model files originate from the student's supplied project and a tested correction package; the independent evaluation and some helper refactoring were produced with AI assistance. Review and attribute all work honestly in accordance with your assessment's generative-AI policy. The original dataset was described as **PhiUSIIL**; confirm permission before publicly redistributing any dataset or third-party material. **Keep the repository private until permissions and university submission access requirements are resolved.**

The saved `.pkl` model and feature list are Python pickle/joblib objects. **Loading pickles can execute arbitrary code.** Only run files from a trusted source in an isolated environment. The provided checksum manifest verifies file consistency, **not model safety**.

No actual browsing of candidate phishing domains is required to test the app's URL feature pipeline.

See `docs/SUBMISSION_CHECKLIST.md` for report filename and Blackboard repository-link instructions.
