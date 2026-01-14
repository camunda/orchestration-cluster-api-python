from http import HTTPStatus
from io import BytesIO
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_resource_content_response_404 import GetResourceContentResponse404
from ...models.get_resource_content_response_500 import GetResourceContentResponse500
from ...types import File, Response

def _get_kwargs(resource_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/resources/{resource_key}/content'.format(resource_key=quote(str(resource_key), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> File | GetResourceContentResponse404 | GetResourceContentResponse500 | None:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))
        return response_200
    if response.status_code == 404:
        response_404 = GetResourceContentResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetResourceContentResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[File | GetResourceContentResponse404 | GetResourceContentResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(resource_key: str, *, client: AuthenticatedClient | Client) -> Response[File | GetResourceContentResponse404 | GetResourceContentResponse500]:
    """Get resource content

     Returns the content of a deployed resource.
    :::info
    Currently, this endpoint only supports RPA resources.
    :::

    Args:
        resource_key (str): The system-assigned key for this resource.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File | GetResourceContentResponse404 | GetResourceContentResponse500]
    """
    kwargs = _get_kwargs(resource_key=resource_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(resource_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> File:
    """Get resource content

 Returns the content of a deployed resource.
:::info
Currently, this endpoint only supports RPA resources.
:::

Args:
    resource_key (str): The system-assigned key for this resource.

Raises:
    errors.GetResourceContentNotFound: If the response status code is 404.
    errors.GetResourceContentInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    File"""
    response = sync_detailed(resource_key=resource_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 404:
            raise errors.GetResourceContentNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetResourceContentResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetResourceContentInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetResourceContentResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(resource_key: str, *, client: AuthenticatedClient | Client) -> Response[File | GetResourceContentResponse404 | GetResourceContentResponse500]:
    """Get resource content

     Returns the content of a deployed resource.
    :::info
    Currently, this endpoint only supports RPA resources.
    :::

    Args:
        resource_key (str): The system-assigned key for this resource.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File | GetResourceContentResponse404 | GetResourceContentResponse500]
    """
    kwargs = _get_kwargs(resource_key=resource_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(resource_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> File:
    """Get resource content

 Returns the content of a deployed resource.
:::info
Currently, this endpoint only supports RPA resources.
:::

Args:
    resource_key (str): The system-assigned key for this resource.

Raises:
    errors.GetResourceContentNotFound: If the response status code is 404.
    errors.GetResourceContentInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    File"""
    response = await asyncio_detailed(resource_key=resource_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 404:
            raise errors.GetResourceContentNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetResourceContentResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetResourceContentInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetResourceContentResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed