from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_start_process_form_response_200 import GetStartProcessFormResponse200
from ...models.get_start_process_form_response_400 import GetStartProcessFormResponse400
from ...models.get_start_process_form_response_401 import GetStartProcessFormResponse401
from ...models.get_start_process_form_response_403 import GetStartProcessFormResponse403
from ...models.get_start_process_form_response_404 import GetStartProcessFormResponse404
from ...models.get_start_process_form_response_500 import GetStartProcessFormResponse500
from ...types import Response

def _get_kwargs(process_definition_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/process-definitions/{process_definition_key}/form'.format(process_definition_key=quote(str(process_definition_key), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | GetStartProcessFormResponse200 | GetStartProcessFormResponse400 | GetStartProcessFormResponse401 | GetStartProcessFormResponse403 | GetStartProcessFormResponse404 | GetStartProcessFormResponse500 | None:
    if response.status_code == 200:
        response_200 = GetStartProcessFormResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = GetStartProcessFormResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetStartProcessFormResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetStartProcessFormResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetStartProcessFormResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetStartProcessFormResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | GetStartProcessFormResponse200 | GetStartProcessFormResponse400 | GetStartProcessFormResponse401 | GetStartProcessFormResponse403 | GetStartProcessFormResponse404 | GetStartProcessFormResponse500]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(process_definition_key: str, *, client: AuthenticatedClient | Client) -> Response[Any | GetStartProcessFormResponse200 | GetStartProcessFormResponse400 | GetStartProcessFormResponse401 | GetStartProcessFormResponse403 | GetStartProcessFormResponse404 | GetStartProcessFormResponse500]:
    """Get process start form

     Get the start form of a process.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetStartProcessFormResponse200 | GetStartProcessFormResponse400 | GetStartProcessFormResponse401 | GetStartProcessFormResponse403 | GetStartProcessFormResponse404 | GetStartProcessFormResponse500]
    """
    kwargs = _get_kwargs(process_definition_key=process_definition_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(process_definition_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Get process start form

 Get the start form of a process.
Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

Args:
    process_definition_key (str): System-generated key for a deployed process definition.
        Example: 2251799813686749.

Raises:
    errors.GetStartProcessFormBadRequest: If the response status code is 400.
    errors.GetStartProcessFormUnauthorized: If the response status code is 401.
    errors.GetStartProcessFormForbidden: If the response status code is 403.
    errors.GetStartProcessFormNotFound: If the response status code is 404.
    errors.GetStartProcessFormInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = sync_detailed(process_definition_key=process_definition_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetStartProcessFormBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetStartProcessFormUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetStartProcessFormForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetStartProcessFormNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetStartProcessFormInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(process_definition_key: str, *, client: AuthenticatedClient | Client) -> Response[Any | GetStartProcessFormResponse200 | GetStartProcessFormResponse400 | GetStartProcessFormResponse401 | GetStartProcessFormResponse403 | GetStartProcessFormResponse404 | GetStartProcessFormResponse500]:
    """Get process start form

     Get the start form of a process.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetStartProcessFormResponse200 | GetStartProcessFormResponse400 | GetStartProcessFormResponse401 | GetStartProcessFormResponse403 | GetStartProcessFormResponse404 | GetStartProcessFormResponse500]
    """
    kwargs = _get_kwargs(process_definition_key=process_definition_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(process_definition_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> Any:
    """Get process start form

 Get the start form of a process.
Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

Args:
    process_definition_key (str): System-generated key for a deployed process definition.
        Example: 2251799813686749.

Raises:
    errors.GetStartProcessFormBadRequest: If the response status code is 400.
    errors.GetStartProcessFormUnauthorized: If the response status code is 401.
    errors.GetStartProcessFormForbidden: If the response status code is 403.
    errors.GetStartProcessFormNotFound: If the response status code is 404.
    errors.GetStartProcessFormInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    Any"""
    response = await asyncio_detailed(process_definition_key=process_definition_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetStartProcessFormBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetStartProcessFormUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetStartProcessFormForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetStartProcessFormNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetStartProcessFormInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetStartProcessFormResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed