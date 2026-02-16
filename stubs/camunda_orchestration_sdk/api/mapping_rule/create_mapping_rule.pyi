from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.mapping_rule_create_request import MappingRuleCreateRequest
from ...models.mapping_rule_update_result import MappingRuleUpdateResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(body: MappingRuleCreateRequest | Unset = UNSET) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> MappingRuleUpdateResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[MappingRuleUpdateResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: MappingRuleCreateRequest | Unset = UNSET
) -> Response[MappingRuleUpdateResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: MappingRuleCreateRequest | Unset = UNSET,
    **kwargs: Any,
) -> MappingRuleUpdateResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: MappingRuleCreateRequest | Unset = UNSET
) -> Response[MappingRuleUpdateResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: MappingRuleCreateRequest | Unset = UNSET,
    **kwargs: Any,
) -> MappingRuleUpdateResult: ...
