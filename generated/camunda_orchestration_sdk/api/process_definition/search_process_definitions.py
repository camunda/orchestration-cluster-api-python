from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_process_definitions_data import SearchProcessDefinitionsData
from ...models.search_process_definitions_response_200 import SearchProcessDefinitionsResponse200
from ...models.search_process_definitions_response_400 import SearchProcessDefinitionsResponse400
from ...models.search_process_definitions_response_401 import SearchProcessDefinitionsResponse401
from ...models.search_process_definitions_response_403 import SearchProcessDefinitionsResponse403
from ...models.search_process_definitions_response_500 import SearchProcessDefinitionsResponse500
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: SearchProcessDefinitionsData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/process-definitions/search'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> SearchProcessDefinitionsResponse200 | SearchProcessDefinitionsResponse400 | SearchProcessDefinitionsResponse401 | SearchProcessDefinitionsResponse403 | SearchProcessDefinitionsResponse500 | None:
    if response.status_code == 200:
        response_200 = SearchProcessDefinitionsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = SearchProcessDefinitionsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = SearchProcessDefinitionsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = SearchProcessDefinitionsResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = SearchProcessDefinitionsResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[SearchProcessDefinitionsResponse200 | SearchProcessDefinitionsResponse400 | SearchProcessDefinitionsResponse401 | SearchProcessDefinitionsResponse403 | SearchProcessDefinitionsResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: SearchProcessDefinitionsData | Unset=UNSET) -> Response[SearchProcessDefinitionsResponse200 | SearchProcessDefinitionsResponse400 | SearchProcessDefinitionsResponse401 | SearchProcessDefinitionsResponse403 | SearchProcessDefinitionsResponse500]:
    """Search process definitions

     Search for process definitions based on given criteria.

    Args:
        body (SearchProcessDefinitionsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchProcessDefinitionsResponse200 | SearchProcessDefinitionsResponse400 | SearchProcessDefinitionsResponse401 | SearchProcessDefinitionsResponse403 | SearchProcessDefinitionsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: SearchProcessDefinitionsData | Unset=UNSET, **kwargs) -> SearchProcessDefinitionsResponse200:
    """Search process definitions

 Search for process definitions based on given criteria.

Args:
    body (SearchProcessDefinitionsData | Unset):

Raises:
    errors.SearchProcessDefinitionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchProcessDefinitionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchProcessDefinitionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchProcessDefinitionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchProcessDefinitionsResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchProcessDefinitionsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchProcessDefinitionsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchProcessDefinitionsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchProcessDefinitionsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchProcessDefinitionsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchProcessDefinitionsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchProcessDefinitionsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchProcessDefinitionsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: SearchProcessDefinitionsData | Unset=UNSET) -> Response[SearchProcessDefinitionsResponse200 | SearchProcessDefinitionsResponse400 | SearchProcessDefinitionsResponse401 | SearchProcessDefinitionsResponse403 | SearchProcessDefinitionsResponse500]:
    """Search process definitions

     Search for process definitions based on given criteria.

    Args:
        body (SearchProcessDefinitionsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchProcessDefinitionsResponse200 | SearchProcessDefinitionsResponse400 | SearchProcessDefinitionsResponse401 | SearchProcessDefinitionsResponse403 | SearchProcessDefinitionsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: SearchProcessDefinitionsData | Unset=UNSET, **kwargs) -> SearchProcessDefinitionsResponse200:
    """Search process definitions

 Search for process definitions based on given criteria.

Args:
    body (SearchProcessDefinitionsData | Unset):

Raises:
    errors.SearchProcessDefinitionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchProcessDefinitionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchProcessDefinitionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchProcessDefinitionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchProcessDefinitionsResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchProcessDefinitionsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchProcessDefinitionsResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.SearchProcessDefinitionsUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(SearchProcessDefinitionsResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.SearchProcessDefinitionsForbidden(status_code=response.status_code, content=response.content, parsed=cast(SearchProcessDefinitionsResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.SearchProcessDefinitionsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchProcessDefinitionsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed