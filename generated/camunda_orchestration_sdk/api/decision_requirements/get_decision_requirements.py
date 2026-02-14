from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_decision_requirements_response_200 import (
    GetDecisionRequirementsResponse200,
)
from ...models.get_decision_requirements_response_400 import (
    GetDecisionRequirementsResponse400,
)
from ...models.get_decision_requirements_response_401 import (
    GetDecisionRequirementsResponse401,
)
from ...models.get_decision_requirements_response_403 import (
    GetDecisionRequirementsResponse403,
)
from ...models.get_decision_requirements_response_404 import (
    GetDecisionRequirementsResponse404,
)
from ...models.get_decision_requirements_response_500 import (
    GetDecisionRequirementsResponse500,
)
from ...types import Response


def _get_kwargs(decision_requirements_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/decision-requirements/{decision_requirements_key}".format(
            decision_requirements_key=quote(str(decision_requirements_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetDecisionRequirementsResponse200
    | GetDecisionRequirementsResponse400
    | GetDecisionRequirementsResponse401
    | GetDecisionRequirementsResponse403
    | GetDecisionRequirementsResponse404
    | GetDecisionRequirementsResponse500
    | None
):
    if response.status_code == 200:
        response_200 = GetDecisionRequirementsResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = GetDecisionRequirementsResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetDecisionRequirementsResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetDecisionRequirementsResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetDecisionRequirementsResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetDecisionRequirementsResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetDecisionRequirementsResponse200
    | GetDecisionRequirementsResponse400
    | GetDecisionRequirementsResponse401
    | GetDecisionRequirementsResponse403
    | GetDecisionRequirementsResponse404
    | GetDecisionRequirementsResponse500
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    decision_requirements_key: str, *, client: AuthenticatedClient | Client
) -> Response[
    GetDecisionRequirementsResponse200
    | GetDecisionRequirementsResponse400
    | GetDecisionRequirementsResponse401
    | GetDecisionRequirementsResponse403
    | GetDecisionRequirementsResponse404
    | GetDecisionRequirementsResponse500
]:
    """Get decision requirements

     Returns Decision Requirements as JSON.

    Args:
        decision_requirements_key (str): System-generated key for a deployed decision requirements
            definition. Example: 2251799813683346.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDecisionRequirementsResponse200 | GetDecisionRequirementsResponse400 | GetDecisionRequirementsResponse401 | GetDecisionRequirementsResponse403 | GetDecisionRequirementsResponse404 | GetDecisionRequirementsResponse500]
    """
    kwargs = _get_kwargs(decision_requirements_key=decision_requirements_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    decision_requirements_key: str,
    *,
    client: AuthenticatedClient | Client,
    **kwargs: Any,
) -> GetDecisionRequirementsResponse200:
    """Get decision requirements

     Returns Decision Requirements as JSON.

    Args:
        decision_requirements_key (str): System-generated key for a deployed decision requirements
            definition. Example: 2251799813683346.

    Raises:
        errors.GetDecisionRequirementsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetDecisionRequirementsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetDecisionRequirementsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetDecisionRequirementsNotFound: If the response status code is 404. The decision requirements with the given key was not found. More details are provided in the response body.
        errors.GetDecisionRequirementsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetDecisionRequirementsResponse200"""
    response = sync_detailed(
        decision_requirements_key=decision_requirements_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetDecisionRequirementsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetDecisionRequirementsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetDecisionRequirementsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetDecisionRequirementsNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetDecisionRequirementsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetDecisionRequirementsResponse200, response.parsed)


async def asyncio_detailed(
    decision_requirements_key: str, *, client: AuthenticatedClient | Client
) -> Response[
    GetDecisionRequirementsResponse200
    | GetDecisionRequirementsResponse400
    | GetDecisionRequirementsResponse401
    | GetDecisionRequirementsResponse403
    | GetDecisionRequirementsResponse404
    | GetDecisionRequirementsResponse500
]:
    """Get decision requirements

     Returns Decision Requirements as JSON.

    Args:
        decision_requirements_key (str): System-generated key for a deployed decision requirements
            definition. Example: 2251799813683346.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDecisionRequirementsResponse200 | GetDecisionRequirementsResponse400 | GetDecisionRequirementsResponse401 | GetDecisionRequirementsResponse403 | GetDecisionRequirementsResponse404 | GetDecisionRequirementsResponse500]
    """
    kwargs = _get_kwargs(decision_requirements_key=decision_requirements_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    decision_requirements_key: str,
    *,
    client: AuthenticatedClient | Client,
    **kwargs: Any,
) -> GetDecisionRequirementsResponse200:
    """Get decision requirements

     Returns Decision Requirements as JSON.

    Args:
        decision_requirements_key (str): System-generated key for a deployed decision requirements
            definition. Example: 2251799813683346.

    Raises:
        errors.GetDecisionRequirementsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetDecisionRequirementsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetDecisionRequirementsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetDecisionRequirementsNotFound: If the response status code is 404. The decision requirements with the given key was not found. More details are provided in the response body.
        errors.GetDecisionRequirementsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        GetDecisionRequirementsResponse200"""
    response = await asyncio_detailed(
        decision_requirements_key=decision_requirements_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetDecisionRequirementsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetDecisionRequirementsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetDecisionRequirementsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetDecisionRequirementsNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetDecisionRequirementsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetDecisionRequirementsResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(GetDecisionRequirementsResponse200, response.parsed)
