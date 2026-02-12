from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.search_batch_operation_items_data import SearchBatchOperationItemsData
from ...models.search_batch_operation_items_response_200 import SearchBatchOperationItemsResponse200
from ...models.search_batch_operation_items_response_400 import SearchBatchOperationItemsResponse400
from ...models.search_batch_operation_items_response_500 import SearchBatchOperationItemsResponse500
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: SearchBatchOperationItemsData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/batch-operation-items/search'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> SearchBatchOperationItemsResponse200 | SearchBatchOperationItemsResponse400 | SearchBatchOperationItemsResponse500 | None:
    if response.status_code == 200:
        response_200 = SearchBatchOperationItemsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = SearchBatchOperationItemsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 500:
        response_500 = SearchBatchOperationItemsResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[SearchBatchOperationItemsResponse200 | SearchBatchOperationItemsResponse400 | SearchBatchOperationItemsResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: SearchBatchOperationItemsData | Unset=UNSET) -> Response[SearchBatchOperationItemsResponse200 | SearchBatchOperationItemsResponse400 | SearchBatchOperationItemsResponse500]:
    """Search batch operation items

     Search for batch operation items based on given criteria.

    Args:
        body (SearchBatchOperationItemsData | Unset): Batch operation item search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchBatchOperationItemsResponse200 | SearchBatchOperationItemsResponse400 | SearchBatchOperationItemsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: SearchBatchOperationItemsData | Unset=UNSET, **kwargs: Any) -> SearchBatchOperationItemsResponse200:
    """Search batch operation items

 Search for batch operation items based on given criteria.

Args:
    body (SearchBatchOperationItemsData | Unset): Batch operation item search request.

Raises:
    errors.SearchBatchOperationItemsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchBatchOperationItemsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchBatchOperationItemsResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchBatchOperationItemsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchBatchOperationItemsResponse400, response.parsed))
        if response.status_code == 500:
            raise errors.SearchBatchOperationItemsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchBatchOperationItemsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchBatchOperationItemsResponse200, response.parsed)

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: SearchBatchOperationItemsData | Unset=UNSET) -> Response[SearchBatchOperationItemsResponse200 | SearchBatchOperationItemsResponse400 | SearchBatchOperationItemsResponse500]:
    """Search batch operation items

     Search for batch operation items based on given criteria.

    Args:
        body (SearchBatchOperationItemsData | Unset): Batch operation item search request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SearchBatchOperationItemsResponse200 | SearchBatchOperationItemsResponse400 | SearchBatchOperationItemsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: SearchBatchOperationItemsData | Unset=UNSET, **kwargs: Any) -> SearchBatchOperationItemsResponse200:
    """Search batch operation items

 Search for batch operation items based on given criteria.

Args:
    body (SearchBatchOperationItemsData | Unset): Batch operation item search request.

Raises:
    errors.SearchBatchOperationItemsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchBatchOperationItemsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchBatchOperationItemsResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchBatchOperationItemsBadRequest(status_code=response.status_code, content=response.content, parsed=cast(SearchBatchOperationItemsResponse400, response.parsed))
        if response.status_code == 500:
            raise errors.SearchBatchOperationItemsInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(SearchBatchOperationItemsResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchBatchOperationItemsResponse200, response.parsed)