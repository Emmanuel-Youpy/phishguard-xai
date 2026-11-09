# Dataset attribution and code rights

## Dataset provenance and public-repository notice

The processed numeric table `data/processed/phishing_url_features_v2.csv` is described in the development record as a derivative of the **PhiUSIIL Phishing URL Dataset** by **Arvind Prasad and Shalini Chandra**. The dataset is published under **CC BY 4.0**:

- **Source data:** Prasad, A. and Chandra, S. (2023) *PhiUSIIL Phishing URL Dataset*, Version 2, Mendeley Data. https://doi.org/10.17632/shwpxscxy2.2
- **Source licence:** Creative Commons Attribution 4.0 International. https://creativecommons.org/licenses/by/4.0/
- **Associated research article:** https://doi.org/10.1016/j.cose.2023.103545

The derivative file contains a numeric 20-feature representation and labels instead of the source's raw URL/web-content columns. The separate evaluation script deduplicates repeated feature vectors and excludes patterns with contradictory labels. These are project-level modifications, not changes made by the original dataset authors. The detailed original data-preparation history has not been independently reconstructed.

A public repository containing adapted CC BY material should preserve credit, the licence link and a meaningful indication of changes. **The dataset licence does not automatically license the full repository's software, model, screenshots or documentation.**

## Code, AI assistance and research integrity

The application relies on third-party Python packages with their own licences. A working inventory of generative-AI-assisted coding, documentation and report drafting is provided in [`AI_ASSISTANCE_AND_THIRD_PARTY_CREDITS.md`](AI_ASSISTANCE_AND_THIRD_PARTY_CREDITS.md). It is a **draft for student verification and supervisor discussion**, not a declaration that UWE approved those activities. The module brief's permitted AI support is narrower than a blanket permission to submit AI-authored work. The student must confirm the assessment requirements and be able to explain their own contributions.

No single copyright or software licence is asserted over the entire codebase by preparing this repository. Check for credentials, third-party code, personal data and redistribution restrictions before adding new files to this public repository.

## Research safety

This prototype does not establish whether a live website is safe. Its numerical scores and SHAP/LIME explanations should be interpreted as exploratory research outputs. Do not execute untrusted `.pkl`/`.joblib` artefacts because unpickling can execute arbitrary code.
