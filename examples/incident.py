# Compilable usage examples for incident management.
# These examples are type-checked during build to guard against API regressions.
from __future__ import annotations

from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.models.incident_search_query import (
    IncidentSearchQuery,
)
from camunda_orchestration_sdk.semantic_types import IncidentKey
from camunda_orchestration_sdk.types import Unset


# region SearchIncidents
def search_incidents_example() -> None:
    client = CamundaClient()

    result = client.search_incidents(
        data=IncidentSearchQuery()
    )

    if not isinstance(result.items, Unset):
        for incident in result.items:
            print(f"Incident key: {incident.incident_key}")
# endregion SearchIncidents


# region GetIncident
def get_incident_example() -> None:
    client = CamundaClient()

    incident = client.get_incident(incident_key=IncidentKey("123456"))

    print(f"Incident error type: {incident.error_type}")
# endregion GetIncident


# region ResolveIncident
def resolve_incident_example() -> None:
    client = CamundaClient()

    client.resolve_incident(incident_key=IncidentKey("123456"))
# endregion ResolveIncident
