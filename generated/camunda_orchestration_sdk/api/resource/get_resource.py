from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_resource_response_200 import GetResourceResponse200
from ...models.get_resource_response_404 import GetResourceResponse404
from ...models.get_resource_response_500 import GetResourceResponse500
from ...types import Response


def _get_kwargs(resource_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/resources/{resource_key}".format(
            resource_key=quote(str(resource_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetResourceResponse200 | GetResourceResponse404 | GetResourceResponse500 | None:
    if response.status_code == 200:
        response_200 = GetResourceResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 404:
        response_404 = GetResourceResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetResourceResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetResourceResponse200 | GetResourceResponse404 | GetResourceResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    resource_key: str, *, client: AuthenticatedClient | Client
) -> Response[GetResourceResponse200 | GetResourceResponse404 | GetResourceResponse500]:
    """Get resource

     Returns a deployed resource.
    :::info
    Currently, this endpoint only supports RPA resources.
    :::

    Args:
        resource_key (str): The system-assigned key for this resource.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetResourceResponse200 | GetResourceResponse404 | GetResourceResponse500]
    """
    kwargs = _get_kwargs(resource_key=resource_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    resource_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetResourceResponse200:
    """Get resource

     Returns a deployed resource.
    :::info
    Currently, this endpoint only supports RPA resources.
    :::

    Args:
        resource_key (str): The system-assigned key for this resource.

    Raises:
        errors.GetResourceNotFound: If the response status code is 404. A resource with the given key was not found.
        errors.GetResourceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetResourceResponse200"""
    response = sync_detailed(resource_key=resource_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 404:
            raise errors.GetResourceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetResourceResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetResourceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetResourceResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetResourceResponse200, response.parsed)


async def asyncio_detailed(
    resource_key: str, *, client: AuthenticatedClient | Client
) -> Response[GetResourceResponse200 | GetResourceResponse404 | GetResourceResponse500]:
    """Get resource

     Returns a deployed resource.
    :::info
    Currently, this endpoint only supports RPA resources.
    :::

    Args:
        resource_key (str): The system-assigned key for this resource.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetResourceResponse200 | GetResourceResponse404 | GetResourceResponse500]
    """
    kwargs = _get_kwargs(resource_key=resource_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    resource_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetResourceResponse200:
    """Get resource

     Returns a deployed resource.
    :::info
    Currently, this endpoint only supports RPA resources.
    :::

    Args:
        resource_key (str): The system-assigned key for this resource.

    Raises:
        errors.GetResourceNotFound: If the response status code is 404. A resource with the given key was not found.
        errors.GetResourceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetResourceResponse200"""
    response = await asyncio_detailed(resource_key=resource_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 404:
            raise errors.GetResourceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetResourceResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetResourceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetResourceResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetResourceResponse200, response.parsed)
