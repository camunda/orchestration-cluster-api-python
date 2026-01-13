#!/usr/bin/env python
"""
Deploy the loan application BPMN process to Camunda and get the process definition key.
Run this script to deploy the process before using the frontend.
"""
from pathlib import Path
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.semantic_types import ProcessDefinitionKey


async def deploy_loan_process(camunda: CamundaClient) -> ProcessDefinitionKey:
    """Deploy the loan application process and return the process definition key"""

    # Get the BPMN file path
    bpmn_file = Path(__file__).parent / "loan-application-process.bpmn"

    if not bpmn_file.exists():
        raise Exception(f"❌ Error: BPMN file not found at {bpmn_file}")

    print(f"📦 Deploying: {bpmn_file.name}")

    # Deploy the process
    result = await camunda.deploy_resources_from_files_async(files=[str(bpmn_file)])

    if not result.processes:
        raise Exception("❌ Error: No processes were deployed")

    process = result.processes[0]

    print(f"✅ Deployment successful!\n")
    print(f"📋 Deployment Details:")
    print(f"   Deployment Key: {result.deployment_key}")
    print(f"   Tenant ID: {result.tenant_id}")
    print(f"\n🔑 Process Information:")
    print(f"   Process Definition ID: {process.process_definition_id}")
    print(f"   Process Definition Key: {process.process_definition_key}  ⭐ USE THIS!")
    print(f"   Process Version: {process.process_definition_version}")
    print(f"   Resource Name: {process.resource_name}")

    # Update instructions
    print(f"\n📝 Next Step: Visit http://localhost:8000 and submit a loan application")

    return process.process_definition_key
