from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_decision_instances_batch_operation_data import DeleteDecisionInstancesBatchOperationData
from ...models.delete_decision_instances_batch_operation_response_200 import DeleteDecisionInstancesBatchOperationResponse200
from ...models.delete_decision_instances_batch_operation_response_400 import DeleteDecisionInstancesBatchOperationResponse400
from ...models.delete_decision_instances_batch_operation_response_401 import DeleteDecisionInstancesBatchOperationResponse401
from ...models.delete_decision_instances_batch_operation_response_403 import DeleteDecisionInstancesBatchOperationResponse403
from ...models.delete_decision_instances_batch_operation_response_500 import DeleteDecisionInstancesBatchOperationResponse500
from ...types import Response

def _get_kwargs(*, body: DeleteDecisionInstancesBatchOperationData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/decision-instances/deletion'}
    _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteDecisionInstancesBatchOperationResponse200 | DeleteDecisionInstancesBatchOperationResponse400 | DeleteDecisionInstancesBatchOperationResponse401 | DeleteDecisionInstancesBatchOperationResponse403 | DeleteDecisionInstancesBatchOperationResponse500 | None:
    if response.status_code == 200:
        response_200 = DeleteDecisionInstancesBatchOperationResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = DeleteDecisionInstancesBatchOperationResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = DeleteDecisionInstancesBatchOperationResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = DeleteDecisionInstancesBatchOperationResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = DeleteDecisionInstancesBatchOperationResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteDecisionInstancesBatchOperationResponse200 | DeleteDecisionInstancesBatchOperationResponse400 | DeleteDecisionInstancesBatchOperationResponse401 | DeleteDecisionInstancesBatchOperationResponse403 | DeleteDecisionInstancesBatchOperationResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: DeleteDecisionInstancesBatchOperationData) -> Response[DeleteDecisionInstancesBatchOperationResponse200 | DeleteDecisionInstancesBatchOperationResponse400 | DeleteDecisionInstancesBatchOperationResponse401 | DeleteDecisionInstancesBatchOperationResponse403 | DeleteDecisionInstancesBatchOperationResponse500]:
    """Delete decision instances (batch)

     Delete multiple decision instances. This will delete the historic data from secondary storage.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (DeleteDecisionInstancesBatchOperationData): The decision instance filter that
            defines which decision instances should be deleted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteDecisionInstancesBatchOperationResponse200 | DeleteDecisionInstancesBatchOperationResponse400 | DeleteDecisionInstancesBatchOperationResponse401 | DeleteDecisionInstancesBatchOperationResponse403 | DeleteDecisionInstancesBatchOperationResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: DeleteDecisionInstancesBatchOperationData, **kwargs) -> DeleteDecisionInstancesBatchOperationResponse200:
    """Delete decision instances (batch)

 Delete multiple decision instances. This will delete the historic data from secondary storage.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (DeleteDecisionInstancesBatchOperationData): The decision instance filter that
        defines which decision instances should be deleted.

Raises:
    errors.DeleteDecisionInstancesBatchOperationBadRequest: If the response status code is 400. The decision instance batch operation failed. More details are provided in the response body.
    errors.DeleteDecisionInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteDecisionInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteDecisionInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteDecisionInstancesBatchOperationResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteDecisionInstancesBatchOperationBadRequest(status_code=response.status_code, content=response.content, parsed=cast(DeleteDecisionInstancesBatchOperationResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.DeleteDecisionInstancesBatchOperationUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(DeleteDecisionInstancesBatchOperationResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.DeleteDecisionInstancesBatchOperationForbidden(status_code=response.status_code, content=response.content, parsed=cast(DeleteDecisionInstancesBatchOperationResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.DeleteDecisionInstancesBatchOperationInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(DeleteDecisionInstancesBatchOperationResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: DeleteDecisionInstancesBatchOperationData) -> Response[DeleteDecisionInstancesBatchOperationResponse200 | DeleteDecisionInstancesBatchOperationResponse400 | DeleteDecisionInstancesBatchOperationResponse401 | DeleteDecisionInstancesBatchOperationResponse403 | DeleteDecisionInstancesBatchOperationResponse500]:
    """Delete decision instances (batch)

     Delete multiple decision instances. This will delete the historic data from secondary storage.
    This is done asynchronously, the progress can be tracked using the batchOperationKey from the
    response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

    Args:
        body (DeleteDecisionInstancesBatchOperationData): The decision instance filter that
            defines which decision instances should be deleted.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteDecisionInstancesBatchOperationResponse200 | DeleteDecisionInstancesBatchOperationResponse400 | DeleteDecisionInstancesBatchOperationResponse401 | DeleteDecisionInstancesBatchOperationResponse403 | DeleteDecisionInstancesBatchOperationResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: DeleteDecisionInstancesBatchOperationData, **kwargs) -> DeleteDecisionInstancesBatchOperationResponse200:
    """Delete decision instances (batch)

 Delete multiple decision instances. This will delete the historic data from secondary storage.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (DeleteDecisionInstancesBatchOperationData): The decision instance filter that
        defines which decision instances should be deleted.

Raises:
    errors.DeleteDecisionInstancesBatchOperationBadRequest: If the response status code is 400. The decision instance batch operation failed. More details are provided in the response body.
    errors.DeleteDecisionInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteDecisionInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteDecisionInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteDecisionInstancesBatchOperationResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteDecisionInstancesBatchOperationBadRequest(status_code=response.status_code, content=response.content, parsed=cast(DeleteDecisionInstancesBatchOperationResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.DeleteDecisionInstancesBatchOperationUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(DeleteDecisionInstancesBatchOperationResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.DeleteDecisionInstancesBatchOperationForbidden(status_code=response.status_code, content=response.content, parsed=cast(DeleteDecisionInstancesBatchOperationResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.DeleteDecisionInstancesBatchOperationInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(DeleteDecisionInstancesBatchOperationResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed