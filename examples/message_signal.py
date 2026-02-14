# Compilable usage examples for message and signal operations.
# These examples are type-checked during build to guard against API regressions.
from __future__ import annotations

from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.models.message_correlation_request import (
    MessageCorrelationRequest,
)
from camunda_orchestration_sdk.models.message_publication_request import (
    MessagePublicationRequest,
)
from camunda_orchestration_sdk.models.signal_broadcast_request import (
    SignalBroadcastRequest,
)
from camunda_orchestration_sdk.types import Unset


# region CorrelateMessage
def correlate_message_example() -> None:
    client = CamundaClient()

    result = client.correlate_message(
        data=MessageCorrelationRequest(
            name="payment-received",
            correlation_key="order-12345",
        )
    )

    if not isinstance(result.message_key, Unset):
        print(f"Message key: {result.message_key}")
# endregion CorrelateMessage


# region PublishMessage
def publish_message_example() -> None:
    client = CamundaClient()

    result = client.publish_message(
        data=MessagePublicationRequest(
            name="order-created",
            correlation_key="order-12345",
            time_to_live=60000,
        )
    )

    if not isinstance(result.message_key, Unset):
        print(f"Message key: {result.message_key}")
# endregion PublishMessage


# region BroadcastSignal
def broadcast_signal_example() -> None:
    client = CamundaClient()

    result = client.broadcast_signal(
        data=SignalBroadcastRequest(
            signal_name="order-cancelled",
        )
    )

    print(f"Signal key: {result.signal_key}")
# endregion BroadcastSignal
