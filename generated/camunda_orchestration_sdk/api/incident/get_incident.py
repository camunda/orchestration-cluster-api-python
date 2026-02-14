from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_incident_response_200 import GetIncidentResponse200
from ...models.get_incident_response_400 import GetIncidentResponse400
from ...models.get_incident_response_401 import GetIncidentResponse401
from ...models.get_incident_response_403 import GetIncidentResponse403
from ...models.get_incident_response_404 import GetIncidentResponse404
from ...models.get_incident_response_500 import GetIncidentResponse500
from ...types import Response


def _get_kwargs(incident_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/incidents/{incident_key}".format(
            incident_key=quote(str(incident_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetIncidentResponse200
    | GetIncidentResponse400
    | GetIncidentResponse401
    | GetIncidentResponse403
    | GetIncidentResponse404
    | GetIncidentResponse500
    | None
):
    if response.status_code == 200:
        response_200 = GetIncidentResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = GetIncidentResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetIncidentResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetIncidentResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetIncidentResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetIncidentResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetIncidentResponse200
    | GetIncidentResponse400
    | GetIncidentResponse401
    | GetIncidentResponse403
    | GetIncidentResponse404
    | GetIncidentResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    incident_key: str, *, client: AuthenticatedClient | Client
) -> Response[
    GetIncidentResponse200
    | GetIncidentResponse400
    | GetIncidentResponse401
    | GetIncidentResponse403
    | GetIncidentResponse404
    | GetIncidentResponse500
]:
    """Get incident

     Returns incident as JSON.

    Args:
        incident_key (str): System-generated key for a incident. Example: 2251799813689432.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetIncidentResponse200 | GetIncidentResponse400 | GetIncidentResponse401 | GetIncidentResponse403 | GetIncidentResponse404 | GetIncidentResponse500]
    """
    kwargs = _get_kwargs(incident_key=incident_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    incident_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetIncidentResponse200:
    """Get incident

     Returns incident as JSON.

    Args:
        incident_key (str): System-generated key for a incident. Example: 2251799813689432.

    Raises:
        errors.GetIncidentBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetIncidentUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetIncidentForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetIncidentNotFound: If the response status code is 404. The incident with the given key was not found.
        errors.GetIncidentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetIncidentResponse200"""
    response = sync_detailed(incident_key=incident_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetIncidentBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetIncidentUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetIncidentForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetIncidentNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetIncidentInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetIncidentResponse200, response.parsed)


async def asyncio_detailed(
    incident_key: str, *, client: AuthenticatedClient | Client
) -> Response[
    GetIncidentResponse200
    | GetIncidentResponse400
    | GetIncidentResponse401
    | GetIncidentResponse403
    | GetIncidentResponse404
    | GetIncidentResponse500
]:
    """Get incident

     Returns incident as JSON.

    Args:
        incident_key (str): System-generated key for a incident. Example: 2251799813689432.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetIncidentResponse200 | GetIncidentResponse400 | GetIncidentResponse401 | GetIncidentResponse403 | GetIncidentResponse404 | GetIncidentResponse500]
    """
    kwargs = _get_kwargs(incident_key=incident_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    incident_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> GetIncidentResponse200:
    """Get incident

     Returns incident as JSON.

    Args:
        incident_key (str): System-generated key for a incident. Example: 2251799813689432.

    Raises:
        errors.GetIncidentBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetIncidentUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetIncidentForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetIncidentNotFound: If the response status code is 404. The incident with the given key was not found.
        errors.GetIncidentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetIncidentResponse200"""
    response = await asyncio_detailed(incident_key=incident_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetIncidentBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetIncidentUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetIncidentForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetIncidentNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetIncidentInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetIncidentResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetIncidentResponse200, response.parsed)
