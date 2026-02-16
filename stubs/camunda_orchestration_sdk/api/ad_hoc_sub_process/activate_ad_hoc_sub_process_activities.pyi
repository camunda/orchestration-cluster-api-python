from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.ad_hoc_sub_process_activate_activities_instruction import (
    AdHocSubProcessActivateActivitiesInstruction,
)
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(
    ad_hoc_sub_process_instance_key: str,
    body: AdHocSubProcessActivateActivitiesInstruction,
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]: ...
def sync_detailed(
    ad_hoc_sub_process_instance_key: str,
    client: AuthenticatedClient | Client,
    body: AdHocSubProcessActivateActivitiesInstruction,
) -> Response[Any | ProblemDetail]: ...
def sync(
    ad_hoc_sub_process_instance_key: str,
    client: AuthenticatedClient | Client,
    body: AdHocSubProcessActivateActivitiesInstruction,
    **kwargs: Any,
) -> None: ...
async def asyncio_detailed(
    ad_hoc_sub_process_instance_key: str,
    client: AuthenticatedClient | Client,
    body: AdHocSubProcessActivateActivitiesInstruction,
) -> Response[Any | ProblemDetail]: ...
async def asyncio(
    ad_hoc_sub_process_instance_key: str,
    client: AuthenticatedClient | Client,
    body: AdHocSubProcessActivateActivitiesInstruction,
    **kwargs: Any,
) -> None: ...
