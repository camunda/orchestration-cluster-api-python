from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_definition_instance_statistics_query import (
    ProcessDefinitionInstanceStatisticsQuery,
)
from ...models.process_definition_instance_statistics_query_result import (
    ProcessDefinitionInstanceStatisticsQueryResult,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/process-definitions/statistics/process-instances",
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult | None:
    if response.status_code == 200:
        response_200 = ProcessDefinitionInstanceStatisticsQueryResult.from_dict(
            response.json()
        )
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
) -> Response[ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult]:
    """Get process instance statistics

     Get statistics about process instances, grouped by process definition and tenant.

    Args:
        body (ProcessDefinitionInstanceStatisticsQuery | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionInstanceStatisticsQueryResult:
    """Get process instance statistics

     Get statistics about process instances, grouped by process definition and tenant.

    Args:
        body (ProcessDefinitionInstanceStatisticsQuery | Unset):

    Raises:
        errors.GetProcessDefinitionInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessDefinitionInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessDefinitionInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessDefinitionInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ProcessDefinitionInstanceStatisticsQueryResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessDefinitionInstanceStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessDefinitionInstanceStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessDefinitionInstanceStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessDefinitionInstanceStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ProcessDefinitionInstanceStatisticsQueryResult, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult]:
    """Get process instance statistics

     Get statistics about process instances, grouped by process definition and tenant.

    Args:
        body (ProcessDefinitionInstanceStatisticsQuery | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | ProcessDefinitionInstanceStatisticsQueryResult]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionInstanceStatisticsQueryResult:
    """Get process instance statistics

     Get statistics about process instances, grouped by process definition and tenant.

    Args:
        body (ProcessDefinitionInstanceStatisticsQuery | Unset):

    Raises:
        errors.GetProcessDefinitionInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessDefinitionInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessDefinitionInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessDefinitionInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ProcessDefinitionInstanceStatisticsQueryResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessDefinitionInstanceStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessDefinitionInstanceStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessDefinitionInstanceStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessDefinitionInstanceStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ProcessDefinitionInstanceStatisticsQueryResult, response.parsed)
