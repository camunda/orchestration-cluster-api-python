from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_mapping_rule_response_401 import DeleteMappingRuleResponse401
from ...models.delete_mapping_rule_response_404 import DeleteMappingRuleResponse404
from ...models.delete_mapping_rule_response_500 import DeleteMappingRuleResponse500
from ...models.delete_mapping_rule_response_503 import DeleteMappingRuleResponse503
from ...types import Response

def _get_kwargs(mapping_rule_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'delete', 'url': '/mapping-rules/{mapping_rule_id}'.format(mapping_rule_id=quote(str(mapping_rule_id), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | DeleteMappingRuleResponse401 | DeleteMappingRuleResponse404 | DeleteMappingRuleResponse500 | DeleteMappingRuleResponse503 | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 401:
        response_401 = DeleteMappingRuleResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 404:
        response_404 = DeleteMappingRuleResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = DeleteMappingRuleResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = DeleteMappingRuleResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | DeleteMappingRuleResponse401 | DeleteMappingRuleResponse404 | DeleteMappingRuleResponse500 | DeleteMappingRuleResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(mapping_rule_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | DeleteMappingRuleResponse401 | DeleteMappingRuleResponse404 | DeleteMappingRuleResponse500 | DeleteMappingRuleResponse503]:
    """Delete a mapping rule

     Deletes the mapping rule with the given ID.

    Args:
        mapping_rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteMappingRuleResponse401 | DeleteMappingRuleResponse404 | DeleteMappingRuleResponse500 | DeleteMappingRuleResponse503]
    """
    kwargs = _get_kwargs(mapping_rule_id=mapping_rule_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(mapping_rule_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Delete a mapping rule

 Deletes the mapping rule with the given ID.

Args:
    mapping_rule_id (str):

Raises:
    errors.DeleteMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteMappingRuleNotFound: If the response status code is 404. The mapping rule with the mappingRuleId was not found.
    errors.DeleteMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(mapping_rule_id=mapping_rule_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteMappingRuleUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(DeleteMappingRuleResponse401, response.parsed))
        if response.status_code == 404:
            raise errors.DeleteMappingRuleNotFound(status_code=response.status_code, content=response.content, parsed=cast(DeleteMappingRuleResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.DeleteMappingRuleInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(DeleteMappingRuleResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.DeleteMappingRuleServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(DeleteMappingRuleResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(mapping_rule_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | DeleteMappingRuleResponse401 | DeleteMappingRuleResponse404 | DeleteMappingRuleResponse500 | DeleteMappingRuleResponse503]:
    """Delete a mapping rule

     Deletes the mapping rule with the given ID.

    Args:
        mapping_rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteMappingRuleResponse401 | DeleteMappingRuleResponse404 | DeleteMappingRuleResponse500 | DeleteMappingRuleResponse503]
    """
    kwargs = _get_kwargs(mapping_rule_id=mapping_rule_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(mapping_rule_id: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Delete a mapping rule

 Deletes the mapping rule with the given ID.

Args:
    mapping_rule_id (str):

Raises:
    errors.DeleteMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteMappingRuleNotFound: If the response status code is 404. The mapping rule with the mappingRuleId was not found.
    errors.DeleteMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(mapping_rule_id=mapping_rule_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteMappingRuleUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(DeleteMappingRuleResponse401, response.parsed))
        if response.status_code == 404:
            raise errors.DeleteMappingRuleNotFound(status_code=response.status_code, content=response.content, parsed=cast(DeleteMappingRuleResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.DeleteMappingRuleInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(DeleteMappingRuleResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.DeleteMappingRuleServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(DeleteMappingRuleResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed