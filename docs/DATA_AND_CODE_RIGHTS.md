# Data, attribution and redistribution precautions

**Original research dataset:** The student's project cites the PhiUSIIL phishing-URL dataset and the published research by Prasad and Chandra (2024), *Computers & Security*, DOI `10.1016/j.cose.2023.103545` (bibliographic details should be checked against publisher records at submission).

The repository candidate contains a **processed numeric feature dataset** without raw URL strings, because the app's SHAP/LIME background routines and evaluation reconstruction read this specific file. It does not contain the much larger original raw dataset or `verified_online.csv`. The dataset's licence and redistribution permission have **not** been independently verified in this packaging step. Do not make the project repository public until permission is confirmed.

The student must review source-code authorship, third-party components and any AI-assisted contributions against UWE's academic integrity rules, make accurate attributions, and check whether a disclosure is required. No copyright or licence for the student's entire codebase is asserted by this packaging step.

**Safety:** This system is for research/demonstration only. It must not be used to decide that a URL is safe for users. Never load untrusted `.pkl`/`.joblib` models or place service credentials in a public repository.
