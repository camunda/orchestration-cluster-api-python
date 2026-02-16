from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.mapping_rule_update_request import MappingRuleUpdateRequest
from ...models.mapping_rule_update_result import MappingRuleUpdateResult
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset

def _get_kwargs(
    mapping_rule_id: str, body: MappingRuleUpdateRequest | Unset = UNSET
) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> MappingRuleUpdateResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[MappingRuleUpdateResult | ProblemDetail]: ...
def sync_detailed(
    mapping_rule_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleUpdateRequest | Unset = UNSET,
) -> Response[MappingRuleUpdateResult | ProblemDetail]: ...
def sync(
    mapping_rule_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleUpdateRequest | Unset = UNSET,
    **kwargs: Any,
) -> MappingRuleUpdateResult: ...
async def asyncio_detailed(
    mapping_rule_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleUpdateRequest | Unset = UNSET,
) -> Response[MappingRuleUpdateResult | ProblemDetail]: ...
async def asyncio(
    mapping_rule_id: str,
    client: AuthenticatedClient | Client,
    body: MappingRuleUpdateRequest | Unset = UNSET,
    **kwargs: Any,
) -> MappingRuleUpdateResult: ...
