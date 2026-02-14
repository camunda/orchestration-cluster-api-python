from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_process_definition_instance_statistics_data import (
    GetProcessDefinitionInstanceStatisticsData,
)
from ...models.get_process_definition_instance_statistics_response_200 import (
    GetProcessDefinitionInstanceStatisticsResponse200,
)
from ...models.get_process_definition_instance_statistics_response_400 import (
    GetProcessDefinitionInstanceStatisticsResponse400,
)
from ...models.get_process_definition_instance_statistics_response_401 import (
    GetProcessDefinitionInstanceStatisticsResponse401,
)
from ...models.get_process_definition_instance_statistics_response_403 import (
    GetProcessDefinitionInstanceStatisticsResponse403,
)
from ...models.get_process_definition_instance_statistics_response_500 import (
    GetProcessDefinitionInstanceStatisticsResponse500,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: GetProcessDefinitionInstanceStatisticsData | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/process-definitions/statistics/process-instances",
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetProcessDefinitionInstanceStatisticsResponse200
    | GetProcessDefinitionInstanceStatisticsResponse400
    | GetProcessDefinitionInstanceStatisticsResponse401
    | GetProcessDefinitionInstanceStatisticsResponse403
    | GetProcessDefinitionInstanceStatisticsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = GetProcessDefinitionInstanceStatisticsResponse200.from_dict(
            response.json()
        )
        return response_200
    if response.status_code == 400:
        response_400 = GetProcessDefinitionInstanceStatisticsResponse400.from_dict(
            response.json()
        )
        return response_400
    if response.status_code == 401:
        response_401 = GetProcessDefinitionInstanceStatisticsResponse401.from_dict(
            response.json()
        )
        return response_401
    if response.status_code == 403:
        response_403 = GetProcessDefinitionInstanceStatisticsResponse403.from_dict(
            response.json()
        )
        return response_403
    if response.status_code == 500:
        response_500 = GetProcessDefinitionInstanceStatisticsResponse500.from_dict(
            response.json()
        )
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetProcessDefinitionInstanceStatisticsResponse200
    | GetProcessDefinitionInstanceStatisticsResponse400
    | GetProcessDefinitionInstanceStatisticsResponse401
    | GetProcessDefinitionInstanceStatisticsResponse403
    | GetProcessDefinitionInstanceStatisticsResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: GetProcessDefinitionInstanceStatisticsData | Unset = UNSET,
) -> Response[
    GetProcessDefinitionInstanceStatisticsResponse200
    | GetProcessDefinitionInstanceStatisticsResponse400
    | GetProcessDefinitionInstanceStatisticsResponse401
    | GetProcessDefinitionInstanceStatisticsResponse403
    | GetProcessDefinitionInstanceStatisticsResponse500
]:
    """Get process instance statistics

     Get statistics about process instances, grouped by process definition and tenant.

    Args:
        body (GetProcessDefinitionInstanceStatisticsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessDefinitionInstanceStatisticsResponse200 | GetProcessDefinitionInstanceStatisticsResponse400 | GetProcessDefinitionInstanceStatisticsResponse401 | GetProcessDefinitionInstanceStatisticsResponse403 | GetProcessDefinitionInstanceStatisticsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: GetProcessDefinitionInstanceStatisticsData | Unset = UNSET,
    **kwargs: Any,
) -> GetProcessDefinitionInstanceStatisticsResponse200:
    """Get process instance statistics

     Get statistics about process instances, grouped by process definition and tenant.

    Args:
        body (GetProcessDefinitionInstanceStatisticsData | Unset):

    Raises:
        errors.GetProcessDefinitionInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessDefinitionInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessDefinitionInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessDefinitionInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetProcessDefinitionInstanceStatisticsResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessDefinitionInstanceStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(
                    GetProcessDefinitionInstanceStatisticsResponse400, response.parsed
                ),
            )
        if response.status_code == 401:
            raise errors.GetProcessDefinitionInstanceStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(
                    GetProcessDefinitionInstanceStatisticsResponse401, response.parsed
                ),
            )
        if response.status_code == 403:
            raise errors.GetProcessDefinitionInstanceStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(
                    GetProcessDefinitionInstanceStatisticsResponse403, response.parsed
                ),
            )
        if response.status_code == 500:
            raise errors.GetProcessDefinitionInstanceStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(
                    GetProcessDefinitionInstanceStatisticsResponse500, response.parsed
                ),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetProcessDefinitionInstanceStatisticsResponse200, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: GetProcessDefinitionInstanceStatisticsData | Unset = UNSET,
) -> Response[
    GetProcessDefinitionInstanceStatisticsResponse200
    | GetProcessDefinitionInstanceStatisticsResponse400
    | GetProcessDefinitionInstanceStatisticsResponse401
    | GetProcessDefinitionInstanceStatisticsResponse403
    | GetProcessDefinitionInstanceStatisticsResponse500
]:
    """Get process instance statistics

     Get statistics about process instances, grouped by process definition and tenant.

    Args:
        body (GetProcessDefinitionInstanceStatisticsData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessDefinitionInstanceStatisticsResponse200 | GetProcessDefinitionInstanceStatisticsResponse400 | GetProcessDefinitionInstanceStatisticsResponse401 | GetProcessDefinitionInstanceStatisticsResponse403 | GetProcessDefinitionInstanceStatisticsResponse500]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: GetProcessDefinitionInstanceStatisticsData | Unset = UNSET,
    **kwargs: Any,
) -> GetProcessDefinitionInstanceStatisticsResponse200:
    """Get process instance statistics

     Get statistics about process instances, grouped by process definition and tenant.

    Args:
        body (GetProcessDefinitionInstanceStatisticsData | Unset):

    Raises:
        errors.GetProcessDefinitionInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessDefinitionInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessDefinitionInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessDefinitionInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetProcessDefinitionInstanceStatisticsResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessDefinitionInstanceStatisticsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(
                    GetProcessDefinitionInstanceStatisticsResponse400, response.parsed
                ),
            )
        if response.status_code == 401:
            raise errors.GetProcessDefinitionInstanceStatisticsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(
                    GetProcessDefinitionInstanceStatisticsResponse401, response.parsed
                ),
            )
        if response.status_code == 403:
            raise errors.GetProcessDefinitionInstanceStatisticsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(
                    GetProcessDefinitionInstanceStatisticsResponse403, response.parsed
                ),
            )
        if response.status_code == 500:
            raise errors.GetProcessDefinitionInstanceStatisticsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(
                    GetProcessDefinitionInstanceStatisticsResponse500, response.parsed
                ),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetProcessDefinitionInstanceStatisticsResponse200, response.parsed)
