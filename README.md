<div align="center">

# Fareclock – Shift Planner

A simple and fast way to manage workers and shifts. The backend runs on FastAPI, the frontend is Vue 3, both deployed on Google Cloud.

</div>

## Table of Contents

1. [Live URLs](#live-urls)
2. [Requirement Coverage](#requirement-coverage)
3. [Architecture Snapshot](#architecture-snapshot)
4. [Feature Highlights](#feature-highlights)
5. [Tech Stack](#tech-stack)
6. [Getting Started](#getting-started)
7. [Testing](#testing)
8. [Production Deployment](#production-deployment)
9. [Smoke-Test Checklist](#smoke-test-checklist)
10. [Data Model](#data-model)
11. [API Overview](#api-overview)
12. [Monitoring & Ops](#monitoring--ops)
13. [Extra Touches](#extra-touches)
14. [Repository Layout](#repository-layout)
15. [Next Steps](#next-steps)

## Live URLs

| Layer | URL |
| --- | --- |
| **Frontend (Firebase Hosting)** | https://fc-itw-esteban.web.app |
| **Backend (Cloud Run)** | https://fareclock-backend-1037267129816.us-central1.run.app |
| **OpenAPI Docs** | `https://fareclock-backend-1037267129816.us-central1.run.app/docs` |

## Requirement Coverage

- **Timezones:** We have a special page to change your preferred timezone. When you change it, all dates and times on the page will update.
- **Workers:** You can add, remove, and change worker names. We make sure that each worker has a unique name.
- **Shifts:** You can add, remove, and change shifts. We automatically calculate the shift duration and make sure that shifts don't overlap and are not too long.
- **Datastore:** We store all data in Google Cloud Datastore.
- **Cloud Run + Firebase Hosting:** We use Cloud Run and Firebase Hosting to deploy our app.
- **Responsive Vue UI:** Our app works well on desktop, tablet, and phone. We show dates and times in your preferred timezone.
- **Automated tests:** We have tests to make sure that our app works correctly.

## Architecture Snapshot

```
┌────────────┐      REST over TLS      ┌──────────────┐
│ Vue 3 SPA  │  <------------------->  │ FastAPI API  │
│ (Vite)     │                         │ (Cloud Run)  │
└────────────┘                         └─────┬────────┘
       │ Firebase Hosting                     │ Datastore client
       └────────────── CDN/HTTPS ─────────────┘ Cloud Firestore (Datastore Mode)
```

## Feature Highlights

- One timezone switch updates every date/time on the page.
- Shift dialog shows live duration and warns before you save.
- Analytics chips highlight total hours, workers on duty today, and the next shift.
- Layout works on desktop, tablet, and phone.

## Tech Stack

- **Backend:** FastAPI, Pydantic v2, Google Cloud Datastore client, pytest.
- **Frontend:** Vue 3 + TypeScript, Vite, Tailwind-based UI components, Vitest.
- **Infra / Tooling:** Docker, Cloud Build, Cloud Run, Firebase Hosting, gcloud CLI, Firebase CLI.

## Getting Started

### 1. Prerequisites

- Python 3.11+
- Node.js 20+
- Google Cloud SDK (`gcloud`) with access to project `fc-itw-esteban`
- Firebase CLI (`npm install -g firebase-tools`)
- Docker (for local container builds)

### 2. Clone & Workspace

```bash
git clone https://github.com/<your-org>/fareclock-developer-exercise.git
cd fareclock-developer-exercise
```

### 3. Environment Variables

#### Backend (`backend/.env`)

```
GCP_PROJECT_ID=fc-itw-esteban          # override per environment
DATASTORE_EMULATOR_HOST=localhost:8081   # omit in production
ENVIRONMENT=development
PORT=8080
# optional overrides
CORS_ORIGINS=https://fc-itw-esteban.web.app,https://fc-itw-esteban.firebaseapp.com
```

#### Frontend (`frontend/.env`)

```
VITE_API_BASE_URL=https://fareclock-backend-1037267129816.us-central1.run.app
```

### 4. Backend — Local Development

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (Optional) start Datastore emulator
gcloud beta emulators datastore start --project=$GCP_PROJECT_ID --host-port=localhost:8081

uvicorn app.main:app --reload --port 8080
```

> API runs at `http://localhost:8080` and docs live at `/docs`.

### 5. Frontend — Local Development

```bash
cd frontend
npm install
npm run dev  # launches Vite dev server on http://localhost:5173
```

## Testing

| Layer | Command | Notes |
| --- | --- | --- |
| Backend | `cd backend && pytest` | Uses TestClient and Datastore emulator. |
| Frontend | `cd frontend && npm run test:run` | Vitest checks date/time helpers. |

> Tip: add `--maxfail=1 -q` to Pytest for quicker feedback.

## Production Deployment

### Backend → Cloud Run

1. Ensure Docker and gcloud are authenticated (`gcloud auth login`, `gcloud auth configure-docker`).
2. Submit the Cloud Build pipeline (manually specifying a tag for local runs):

```bash
cd backend
gcloud builds submit \
  --config cloudbuild.yaml \
  --project fc-itw-esteban \
  --substitutions SHORT_SHA=manual-$(date +%Y%m%d%H%M%S)
```

Cloud Build will: build → push → deploy to Cloud Run service `fareclock-backend` in `us-central1` with the required env vars.

### Frontend → Firebase Hosting

```bash
cd frontend
npm run build        # generates /dist
firebase login       # once
firebase use prod    # alias pointing to fc-itw-esteban
firebase deploy --only hosting
```

## Smoke-Test Checklist

1. **Workers:** Create, rename, and delete entries. Confirm toast/alerts render and table refreshes.
2. **Shifts:** Add 1–2 shifts per worker, verify duration preview, ensure overlap/12h guards show inline warnings.
3. **Timezone:** Switch timezone on Settings page; confirm displayed datetimes immediately reflect the new zone.
4. **API Health:** `curl https://fareclock-backend-1037267129816.us-central1.run.app/health` should return `{"status": "healthy"}`.
5. **Cross-Origin:** Confirm Firebase-hosted UI loads data without “Failed to fetch” errors (CORS allowlist includes both hosting domains).

## Data Model

| Entity | Key Fields | Notes |
| --- | --- | --- |
| `Timezone` | `timezone` | single record storing preferred IANA string (defaults to `UTC`). |
| `Worker` | `id`, `name` | minimal profile; name is unique-enforced in UI. |
| `Shift` | `id`, `worker_id`, `start`, `end`, `duration` | duration computed server-side; `start`/`end` stored as ISO 8601 UTC and formatted per preference. |

## API Overview

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/timezone` | Retrieve current timezone setting. |
| `POST` | `/api/timezone` | Update timezone (validates IANA string). |
| `GET` | `/api/workers` | List all workers. |
| `POST` | `/api/workers` | Create worker (name required). |
| `GET/PUT/DELETE` | `/api/workers/{id}` | Read/update/remove a specific worker. |
| `GET` | `/api/shifts?worker_id=` | List shifts (optionally filter by worker). |
| `POST` | `/api/shifts` | Create shift (validates overlap & ≤12h). |
| `GET/PUT/DELETE` | `/api/shifts/{id}` | Read/update/delete shift. |

Swagger UI is available at [`/docs`](https://fareclock-backend-1037267129816.us-central1.run.app/docs) for interactive exploration.

## Monitoring & Ops

- **Health check:** `GET /health` responds with `{ "status": "healthy" }` for uptime probes.
- **Cloud Logging:** All Cloud Run stdout/stderr is forwarded to Google Cloud Logging with labels for version + region.
- **Alerting suggestion:** add a Cloud Monitoring alert on 5xx rate or latency to catch regressions early.

## Extra Touches

- Analytics strip summarizing total scheduled hours, workers on duty today, and the next shift.
- Mini timeline visualization for upcoming shifts.
- Inline duration preview + warning list in the shift dialog (overlaps, >12h, end-before-start).
- Custom modal confirmations and success banners replacing browser alerts/toasts.

## Repository Layout

```
├── backend/
│   ├── app/                # FastAPI modules (api, services, datastore)
│   ├── tests/              # Pytest suites for timezone/workers/shifts
│   ├── requirements.txt
│   ├── cloudbuild.yaml     # Build+deploy pipeline for Cloud Run
│   └── .env.example
├── frontend/
│   ├── src/                # Vue 3 application
│   ├── public/
│   ├── vite.config.ts / vitest.config.ts
│   └── .env.example
└── README.md (this file)

