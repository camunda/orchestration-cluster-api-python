"""Integration tests: publishing a message from within a job handler via ConnectedJobContext.client.

The BPMN process (message_handler_test.bpmn) has:
  Start → ServiceTask(jobType=<unique>) → IntermediateMessageCatch(correlationKey) → End

The job handler uses ``job.client.publish_message(...)`` to unblock the message catch event.
We use ``await_completion=True`` on ``create_process_instance`` so the test call blocks
until the full process completes (or times out).

Two variants are tested:
  1. async handler (execution_strategy="async")
  2. sync handler  (execution_strategy="thread") — job.client is a sync CamundaClient,
     so methods can be called directly without async.
"""

import os
import uuid

import pytest

from camunda_orchestration_sdk import (
    CamundaAsyncClient,
    ConnectedJobContext,
    MessagePublicationRequest,
    ProcessCreationByKey,
    ProcessInstanceCreationInstructionByKeyVariables,
    ProcessInstanceKey,
    SyncJobContext,
    WorkerConfig,
)

pytestmark = pytest.mark.skipif(
    os.environ.get("CAMUNDA_INTEGRATION") != "1",
    reason="Integration tests are disabled unless CAMUNDA_INTEGRATION=1",
)

BPMN_PATH = "./tests/integration/resources/message_handler_test.bpmn"


async def _safe_cancel(
    client: CamundaAsyncClient, process_instance_key: ProcessInstanceKey | None
) -> None:
    if process_instance_key is None:
        return
    try:
        await client.cancel_process_instance(process_instance_key=process_instance_key)
    except Exception:
        pass


@pytest.mark.asyncio
async def test_async_handler_publishes_message():
    """Async job handler uses job.client to publish a message that unblocks the process."""
    job_type = f"msg-handler-async-{uuid.uuid4()}"
    correlation_key = f"corr-{uuid.uuid4()}"
    message_name = f"msg-{uuid.uuid4()}"
    instance_key = None

    async with CamundaAsyncClient() as client:
        deployment = await client.deploy_resources_from_files([BPMN_PATH])
        process_def = deployment.processes[0]

        async def handler(job: ConnectedJobContext) -> dict[str, object]:
            await job.client.publish_message(
                data=MessagePublicationRequest(
                    name=message_name,
                    correlation_key=correlation_key,
                    time_to_live=60_000,
                )
            )
            return {"handlerRan": True}

        client.create_job_worker(
            config=WorkerConfig(
                job_type=job_type,
                job_timeout_milliseconds=30_000,
            ),
            callback=handler,
            execution_strategy="async",
        )

        variables = ProcessInstanceCreationInstructionByKeyVariables()
        variables["jobType"] = job_type
        variables["correlationKey"] = correlation_key
        variables["messageName"] = message_name

        try:
            result = await client.create_process_instance(
                data=ProcessCreationByKey(
                    process_definition_key=process_def.process_definition_key,
                    variables=variables,
                    await_completion=True,
                    request_timeout=30_000,
                )
            )
            instance_key = result.process_instance_key
            # If we get here, the process completed — the message was published
            # successfully from the async handler.
        finally:
            await _safe_cancel(client, instance_key)


@pytest.mark.asyncio
async def test_thread_handler_publishes_message():
    """Sync (thread) job handler uses job.client to publish a message that unblocks the process."""
    job_type = f"msg-handler-thread-{uuid.uuid4()}"
    correlation_key = f"corr-{uuid.uuid4()}"
    message_name = f"msg-{uuid.uuid4()}"
    instance_key = None

    async with CamundaAsyncClient() as client:
        deployment = await client.deploy_resources_from_files([BPMN_PATH])
        process_def = deployment.processes[0]

        def handler(job: SyncJobContext) -> dict[str, object]:
            # In thread strategy, job.client is a sync CamundaClient —
            # call methods directly, no async needed.
            job.client.publish_message(
                data=MessagePublicationRequest(
                    name=message_name,
                    correlation_key=correlation_key,
                    time_to_live=60_000,
                )
            )
            return {"handlerRan": True}

        client.create_job_worker(
            config=WorkerConfig(
                job_type=job_type,
                job_timeout_milliseconds=30_000,
            ),
            callback=handler,
            execution_strategy="thread",
        )

        variables = ProcessInstanceCreationInstructionByKeyVariables()
        variables["jobType"] = job_type
        variables["correlationKey"] = correlation_key
        variables["messageName"] = message_name

        try:
            result = await client.create_process_instance(
                data=ProcessCreationByKey(
                    process_definition_key=process_def.process_definition_key,
                    variables=variables,
                    await_completion=True,
                    request_timeout=30_000,
                )
            )
            instance_key = result.process_instance_key
        finally:
            await _safe_cancel(client, instance_key)
