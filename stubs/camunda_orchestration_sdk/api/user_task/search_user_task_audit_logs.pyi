from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.search_user_task_audit_logs_data import SearchUserTaskAuditLogsData
from ...models.search_user_task_audit_logs_response_200 import (
    SearchUserTaskAuditLogsResponse200,
)
from ...types import UNSET, Response, Unset

def _get_kwargs(
    user_task_key: str, body: SearchUserTaskAuditLogsData | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | SearchUserTaskAuditLogsResponse200 | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | SearchUserTaskAuditLogsResponse200]: ...
def sync_detailed(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskAuditLogsData | Unset = UNSET,
) -> Response[ProblemDetail | SearchUserTaskAuditLogsResponse200]: ...
def sync(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskAuditLogsData | Unset = UNSET,
    **kwargs: Any,
) -> SearchUserTaskAuditLogsResponse200: ...
async def asyncio_detailed(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskAuditLogsData | Unset = UNSET,
) -> Response[ProblemDetail | SearchUserTaskAuditLogsResponse200]: ...
async def asyncio(
    user_task_key: str,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskAuditLogsData | Unset = UNSET,
    **kwargs: Any,
) -> SearchUserTaskAuditLogsResponse200: ...
