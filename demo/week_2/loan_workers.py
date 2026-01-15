#!/usr/bin/env python
"""
Loan Application Workers

This script implements all the job workers needed for the loan application BPMN process.
Run this alongside the FastAPI server to process loan applications end-to-end.

Job Types Handled:
- validate-loan-application
- check-credit-score
- assess-risk
- send-approval-notification
- send-rejection-notification
"""
import os
from pathlib import Path
from typing import Any, TypedDict
from dotenv import load_dotenv
from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.runtime.job_worker import (
    AsyncJobHandler,
    WorkerConfig,
    JobContext,
)

# Load environment variables from .env file
load_dotenv(Path(__file__).parent / ".env")

class WorkerDefinition(TypedDict):
    """Configuration for registering a job worker."""
    job_type: str
    callback: AsyncJobHandler
    description: str

# Configuration
CAMUNDA_BASE_URL = os.getenv("CAMUNDA_BASE_URL", "http://localhost:8080/v2")
CAMUNDA_TOKEN = os.getenv("CAMUNDA_TOKEN")

# Worker 1: Validate Loan Application
async def validate_application(job_context: JobContext) -> dict[str, Any]:
    """
    Validates the loan application data.
    Checks that all required fields are present and valid.
    """
    variables = job_context.variables.to_dict()

    print(f"\n{'='*60}")
    print(f"📋 VALIDATING APPLICATION")
    print(f"{'='*60}")
    print(f"Job Key: {job_context.job_key}")
    print(
        f"Applicant: {variables.get('applicantFirstName')} {variables.get('applicantLastName')}"
    )
    print(f"Email: {variables.get('applicantEmail')}")
    print(f"Loan Amount: ${variables.get('loanAmount'):,.2f}")
    print(f"Purpose: {variables.get('loanPurpose')}")

    # Validation logic
    is_valid = True
    validation_errors: list[str] = []

    # Check required fields
    loan_amount = variables.get("loanAmount", 0)
    if loan_amount <= 0:
        is_valid = False
        validation_errors.append("Loan amount must be greater than 0")

    annual_income = variables.get("annualIncome", 0)
    if annual_income <= 0:
        is_valid = False
        validation_errors.append("Annual income must be greater than 0")

    if not variables.get("applicantEmail"):
        is_valid = False
        validation_errors.append("Email is required")

    if not variables.get("loanPurpose"):
        is_valid = False
        validation_errors.append("Loan purpose is required")

    print(f"\nValidation Result: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    if validation_errors:
        print(f"Errors: {', '.join(validation_errors)}")

    return {
        "isValid": is_valid,
        "validationErrors": validation_errors if validation_errors else [],
    }

# Worker 2: Check Credit Score
async def check_credit_score(job_context: JobContext):
    """
    Checks or assigns a credit score.
    In a real system, this would call a credit bureau API.
    """
    variables = job_context.variables.to_dict()

    print(f"\n{'='*60}")
    print(f"💳 CHECKING CREDIT SCORE")
    print(f"{'='*60}")
    print(f"Job Key: {job_context.job_key}")
    print(
        f"Applicant: {variables.get('applicantFirstName')} {variables.get('applicantLastName')}"
    )

    # Use provided credit score or simulate one based on income
    if variables.get("creditScore"):
        credit_score = variables.get("creditScore", 0)
        print(f"Using provided credit score: {credit_score}")
    else:
        # Simulate credit score based on income and employment
        income = variables.get("annualIncome", 50000)
        employment = variables.get("employmentStatus", "employed")

        if employment == "employed" and income > 75000:
            credit_score = 750
        elif employment == "employed" and income > 50000:
            credit_score = 700
        elif employment == "self-employed" and income > 60000:
            credit_score = 680
        elif employment == "employed":
            credit_score = 650
        else:
            credit_score = 600

        print(f"Simulated credit score: {credit_score}")

    # Determine credit rating
    if credit_score >= 750:
        credit_rating = "EXCELLENT"
    elif credit_score >= 700:
        credit_rating = "GOOD"
    elif credit_score >= 650:
        credit_rating = "FAIR"
    else:
        credit_rating = "POOR"

    print(f"Credit Rating: {credit_rating}")

    return {
                "creditScore": credit_score,
                "creditRating": credit_rating,
            }

# Worker 3: Assess Risk and Make Decision
async def assess_risk(job_context: JobContext):
    """
    Assesses the risk profile and makes the loan approval decision.
    This is the core decision-making logic.
    """
    variables = job_context.variables.to_dict()

    print(f"\n{'='*60}")
    print(f"⚖️  RISK ASSESSMENT & LOAN DECISION")
    print(f"{'='*60}")
    print(f"Job Key: {job_context.job_key}")
    print(
        f"Applicant: {variables.get('applicantFirstName')} {variables.get('applicantLastName')}"
    )

    # Get application details
    loan_amount = variables.get("loanAmount", 0)
    annual_income = variables.get("annualIncome", 0)
    credit_score = variables.get("creditScore", 600)
    employment_status = variables.get("employmentStatus", "unemployed")

    print(f"\nApplication Details:")
    print(f"  Loan Amount: ${loan_amount:,.2f}")
    print(f"  Annual Income: ${annual_income:,.2f}")
    print(f"  Credit Score: {credit_score}")
    print(f"  Employment: {employment_status}")

    # Calculate debt-to-income ratio
    debt_to_income_ratio = loan_amount / annual_income if annual_income > 0 else 999

    print(f"\nRisk Metrics:")
    print(f"  Debt-to-Income Ratio: {debt_to_income_ratio:.2f}")

    # Decision logic
    approved = False
    risk_level = "HIGH"
    rejection_reason = None

    # Rule 1: Maximum loan amount relative to income
    max_loan_multiplier = 5
    if loan_amount > annual_income * max_loan_multiplier:
        rejection_reason = f"Loan amount exceeds {max_loan_multiplier}x annual income"
        risk_level = "HIGH"

    # Rule 2: Unemployed or retired with low income
    elif employment_status in ["unemployed", "retired"] and annual_income < 40000:
        rejection_reason = "Insufficient income for employment status"
        risk_level = "HIGH"

    # Rule 3: Poor credit score
    elif credit_score < 600:
        rejection_reason = "Credit score below minimum threshold (600)"
        risk_level = "HIGH"

    # Rule 4: High debt-to-income ratio with mediocre credit
    elif debt_to_income_ratio > 3 and credit_score < 700:
        rejection_reason = "High debt-to-income ratio with insufficient credit score"
        risk_level = "HIGH"

    # Approved scenarios
    elif credit_score >= 750:
        approved = True
        risk_level = "LOW"
    elif credit_score >= 700 and debt_to_income_ratio <= 3:
        approved = True
        risk_level = "LOW"
    elif (
        credit_score >= 650
        and debt_to_income_ratio <= 2
        and employment_status == "employed"
    ):
        approved = True
        risk_level = "MEDIUM"
    else:
        rejection_reason = "Does not meet approval criteria"
        risk_level = "HIGH"

    # Calculate interest rate based on risk
    if approved:
        if risk_level == "LOW":
            interest_rate = 3.9
        elif risk_level == "MEDIUM":
            interest_rate = 5.9
        else:
            interest_rate = 7.9
    else:
        interest_rate = None

    print(f"\nDecision:")
    print(f"  Risk Level: {risk_level}")
    print(f"  Approved: {'✅ YES' if approved else '❌ NO'}")
    if approved:
        print(f"  Interest Rate: {interest_rate}%")
    else:
        print(f"  Reason: {rejection_reason}")

    return {
        "loanApproved": approved,
        "riskLevel": risk_level,
        "debtToIncomeRatio": round(debt_to_income_ratio, 2),
        "interestRate": interest_rate,
        "rejectionReason": rejection_reason,
        "decisionDate": variables.get("applicationDate"),
    }



# Worker 4: Send Approval Notification
async def send_approval_notification(job_context: JobContext):
    """
    Sends approval notification to the applicant.
    In a real system, this would send an email or SMS.
    """
    variables = job_context.variables.to_dict()

    print(f"\n{'='*60}")
    print(f"✅ SENDING APPROVAL NOTIFICATION")
    print(f"{'='*60}")
    print(f"Job Key: {job_context.job_key}")

    applicant_name = (
        f"{variables.get('applicantFirstName')} {variables.get('applicantLastName')}"
    )
    email = variables.get("applicantEmail")
    loan_amount = variables.get("loanAmount", 0)
    interest_rate = variables.get("interestRate", 0)

    print(f"\n📧 Email Notification")
    print(f"To: {email}")
    print(f"Subject: Loan Application Approved! 🎉")
    print(f"\nDear {applicant_name},")
    print(f"\nCongratulations! Your loan application has been approved.")
    print(f"\nLoan Details:")
    print(f"  Amount: ${loan_amount:,.2f}")
    print(f"  Interest Rate: {interest_rate}%")
    print(f"  Risk Level: {variables.get('riskLevel', 'N/A')}")
    print(
        f"\nNext steps: Our team will contact you within 24 hours to finalize the loan."
    )
    print(f"\nBest regards,")
    print(f"QuickLoan Bank")

    return {
        "notificationSent": True,
        "notificationType": "approval",
        "notificationDate": variables.get("applicationDate"),
    }



# Worker 5: Send Rejection Notification
async def send_rejection_notification(
    job_context: JobContext,
):
    """
    Sends rejection notification to the applicant.
    In a real system, this would send an email or SMS.
    """
    variables = job_context.variables.to_dict()

    print(f"\n{'='*60}")
    print(f"❌ SENDING REJECTION NOTIFICATION")
    print(f"{'='*60}")
    print(f"Job Key: {job_context.job_key}")

    applicant_name = (
        f"{variables.get('applicantFirstName')} {variables.get('applicantLastName')}"
    )
    email = variables.get("applicantEmail")
    rejection_reason = variables.get(
        "rejectionReason", "Application does not meet our criteria"
    )

    print(f"\n📧 Email Notification")
    print(f"To: {email}")
    print(f"Subject: Loan Application Status Update")
    print(f"\nDear {applicant_name},")
    print(f"\nThank you for your interest in QuickLoan Bank.")
    print(
        f"\nAfter careful review, we are unable to approve your loan application at this time."
    )
    print(f"\nReason: {rejection_reason}")
    print(
        f"\nYou may reapply after 90 days or contact us to discuss alternative options."
    )
    print(f"\nBest regards,")
    print(f"QuickLoan Bank")

    return {
        "notificationSent": True,
        "notificationType": "rejection",
        "notificationDate": variables.get("applicationDate"),
    }

async def run_workers(camunda: CamundaAsyncClient):
    """
    Main function to register all workers and keep them running.
    """
    print("=" * 70)
    print("🚀 STARTING LOAN APPLICATION WORKERS")
    print("=" * 70)
    print(f"Camunda URL: {CAMUNDA_BASE_URL}")
    print()

    # Define workers configuration
    workers: list[WorkerDefinition] = [
        {
            "job_type": "validate-loan-application",
            "callback": validate_application,
            "description": "Validates loan application data",
        },
        {
            "job_type": "check-credit-score",
            "callback": check_credit_score,
            "description": "Checks or simulates credit score",
        },
        {
            "job_type": "assess-risk",
            "callback": assess_risk,
            "description": "Assesses risk and makes loan decision",
        },
        {
            "job_type": "send-approval-notification",
            "callback": send_approval_notification,
            "description": "Sends approval notification",
        },
        {
            "job_type": "send-rejection-notification",
            "callback": send_rejection_notification,
            "description": "Sends rejection notification",
        },
    ]

    # Register all workers
    for worker_def in workers:
        config = WorkerConfig(
            job_type=worker_def["job_type"],
            job_timeout_milliseconds=30_000,  # 30 seconds
            request_timeout_milliseconds=20_000,  # 20 seconds
            max_concurrent_jobs=10,
            execution_strategy="async",
        )

        # Type ignore: SDK runtime accepts CompleteJobData but type hints only declare dict
        camunda.create_job_worker(config=config, callback=worker_def["callback"])  # type: ignore[arg-type]

        print(f"✅ Registered worker: {worker_def['job_type']}")
        print(f"   Description: {worker_def['description']}")

    print(f"\n{'='*70}")
    print("🎯 ALL WORKERS ACTIVE - Processing loan applications...")
    print("   Press Ctrl+C to stop")
    print("=" * 70)
    print()
