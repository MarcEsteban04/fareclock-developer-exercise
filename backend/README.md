# Fareclock Backend API

A FastAPI-based backend service for managing working shifts with Google Cloud Datastore.

## Features

- **Timezone Management**: Configure and manage preferred IANA timezone
- **Workers CRUD**: Full create, read, update, delete operations for workers
- **Shifts CRUD**: Manage working shifts with automatic validation:
  - No overlapping shifts for the same worker
  - Maximum 12-hour duration per shift
  - Timezone-aware datetime handling
  - Computed duration (read-only)

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Google Cloud Datastore**: NoSQL database for scalable data storage
- **Pydantic**: Data validation using Python type annotations
- **Pytest**: Testing framework

## Prerequisites

- Python 3.11+
- Google Cloud SDK (for deployment)
- Google Cloud Project with Datastore enabled

## Local Development Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
GCP_PROJECT_ID=your-project-id
DATASTORE_EMULATOR_HOST=localhost:8081
ENVIRONMENT=development
PORT=8080
```

### 3. Start Datastore Emulator (for local development)

```bash
gcloud beta emulators datastore start --host-port=localhost:8081
```

Keep this running in a separate terminal.

### 4. Run the Application

```bash
python run.py
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --port 8080
```

The API will be available at `http://localhost:8080`

API documentation (Swagger UI): `http://localhost:8080/docs`

## API Endpoints

### Timezone

- `GET /api/timezone` - Get current timezone setting
- `POST /api/timezone` - Set timezone (body: `{"timezone": "America/New_York"}`)

### Workers

- `GET /api/workers` - Get all workers
- `GET /api/workers/{worker_id}` - Get a specific worker
- `POST /api/workers` - Create a worker (body: `{"name": "John Doe"}`)
- `PUT /api/workers/{worker_id}` - Update a worker
- `DELETE /api/workers/{worker_id}` - Delete a worker

### Shifts

- `GET /api/shifts` - Get all shifts (optional query: `?worker_id=xxx`)
- `GET /api/shifts/{shift_id}` - Get a specific shift
- `POST /api/shifts` - Create a shift (body: `{"worker_id": "xxx", "start": "2024-01-01T09:00:00Z", "end": "2024-01-01T17:00:00Z"}`)
- `PUT /api/shifts/{shift_id}` - Update a shift
- `DELETE /api/shifts/{shift_id}` - Delete a shift

## Running Tests

```bash
# Make sure Datastore emulator is running
gcloud beta emulators datastore start --host-port=localhost:8081

# In another terminal, run tests
pytest
```

## Deployment to Google Cloud Run

### 1. Build and Push Docker Image

```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Build the image
docker build -t gcr.io/$PROJECT_ID/fareclock-backend .

# Push to Google Container Registry
docker push gcr.io/$PROJECT_ID/fareclock-backend
```

### 2. Deploy to Cloud Run

```bash
gcloud run deploy fareclock-backend \
  --image gcr.io/$PROJECT_ID/fareclock-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=$PROJECT_ID \
  --port 8080
```

### 3. Using Cloud Build (CI/CD)

```bash
gcloud builds submit --config cloudbuild.yaml
```

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── timezone.py
│   │       ├── workers.py
│   │       └── shifts.py
│   ├── core/
│   │   ├── config.py
│   │   └── datastore.py
│   ├── models/
│   │   ├── entities.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── timezone_service.py
│   │   ├── worker_service.py
│   │   └── shift_service.py
│   ├── utils/
│   │   └── timezone.py
│   └── main.py
├── tests/
│   ├── test_timezone.py
│   ├── test_workers.py
│   └── test_shifts.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Environment Variables

- `GCP_PROJECT_ID`: Your Google Cloud Project ID
- `DATASTORE_EMULATOR_HOST`: Datastore emulator host (for local dev)
- `ENVIRONMENT`: `development` or `production`
- `PORT`: Server port (default: 8080)

## Notes

- Shifts are stored in UTC internally and converted to the configured timezone when returned
- Shift validation ensures no overlaps and maximum 12-hour duration
- The API is designed to handle large amounts of data efficiently with Datastore's scalability
- All datetime strings should be in ISO 8601 format

## License

MIT

