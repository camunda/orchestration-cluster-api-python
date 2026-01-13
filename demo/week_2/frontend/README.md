# QuickLoan Bank Frontend

A modern, responsive fake bank loan website frontend that integrates with the Camunda orchestration API implemented in FastAPI.

## Features

- Modern, professional design with responsive layout
- Comprehensive loan application form with validation
- Real-time API integration with FastAPI backend
- Process instance tracking with detailed status display
- Smooth animations and user-friendly interface

## Quick Start

### Option 1: Using Python HTTP Server (Simplest)

1. Navigate to the frontend directory:
```bash
cd demo/week_2/frontend
```

2. Start a simple HTTP server:
```bash
# Python 3
python -m http.server 8080

# Or Python 2
python -m SimpleHTTPServer 8080
```

3. Open your browser and visit:
```
http://localhost:8080
```

### Option 2: Using Node.js HTTP Server

1. Install http-server globally (if not already installed):
```bash
npm install -g http-server
```

2. Navigate to the frontend directory and start the server:
```bash
cd demo/week_2/frontend
http-server -p 8080
```

3. Open your browser and visit:
```
http://localhost:8080
```

### Option 3: Served by FastAPI (Integrated)

The FastAPI backend can be updated to serve the static files directly. This eliminates CORS issues.

## Prerequisites

Before using the frontend, ensure:

1. **FastAPI Backend is Running**: The backend API should be running at `http://localhost:8000`
   ```bash
   python -m demo.week_2.main
   ```

2. **Camunda is Running**: You need a running Camunda instance (default: `http://localhost:8080/v2`)

3. **Process Deployed**: Deploy a loan application process to Camunda. The frontend expects a process with key `loan-application-process` (you can modify this in `app.js`)

## Configuration

Edit [app.js](app.js) to configure the frontend:

```javascript
// Configuration
const API_BASE_URL = 'http://localhost:8000';
const PROCESS_DEFINITION_KEY = 'loan-application-process';
```

- `API_BASE_URL`: URL of your FastAPI backend
- `PROCESS_DEFINITION_KEY`: The key of your deployed BPMN process

## Form Fields

The loan application form collects:

- **Personal Information**: First name, last name, email, phone
- **Loan Details**: Amount, purpose (personal, home, auto, business, education)
- **Financial Information**: Annual income, employment status
- **Optional**: Credit score

These fields are passed as variables to the Camunda process instance.

## Process Variables

When a loan application is submitted, the following variables are sent to Camunda:

```javascript
{
    applicantFirstName: string,
    applicantLastName: string,
    applicantEmail: string,
    applicantPhone: string,
    loanAmount: number,
    loanPurpose: string,
    annualIncome: number,
    employmentStatus: string,
    creditScore: number | null,
    applicationDate: ISO date string,
    applicationStatus: "pending"
}
```

## API Integration

The frontend communicates with the following FastAPI endpoints:

- `GET /health` - Check API health status
- `POST /process-instance/create` - Create a new loan application process instance

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### CORS Errors

If you encounter CORS errors in the browser console:

1. Ensure the FastAPI backend has CORS enabled (see instructions below)
2. Or serve the frontend through the FastAPI backend as static files

### API Connection Failed

1. Verify the FastAPI backend is running: `curl http://localhost:8000/health`
2. Check the `API_BASE_URL` in `app.js` matches your backend URL
3. Check browser console for detailed error messages

### Process Instance Creation Failed

1. Verify Camunda is running and accessible
2. Ensure you have deployed a process with the correct `PROCESS_DEFINITION_KEY`
3. Check the FastAPI logs for detailed error messages

## Enabling CORS in FastAPI

Add CORS middleware to your FastAPI application:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Demo Flow

1. User lands on the homepage with hero section and features
2. User scrolls down or clicks "Apply Now" to reach the application form
3. User fills out the loan application form
4. On submission, the form data is sent to the FastAPI backend
5. FastAPI creates a Camunda process instance with the application data
6. User sees a success message with process instance details
7. User can submit another application

## Customization

- **Styling**: Edit [styles.css](styles.css) to customize colors, fonts, and layout
- **Content**: Edit [index.html](index.html) to change text content and structure
- **Behavior**: Edit [app.js](app.js) to modify form validation and API interaction

## License

This is a demo application for educational purposes.
