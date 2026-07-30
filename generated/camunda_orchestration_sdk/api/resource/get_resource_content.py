from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(resource_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/resources/{resource_key}/content".format(
            resource_key=quote(str(resource_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | str | None:
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    resource_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | str]:
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
        Response[ProblemDetail | str]
    """
    kwargs = _get_kwargs(resource_key=resource_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    resource_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> str:
    """Get resource content

     Returns the content of a deployed resource.
    :::info
    Currently, this endpoint only supports RPA resources.
    :::

    Args:
        resource_key (str): The system-assigned key for this resource.

    Raises:
        errors.NotFoundError: If the response status code is 404. A resource with the given key was not found.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        str"""
    response = sync_detailed(resource_key=resource_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_resource_content",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_resource_content",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="get_resource_content"
        )
    assert response.parsed is not None
    return cast(str, response.parsed)


async def asyncio_detailed(
    resource_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | str]:
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
        Response[ProblemDetail | str]
    """
    kwargs = _get_kwargs(resource_key=resource_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    resource_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> str:
    """Get resource content

     Returns the content of a deployed resource.
    :::info
    Currently, this endpoint only supports RPA resources.
    :::

    Args:
        resource_key (str): The system-assigned key for this resource.

    Raises:
        errors.NotFoundError: If the response status code is 404. A resource with the given key was not found.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        str"""
    response = await asyncio_detailed(resource_key=resource_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_resource_content",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="get_resource_content",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="get_resource_content"
        )
    assert response.parsed is not None
    return cast(str, response.parsed)
