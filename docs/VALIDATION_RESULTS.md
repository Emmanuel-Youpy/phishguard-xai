# Packaging validation performed on repository candidate — 27 October 2026

## Checks actually executed

- `python -m pytest tests/test_app_logic.py -v`: **14 passed**, no failures. See `evidence/functional_tests/packaged_offline_pytest_output.txt`.
- The five included `.py` source modules were parsed successfully with Python AST (syntax sanity check).
- Independently executed `evaluation/reproduce_evaluation.py` against the copied processed features CSV. The run returned **30,500 cleaned patterns**, split into **24,400 training** and **6,100 test** cases, with **0.999344262295082** hold-out accuracy, and confusion matrix `[[5923,4],[0,173]]`.
- The copied data SHA-256 matched the hash documented by the previous reconstruction: `a829c695ba38497407b83a2c9306576e9bfcbae234a0f0ec3c36877c328c2966`.
- Original model pickle bytes were copied unchanged from the student's uploaded ZIP. **They were not loaded or re-executed in this packaging review.**

## Scope of these checks

This establishes a reproducible **new-model reconstruction**, a consistent packaged feature dataset, and offline helper tests. It does **not** prove that the saved deployed model matches the new model, that every live UI screen works on a marker's computer, or that unknown-site phishing detection is dependable.

The user's earlier screenshots separately document that the corrected app started successfully and that TC03, TC05 and TC07 passed their specified manual UI display checks. Package provenance and details are in `docs/EVALUATION_PROVENANCE.md`.
