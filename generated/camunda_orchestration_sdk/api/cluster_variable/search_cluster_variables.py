from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cluster_variable_search_query_request import (
    ClusterVariableSearchQueryRequest,
)
from ...models.cluster_variable_search_query_result import (
    ClusterVariableSearchQueryResult,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ClusterVariableSearchQueryRequest | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["truncateValues"] = truncate_values
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cluster-variables/search",
        "params": params,
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClusterVariableSearchQueryResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = ClusterVariableSearchQueryResult.from_dict(response.json())
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
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClusterVariableSearchQueryResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ClusterVariableSearchQueryRequest | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ClusterVariableSearchQueryResult | ProblemDetail]:
    """Search for cluster variables based on given criteria. By default, long variable values in the
    response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (ClusterVariableSearchQueryRequest | Unset): Cluster variable search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterVariableSearchQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, truncate_values=truncate_values)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ClusterVariableSearchQueryRequest | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterVariableSearchQueryResult:
    """Search for cluster variables based on given criteria. By default, long variable values in the
    response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (ClusterVariableSearchQueryRequest | Unset): Cluster variable search query request.

    Raises:
        errors.SearchClusterVariablesBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchClusterVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchClusterVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchClusterVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterVariableSearchQueryResult"""
    response = sync_detailed(client=client, body=body, truncate_values=truncate_values)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchClusterVariablesBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchClusterVariablesUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchClusterVariablesForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchClusterVariablesInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ClusterVariableSearchQueryResult, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ClusterVariableSearchQueryRequest | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ClusterVariableSearchQueryResult | ProblemDetail]:
    """Search for cluster variables based on given criteria. By default, long variable values in the
    response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (ClusterVariableSearchQueryRequest | Unset): Cluster variable search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClusterVariableSearchQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body, truncate_values=truncate_values)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ClusterVariableSearchQueryRequest | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> ClusterVariableSearchQueryResult:
    """Search for cluster variables based on given criteria. By default, long variable values in the
    response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (ClusterVariableSearchQueryRequest | Unset): Cluster variable search query request.

    Raises:
        errors.SearchClusterVariablesBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchClusterVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchClusterVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchClusterVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ClusterVariableSearchQueryResult"""
    response = await asyncio_detailed(
        client=client, body=body, truncate_values=truncate_values
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchClusterVariablesBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchClusterVariablesUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchClusterVariablesForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchClusterVariablesInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ClusterVariableSearchQueryResult, response.parsed)
