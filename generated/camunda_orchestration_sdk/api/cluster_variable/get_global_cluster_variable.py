from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_variable_result import ClusterVariableResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(name: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cluster-variables/global/{name}".format(
            name=quote(str(name), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterVariableResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = ClusterVariableResult.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = ProblemDetail.from_dict(response.json())
        return response_403
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
) -> Response[ClusterVariableResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str, *, client: AuthenticatedClient | Client
) -> Response[ClusterVariableResult | ProblemDetail]:
    """Get a global-scoped cluster variable

     Get a global-scoped cluster variable.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterVariableResult | ProblemDetail]
    """
    kwargs = _get_kwargs(name=name)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    name: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterVariableResult:
    """Get a global-scoped cluster variable

     Get a global-scoped cluster variable.

    Args:
        name (str):

    Raises:
        errors.GetGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
        errors.GetGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterVariableResult"""
    response = sync_detailed(name=name, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetGlobalClusterVariableBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetGlobalClusterVariableUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetGlobalClusterVariableForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetGlobalClusterVariableNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetGlobalClusterVariableInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ClusterVariableResult, response.parsed)


async def asyncio_detailed(
    name: str, *, client: AuthenticatedClient | Client
) -> Response[ClusterVariableResult | ProblemDetail]:
    """Get a global-scoped cluster variable

     Get a global-scoped cluster variable.

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterVariableResult | ProblemDetail]
    """
    kwargs = _get_kwargs(name=name)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    name: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ClusterVariableResult:
    """Get a global-scoped cluster variable

     Get a global-scoped cluster variable.

    Args:
        name (str):

    Raises:
        errors.GetGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
        errors.GetGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterVariableResult"""
    response = await asyncio_detailed(name=name, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetGlobalClusterVariableBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetGlobalClusterVariableUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetGlobalClusterVariableForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetGlobalClusterVariableNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetGlobalClusterVariableInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ClusterVariableResult, response.parsed)
