# Running Loan Application Workers

This guide shows you how to run the workers that process your loan applications.

## Quick Start

### Step 1: Start the Workers

Open a **new terminal** (keep your FastAPI server running) and run:

```bash
python demo/week_2/loan_workers.py
```

Or with the shebang:

```bash
./demo/week_2/loan_workers.py
```

You should see:

```
======================================================================
🚀 STARTING LOAN APPLICATION WORKERS
======================================================================
Camunda URL: http://localhost:8080/v2

✅ Registered worker: validate-loan-application
   Description: Validates loan application data
✅ Registered worker: check-credit-score
   Description: Checks or simulates credit score
✅ Registered worker: assess-risk
   Description: Assesses risk and makes loan decision
✅ Registered worker: send-approval-notification
   Description: Sends approval notification
✅ Registered worker: send-rejection-notification
   Description: Sends rejection notification

======================================================================
🎯 ALL WORKERS ACTIVE - Processing loan applications...
   Press Ctrl+C to stop
======================================================================
```

### Step 2: Watch the Magic Happen!

The workers will immediately start processing any waiting loan applications. You'll see output like:

```
============================================================
📋 VALIDATING APPLICATION
============================================================
Job Key: 2251799813843668
Applicant: John Doe
Email: john.doe@email.com
Loan Amount: $50,000.00
Purpose: home

Validation Result: ✅ PASSED

============================================================
💳 CHECKING CREDIT SCORE
============================================================
Job Key: 2251799813843669
Applicant: John Doe
Simulated credit score: 750
Credit Rating: EXCELLENT

============================================================
⚖️  RISK ASSESSMENT & LOAN DECISION
============================================================
Job Key: 2251799813843670
Applicant: John Doe

Application Details:
  Loan Amount: $50,000.00
  Annual Income: $85,000.00
  Credit Score: 750
  Employment: employed

Risk Metrics:
  Debt-to-Income Ratio: 0.59

Decision:
  Risk Level: LOW
  Approved: ✅ YES
  Interest Rate: 3.9%

============================================================
✅ SENDING APPROVAL NOTIFICATION
============================================================
Job Key: 2251799813843671

📧 Email Notification
To: john.doe@email.com
Subject: Loan Application Approved! 🎉

Dear John Doe,

Congratulations! Your loan application has been approved.

Loan Details:
  Amount: $50,000.00
  Interest Rate: 3.9%
  Risk Level: LOW

Next steps: Our team will contact you within 24 hours to finalize the loan.

Best regards,
QuickLoan Bank
```

### Step 3: Submit New Applications

While the workers are running:

1. Go to `http://localhost:8000`
2. Submit a new loan application
3. Watch the terminal - you'll see it being processed in real-time!

## Worker Details

### 5 Workers Implemented

1. **validate-loan-application**
   - Checks all required fields are present
   - Validates loan amount > 0
   - Validates annual income > 0
   - Checks email and purpose are provided

2. **check-credit-score**
   - Uses provided credit score if available
   - Otherwise simulates based on income and employment:
     - Employed + $75K+ income → 750 (Excellent)
     - Employed + $50K+ income → 700 (Good)
     - Self-employed + $60K+ income → 680 (Fair)
     - Other scenarios → 600-650

3. **assess-risk** (Decision Engine)
   - Calculates debt-to-income ratio
   - Applies approval rules:
     - ✅ Credit score >= 750 → Approved (Low risk)
     - ✅ Credit score >= 700 + DTI <= 3 → Approved (Low risk)
     - ✅ Credit score >= 650 + DTI <= 2 + Employed → Approved (Medium risk)
     - ❌ Otherwise → Rejected
   - Assigns interest rate:
     - Low risk: 3.9%
     - Medium risk: 5.9%
     - High risk: 7.9%

4. **send-approval-notification**
   - Simulates email with approval details
   - Shows loan amount and interest rate

5. **send-rejection-notification**
   - Simulates email with rejection reason
   - Provides feedback to applicant

## Testing Different Scenarios

### Scenario 1: High-Quality Applicant (Will be Approved)

```
First Name: Jane
Last Name: Smith
Email: jane.smith@email.com
Phone: 555-9999
Loan Amount: $30,000
Purpose: Home Purchase
Annual Income: $100,000
Employment: Employed
Credit Score: 780
```

**Expected Result**: ✅ Approved, 3.9% interest rate, LOW risk

### Scenario 2: Marginal Applicant (Will be Approved)

```
First Name: Bob
Last Name: Johnson
Email: bob.j@email.com
Phone: 555-8888
Loan Amount: $40,000
Purpose: Auto Purchase
Annual Income: $65,000
Employment: Employed
Credit Score: 680
```

**Expected Result**: ✅ Approved, 5.9% interest rate, MEDIUM risk

### Scenario 3: High Risk (Will be Rejected)

```
First Name: Alice
Last Name: Brown
Email: alice.b@email.com
Phone: 555-7777
Loan Amount: $100,000
Purpose: Personal
Annual Income: $35,000
Employment: Self-Employed
Credit Score: 620
```

**Expected Result**: ❌ Rejected (High debt-to-income ratio + low credit)

### Scenario 4: Poor Credit (Will be Rejected)

```
First Name: Charlie
Last Name: Davis
Email: charlie.d@email.com
Phone: 555-6666
Loan Amount: $25,000
Purpose: Business
Annual Income: $55,000
Employment: Employed
Credit Score: 580
```

**Expected Result**: ❌ Rejected (Credit score below minimum threshold)

## Monitoring

### Check Process Instance Status

While workers are running, check if your previous instances completed:

```bash
curl -s 'http://localhost:8080/v2/process-instances/search' \
  -H 'Content-Type: application/json' \
  -d '{"filter": {"processDefinitionKey": "2251799813843646"}, "page": {"limit": 10}}' \
  | python3 -m json.tool
```

Look for `"state": "COMPLETED"` - that means the process finished!

### Check for Remaining Jobs

```bash
curl -s 'http://localhost:8080/v2/jobs/search' \
  -H 'Content-Type: application/json' \
  -d '{"filter": {"state": "ACTIVATABLE"}, "page": {"limit": 10}}' \
  | python3 -m json.tool
```

If `"totalItems": 0`, all jobs have been processed!

## Stopping the Workers

Press `Ctrl+C` in the terminal where workers are running.

You'll see:

```
======================================================================
👋 Shutting down workers...
======================================================================
```

## Troubleshooting

### Workers not processing jobs

**Check 1**: Are workers actually running?
- Look for "🎯 ALL WORKERS ACTIVE" message

**Check 2**: Is Camunda accessible?
```bash
curl http://localhost:8080/v2/topology
```

**Check 3**: Are there jobs waiting?
```bash
curl -s 'http://localhost:8080/v2/jobs/search' \
  -H 'Content-Type: application/json' \
  -d '{"filter": {"state": "ACTIVATABLE"}}' | python3 -m json.tool
```

### Worker errors

Check the terminal output for error messages. Common issues:
- Connection to Camunda lost
- Invalid variable types
- Missing variables

### Process stuck mid-way

If a worker fails, the job will be retried. Check the worker logs for errors.

## Running in Production

For production, you'd want to:

1. **Run as a service** (systemd, Docker, Kubernetes)
2. **Add proper logging** (not just print statements)
3. **Implement real integrations** (actual email service, credit bureau API)
4. **Add monitoring** (Prometheus, Grafana)
5. **Handle errors gracefully** (retry logic, dead letter queues)
6. **Scale workers** (multiple instances for high throughput)

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

Happy processing! 🚀
