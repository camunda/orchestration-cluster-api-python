from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.variable_result import VariableResult
from ...types import Response


def _get_kwargs(variable_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/variables/{variable_key}".format(
            variable_key=quote(str(variable_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | VariableResult | None:
    if response.status_code == 200:
        response_200 = VariableResult.from_dict(response.json())
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
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | VariableResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    variable_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | VariableResult]:
    """Get variable

     Get the variable by the variable key.

    Args:
        variable_key (str): System-generated key for a variable. Example: 2251799813683287.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | VariableResult]
    """
    kwargs = _get_kwargs(variable_key=variable_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    variable_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> VariableResult:
    """Get variable

     Get the variable by the variable key.

    Args:
        variable_key (str): System-generated key for a variable. Example: 2251799813683287.

    Raises:
        errors.GetVariableBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetVariableNotFound: If the response status code is 404. Not found
        errors.GetVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        VariableResult"""
    response = sync_detailed(variable_key=variable_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetVariableBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetVariableUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetVariableForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetVariableNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetVariableInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(VariableResult, response.parsed)


async def asyncio_detailed(
    variable_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | VariableResult]:
    """Get variable

     Get the variable by the variable key.

    Args:
        variable_key (str): System-generated key for a variable. Example: 2251799813683287.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | VariableResult]
    """
    kwargs = _get_kwargs(variable_key=variable_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    variable_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> VariableResult:
    """Get variable

     Get the variable by the variable key.

    Args:
        variable_key (str): System-generated key for a variable. Example: 2251799813683287.

    Raises:
        errors.GetVariableBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetVariableNotFound: If the response status code is 404. Not found
        errors.GetVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        VariableResult"""
    response = await asyncio_detailed(variable_key=variable_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetVariableBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetVariableUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetVariableForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetVariableNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetVariableInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(VariableResult, response.parsed)
