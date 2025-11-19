<div align="center">

# Fareclock — Shift Planner

![Cloud Run](https://img.shields.io/badge/Backend-Google%20Cloud%20Run-4285F4?logo=googlecloud&logoColor=white)
![Firebase Hosting](https://img.shields.io/badge/Frontend-Firebase%20Hosting-FFCA28?logo=firebase&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/UI-Vue%203-42B883?logo=vue.js&logoColor=white)

> A full-stack scheduling experience for high-volume shift operations. Built with FastAPI + Datastore on the backend, Vue 3 + Vite on the frontend, fully deployed to Google Cloud.

</div>

## 🌐 Live URLs

| Layer | URL |
| --- | --- |
| **Frontend (Firebase Hosting)** | https://fc-itw-esteban.web.app |
| **Backend (Cloud Run)** | https://fareclock-backend-1037267129816.us-central1.run.app |
| **OpenAPI Docs** | `https://fareclock-backend-1037267129816.us-central1.run.app/docs` |

## ✅ Requirement Coverage

- **Timezones:** Dedicated endpoint to read/update preferred IANA timezone; existing shifts re-render using the saved zone.
- **Workers CRUD:** Name-only workers with full REST semantics + validation tests.
- **Shift CRUD:** ISO-8601 datetimes, automatic duration computation, overlap + 12h max enforcement, per-worker filters.
- **Datastore persistence:** Google Cloud Datastore (Firestore in Datastore mode) accessed via the official Python client.
- **Cloud Run + Firebase Hosting:** Automated Docker build/deploy pipeline (Cloud Build) and Firebase Hosting for the Vue app.
- **Responsive Vue UI:** Desktop/mobile friendly layout, timezone-aware formatting, analytics strip, shift timeline, contextual alerts.
- **Automated tests:** Pytest suite for all endpoints, Vitest unit tests for date utilities.

## 🧱 Architecture Snapshot

```
┌────────────┐      REST over TLS      ┌──────────────┐
│ Vue 3 SPA  │  <------------------->  │ FastAPI API  │
│ (Vite)     │                         │ (Cloud Run)  │
└────────────┘                         └─────┬────────┘
       │ Firebase Hosting                     │ Datastore client
       └────────────── CDN/HTTPS ─────────────┘ Cloud Firestore (Datastore Mode)
```

## 🛠️ Tech Stack

- **Backend:** FastAPI, Pydantic v2, Google Cloud Datastore client, pytest.
- **Frontend:** Vue 3 + TypeScript, Vite, Tailwind-based UI components, Vitest.
- **Infra / Tooling:** Docker, Cloud Build, Cloud Run, Firebase Hosting, gcloud CLI, Firebase CLI.

## 🚀 Getting Started

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
GCP_PROJECT_ID=fc-itw-esteban
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

> The API will be available at `http://localhost:8080`. Swagger docs live at `/docs`.

### 5. Frontend — Local Development

```bash
cd frontend
npm install
npm run dev  # launches Vite dev server on http://localhost:5173
```

## 🧪 Testing

| Layer | Command | Notes |
| --- | --- | --- |
| Backend | `cd backend && pytest` | Uses FastAPI TestClient + Datastore emulator fixtures. |
| Frontend | `cd frontend && npm run test:run` | Vitest unit tests for date/zone helpers. |

## 📦 Production Deployment

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

## 🔍 Smoke-Test Checklist

1. **Workers:** Create, rename, and delete entries. Confirm toast/alerts render and table refreshes.
2. **Shifts:** Add 1–2 shifts per worker, verify duration preview, ensure overlap/12h guards show inline warnings.
3. **Timezone:** Switch timezone on Settings page; confirm displayed datetimes immediately reflect the new zone.
4. **API Health:** `curl https://fareclock-backend-1037267129816.us-central1.run.app/health` should return `{"status": "healthy"}`.
5. **Cross-Origin:** Confirm Firebase-hosted UI loads data without “Failed to fetch” errors (CORS allowlist includes both hosting domains).

## ✨ Extra Touches

- Analytics strip summarizing total scheduled hours, workers on duty today, and the next shift.
- Mini timeline visualization for upcoming shifts.
- Inline duration preview + warning list in the shift dialog (overlaps, >12h, end-before-start).
- Custom modal confirmations and success banners replacing browser alerts/toasts.

## 📄 Repository Layout

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

