from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(tenant_id: str, name: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/cluster-variables/tenants/{tenant_id}/{name}".format(
            tenant_id=quote(str(tenant_id), safe=""), name=quote(str(name), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Any | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str, name: str, *, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]:
    """Delete a tenant-scoped cluster variable

     Delete a tenant-scoped cluster variable.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, name=name)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    tenant_id: str, name: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> None:
    """Delete a tenant-scoped cluster variable

     Delete a tenant-scoped cluster variable.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        name (str):

    Raises:
        errors.DeleteTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
        errors.DeleteTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.DeleteTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
        errors.DeleteTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(tenant_id=tenant_id, name=name, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteTenantClusterVariableBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.DeleteTenantClusterVariableUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.DeleteTenantClusterVariableForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteTenantClusterVariableNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteTenantClusterVariableInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    tenant_id: str, name: str, *, client: AuthenticatedClient | Client
) -> Response[Any | ProblemDetail]:
    """Delete a tenant-scoped cluster variable

     Delete a tenant-scoped cluster variable.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(tenant_id=tenant_id, name=name)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str, name: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> None:
    """Delete a tenant-scoped cluster variable

     Delete a tenant-scoped cluster variable.

    Args:
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        name (str):

    Raises:
        errors.DeleteTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
        errors.DeleteTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.DeleteTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.DeleteTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
        errors.DeleteTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(tenant_id=tenant_id, name=name, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.DeleteTenantClusterVariableBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.DeleteTenantClusterVariableUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.DeleteTenantClusterVariableForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.DeleteTenantClusterVariableNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.DeleteTenantClusterVariableInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
