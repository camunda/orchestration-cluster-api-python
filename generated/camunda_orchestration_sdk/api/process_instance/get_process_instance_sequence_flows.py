from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_instance_sequence_flows_query_result import (
    ProcessInstanceSequenceFlowsQueryResult,
)
from ...types import Response


def _get_kwargs(process_instance_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/process-instances/{process_instance_key}/sequence-flows".format(
            process_instance_key=quote(str(process_instance_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | ProcessInstanceSequenceFlowsQueryResult | None:
    if response.status_code == 200:
        response_200 = ProcessInstanceSequenceFlowsQueryResult.from_dict(
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
) -> Response[ProblemDetail | ProcessInstanceSequenceFlowsQueryResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    process_instance_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | ProcessInstanceSequenceFlowsQueryResult]:
    """Get sequence flows

     Get sequence flows taken by the process instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | ProcessInstanceSequenceFlowsQueryResult]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ProcessInstanceSequenceFlowsQueryResult:
    """Get sequence flows

     Get sequence flows taken by the process instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.GetProcessInstanceSequenceFlowsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessInstanceSequenceFlowsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessInstanceSequenceFlowsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessInstanceSequenceFlowsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ProcessInstanceSequenceFlowsQueryResult"""
    response = sync_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceSequenceFlowsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessInstanceSequenceFlowsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessInstanceSequenceFlowsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessInstanceSequenceFlowsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ProcessInstanceSequenceFlowsQueryResult, response.parsed)


async def asyncio_detailed(
    process_instance_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | ProcessInstanceSequenceFlowsQueryResult]:
    """Get sequence flows

     Get sequence flows taken by the process instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | ProcessInstanceSequenceFlowsQueryResult]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> ProcessInstanceSequenceFlowsQueryResult:
    """Get sequence flows

     Get sequence flows taken by the process instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.GetProcessInstanceSequenceFlowsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessInstanceSequenceFlowsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessInstanceSequenceFlowsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessInstanceSequenceFlowsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ProcessInstanceSequenceFlowsQueryResult"""
    response = await asyncio_detailed(
        process_instance_key=process_instance_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceSequenceFlowsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessInstanceSequenceFlowsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessInstanceSequenceFlowsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessInstanceSequenceFlowsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(ProcessInstanceSequenceFlowsQueryResult, response.parsed)
