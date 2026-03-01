# Agentic Workflow Demo

This repository now demonstrates a simple **daily status report workflow**
using GitHub Actions.

### Purpose
The scheduled workflow collects repository activity—new issues, merged pull
requests, and any open blockers—and creates or updates a single "Daily Status"
issue containing the summary. It runs every 24 hours (UTC) and can also be
triggered manually from the Actions tab.

### Setup & usage
No special dependencies are required beyond the GitHub Actions runner. A
recent `requirements.txt` only lists Flask because the application remains a
minimal web service; no linting/test support is needed for the workflow.

You can inspect the workflow file at `.github/workflows/daily_status.yml`.

### README auto-update workflow
A second agentic workflow (`.github/workflows/update-readme.lock.yml`) runs on every push to **main**. It compares recent commits against the current README, detects documentation drift, and opens a pull request with corrections when needed. If the README is already accurate, the workflow takes no action.

---

**Notes for the demo presentation**
- Walk through the issue text, planned steps, and preview before applying.
- Show how the lint/test pipeline provides fast feedback to the developer.
- Both scripts are safe and intentionally minimal — adapt to your audience.
