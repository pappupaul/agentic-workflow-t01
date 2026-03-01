# Agentic Workflow Demo Pipeline

This folder contains two demo pipelines that show how an "agentic" workflow can help developers:

1) Auto lint + run tests
- Purpose: Show automated quality checks and feedback loops.
- Script: `demos/auto_lint_and_test.py`
- Run: `python demos/auto_lint_and_test.py`

2) Feature-from-issue patching
- Purpose: Show how an agent can convert a plain-language issue into a concrete code change and apply it safely.
- Script: `demos/feature_from_issue.py`
- Preview: `python demos/feature_from_issue.py`
- Apply change: `python demos/feature_from_issue.py --apply`

Notes:
- Both demos are intentionally simple and safe. The feature-from-issue script makes a backup before modifying `app.py`.
- Install dependencies from `requirements.txt` before running: `pip install -r requirements.txt`.
