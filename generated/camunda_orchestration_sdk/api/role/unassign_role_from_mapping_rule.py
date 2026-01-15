from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.unassign_role_from_mapping_rule_response_400 import UnassignRoleFromMappingRuleResponse400
from ...models.unassign_role_from_mapping_rule_response_403 import UnassignRoleFromMappingRuleResponse403
from ...models.unassign_role_from_mapping_rule_response_404 import UnassignRoleFromMappingRuleResponse404
from ...models.unassign_role_from_mapping_rule_response_500 import UnassignRoleFromMappingRuleResponse500
from ...models.unassign_role_from_mapping_rule_response_503 import UnassignRoleFromMappingRuleResponse503
from ...types import Response

def _get_kwargs(role_id: str, mapping_rule_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'delete', 'url': '/roles/{role_id}/mapping-rules/{mapping_rule_id}'.format(role_id=quote(str(role_id), safe=''), mapping_rule_id=quote(str(mapping_rule_id), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | UnassignRoleFromMappingRuleResponse400 | UnassignRoleFromMappingRuleResponse403 | UnassignRoleFromMappingRuleResponse404 | UnassignRoleFromMappingRuleResponse500 | UnassignRoleFromMappingRuleResponse503 | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = UnassignRoleFromMappingRuleResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = UnassignRoleFromMappingRuleResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = UnassignRoleFromMappingRuleResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = UnassignRoleFromMappingRuleResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = UnassignRoleFromMappingRuleResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | UnassignRoleFromMappingRuleResponse400 | UnassignRoleFromMappingRuleResponse403 | UnassignRoleFromMappingRuleResponse404 | UnassignRoleFromMappingRuleResponse500 | UnassignRoleFromMappingRuleResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(role_id: str, mapping_rule_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | UnassignRoleFromMappingRuleResponse400 | UnassignRoleFromMappingRuleResponse403 | UnassignRoleFromMappingRuleResponse404 | UnassignRoleFromMappingRuleResponse500 | UnassignRoleFromMappingRuleResponse503]:
    """Unassign a role from a mapping rule

     Unassigns a role from a mapping rule.

    Args:
        role_id (str):
        mapping_rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UnassignRoleFromMappingRuleResponse400 | UnassignRoleFromMappingRuleResponse403 | UnassignRoleFromMappingRuleResponse404 | UnassignRoleFromMappingRuleResponse500 | UnassignRoleFromMappingRuleResponse503]
    """
    kwargs = _get_kwargs(role_id=role_id, mapping_rule_id=mapping_rule_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(role_id: str, mapping_rule_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Unassign a role from a mapping rule

 Unassigns a role from a mapping rule.

Args:
    role_id (str):
    mapping_rule_id (str):

Raises:
    errors.UnassignRoleFromMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromMappingRuleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromMappingRuleNotFound: If the response status code is 404. The role or mapping rule with the given ID was not found.
    errors.UnassignRoleFromMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(role_id=role_id, mapping_rule_id=mapping_rule_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UnassignRoleFromMappingRuleBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.UnassignRoleFromMappingRuleForbidden(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UnassignRoleFromMappingRuleNotFound(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UnassignRoleFromMappingRuleInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UnassignRoleFromMappingRuleServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(role_id: str, mapping_rule_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | UnassignRoleFromMappingRuleResponse400 | UnassignRoleFromMappingRuleResponse403 | UnassignRoleFromMappingRuleResponse404 | UnassignRoleFromMappingRuleResponse500 | UnassignRoleFromMappingRuleResponse503]:
    """Unassign a role from a mapping rule

     Unassigns a role from a mapping rule.

    Args:
        role_id (str):
        mapping_rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UnassignRoleFromMappingRuleResponse400 | UnassignRoleFromMappingRuleResponse403 | UnassignRoleFromMappingRuleResponse404 | UnassignRoleFromMappingRuleResponse500 | UnassignRoleFromMappingRuleResponse503]
    """
    kwargs = _get_kwargs(role_id=role_id, mapping_rule_id=mapping_rule_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(role_id: str, mapping_rule_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Unassign a role from a mapping rule

 Unassigns a role from a mapping rule.

Args:
    role_id (str):
    mapping_rule_id (str):

Raises:
    errors.UnassignRoleFromMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromMappingRuleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromMappingRuleNotFound: If the response status code is 404. The role or mapping rule with the given ID was not found.
    errors.UnassignRoleFromMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(role_id=role_id, mapping_rule_id=mapping_rule_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.UnassignRoleFromMappingRuleBadRequest(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.UnassignRoleFromMappingRuleForbidden(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.UnassignRoleFromMappingRuleNotFound(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.UnassignRoleFromMappingRuleInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.UnassignRoleFromMappingRuleServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(UnassignRoleFromMappingRuleResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed