# Camunda Orchestration API - Week 2 Demo

A FastAPI application demonstrating the Camunda Python Orchestration SDK.

## Features

- RESTful API for Camunda operations
- Automatic OpenAPI documentation
- Async/await throughout
- Process deployment and instance creation
- Job worker registration

## Setup

Since this is a demo for the SDK that's currently in development, you'll need to:

1. Install the main SDK dependencies (from the project root):

```bash
# Install the SDK in editable mode
pip install -e .
```

2. Install the demo app dependencies:

```bash
# Install FastAPI and uvicorn for the demo
pip install -e demo/week_2
```

Or install dependencies manually:

```bash
pip install fastapi uvicorn[standard]
```

## Configuration

Set environment variables for Camunda connection (optional, defaults shown):

```bash
export CAMUNDA_BASE_URL="http://localhost:8080"  # Default Camunda cluster URL
export CAMUNDA_TOKEN="your-token-here"           # Optional: for authenticated clusters
```

## Running the App

**Important:** Run the app from the project root directory, not from demo/week_2, so Python can find the SDK modules.

From the project root:

```bash
python -m demo.week_2.main
```

With custom Camunda URL:

```bash
CAMUNDA_BASE_URL="http://your-camunda:8080" python -m demo.week_2.main
```

Or using uvicorn directly:

```bash
uvicorn demo.week_2.main:app --reload --host 0.0.0.0 --port 8000
```

Or add the project root to your PYTHONPATH:

```bash
cd demo/week_2
PYTHONPATH=../.. python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```bash
GET /health
```

### Deploy a BPMN Resource
```bash
POST /deploy/resource
Content-Type: application/json

{
  "file_path": "./path/to/process.bpmn"
}
```

### Create Process Instance
```bash
POST /process-instance/create
Content-Type: application/json

{
  "process_definition_key": 123456789,
  "variables": {
    "customerId": "12345",
    "orderAmount": 100.50
  }
}
```

### Register Job Worker
```bash
POST /worker/register
Content-Type: application/json

{
  "job_type": "my-task-type",
  "job_timeout_milliseconds": 30000,
  "max_concurrent_jobs": 10,
  "execution_strategy": "async"
}
```

## Example Usage

Using `curl`:

```bash
# Health check
curl http://localhost:8000/health

# Deploy a process
curl -X POST http://localhost:8000/deploy/resource \
  -H "Content-Type: application/json" \
  -d '{"file_path": "./tests/integration/resources/job_worker_load_test_process_1.bpmn"}'

# Create a process instance
curl -X POST http://localhost:8000/process-instance/create \
  -H "Content-Type: application/json" \
  -d '{"process_definition_key": 123456789, "variables": {"test": "value"}}'
```

## Development

The app uses:
- **FastAPI** for the web framework
- **Uvicorn** as the ASGI server
- **Pydantic** for request/response validation
- **Camunda Orchestration SDK** for Camunda integration

## Next Steps

- Add more endpoints for process queries, cancellation, etc.
- Implement custom job handlers with business logic
- Add authentication and authorization
- Connect to a real Camunda cluster
