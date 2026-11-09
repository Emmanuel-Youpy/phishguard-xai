# Dataset attribution, third-party software and AI-assisted work

**Status: factual repository notice and student-review draft; not a UWE ethics decision or approval of AI use.**  
**Documentation reviewed:** 9 November 2026.

## 1. Dataset source and licence

The project's processed file `data/processed/phishing_url_features_v2.csv` is described in the project development materials as derived from the **PhiUSIIL Phishing URL Dataset** by **Arvind Prasad and Shalini Chandra**. The original research data are published on Mendeley Data as version 2:

> Prasad, A. and Chandra, S. (2023) *PhiUSIIL Phishing URL Dataset* [Dataset]. Version 2. Mendeley Data. Available from: https://doi.org/10.17632/shwpxscxy2.2

The published dataset's licence is **Creative Commons Attribution 4.0 International (CC BY 4.0)**: https://creativecommons.org/licenses/by/4.0/. This licence permits sharing and adaptation subject to the licence conditions, including credit, a link to the licence and indication of changes. See the publisher's record: https://data.mendeley.com/datasets/shwpxscxy2/2.

**Changes described by this project:** a derived numeric dataset of 20 URL-lexical features and a classification label was created for the phishing-detection prototype. The separate reproducible evaluation script subsequently deduplicates identical feature patterns and excludes patterns with conflicting labels. The repository **does not contain the original raw URL/content dataset**. This summary is based on surviving project records; it is not an independent reconstruction of every original preprocessing decision. **The adapted dataset should be attributed to the original authors; the 20-feature extraction and evaluation changes must not be presented as the authors' own work.**

**Associated paper:** Prasad, A. and Chandra, S. (2024) 'PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning', *Computers & Security*. Available from: https://doi.org/10.1016/j.cose.2023.103545.

## 2. Third-party libraries and intellectual property

The code imports third-party packages, including Streamlit, scikit-learn, SHAP, LIME, pandas, NumPy, SciPy, Matplotlib and joblib. These frameworks, algorithms and external packages are **not** original code written for this project; their software licence terms remain separate from the source dataset's CC BY 4.0 licence. Consult `requirements.txt` for dependencies and the academic report for citations to relevant research.

**No licence for this whole source-code repository is granted by this notice.** Public GitHub visibility does not mean that every file is licensed under CC BY 4.0. If an open-source software licence is considered later, assess code ownership and any adapted third-party code first. Avoid committing secrets, private university correspondence, or unredacted personal data.

## 3. Record of generative-AI assistance — subject to student verification

The student's project development record includes **OpenAI ChatGPT** assistance with some coding, testing, documentation and academic writing. The following is a traceable *working account*, not a claim of full authorship by either party:

| Component | AI contribution described in development records | Clarification |
| --- | --- | --- |
| `app/app.py` | Suggested/revised URL validation and LIME display integration | An application file existed in the earlier student project. The degree of independent human modification of other portions has not been established. |
| `src/url_validation.py` | Generated/refined URL validation helper | Its behaviour was tested, but code-testing alone is not proof of permitted AI use. |
| `src/lime_formatting.py` | Generated/refined LIME condition-formatting logic | Formatting defect was corrected and visually retested. |
| `tests/test_app_logic.py` | Generated/refined automated regression tests | 14 tests were subsequently reported passing. |
| `evaluation/reproduce_evaluation.py` | Produced an **independent** evaluation reconstruction | Trained a *new* classifier; not the lost original model-training notebook or a verified evaluation of the shipped pickle. |
| `README.md`, repository packaging and supporting guidance | AI-assisted documentation and organisation | Human review and correction required. |
| MSc report (separate submission) | Substantial AI-assisted drafting and editing | This extends beyond simple proofreading; formal assessment permissibility and any disclosure must be checked with the supervisor. |

**What this acknowledgement does not do:** it does not certify that all assistance was permitted under the module assessment brief, prove independent authorship of any file, or make AI-generated report prose safe to submit unchanged. The student must independently check the code and academic claims, correct this account where incomplete and seek module-specific guidance before submitting coursework. Other code sources or AI tools, if any, should also be documented honestly.

The **UFCF9Y-60-M Artefact and Report assessment specification (2025–26), Section 6.4**, describes permitted AI support for *clarity of reporting* and warns not to copy/paste generated responses into the assignment. That wording should **not** be interpreted as blanket approval for substantive AI-authored code or report sections. UWE's general AI guidance also advises students to consult their tutor when assignment-specific permission is unclear: https://www.uwe.ac.uk/study/study-support/study-skills/using-generative-ai-at-uwe-bristol.

**Action before submission:** Ask the module supervisor what disclosures and independent revision are required for this particular level of AI assistance. Keep a truthful record of prompts, changes and checks as the university directs.

## 4. Model provenance and safe use

The shipped `models/phishing_detector_final.pkl` was supplied as a pre-existing project artefact. Its original training notebooks were empty in the supplied archive. The reproducible evaluation code trained another classifier; its excellent internal hold-out metrics **must not** be attributed as independently verified performance of the shipped pickle. See `docs/EVALUATION_PROVENANCE.md`.

The prototype predicts patterns in URL text and **cannot certify a URL as safe**. SHAP/LIME explain aspects of a model prediction, not whether the model is correct. Loading untrusted Python pickle objects can execute code; use only trusted artefacts.
