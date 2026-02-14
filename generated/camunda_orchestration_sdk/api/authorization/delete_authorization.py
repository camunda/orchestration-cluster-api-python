from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(authorization_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/authorizations/{authorization_key}".format(
            authorization_key=quote(str(authorization_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
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
) -> Response[Any | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    authorization_key: str, *, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]:
    """Delete authorization

     Deletes the authorization with the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(authorization_key=authorization_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    authorization_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> None:
    """Delete authorization

     Deletes the authorization with the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.

    Raises:
        errors.DeleteAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteAuthorizationNotFound: If the response status code is 404. The authorization with the authorizationKey was not found.
        errors.DeleteAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.DeleteAuthorizationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(authorization_key=authorization_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteAuthorizationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteAuthorizationNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteAuthorizationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.DeleteAuthorizationServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    authorization_key: str, *, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]:
    """Delete authorization

     Deletes the authorization with the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(authorization_key=authorization_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    authorization_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> None:
    """Delete authorization

     Deletes the authorization with the given key.

    Args:
        authorization_key (str): System-generated key for an authorization. Example:
            2251799813684332.

    Raises:
        errors.DeleteAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteAuthorizationNotFound: If the response status code is 404. The authorization with the authorizationKey was not found.
        errors.DeleteAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.DeleteAuthorizationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        authorization_key=authorization_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.DeleteAuthorizationUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteAuthorizationNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteAuthorizationInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.DeleteAuthorizationServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
