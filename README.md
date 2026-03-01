# Agentic Workflow Demo

A minimal **Flask web service** paired with **GitHub Actions automation** — showcasing a REST API with a live dashboard, containerised deployment, and a scheduled daily-status workflow.

---

## Overview

This project serves two purposes:

1. **Flask REST API & dashboard** — a runnable Python web application with a dark-themed UI, CRUD endpoints for in-memory items, a health-check endpoint, and an echo utility.
2. **Agentic GitHub Actions workflows** — a scheduled job that collects repository activity (open issues, merged PRs) and maintains a single "Daily Status" GitHub issue, plus an automated README-update workflow.

---

## Architecture

```
Browser / HTTP client
        │
        ▼
  Flask (app.py)
  ├── GET  /                 → renders templates/index.html (dashboard)
  ├── GET  /api/health       → JSON health & runtime info
  ├── GET  /api/items        → in-memory item list
  ├── POST /api/items        → create item
  ├── DELETE /api/items/:id  → delete item
  └── POST /api/echo         → echo JSON payload

  GitHub Actions
  ├── daily_status.yml       → cron @ 00:00 UTC; creates/updates "Daily Status" issue
  └── update-readme.lock.yml → triggers on push to main; updates this README
```

State is held **in-memory** — no database. All data resets when the process restarts.

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.12 |
| Web framework | Flask | 3.1.0 |
| Frontend | Vanilla HTML/CSS/JS | — |
| Container | Docker (python:3.12-slim base) | — |
| CI/CD | GitHub Actions | — |

---

## Directory Structure

```
.
├── app.py                  # Flask application & all route handlers
├── requirements.txt        # Python dependencies (flask==3.1.0)
├── Dockerfile              # Container build instructions
├── templates/
│   └── index.html          # Single-page dashboard UI
└── .github/
    └── workflows/
        ├── daily_status.yml               # Scheduled daily-status report workflow
        ├── daily-activity-report.lock.yml # Lock file for activity-report workflow
        └── update-readme.lock.yml         # Lock file for README-update workflow
```

---

## Prerequisites

- **Python 3.12+** (for local development)
- **pip** (bundled with Python)
- **Docker** (optional, for containerised runs)
- **GitHub CLI (`gh`)** + a `GH_TOKEN` secret (required only for the Actions workflows)

---

## Getting Started

### Local development

```bash
# 1. Clone the repository
git clone https://github.com/pappupaul/agentic-workflow-t01.git
cd agentic-workflow-t01

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py
```

The server starts on **http://localhost:5000** by default.

### Docker

```bash
# Build the image
docker build -t agentic-workflow-demo .

# Run the container
docker run -p 5000:5000 agentic-workflow-demo
```

Open **http://localhost:5000** in your browser.

---

## Configuration & Environment Variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `5000` | Port the Flask server listens on |

Set `PORT` before starting the server to override the default:

```bash
PORT=8080 python app.py
# or with Docker:
docker run -e PORT=8080 -p 8080:8080 agentic-workflow-demo
```

For the GitHub Actions workflows, configure the following repository secret:

| Secret | Required by | Description |
|---|---|---|
| `GH_TOKEN` | `daily_status.yml` | Personal access token with `repo` scope for creating/editing issues |

---

## API Reference

All API endpoints return `application/json`.

### `GET /`

Serves the HTML dashboard (`templates/index.html`).

---

### `GET /api/health`

Returns server health information.

**Response `200`:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-01T05:00:00+00:00",
  "python_version": "3.12.0 (main, ...)",
  "platform": "Linux-5.15..."
}
```

---

### `GET /api/items`

Returns all items currently in memory.

**Response `200`:**
```json
[
  {
    "id": 1,
    "name": "My item",
    "description": "Optional description",
    "created_at": "2026-03-01T05:01:00+00:00"
  }
]
```

---

### `POST /api/items`

Creates a new item.

**Request body:**
```json
{ "name": "My item", "description": "Optional" }
```

**Response `201`:**
```json
{ "id": 1, "name": "My item", "description": "Optional", "created_at": "..." }
```

**Response `400`** if `name` is missing:
```json
{ "error": "Name is required" }
```

---

### `DELETE /api/items/<id>`

Deletes an item by numeric ID.

**Response `200`:**
```json
{ "message": "Item deleted" }
```

**Response `404`** if the item does not exist:
```json
{ "error": "Item not found" }
```

---

### `POST /api/echo`

Echoes back whatever JSON payload is sent.

**Request body:** any valid JSON  
**Response `200`:**
```json
{ "echo": { "message": "hello world" } }
```

---

## Deployment

### Docker (production)

```bash
docker build -t agentic-workflow-demo .
docker run -d -p 5000:5000 --name demo agentic-workflow-demo
```

### GitHub Actions CI/CD

Two automated workflows run on pushes to `main`:

| Workflow file | Trigger | What it does |
|---|---|---|
| `update-readme.lock.yml` | Push to `main` | Analyses the codebase and opens a PR to update this README |
| `daily_status.yml` | Cron `0 0 * * *` + manual dispatch | Gathers open issues & merged PRs, then creates or updates a "Daily Status" GitHub issue |

The daily-status workflow requires the `GH_TOKEN` secret (see [Configuration](#configuration--environment-variables)).

---

## Testing

There is no automated test suite in the repository at this time. To manually verify the API:

```bash
# Health check
curl http://localhost:5000/api/health

# Create an item
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "description": "demo item"}'

# List items
curl http://localhost:5000/api/items

# Delete item with id=1
curl -X DELETE http://localhost:5000/api/items/1

# Echo
curl -X POST http://localhost:5000/api/echo \
  -H "Content-Type: application/json" \
  -d '{"hello": "world"}'
```

---

## Contributing

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Commit with concise, conventional commit messages (`feat:`, `fix:`, `chore:`, `docs:`).
3. Open a pull request against `main` with a clear description of the change.

---

## Troubleshooting / FAQ

**Q: The server fails to start with "Address already in use".**  
A: Change the port with `PORT=8081 python app.py` or stop the process already using port 5000.

**Q: The daily-status workflow fails with "gh: command not found".**  
A: The workflow installs `gh` via `apt` at runtime — ensure the runner has internet access. Confirm `GH_TOKEN` is set in repository secrets.

**Q: Items disappear after a restart.**  
A: Items are stored in-memory only. This is by design for the demo; add a database (e.g. SQLite via SQLAlchemy) for persistence.

**Q: `secrets.GITHUB_TOKEN` vs `secrets.GH_TOKEN`?**  
A: The workflows use `secrets.GH_TOKEN` (a personal access token). The built-in `GITHUB_TOKEN` does not have sufficient permissions to create issues across all repository configurations.

---

## License

This project does not currently specify a license. All rights are reserved by the repository owner unless otherwise stated.
