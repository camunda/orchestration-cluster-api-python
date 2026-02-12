from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_mapping_rule_data import CreateMappingRuleData
from ...models.create_mapping_rule_response_201 import CreateMappingRuleResponse201
from ...models.create_mapping_rule_response_400 import CreateMappingRuleResponse400
from ...models.create_mapping_rule_response_403 import CreateMappingRuleResponse403
from ...models.create_mapping_rule_response_404 import CreateMappingRuleResponse404
from ...models.create_mapping_rule_response_500 import CreateMappingRuleResponse500
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: CreateMappingRuleData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/mapping-rules'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CreateMappingRuleResponse201 | CreateMappingRuleResponse400 | CreateMappingRuleResponse403 | CreateMappingRuleResponse404 | CreateMappingRuleResponse500 | None:
    if response.status_code == 201:
        response_201 = CreateMappingRuleResponse201.from_dict(response.json())
        return response_201
    if response.status_code == 400:
        response_400 = CreateMappingRuleResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = CreateMappingRuleResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = CreateMappingRuleResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = CreateMappingRuleResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CreateMappingRuleResponse201 | CreateMappingRuleResponse400 | CreateMappingRuleResponse403 | CreateMappingRuleResponse404 | CreateMappingRuleResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: CreateMappingRuleData | Unset=UNSET) -> Response[CreateMappingRuleResponse201 | CreateMappingRuleResponse400 | CreateMappingRuleResponse403 | CreateMappingRuleResponse404 | CreateMappingRuleResponse500]:
    """Create mapping rule

     Create a new mapping rule

    Args:
        body (CreateMappingRuleData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateMappingRuleResponse201 | CreateMappingRuleResponse400 | CreateMappingRuleResponse403 | CreateMappingRuleResponse404 | CreateMappingRuleResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: CreateMappingRuleData | Unset=UNSET, **kwargs: Any) -> CreateMappingRuleResponse201:
    """Create mapping rule

 Create a new mapping rule

Args:
    body (CreateMappingRuleData | Unset):

Raises:
    errors.CreateMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateMappingRuleForbidden: If the response status code is 403. The request to create a mapping rule was denied. More details are provided in the response body.
    errors.CreateMappingRuleNotFound: If the response status code is 404. The request to create a mapping rule was denied.
    errors.CreateMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateMappingRuleResponse201"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateMappingRuleBadRequest(status_code=response.status_code, content=response.content, parsed=cast(CreateMappingRuleResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.CreateMappingRuleForbidden(status_code=response.status_code, content=response.content, parsed=cast(CreateMappingRuleResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.CreateMappingRuleNotFound(status_code=response.status_code, content=response.content, parsed=cast(CreateMappingRuleResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.CreateMappingRuleInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(CreateMappingRuleResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateMappingRuleResponse201, response.parsed)

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: CreateMappingRuleData | Unset=UNSET) -> Response[CreateMappingRuleResponse201 | CreateMappingRuleResponse400 | CreateMappingRuleResponse403 | CreateMappingRuleResponse404 | CreateMappingRuleResponse500]:
    """Create mapping rule

     Create a new mapping rule

    Args:
        body (CreateMappingRuleData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateMappingRuleResponse201 | CreateMappingRuleResponse400 | CreateMappingRuleResponse403 | CreateMappingRuleResponse404 | CreateMappingRuleResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: CreateMappingRuleData | Unset=UNSET, **kwargs: Any) -> CreateMappingRuleResponse201:
    """Create mapping rule

 Create a new mapping rule

Args:
    body (CreateMappingRuleData | Unset):

Raises:
    errors.CreateMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateMappingRuleForbidden: If the response status code is 403. The request to create a mapping rule was denied. More details are provided in the response body.
    errors.CreateMappingRuleNotFound: If the response status code is 404. The request to create a mapping rule was denied.
    errors.CreateMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateMappingRuleResponse201"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateMappingRuleBadRequest(status_code=response.status_code, content=response.content, parsed=cast(CreateMappingRuleResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.CreateMappingRuleForbidden(status_code=response.status_code, content=response.content, parsed=cast(CreateMappingRuleResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.CreateMappingRuleNotFound(status_code=response.status_code, content=response.content, parsed=cast(CreateMappingRuleResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.CreateMappingRuleInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(CreateMappingRuleResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateMappingRuleResponse201, response.parsed)