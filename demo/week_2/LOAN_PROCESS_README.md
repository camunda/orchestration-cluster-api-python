# Bank Loan Application Process

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

## Quick Start

### Step 1: Ensure Camunda is Running

```bash
# Check if Camunda is accessible
curl http://localhost:8080/actuator/health
```

If not running, start Camunda (e.g., using Docker):
```bash
docker run -d --name camunda -p 8080:8080 camunda/zeebe:latest
```

### Step 2: Deploy the BPMN Process

Run the deployment script:

```bash
python demo/week_2/deploy_loan_process.py
```

This will:
- Deploy the BPMN process to Camunda
- Return the **process definition key** (a numeric string like "2251799813686749")
- Show you exactly what to update in the frontend

Example output:
```
✅ Deployment successful!

🔑 Process Information:
   Process Definition ID: loan-application-process
   Process Definition Key: 2251799813686749  ⭐ USE THIS!

📝 Next Steps:
   1. Copy this process definition key: 2251799813686749
   2. Update frontend/app.js line 6:
      const PROCESS_DEFINITION_KEY = '2251799813686749';
```

### Step 3: Update the Frontend Configuration

Edit [frontend/app.js](frontend/app.js) and update line 6:

```javascript
const PROCESS_DEFINITION_KEY = '2251799813686749'; // Use your actual key from deployment
```

### Step 4: Start the FastAPI Server

```bash
python -m demo.week_2.main
```

The server will start on `http://localhost:8000`

### Step 5: Access the Web Application

Open your browser and visit:
```
http://localhost:8000
```

You should see the QuickLoan Bank website. Fill out the loan application form and submit!

## Process Variables

When you submit the form, these variables are sent to Camunda:

```javascript
{
    applicantFirstName: "John",
    applicantLastName: "Doe",
    applicantEmail: "john.doe@email.com",
    applicantPhone: "555-1234",
    loanAmount: 50000,
    loanPurpose: "home",
    annualIncome: 85000,
    employmentStatus: "employed",
    creditScore: 720,  // optional
    applicationDate: "2024-01-09T10:00:00Z",
    applicationStatus: "pending"
}
```

## Implementing Job Workers

The BPMN process defines service tasks that need workers to execute them. Here's how to implement them:

### Example: Simple Worker Implementation

Create a file `loan_workers.py`:

```python
import asyncio
from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.runtime.job_worker import WorkerConfig

async def validate_application(job_context):
    """Validate the loan application data"""
    variables = job_context.variables

    print(f"Validating application for {variables['applicantFirstName']} {variables['applicantLastName']}")

    # Simple validation
    is_valid = (
        variables['loanAmount'] > 0 and
        variables['annualIncome'] > 0 and
        len(variables['applicantEmail']) > 0
    )

    return {"isValid": is_valid}

async def check_credit_score(job_context):
    """Check or assign credit score"""
    variables = job_context.variables

    # Use provided credit score or assign a default
    credit_score = variables.get('creditScore', 650)

    print(f"Credit score for {variables['applicantEmail']}: {credit_score}")

    return {"creditScore": credit_score}

async def assess_risk(job_context):
    """Assess risk and make loan decision"""
    variables = job_context.variables

    loan_amount = variables['loanAmount']
    annual_income = variables['annualIncome']
    credit_score = variables.get('creditScore', 650)

    # Simple decision logic
    debt_to_income = loan_amount / annual_income

    # Approval criteria:
    # - Credit score >= 700 OR (>= 650 AND debt-to-income < 3)
    # - Loan amount <= annual income * 5
    approved = (
        (credit_score >= 700 or (credit_score >= 650 and debt_to_income < 3)) and
        loan_amount <= annual_income * 5
    )

    risk_level = "LOW" if credit_score >= 750 else "MEDIUM" if credit_score >= 650 else "HIGH"

    print(f"Risk assessment: {risk_level}, Approved: {approved}")

    return {
        "loanApproved": approved,
        "riskLevel": risk_level,
        "debtToIncomeRatio": debt_to_income
    }

async def send_approval_notification(job_context):
    """Send approval notification"""
    variables = job_context.variables

    print(f"✅ Sending approval notification to {variables['applicantEmail']}")
    print(f"   Loan Amount: ${variables['loanAmount']}")
    print(f"   Risk Level: {variables.get('riskLevel', 'N/A')}")

    return {"notificationSent": True}

async def send_rejection_notification(job_context):
    """Send rejection notification"""
    variables = job_context.variables

    print(f"❌ Sending rejection notification to {variables['applicantEmail']}")
    print(f"   Reason: Risk assessment did not meet approval criteria")

    return {"notificationSent": True}

async def main():
    """Register all workers and keep them running"""
    camunda = CamundaAsyncClient(base_url="http://localhost:8080/v2")

    # Register workers
    workers = [
        ("validate-loan-application", validate_application),
        ("check-credit-score", check_credit_score),
        ("assess-risk", assess_risk),
        ("send-approval-notification", send_approval_notification),
        ("send-rejection-notification", send_rejection_notification),
    ]

    for job_type, callback in workers:
        config = WorkerConfig(
            job_type=job_type,
            job_timeout_milliseconds=30_000,
            max_concurrent_jobs=10,
            execution_strategy="async"
        )
        camunda.create_job_worker(config=config, callback=callback)
        print(f"✅ Worker registered: {job_type}")

    print("\n🚀 All workers are running. Press Ctrl+C to stop.\n")

    # Keep running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n👋 Shutting down workers...")

if __name__ == "__main__":
    asyncio.run(main())
```

### Running the Workers

In a separate terminal:

```bash
python loan_workers.py
```

## Testing the Complete Flow

1. **Start Camunda** (if not running)
2. **Deploy the process**: `python demo/week_2/deploy_loan_process.py`
3. **Update frontend config** with the process key
4. **Start FastAPI server**: `python -m demo.week_2.main`
5. **Start workers**: `python loan_workers.py` (in another terminal)
6. **Open browser**: Visit `http://localhost:8000`
7. **Submit application**: Fill out the form and submit

You should see:
- Frontend shows success with process instance details
- Workers log the processing steps
- Process completes with approval or rejection

## Process Decision Logic (in example workers)

The example risk assessment logic:

- **Approved if**:
  - Credit score >= 700, OR
  - Credit score >= 650 AND debt-to-income ratio < 3
  - AND loan amount <= 5x annual income

- **Rejected if**:
  - Credit score < 650, OR
  - Debt-to-income ratio >= 3 (when credit < 700), OR
  - Loan amount > 5x annual income

## Monitoring

- **Camunda Operate** (if available): View process instances and their progress
- **FastAPI Docs**: `http://localhost:8000/docs` - API documentation and testing
- **Worker Logs**: Check the terminal where workers are running
- **FastAPI Logs**: Check the terminal where the server is running

## Troubleshooting

### "Failed to create process instance: For input string..."

- **Cause**: The frontend is using a non-numeric process key
- **Fix**: Run the deployment script and update `frontend/app.js` with the numeric key

### "Camunda client not initialized"

- **Cause**: Camunda is not accessible
- **Fix**: Verify Camunda is running: `curl http://localhost:8080/actuator/health`

### Process instance created but nothing happens

- **Cause**: No workers are running to handle the service tasks
- **Fix**: Start the workers: `python loan_workers.py`

### Worker errors

- **Cause**: Workers might be failing due to missing variables or logic errors
- **Fix**: Check worker logs for detailed error messages

## Next Steps

1. **Customize the BPMN process** - Add more steps, user tasks, or decision logic
2. **Enhance workers** - Add real credit check APIs, email services, database storage
3. **Add authentication** - Secure the API and track user applications
4. **Implement user tasks** - Add manual review steps for edge cases
5. **Add database** - Store applications and their status
6. **Build admin dashboard** - View all applications and their processing status

## File Structure

```
demo/week_2/
├── loan-application-process.bpmn  # BPMN process definition
├── deploy_loan_process.py         # Script to deploy the process
├── main.py                         # FastAPI backend
├── loan_workers.py                 # Example worker implementation (you create this)
└── frontend/
    ├── index.html                  # Frontend HTML
    ├── styles.css                  # Frontend styles
    ├── app.js                      # Frontend JavaScript
    └── *.md                        # Documentation
```

Happy building! 🚀
