# Agentic Workflow Demo

This repository includes two small demo pipelines that illustrate how an agentic workflow can help a developer:

**Demos**
- `demos/auto_lint_and_test.py`: Runs linting (`flake8`) and tests (`pytest`) to show automated quality checks.
- `demos/feature_from_issue.py`: Converts a plain-language issue into a concrete code change and can (optionally) apply the patch to `app.py` (creates a `.bak` backup).

**Setup**
Install dependencies:

```bash
pip install -r requirements.txt
```

**Run demos**

Lint + tests:

```bash
python demos/auto_lint_and_test.py
```

Feature-from-issue (preview):

```bash
python demos/feature_from_issue.py
```

Feature-from-issue (apply change):

```bash
python demos/feature_from_issue.py --apply
```

---

### GitHub Actions pipeline

This repository includes a simple GitHub Actions workflow located at
`.github/workflows/demo.yml` that exercises the same two use cases:

1. **Lint & test** job runs `flake8` and `pytest` on every push/PR.
2. **Issue‑to‑patch** job runs the `feature_from_issue.py` script, first
   previewing and then applying the generated patch, and finally outputs a
diff of `app.py`.

You can see the workflow results on GitHub by opening the _Actions_ tab for
this repo or by creating a pull request against `main`.

**Notes for the demo presentation**
- Walk through the issue text, planned steps, and preview before applying.
- Show how the lint/test pipeline provides fast feedback to the developer.
- Both scripts are safe and intentionally minimal — adapt to your audience.
