#!/usr/bin/env python
"""
Simple test script for the Camunda FastAPI demo app.
Run this after starting the FastAPI server with: python -m demo.week_2.main
"""
import asyncio
import json
from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.models.processcreationbykey import Processcreationbykey


async def main():
    print("🚀 Testing Camunda Python SDK\n")

    # Initialize client (note: base_url should include /v2)
    camunda = CamundaAsyncClient(base_url="http://localhost:8080/v2", token=None)
    print("✅ Camunda client initialized")

    # Step 1: Deploy a process
    print("\n📦 Step 1: Deploying BPMN process...")
    try:
        deployed_resources = await camunda.deploy_resources_from_files(
            files=["./tests/integration/resources/job_worker_load_test_process_1.bpmn"]
        )

        process_definition = deployed_resources.processes[0]
        process_definition_key = process_definition.process_definition_key
        process_definition_id = process_definition.process_definition_id

        print(f"✅ Deployed: {process_definition_id}")
        print(f"   Process Key: {process_definition_key}")
        print(f"   Deployment Key: {deployed_resources.deployment_key}")
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return

    # Step 2: Create a process instance
    print("\n🎬 Step 2: Creating process instance...")
    try:
        process_instance = await camunda.create_process_instance(
            data=Processcreationbykey(
                process_definition_key=process_definition_key
            )
        )

        print(f"✅ Created instance: {process_instance.process_instance_key}")
        print(f"   Process Definition Key: {process_instance.process_definition_key}")
    except Exception as e:
        print(f"❌ Failed to create instance: {e}")
        return

    # Step 3: Check topology
    print("\n🔍 Step 3: Checking Camunda topology...")
    try:
        topology = await camunda.get_topology()
        print(f"✅ Cluster Size: {topology.cluster_size}")
        print(f"   Partitions: {topology.partitions_count}")
        print(f"   Version: {topology.brokers[0].version}")
    except Exception as e:
        print(f"❌ Failed to get topology: {e}")

    print("\n✨ All tests completed!\n")


if __name__ == "__main__":
    asyncio.run(main())
