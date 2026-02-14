from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.search_variables_data import SearchVariablesData
from ...models.variable_search_query_result import VariableSearchQueryResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: SearchVariablesData | Unset = UNSET, truncate_values: bool | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["truncateValues"] = truncate_values
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/variables/search",
        "params": params,
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | VariableSearchQueryResult | None:
    if response.status_code == 200:
        response_200 = VariableSearchQueryResult.from_dict(response.json())
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
) -> Response[ProblemDetail | VariableSearchQueryResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SearchVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableSearchQueryResult]:
    """Search variables

     Search for process and local variables based on given criteria. By default, long variable values in
    the response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (SearchVariablesData | Unset): Variable search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | VariableSearchQueryResult]
    """
    kwargs = _get_kwargs(body=body, truncate_values=truncate_values)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: SearchVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableSearchQueryResult:
    """Search variables

     Search for process and local variables based on given criteria. By default, long variable values in
    the response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (SearchVariablesData | Unset): Variable search query request.

    Raises:
        errors.SearchVariablesBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        VariableSearchQueryResult"""
    response = sync_detailed(client=client, body=body, truncate_values=truncate_values)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchVariablesBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchVariablesUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchVariablesForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchVariablesInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(VariableSearchQueryResult, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SearchVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableSearchQueryResult]:
    """Search variables

     Search for process and local variables based on given criteria. By default, long variable values in
    the response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (SearchVariablesData | Unset): Variable search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | VariableSearchQueryResult]
    """
    kwargs = _get_kwargs(body=body, truncate_values=truncate_values)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: SearchVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableSearchQueryResult:
    """Search variables

     Search for process and local variables based on given criteria. By default, long variable values in
    the response are truncated.

    Args:
        truncate_values (bool | Unset):
        body (SearchVariablesData | Unset): Variable search query request.

    Raises:
        errors.SearchVariablesBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        VariableSearchQueryResult"""
    response = await asyncio_detailed(
        client=client, body=body, truncate_values=truncate_values
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchVariablesBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchVariablesUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchVariablesForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchVariablesInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(VariableSearchQueryResult, response.parsed)
