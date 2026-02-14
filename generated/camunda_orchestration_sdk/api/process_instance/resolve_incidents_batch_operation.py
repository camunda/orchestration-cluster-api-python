from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_created_result import BatchOperationCreatedResult
from ...models.problem_detail import ProblemDetail
from ...models.resolve_incidents_batch_operation_data import (
    ResolveIncidentsBatchOperationData,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: ResolveIncidentsBatchOperationData | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/process-instances/incident-resolution",
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BatchOperationCreatedResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = BatchOperationCreatedResult.from_dict(response.json())
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
) -> Response[BatchOperationCreatedResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ResolveIncidentsBatchOperationData | Unset = UNSET,
) -> Response[BatchOperationCreatedResult | ProblemDetail]:
    """Resolve related incidents (batch)

     Resolves multiple instances of process instances.
    Since only process instances with ACTIVE state can have unresolved incidents, any given
    filters for state are ignored and overridden during this batch operation.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (ResolveIncidentsBatchOperationData | Unset): The process instance filter that
            defines which process instances should have their incidents resolved.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchOperationCreatedResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ResolveIncidentsBatchOperationData | Unset = UNSET,
    **kwargs: Any,
) -> BatchOperationCreatedResult:
    """Resolve related incidents (batch)

     Resolves multiple instances of process instances.
    Since only process instances with ACTIVE state can have unresolved incidents, any given
    filters for state are ignored and overridden during this batch operation.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (ResolveIncidentsBatchOperationData | Unset): The process instance filter that
            defines which process instances should have their incidents resolved.

    Raises:
        errors.ResolveIncidentsBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
        errors.ResolveIncidentsBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ResolveIncidentsBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.ResolveIncidentsBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationCreatedResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.ResolveIncidentsBatchOperationBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.ResolveIncidentsBatchOperationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.ResolveIncidentsBatchOperationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.ResolveIncidentsBatchOperationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(BatchOperationCreatedResult, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ResolveIncidentsBatchOperationData | Unset = UNSET,
) -> Response[BatchOperationCreatedResult | ProblemDetail]:
    """Resolve related incidents (batch)

     Resolves multiple instances of process instances.
    Since only process instances with ACTIVE state can have unresolved incidents, any given
    filters for state are ignored and overridden during this batch operation.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (ResolveIncidentsBatchOperationData | Unset): The process instance filter that
            defines which process instances should have their incidents resolved.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchOperationCreatedResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ResolveIncidentsBatchOperationData | Unset = UNSET,
    **kwargs: Any,
) -> BatchOperationCreatedResult:
    """Resolve related incidents (batch)

     Resolves multiple instances of process instances.
    Since only process instances with ACTIVE state can have unresolved incidents, any given
    filters for state are ignored and overridden during this batch operation.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (ResolveIncidentsBatchOperationData | Unset): The process instance filter that
            defines which process instances should have their incidents resolved.

    Raises:
        errors.ResolveIncidentsBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
        errors.ResolveIncidentsBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ResolveIncidentsBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.ResolveIncidentsBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationCreatedResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.ResolveIncidentsBatchOperationBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.ResolveIncidentsBatchOperationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.ResolveIncidentsBatchOperationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.ResolveIncidentsBatchOperationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(BatchOperationCreatedResult, response.parsed)
