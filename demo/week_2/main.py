from camunda_orchestration_sdk.models.processcreationbyid_variables import (
    ProcesscreationbyidVariables,
)
from camunda_orchestration_sdk.semantic_types import ProcessDefinitionKey
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, Optional
from contextlib import asynccontextmanager
from pathlib import Path
from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.models.processcreationbykey import Processcreationbykey
from camunda_orchestration_sdk.models.search_process_instances_data import SearchProcessInstancesData
from camunda_orchestration_sdk.models.search_process_instances_data_filter import SearchProcessInstancesDataFilter
from camunda_orchestration_sdk.models.state_exactmatch_3 import StateExactmatch3
from camunda_orchestration_sdk.models.search_variables_data import SearchVariablesData
from camunda_orchestration_sdk.models.search_variables_data_filter import SearchVariablesDataFilter
import asyncio
import json
from datetime import datetime
from loguru import logger

from demo.week_2.loan_workers import run_workers

from .deploy_loan_process import deploy_loan_process

# Global Camunda client instance
camunda_client: Optional[CamundaAsyncClient] = None
process_definition_key: ProcessDefinitionKey


class Settings(BaseSettings):
    camunda_rest_address: str = Field(
        default="http://localhost:8080/v2",
        validation_alias="CAMUNDA_REST_ADDRESS",
    )

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Settings singleton
settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI app - sets up and tears down resources"""
    global camunda_client
    global process_definition_key

    # Startup: Initialize Camunda client
    camunda_client = CamundaAsyncClient(
        configuration={"CAMUNDA_REST_ADDRESS": settings.camunda_rest_address}
    )
    logger.info(
        f"Camunda client initialized (CAMUNDA_REST_ADDRESS: {settings.camunda_rest_address})"
    )

    process_definition_key = await deploy_loan_process(camunda_client)

    await run_workers(camunda_client)
    yield

    # Shutdown: Clean up resources
    # if camunda_client:
    #     # Stop any running workers
    #     for worker in camunda_client._workers:
    #         worker.stop()
    #     print("Camunda client shutdown")


app = FastAPI(
    title="Camunda Orchestration API",
    description="FastAPI demo for Camunda Python SDK - Week 2",
    version="0.1.0",
    lifespan=lifespan,
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8088",
        "http://localhost:8088",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend (optional - for serving frontend directly)
frontend_path = Path(__file__).parent / "frontend"
if frontend_path.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_path)), name="frontend")


@app.get("/")
async def root():
    """Root endpoint - serves frontend if available, otherwise API information"""
    frontend_index = Path(__file__).parent / "frontend" / "index.html"
    if frontend_index.exists():
        return FileResponse(frontend_index, media_type="text/html")
    return {
        "message": "Camunda Orchestration API - Week 2 Demo",
        "docs": "/docs",
        "version": "0.1.0",
        "frontend": "/frontend/index.html",
    }

class LoanApplicationRequest(BaseModel):
    variables: dict[str, Any]


@app.post(
    "/loan-application",
    response_model=None,
    status_code=201,
)
async def loan_application(request: LoanApplicationRequest):
    """Create a new process instance and poll for completion"""
    if not camunda_client:
        raise HTTPException(status_code=500, detail="Camunda client not initialized")

    try:
        # Create the process instance
        process_instance = await camunda_client.create_process_instance(
            data=Processcreationbykey(
                process_definition_key=process_definition_key,
                variables=ProcesscreationbyidVariables.from_dict(request.variables),
            )
        )

        start_time = datetime.now()
        logger.info(f"Process instance created: {process_instance.process_instance_key}")

        # Poll for up to 10 seconds to see if the process completes
        # This polling pattern is not recommended for production. Better would be to put a REST task
        # in the model to do a webhook callback on completion. But for this demo, we use polling.
        max_attempts = 10
        poll_interval = 1.0  # seconds

        for attempt in range(max_attempts):
            # Wait before polling (except first attempt)
            if attempt > 0:
                await asyncio.sleep(poll_interval)

            # Search for completed process instance
            search_result = await camunda_client.search_process_instances(
                data=SearchProcessInstancesData(
                    filter_=SearchProcessInstancesDataFilter(
                        process_instance_key=process_instance.process_instance_key,
                        state=StateExactmatch3.COMPLETED,
                    )
                )
            )

            # If we found a completed instance, fetch variables and build response
            if search_result.items and len(search_result.items) > 0:
                logger.info(f"Process {process_instance.process_instance_key} completed after {(datetime.now() - start_time).total_seconds():.1f}s")

                # Fetch all variables for the completed process instance
                variables_result = await camunda_client.search_variables(
                    data=SearchVariablesData(
                        filter_=SearchVariablesDataFilter(
                            process_instance_key=process_instance.process_instance_key
                        )
                    ),
                    truncate_values=False
                )

                # Convert variables list to a dictionary for easy access
                variables_dict: dict[str, Any] = {}
                if variables_result.items:
                    for var in variables_result.items:
                        if var.name:
                            # Parse JSON values
                            try:
                                var_value = var.value if var.value else None
                                variables_dict[var.name] = json.loads(var_value) if var_value else None
                            except (json.JSONDecodeError, TypeError):
                                variables_dict[var.name] = var.value

                # Build email-like response based on approval status
                applicant_name = f"{variables_dict.get('applicantFirstName', '')} {variables_dict.get('applicantLastName', '')}".strip()
                email = variables_dict.get('applicantEmail', '')
                loan_approved = variables_dict.get('loanApproved', False)

                if loan_approved:
                    # Approval response
                    logger.info(f"Loan APPROVED for {applicant_name} - Amount: ${variables_dict.get('loanAmount', 0):,.0f}, Rate: {variables_dict.get('interestRate')}%")
                    return {
                        "status": "approved",
                        "subject": "Loan Application Approved! 🎉",
                        "message": f"Dear {applicant_name},\n\n"
                                   f"Congratulations! Your loan application has been approved.\n\n"
                                   f"Loan Details:\n"
                                   f"  Amount: ${variables_dict.get('loanAmount', 0):,.2f}\n"
                                   f"  Interest Rate: {variables_dict.get('interestRate', 0)}%\n"
                                   f"  Risk Level: {variables_dict.get('riskLevel', 'N/A')}\n\n"
                                   f"Next steps: Our team will contact you within 24 hours to finalize the loan.\n\n"
                                   f"Best regards,\n"
                                   f"QuickLoan Bank",
                        "email": email,
                        "loanAmount": variables_dict.get('loanAmount'),
                        "interestRate": variables_dict.get('interestRate'),
                        "riskLevel": variables_dict.get('riskLevel'),
                    }
                else:
                    # Rejection response
                    rejection_reason = variables_dict.get('rejectionReason', 'Application does not meet our criteria')
                    logger.info(f"Loan REJECTED for {applicant_name} - Reason: {rejection_reason}")
                    return {
                        "status": "rejected",
                        "subject": "Loan Application Status Update",
                        "message": f"Dear {applicant_name},\n\n"
                                   f"Thank you for your interest in QuickLoan Bank.\n\n"
                                   f"After careful review, we are unable to approve your loan application at this time.\n\n"
                                   f"Reason: {rejection_reason}\n\n"
                                   f"You may reapply after 90 days or contact us to discuss alternative options.\n\n"
                                   f"Best regards,\n"
                                   f"QuickLoan Bank",
                        "email": email,
                        "rejectionReason": rejection_reason,
                    }

        # If we didn't find a completed instance within 10 seconds, return a fallback message
        total_elapsed = (datetime.now() - start_time).total_seconds()
        logger.warning(f"Process {process_instance.process_instance_key} did not complete within {total_elapsed:.1f}s - returning processing response")
        return {
            "status": "processing",
            "subject": "Loan Application Received",
            "message": "Thank you. We are processing your application. We will email you within 24 hours with the outcome.",
            "process_instance_key": process_instance.process_instance_key,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create process instance: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
