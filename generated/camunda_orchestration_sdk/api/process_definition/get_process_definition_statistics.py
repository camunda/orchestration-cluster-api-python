from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_definition_element_statistics_query import (
    ProcessDefinitionElementStatisticsQuery,
)
from ...models.process_definition_element_statistics_query_result import (
    ProcessDefinitionElementStatisticsQueryResult,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    process_definition_key: str,
    *,
    body: ProcessDefinitionElementStatisticsQuery | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/process-definitions/{process_definition_key}/statistics/element-instances".format(
            process_definition_key=quote(str(process_definition_key), safe="")
        ),
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessDefinitionElementStatisticsQueryResult | None:
    if response.status_code == 200:
        response_200 = ProcessDefinitionElementStatisticsQueryResult.from_dict(
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
) -> Response[ProblemDetail | ProcessDefinitionElementStatisticsQueryResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    process_definition_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionElementStatisticsQuery | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionElementStatisticsQueryResult]:
    """Get process definition statistics

     Get statistics about elements in currently running process instances by process definition key and
    search filter.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.
        body (ProcessDefinitionElementStatisticsQuery | Unset): Process definition element
            statistics request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | ProcessDefinitionElementStatisticsQueryResult]
    """
    kwargs = _get_kwargs(process_definition_key=process_definition_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    process_definition_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionElementStatisticsQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionElementStatisticsQueryResult:
    """Get process definition statistics

     Get statistics about elements in currently running process instances by process definition key and
    search filter.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.
        body (ProcessDefinitionElementStatisticsQuery | Unset): Process definition element
            statistics request.

    Raises:
        errors.GetProcessDefinitionStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessDefinitionStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessDefinitionStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessDefinitionStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ProcessDefinitionElementStatisticsQueryResult"""
    response = sync_detailed(
        process_definition_key=process_definition_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessDefinitionStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessDefinitionStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessDefinitionStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessDefinitionStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ProcessDefinitionElementStatisticsQueryResult, response.parsed)


async def asyncio_detailed(
    process_definition_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionElementStatisticsQuery | Unset = UNSET,
) -> Response[ProblemDetail | ProcessDefinitionElementStatisticsQueryResult]:
    """Get process definition statistics

     Get statistics about elements in currently running process instances by process definition key and
    search filter.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.
        body (ProcessDefinitionElementStatisticsQuery | Unset): Process definition element
            statistics request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | ProcessDefinitionElementStatisticsQueryResult]
    """
    kwargs = _get_kwargs(process_definition_key=process_definition_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    process_definition_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: ProcessDefinitionElementStatisticsQuery | Unset = UNSET,
    **kwargs: Any,
) -> ProcessDefinitionElementStatisticsQueryResult:
    """Get process definition statistics

     Get statistics about elements in currently running process instances by process definition key and
    search filter.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.
        body (ProcessDefinitionElementStatisticsQuery | Unset): Process definition element
            statistics request.

    Raises:
        errors.GetProcessDefinitionStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessDefinitionStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessDefinitionStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessDefinitionStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ProcessDefinitionElementStatisticsQueryResult"""
    response = await asyncio_detailed(
        process_definition_key=process_definition_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessDefinitionStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessDefinitionStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessDefinitionStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessDefinitionStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ProcessDefinitionElementStatisticsQueryResult, response.parsed)
