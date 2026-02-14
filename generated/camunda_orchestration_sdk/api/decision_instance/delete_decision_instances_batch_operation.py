from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_created_result import BatchOperationCreatedResult
from ...models.decision_instance_deletion_batch_operation_request import (
    DecisionInstanceDeletionBatchOperationRequest,
)
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(
    *, body: DecisionInstanceDeletionBatchOperationRequest
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/decision-instances/deletion"}
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
    body: DecisionInstanceDeletionBatchOperationRequest,
) -> Response[BatchOperationCreatedResult | ProblemDetail]:
    """Delete decision instances (batch)

     Delete multiple decision instances. This will delete the historic data from secondary storage.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (DecisionInstanceDeletionBatchOperationRequest): The decision instance filter that
            defines which decision instances should be deleted.

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
    body: DecisionInstanceDeletionBatchOperationRequest,
    **kwargs: Any,
) -> BatchOperationCreatedResult:
    """Delete decision instances (batch)

     Delete multiple decision instances. This will delete the historic data from secondary storage.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (DecisionInstanceDeletionBatchOperationRequest): The decision instance filter that
            defines which decision instances should be deleted.

    Raises:
        errors.DeleteDecisionInstancesBatchOperationBadRequest: If the response status code is 400. The decision instance batch operation failed. More details are provided in the response body.
        errors.DeleteDecisionInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteDecisionInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.DeleteDecisionInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationCreatedResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteDecisionInstancesBatchOperationBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.DeleteDecisionInstancesBatchOperationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.DeleteDecisionInstancesBatchOperationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteDecisionInstancesBatchOperationInternalServerError(
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
    body: DecisionInstanceDeletionBatchOperationRequest,
) -> Response[BatchOperationCreatedResult | ProblemDetail]:
    """Delete decision instances (batch)

     Delete multiple decision instances. This will delete the historic data from secondary storage.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (DecisionInstanceDeletionBatchOperationRequest): The decision instance filter that
            defines which decision instances should be deleted.

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
    body: DecisionInstanceDeletionBatchOperationRequest,
    **kwargs: Any,
) -> BatchOperationCreatedResult:
    """Delete decision instances (batch)

     Delete multiple decision instances. This will delete the historic data from secondary storage.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (DecisionInstanceDeletionBatchOperationRequest): The decision instance filter that
            defines which decision instances should be deleted.

    Raises:
        errors.DeleteDecisionInstancesBatchOperationBadRequest: If the response status code is 400. The decision instance batch operation failed. More details are provided in the response body.
        errors.DeleteDecisionInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteDecisionInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.DeleteDecisionInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationCreatedResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteDecisionInstancesBatchOperationBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.DeleteDecisionInstancesBatchOperationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.DeleteDecisionInstancesBatchOperationForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteDecisionInstancesBatchOperationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(BatchOperationCreatedResult, response.parsed)
