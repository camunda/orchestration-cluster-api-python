from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.variable_history_item_search_query import VariableHistoryItemSearchQuery
from ...models.variable_history_item_search_query_result import (
    VariableHistoryItemSearchQueryResult,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["truncateValues"] = truncate_values
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/variables/history/search",
        "params": params,
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | VariableHistoryItemSearchQueryResult | None:
    if response.status_code == 200:
        response_200 = VariableHistoryItemSearchQueryResult.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        try:
            response_400 = ProblemDetail.from_dict(response.json())
        except Exception:  # undecodable error body: keep the status
            return None
        return response_400
    if response.status_code == 401:
        try:
            response_401 = ProblemDetail.from_dict(response.json())
        except Exception:  # undecodable error body: keep the status
            return None
        return response_401
    if response.status_code == 403:
        try:
            response_403 = ProblemDetail.from_dict(response.json())
        except Exception:  # undecodable error body: keep the status
            return None
        return response_403
    if response.status_code == 500:
        try:
            response_500 = ProblemDetail.from_dict(response.json())
        except Exception:  # undecodable error body: keep the status
            return None
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | VariableHistoryItemSearchQueryResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableHistoryItemSearchQueryResult]:
    """Search variable history

     Search for variable history items, which record the changes made to a variable's
    value over time. The audit log configuration decides which changes are recorded;
    by default, only changes made by users are.

    Results are sorted by `variableHistoryItemKey` ascending by default, which lists the
    changes of one variable from oldest to newest. Across partitions, the key says nothing
    about time: a search that spans partitions, for example by process definition, lists the
    changes of one partition after the other.

    By default, the endpoint truncates long variable values in the response. For the output
    collection of a multi-instance element or an ad-hoc sub-process, the endpoint cuts the
    value at the size limit regardless of the `truncateValues` parameter. The truncation
    size limit is configurable.

    Args:
        truncate_values (bool | Unset):
        body (VariableHistoryItemSearchQuery | Unset): Variable history item search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | VariableHistoryItemSearchQueryResult]
    """
    kwargs = _get_kwargs(body=body, truncate_values=truncate_values)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableHistoryItemSearchQueryResult:
    """Search variable history

     Search for variable history items, which record the changes made to a variable's
    value over time. The audit log configuration decides which changes are recorded;
    by default, only changes made by users are.

    Results are sorted by `variableHistoryItemKey` ascending by default, which lists the
    changes of one variable from oldest to newest. Across partitions, the key says nothing
    about time: a search that spans partitions, for example by process definition, lists the
    changes of one partition after the other.

    By default, the endpoint truncates long variable values in the response. For the output
    collection of a multi-instance element or an ad-hoc sub-process, the endpoint cuts the
    value at the size limit regardless of the `truncateValues` parameter. The truncation
    size limit is configurable.

    Args:
        truncate_values (bool | Unset):
        body (VariableHistoryItemSearchQuery | Unset): Variable history item search query request.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        VariableHistoryItemSearchQueryResult"""
    response = sync_detailed(client=client, body=body, truncate_values=truncate_values)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_variable_history",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_variable_history",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_variable_history",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_variable_history",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="search_variable_history",
        )
    assert response.parsed is not None
    return cast(VariableHistoryItemSearchQueryResult, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableHistoryItemSearchQueryResult]:
    """Search variable history

     Search for variable history items, which record the changes made to a variable's
    value over time. The audit log configuration decides which changes are recorded;
    by default, only changes made by users are.

    Results are sorted by `variableHistoryItemKey` ascending by default, which lists the
    changes of one variable from oldest to newest. Across partitions, the key says nothing
    about time: a search that spans partitions, for example by process definition, lists the
    changes of one partition after the other.

    By default, the endpoint truncates long variable values in the response. For the output
    collection of a multi-instance element or an ad-hoc sub-process, the endpoint cuts the
    value at the size limit regardless of the `truncateValues` parameter. The truncation
    size limit is configurable.

    Args:
        truncate_values (bool | Unset):
        body (VariableHistoryItemSearchQuery | Unset): Variable history item search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | VariableHistoryItemSearchQueryResult]
    """
    kwargs = _get_kwargs(body=body, truncate_values=truncate_values)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: VariableHistoryItemSearchQuery | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableHistoryItemSearchQueryResult:
    """Search variable history

     Search for variable history items, which record the changes made to a variable's
    value over time. The audit log configuration decides which changes are recorded;
    by default, only changes made by users are.

    Results are sorted by `variableHistoryItemKey` ascending by default, which lists the
    changes of one variable from oldest to newest. Across partitions, the key says nothing
    about time: a search that spans partitions, for example by process definition, lists the
    changes of one partition after the other.

    By default, the endpoint truncates long variable values in the response. For the output
    collection of a multi-instance element or an ad-hoc sub-process, the endpoint cuts the
    value at the size limit regardless of the `truncateValues` parameter. The truncation
    size limit is configurable.

    Args:
        truncate_values (bool | Unset):
        body (VariableHistoryItemSearchQuery | Unset): Variable history item search query request.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        VariableHistoryItemSearchQueryResult"""
    response = await asyncio_detailed(
        client=client, body=body, truncate_values=truncate_values
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_variable_history",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_variable_history",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_variable_history",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="search_variable_history",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="search_variable_history",
        )
    assert response.parsed is not None
    return cast(VariableHistoryItemSearchQueryResult, response.parsed)
