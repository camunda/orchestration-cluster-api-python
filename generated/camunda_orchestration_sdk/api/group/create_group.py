from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_group_data import CreateGroupData
from ...models.create_group_response_201 import CreateGroupResponse201
from ...models.create_group_response_400 import CreateGroupResponse400
from ...models.create_group_response_401 import CreateGroupResponse401
from ...models.create_group_response_403 import CreateGroupResponse403
from ...models.create_group_response_500 import CreateGroupResponse500
from ...models.create_group_response_503 import CreateGroupResponse503
from ...types import UNSET, Response, Unset

def _get_kwargs(*, body: CreateGroupData | Unset=UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {'method': 'post', 'url': '/groups'}
    if not isinstance(body, Unset):
        _kwargs['json'] = body.to_dict()
    headers['Content-Type'] = 'application/json'
    _kwargs['headers'] = headers
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CreateGroupResponse201 | CreateGroupResponse400 | CreateGroupResponse401 | CreateGroupResponse403 | CreateGroupResponse500 | CreateGroupResponse503 | None:
    if response.status_code == 201:
        response_201 = CreateGroupResponse201.from_dict(response.json())
        return response_201
    if response.status_code == 400:
        response_400 = CreateGroupResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = CreateGroupResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = CreateGroupResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 500:
        response_500 = CreateGroupResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = CreateGroupResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CreateGroupResponse201 | CreateGroupResponse400 | CreateGroupResponse401 | CreateGroupResponse403 | CreateGroupResponse500 | CreateGroupResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(*, client: AuthenticatedClient | Client, body: CreateGroupData | Unset=UNSET) -> Response[CreateGroupResponse201 | CreateGroupResponse400 | CreateGroupResponse401 | CreateGroupResponse403 | CreateGroupResponse500 | CreateGroupResponse503]:
    """Create group

     Create a new group.

    Args:
        body (CreateGroupData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateGroupResponse201 | CreateGroupResponse400 | CreateGroupResponse401 | CreateGroupResponse403 | CreateGroupResponse500 | CreateGroupResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(*, client: AuthenticatedClient | Client, body: CreateGroupData | Unset=UNSET, **kwargs: Any) -> CreateGroupResponse201:
    """Create group

 Create a new group.

Args:
    body (CreateGroupData | Unset):

Raises:
    errors.CreateGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateGroupResponse201"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateGroupBadRequest(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.CreateGroupUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.CreateGroupForbidden(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.CreateGroupInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.CreateGroupServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateGroupResponse201, response.parsed)

async def asyncio_detailed(*, client: AuthenticatedClient | Client, body: CreateGroupData | Unset=UNSET) -> Response[CreateGroupResponse201 | CreateGroupResponse400 | CreateGroupResponse401 | CreateGroupResponse403 | CreateGroupResponse500 | CreateGroupResponse503]:
    """Create group

     Create a new group.

    Args:
        body (CreateGroupData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateGroupResponse201 | CreateGroupResponse400 | CreateGroupResponse401 | CreateGroupResponse403 | CreateGroupResponse500 | CreateGroupResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(*, client: AuthenticatedClient | Client, body: CreateGroupData | Unset=UNSET, **kwargs: Any) -> CreateGroupResponse201:
    """Create group

 Create a new group.

Args:
    body (CreateGroupData | Unset):

Raises:
    errors.CreateGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateGroupResponse201"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateGroupBadRequest(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.CreateGroupUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.CreateGroupForbidden(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse403, response.parsed))
        if response.status_code == 500:
            raise errors.CreateGroupInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.CreateGroupServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(CreateGroupResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateGroupResponse201, response.parsed)