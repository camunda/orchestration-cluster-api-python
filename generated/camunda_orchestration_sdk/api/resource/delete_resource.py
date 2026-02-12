from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_resource_data_type_0 import DeleteResourceDataType0
from ...models.delete_resource_response_200 import DeleteResourceResponse200
from ...models.delete_resource_response_400 import DeleteResourceResponse400
from ...models.delete_resource_response_404 import DeleteResourceResponse404
from ...models.delete_resource_response_500 import DeleteResourceResponse500
from ...models.delete_resource_response_503 import DeleteResourceResponse503
from ...types import UNSET, Response, Unset

def _get_kwargs(resource_key: str, *, body: DeleteResourceDataType0 | None | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/resources/{resource_key}/deletion'.format(resource_key=quote(str(resource_key), safe=''))}
    if isinstance(body, DeleteResourceDataType0):
        _kwargs['json'] = body.to_dict()
    else:
        _kwargs['json'] = body
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteResourceResponse200 | DeleteResourceResponse400 | DeleteResourceResponse404 | DeleteResourceResponse500 | DeleteResourceResponse503 | None:
    if response.status_code == 200:
        response_200 = DeleteResourceResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = DeleteResourceResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 404:
        response_404 = DeleteResourceResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = DeleteResourceResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = DeleteResourceResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteResourceResponse200 | DeleteResourceResponse400 | DeleteResourceResponse404 | DeleteResourceResponse500 | DeleteResourceResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(resource_key: str, *, client: AuthenticatedClient | Client, body: DeleteResourceDataType0 | None | Unset=UNSET) -> Response[DeleteResourceResponse200 | DeleteResourceResponse400 | DeleteResourceResponse404 | DeleteResourceResponse500 | DeleteResourceResponse503]:
    """Delete resource

     Deletes a deployed resource. This can be a process definition, decision requirements
    definition, or form definition deployed using the deploy resources endpoint. Specify the
    resource you want to delete in the `resourceKey` parameter.

    Once a resource has been deleted it cannot be recovered. If the resource needs to be
    available again, a new deployment of the resource is required.

    By default, only the resource itself is deleted from the runtime state. To also delete the
    historic data associated with a resource, set the `deleteHistory` flag in the request body
    to `true`. The historic data is deleted asynchronously via a batch operation. The details of
    the created batch operation are included in the response. Note that history deletion is only
    supported for process resources; for other resource types this flag is ignored and no history
    will be deleted.

    Args:
        resource_key (str): The system-assigned key for this resource.
        body (DeleteResourceDataType0 | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteResourceResponse200 | DeleteResourceResponse400 | DeleteResourceResponse404 | DeleteResourceResponse500 | DeleteResourceResponse503]
    """
    kwargs = _get_kwargs(resource_key=resource_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(resource_key: str, *, client: AuthenticatedClient | Client, body: DeleteResourceDataType0 | None | Unset=UNSET, **kwargs: Any) -> DeleteResourceResponse200:
    """Delete resource

 Deletes a deployed resource. This can be a process definition, decision requirements
definition, or form definition deployed using the deploy resources endpoint. Specify the
resource you want to delete in the `resourceKey` parameter.

Once a resource has been deleted it cannot be recovered. If the resource needs to be
available again, a new deployment of the resource is required.

By default, only the resource itself is deleted from the runtime state. To also delete the
historic data associated with a resource, set the `deleteHistory` flag in the request body
to `true`. The historic data is deleted asynchronously via a batch operation. The details of
the created batch operation are included in the response. Note that history deletion is only
supported for process resources; for other resource types this flag is ignored and no history
will be deleted.

Args:
    resource_key (str): The system-assigned key for this resource.
    body (DeleteResourceDataType0 | None | Unset):

Raises:
    errors.DeleteResourceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteResourceNotFound: If the response status code is 404. The resource is not found.
    errors.DeleteResourceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteResourceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteResourceResponse200"""
    response = sync_detailed(resource_key=resource_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteResourceBadRequest(status_code=response.status_code, content=response.content, parsed=cast(DeleteResourceResponse400, response.parsed))
        if response.status_code == 404:
            raise errors.DeleteResourceNotFound(status_code=response.status_code, content=response.content, parsed=cast(DeleteResourceResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.DeleteResourceInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(DeleteResourceResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.DeleteResourceServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(DeleteResourceResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(DeleteResourceResponse200, response.parsed)

async def asyncio_detailed(resource_key: str, *, client: AuthenticatedClient | Client, body: DeleteResourceDataType0 | None | Unset=UNSET) -> Response[DeleteResourceResponse200 | DeleteResourceResponse400 | DeleteResourceResponse404 | DeleteResourceResponse500 | DeleteResourceResponse503]:
    """Delete resource

     Deletes a deployed resource. This can be a process definition, decision requirements
    definition, or form definition deployed using the deploy resources endpoint. Specify the
    resource you want to delete in the `resourceKey` parameter.

    Once a resource has been deleted it cannot be recovered. If the resource needs to be
    available again, a new deployment of the resource is required.

    By default, only the resource itself is deleted from the runtime state. To also delete the
    historic data associated with a resource, set the `deleteHistory` flag in the request body
    to `true`. The historic data is deleted asynchronously via a batch operation. The details of
    the created batch operation are included in the response. Note that history deletion is only
    supported for process resources; for other resource types this flag is ignored and no history
    will be deleted.

    Args:
        resource_key (str): The system-assigned key for this resource.
        body (DeleteResourceDataType0 | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteResourceResponse200 | DeleteResourceResponse400 | DeleteResourceResponse404 | DeleteResourceResponse500 | DeleteResourceResponse503]
    """
    kwargs = _get_kwargs(resource_key=resource_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(resource_key: str, *, client: AuthenticatedClient | Client, body: DeleteResourceDataType0 | None | Unset=UNSET, **kwargs: Any) -> DeleteResourceResponse200:
    """Delete resource

 Deletes a deployed resource. This can be a process definition, decision requirements
definition, or form definition deployed using the deploy resources endpoint. Specify the
resource you want to delete in the `resourceKey` parameter.

Once a resource has been deleted it cannot be recovered. If the resource needs to be
available again, a new deployment of the resource is required.

By default, only the resource itself is deleted from the runtime state. To also delete the
historic data associated with a resource, set the `deleteHistory` flag in the request body
to `true`. The historic data is deleted asynchronously via a batch operation. The details of
the created batch operation are included in the response. Note that history deletion is only
supported for process resources; for other resource types this flag is ignored and no history
will be deleted.

Args:
    resource_key (str): The system-assigned key for this resource.
    body (DeleteResourceDataType0 | None | Unset):

Raises:
    errors.DeleteResourceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteResourceNotFound: If the response status code is 404. The resource is not found.
    errors.DeleteResourceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteResourceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteResourceResponse200"""
    response = await asyncio_detailed(resource_key=resource_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteResourceBadRequest(status_code=response.status_code, content=response.content, parsed=cast(DeleteResourceResponse400, response.parsed))
        if response.status_code == 404:
            raise errors.DeleteResourceNotFound(status_code=response.status_code, content=response.content, parsed=cast(DeleteResourceResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.DeleteResourceInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(DeleteResourceResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.DeleteResourceServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(DeleteResourceResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(DeleteResourceResponse200, response.parsed)