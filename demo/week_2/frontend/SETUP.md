# QuickLoan Bank - Complete Setup Guide

This guide will walk you through setting up the complete fake bank loan website with Camunda integration.

## Architecture Overview

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Frontend       │─────▶│  FastAPI         │─────▶│  Camunda        │
│  (HTML/CSS/JS)  │      │  Backend         │      │  Orchestration  │
│  Port 8000      │      │  Port 8000       │      │  Port 8080      │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

## Prerequisites

1. **Python 3.8+** installed
2. **Camunda instance** running (Docker or local)
3. **FastAPI dependencies** installed

## Step 1: Start Camunda (if not already running)

### Option A: Using Docker
```bash
docker run -d --name camunda \
  -p 8080:8080 \
  camunda/zeebe:latest
```

### Option B: Using Camunda Platform 8
Follow the official Camunda Platform 8 setup guide.

## Step 2: Install Dependencies

If FastAPI dependencies are not installed, add them:

```bash
# Core dependencies should already be in your environment
pip install fastapi uvicorn python-multipart

# These are typically included with fastapi, but can be installed separately:
pip install starlette aiofiles
```

## Step 3: Deploy a BPMN Process

You need a BPMN process deployed to Camunda for the loan application workflow.

### Create a Simple Loan Process (Optional)

If you don't have a loan process, you can create a simple one or update the frontend to use an existing process key.

1. Update the process key in [app.js](app.js):
```javascript
const PROCESS_DEFINITION_KEY = 'your-process-key-here';
```

2. Or deploy a sample BPMN file using the API:
```bash
curl -X POST http://localhost:8000/deploy/resource \
  -H "Content-Type: application/json" \
  -d '{"file_path": "path/to/your/process.bpmn"}'
```

## Step 4: Start the FastAPI Backend

Navigate to the project root and start the FastAPI server:

```bash
# From the project root
cd /Users/rickwestera/camunda/orchestration-cluster-api-python

# Start the server
python -m demo.week_2.main
```

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
Camunda client initialized (base_url: http://localhost:8080/v2)
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 5: Access the Frontend

Now you have **two options** to access the frontend:

### Option A: Access Through FastAPI (Recommended - No CORS Issues)

Simply open your browser and visit:
```
http://localhost:8000
```

The FastAPI backend now serves the frontend directly, so there are no CORS issues.

### Option B: Run Separate Frontend Server

If you prefer to run the frontend separately:

1. Open a new terminal
2. Navigate to the frontend directory:
```bash
cd demo/week_2/frontend
```

3. Start a simple HTTP server:
```bash
python -m http.server 8080
```

4. Visit: `http://localhost:8080`

## Step 6: Test the Application

1. Fill out the loan application form:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe@email.com
   - Phone: 555-1234
   - Loan Amount: $50,000
   - Loan Purpose: Home Purchase
   - Annual Income: $85,000
   - Employment Status: Employed
   - Credit Score: 720 (optional)

2. Click "Submit Application"

3. You should see a success message with process instance details

4. Check the FastAPI logs to see the process instance creation

## Troubleshooting

### Error: "Camunda client not initialized"

**Solution**: Make sure Camunda is running and accessible at `http://localhost:8080/v2`

Test with:
```bash
curl http://localhost:8000/health
```

Should return:
```json
{"status": "healthy", "camunda_client": true}
```

### Error: "Failed to create process instance: Process definition not found"

**Solution**: The process with the specified key doesn't exist in Camunda.

1. Update `PROCESS_DEFINITION_KEY` in [app.js](app.js) to match an existing process
2. Or deploy a BPMN process to Camunda

### Error: CORS Policy Error (if using separate frontend server)

**Solution**: The FastAPI backend now includes CORS middleware. If you're still getting CORS errors:

1. Verify the frontend URL is in the allowed origins (check [main.py](../main.py:50))
2. Restart the FastAPI server
3. Or use Option A (access through FastAPI at http://localhost:8000)

### Error: "Failed to connect to API server"

**Solution**: Ensure FastAPI is running:
```bash
# Check if the server is running
curl http://localhost:8000/health

# If not running, start it:
python -m demo.week_2.main
```

### Frontend loads but form doesn't submit

**Solution**:
1. Open browser developer console (F12) to see error messages
2. Verify the `API_BASE_URL` in [app.js](app.js) is correct
3. Check that the process definition key matches an existing process

## Verify Setup

Run these commands to verify everything is working:

```bash
# 1. Check FastAPI health
curl http://localhost:8000/health

# 2. Check Camunda topology (through FastAPI)
curl http://localhost:8000/topology

# 3. Test process instance creation (replace with your process key)
curl -X POST http://localhost:8000/process-instance/create \
  -H "Content-Type: application/json" \
  -d '{"process_definition_key": "loan-application-process"}'
```

## Configuration

### Environment Variables

You can configure the Camunda connection using environment variables:

```bash
export CAMUNDA_BASE_URL="http://localhost:8080/v2"
export CAMUNDA_TOKEN="your-token-here"  # Optional

python -m demo.week_2.main
```

### Frontend Configuration

Edit [app.js](app.js) to customize:

```javascript
// API endpoint
const API_BASE_URL = 'http://localhost:8000';

// Process key (must match your deployed BPMN process)
const PROCESS_DEFINITION_KEY = 'loan-application-process';
```

## Next Steps

1. **Customize the BPMN Process**: Create a proper loan approval workflow with decision nodes, user tasks, and service tasks
2. **Add Job Workers**: Implement workers to handle tasks like credit checks, approval notifications, etc.
3. **Enhance the Frontend**: Add features like application status tracking, user authentication, etc.
4. **Add Validation**: Implement proper form validation and error handling
5. **Add Database**: Store application data in a database for persistence

## API Endpoints

The backend provides these endpoints:

- `GET /` - Serves the frontend (if available)
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)
- `POST /deploy/resource` - Deploy BPMN resources
- `POST /process-instance/create` - Create process instance
- `GET /workers` - List registered workers (placeholder)

## Support

For issues related to:
- **FastAPI**: Check the server logs for detailed error messages
- **Camunda**: Verify Camunda is running and accessible
- **Frontend**: Check browser console (F12) for JavaScript errors

## Demo Data

Here's some sample data you can use for testing:

### Approved Loan Scenario
- Loan Amount: $25,000
- Annual Income: $100,000
- Credit Score: 750
- Employment: Employed

### Review Required Scenario
- Loan Amount: $200,000
- Annual Income: $60,000
- Credit Score: 650
- Employment: Self-Employed

### Likely Denied Scenario
- Loan Amount: $300,000
- Annual Income: $30,000
- Credit Score: 550
- Employment: Unemployed

Have fun building your loan application workflow!
