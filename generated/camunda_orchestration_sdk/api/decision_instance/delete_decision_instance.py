from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_operation_created_result import BatchOperationCreatedResult
from ...models.delete_process_instance_request_type_0 import (
    DeleteProcessInstanceRequestType0,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    decision_instance_key: str,
    *,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/decision-instances/{decision_instance_key}/deletion".format(
            decision_instance_key=quote(str(decision_instance_key), safe="")
        ),
    }
    if isinstance(body, DeleteProcessInstanceRequestType0):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BatchOperationCreatedResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = BatchOperationCreatedResult.from_dict(response.json())
        return response_200
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
    if response.status_code == 503:
        response_503 = ProblemDetail.from_dict(response.json())
        return response_503
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
    decision_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
) -> Response[BatchOperationCreatedResult | ProblemDetail]:
    """Delete decision instance

     Delete all associated decision evaluations based on provided key.

    Args:
        decision_instance_key (str): System-generated key for a deployed decision instance.
            Example: 22517998136843567.
        body (DeleteProcessInstanceRequestType0 | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchOperationCreatedResult | ProblemDetail]
    """
    kwargs = _get_kwargs(decision_instance_key=decision_instance_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    decision_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
    **kwargs: Any,
) -> BatchOperationCreatedResult:
    """Delete decision instance

     Delete all associated decision evaluations based on provided key.

    Args:
        decision_instance_key (str): System-generated key for a deployed decision instance.
            Example: 22517998136843567.
        body (DeleteProcessInstanceRequestType0 | None | Unset):

    Raises:
        errors.DeleteDecisionInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteDecisionInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.DeleteDecisionInstanceNotFound: If the response status code is 404. The decision instance is not found.
        errors.DeleteDecisionInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.DeleteDecisionInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationCreatedResult"""
    response = sync_detailed(
        decision_instance_key=decision_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteDecisionInstanceUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.DeleteDecisionInstanceForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteDecisionInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteDecisionInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.DeleteDecisionInstanceServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(BatchOperationCreatedResult, response.parsed)


async def asyncio_detailed(
    decision_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
) -> Response[BatchOperationCreatedResult | ProblemDetail]:
    """Delete decision instance

     Delete all associated decision evaluations based on provided key.

    Args:
        decision_instance_key (str): System-generated key for a deployed decision instance.
            Example: 22517998136843567.
        body (DeleteProcessInstanceRequestType0 | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchOperationCreatedResult | ProblemDetail]
    """
    kwargs = _get_kwargs(decision_instance_key=decision_instance_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    decision_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
    **kwargs: Any,
) -> BatchOperationCreatedResult:
    """Delete decision instance

     Delete all associated decision evaluations based on provided key.

    Args:
        decision_instance_key (str): System-generated key for a deployed decision instance.
            Example: 22517998136843567.
        body (DeleteProcessInstanceRequestType0 | None | Unset):

    Raises:
        errors.DeleteDecisionInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteDecisionInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.DeleteDecisionInstanceNotFound: If the response status code is 404. The decision instance is not found.
        errors.DeleteDecisionInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.DeleteDecisionInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        BatchOperationCreatedResult"""
    response = await asyncio_detailed(
        decision_instance_key=decision_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteDecisionInstanceUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.DeleteDecisionInstanceForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteDecisionInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteDecisionInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.DeleteDecisionInstanceServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(BatchOperationCreatedResult, response.parsed)
