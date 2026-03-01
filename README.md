# Agentic Workflow Demo

A minimal **Python/Flask** web service used to demonstrate agentic GitHub
Actions workflows — automated README updates, daily status reports, and
containerised deployments.

---

## Overview

This repository serves two purposes:

1. **Web application** — A small REST API with an interactive browser UI that
   exposes health, CRUD item management, and echo endpoints.
2. **Workflow sandbox** — A set of GitHub Actions workflows that showcase
   agentic automation: a daily activity report that posts a summary issue and
   an auto-updating README triggered on every push to `main`.

---

## Architecture

```
Browser
  │  GET /
  ▼
Flask (app.py)
  ├── GET  /                  → renders templates/index.html
  ├── GET  /api/health        → JSON health payload
  ├── GET  /api/items         → JSON list (in-memory)
  ├── POST /api/items         → create item (in-memory)
  ├── DELETE /api/items/<id>  → delete item
  └── POST /api/echo          → reflect JSON body

GitHub Actions
  ├── daily_status.yml        → nightly issue with open issues + merged PRs
  └── update-readme.lock.yml  → auto-update README on push to main
```

State is kept **in-memory** only — the items list is reset when the process
restarts. There is no database.

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.12 |
| Web framework | Flask | 3.1.0 |
| Container | Docker (python:3.12-slim) | — |
| CI/CD | GitHub Actions | — |
| Frontend | Vanilla HTML/CSS/JS | — |

---

## Directory Structure

```
.
├── app.py                  # Flask application — routes and in-memory state
├── requirements.txt        # Python dependencies (flask==3.1.0)
├── Dockerfile              # Container build instructions
├── templates/
│   └── index.html          # Single-page dashboard UI
└── .github/
    └── workflows/
        ├── daily_status.yml             # Nightly activity-report workflow
        ├── daily-activity-report.lock.yml
        ├── update-readme.lock.yml       # README auto-update workflow
        └── update-readme.md
```

---

## Prerequisites

- **Python 3.12+** (or Docker)
- **pip**
- A GitHub personal access token stored as `GH_TOKEN` repository secret (only
  needed for the `daily_status.yml` workflow)

---

## Getting Started

### Run locally

```bash
# 1. Clone the repository
git clone https://github.com/pappupaul/agentic-workflow-t01.git
cd agentic-workflow-t01

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the development server
python app.py
```

The app will be available at <http://localhost:5000>.

### Run with Docker

```bash
docker build -t agentic-workflow-t01 .
docker run -p 5000:5000 agentic-workflow-t01
```

---

## Configuration & Environment Variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `5000` | Port the Flask server listens on |

Set `PORT` before starting the app to override the default:

```bash
PORT=8080 python app.py
```

The Docker image sets `ENV PORT=5000` and `EXPOSE ${PORT}` so overriding at
`docker run` time also works:

```bash
docker run -p 8080:8080 -e PORT=8080 agentic-workflow-t01
```

---

## API Reference

All API responses are JSON. The base URL for local development is
`http://localhost:5000`.

### `GET /`

Returns the HTML dashboard page.

---

### `GET /api/health`

Health check. Returns server metadata.

**Response `200`**

```json
{
  "status": "healthy",
  "timestamp": "2026-03-01T05:00:00+00:00",
  "python_version": "3.12.0 (main, ...)",
  "platform": "Linux-..."
}
```

---

### `GET /api/items`

List all in-memory items.

**Response `200`**

```json
[
  {
    "id": 1,
    "name": "Example",
    "description": "An example item",
    "created_at": "2026-03-01T05:00:00+00:00"
  }
]
```

---

### `POST /api/items`

Create a new item.

**Request body**

```json
{ "name": "My item", "description": "Optional description" }
```

`name` is required; `description` is optional (defaults to `""`).

**Response `201`**

```json
{ "id": 1, "name": "My item", "description": "", "created_at": "..." }
```

**Response `400`** — missing `name`

```json
{ "error": "Name is required" }
```

---

### `DELETE /api/items/<id>`

Delete an item by its integer ID.

**Response `200`**

```json
{ "message": "Item deleted" }
```

**Response `404`**

```json
{ "error": "Item not found" }
```

---

### `POST /api/echo`

Reflects the JSON body back to the caller.

**Request body** — any valid JSON

**Response `200`**

```json
{ "echo": { "message": "hello world" } }
```

---

## Deployment

### Docker

```bash
docker build -t agentic-workflow-t01 .
docker run -d -p 5000:5000 --name app agentic-workflow-t01
```

The Dockerfile:

- Uses `python:3.12-slim` as base image.
- Installs only `requirements.txt` dependencies.
- Copies the full workspace into `/app`.
- Starts the server with `python app.py`.

### GitHub Actions — Daily Status Report

The workflow at `.github/workflows/daily_status.yml` runs at **00:00 UTC** daily
(and can be triggered manually via `workflow_dispatch`). It:

1. Lists all open issues in the repository.
2. Lists all recently merged pull requests.
3. Creates or updates a single issue titled **"Daily Status"** with the
   gathered summary.

**Required secret**: `GH_TOKEN` — a GitHub token with `issues: write` and
`pull_requests: read` permissions.

---

## Testing

There is no automated test suite in this repository. The application is
intentionally minimal and the interactive dashboard (`/`) can be used to
manually exercise all endpoints.

To perform a quick smoke-test via `curl`:

```bash
# Health check
curl http://localhost:5000/api/health

# Create an item
curl -X POST http://localhost:5000/api/items \
     -H 'Content-Type: application/json' \
     -d '{"name":"test","description":"smoke test"}'

# List items
curl http://localhost:5000/api/items

# Delete item 1
curl -X DELETE http://localhost:5000/api/items/1

# Echo
curl -X POST http://localhost:5000/api/echo \
     -H 'Content-Type: application/json' \
     -d '{"hello":"world"}'
```

---

## Contributing

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feat/your-feature
   ```
2. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   `feat:`, `fix:`, `docs:`, `chore:`, etc.
3. Open a pull request against `main` with a clear description of your changes.

---

## Troubleshooting / FAQ

**Port already in use**

```
OSError: [Errno 98] Address already in use
```

Set a different port: `PORT=5001 python app.py`

**Items disappear on restart**

By design — state is held in-memory only. Restart the server and the items
list is empty.

**`GH_TOKEN` secret not set** (daily-status workflow fails)

Add a [fine-grained personal access token](https://github.com/settings/tokens)
with `issues: write` permission to the repository secrets under the name
`GH_TOKEN`.

---

## License

This project is provided as a demo and carries no explicit open-source license.
Contact the repository owner for usage terms.
