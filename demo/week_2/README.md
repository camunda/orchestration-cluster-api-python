# Camunda Orchestration API - Week 2 Demo

This directory contains a complete fake bank loan application system with a BPMN process, FastAPI backend, and web frontend.

## Overview

The loan application process includes:

1. **BPMN Process** ([loan-application-process.bpmn](loan-application-process.bpmn)) - Defines the loan approval workflow
2. **FastAPI Backend** ([main.py](main.py)) - REST API that integrates with Camunda
3. **Web Frontend** ([frontend/](frontend/)) - User-facing loan application website

## Process Flow

```
Start → Validate → Credit Check → Risk Assessment → Decision Gateway
                                                      ├─→ Approved → Send Approval → End
                                                      └─→ Rejected → Send Rejection → End
```

### Service Tasks (Job Types)

The process includes these service tasks that need workers:

1. **validate-loan-application** - Validates the application data
2. **check-credit-score** - Performs credit score check
3. **assess-risk** - Assesses the risk profile and makes approval decision
4. **send-approval-notification** - Sends approval email/notification
5. **send-rejection-notification** - Sends rejection email/notification

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

### Access the Demo Application

Open your browser and visit:
```
http://localhost:8000
```

You should see the **QuickLoan Bank** website!

## Test the Application

1. **Fill out the loan application form**:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe@email.com
   - Phone: 555-1234
   - Loan Amount: $50,000
   - Loan Purpose: Home Purchase
   - Annual Income: $85,000
   - Employment Status: Employed
   - Credit Score: 750

2. **Click "Submit Application"**

3. **You should see**:
   - Success message
   - Process instance key
   - Application details

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Frontend       │─────▶│  FastAPI         │─────▶│  Camunda        │
│  (Submit Form)  │      │  (Create Process)│      │  (Orchestrate)  │
└─────────────────┘      └──────────────────┘      └────────┬────────┘
                                                              │
                                                              │ Jobs
                                                              ▼
                                                     ┌─────────────────┐
                                                     │  loan_workers   │
                                                     │  (Process Jobs) │
                                                     └─────────────────┘
```