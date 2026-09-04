from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_created_result import BatchOperationCreatedResult
from ...models.problem_detail import ProblemDetail
from ...models.process_instance_suspension_batch_operation_request import (
    ProcessInstanceSuspensionBatchOperationRequest,
)
from ...types import Response


def _get_kwargs(
    *, body: ProcessInstanceSuspensionBatchOperationRequest
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/process-instances/suspension"}
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
    *, client: AuthenticatedClient, body: ProcessInstanceSuspensionBatchOperationRequest
) -> Response[BatchOperationCreatedResult | ProblemDetail]:
    """Suspend process instances (batch)

     Suspends multiple running process instances.
    Any given filter for state or parentProcessInstanceKey is ignored and overridden, as only
    ACTIVE process instances can be suspended and suspension does not cascade between parent
    and child instances, so child instances are suspended independently of their parent or
    root instance.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (ProcessInstanceSuspensionBatchOperationRequest): The process instance filter that
            defines which process instances should be suspended.

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
    client: AuthenticatedClient,
    body: ProcessInstanceSuspensionBatchOperationRequest,
    **kwargs: Any,
) -> BatchOperationCreatedResult:
    """Suspend process instances (batch)

     Suspends multiple running process instances.
    Any given filter for state or parentProcessInstanceKey is ignored and overridden, as only
    ACTIVE process instances can be suspended and suspension does not cascade between parent
    and child instances, so child instances are suspended independently of their parent or
    root instance.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (ProcessInstanceSuspensionBatchOperationRequest): The process instance filter that
            defines which process instances should be suspended.

    Raises:
        errors.BadRequestError: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationCreatedResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="suspend_process_instances_batch_operation",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="suspend_process_instances_batch_operation",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="suspend_process_instances_batch_operation",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="suspend_process_instances_batch_operation",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="suspend_process_instances_batch_operation",
        )
    assert response.parsed is not None
    return cast(BatchOperationCreatedResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient, body: ProcessInstanceSuspensionBatchOperationRequest
) -> Response[BatchOperationCreatedResult | ProblemDetail]:
    """Suspend process instances (batch)

     Suspends multiple running process instances.
    Any given filter for state or parentProcessInstanceKey is ignored and overridden, as only
    ACTIVE process instances can be suspended and suspension does not cascade between parent
    and child instances, so child instances are suspended independently of their parent or
    root instance.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (ProcessInstanceSuspensionBatchOperationRequest): The process instance filter that
            defines which process instances should be suspended.

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
    client: AuthenticatedClient,
    body: ProcessInstanceSuspensionBatchOperationRequest,
    **kwargs: Any,
) -> BatchOperationCreatedResult:
    """Suspend process instances (batch)

     Suspends multiple running process instances.
    Any given filter for state or parentProcessInstanceKey is ignored and overridden, as only
    ACTIVE process instances can be suspended and suspension does not cascade between parent
    and child instances, so child instances are suspended independently of their parent or
    root instance.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (ProcessInstanceSuspensionBatchOperationRequest): The process instance filter that
            defines which process instances should be suspended.

    Raises:
        errors.BadRequestError: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationCreatedResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="suspend_process_instances_batch_operation",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="suspend_process_instances_batch_operation",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="suspend_process_instances_batch_operation",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="suspend_process_instances_batch_operation",
            )
        raise errors.UnexpectedStatus(
            response.status_code,
            response.content,
            operation_id="suspend_process_instances_batch_operation",
        )
    assert response.parsed is not None
    return cast(BatchOperationCreatedResult, response.parsed)
