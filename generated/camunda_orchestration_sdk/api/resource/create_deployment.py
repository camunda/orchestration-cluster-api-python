from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_deployment_data import CreateDeploymentData
from ...models.create_deployment_response_200 import CreateDeploymentResponse200
from ...models.create_deployment_response_400 import CreateDeploymentResponse400
from ...models.create_deployment_response_503 import CreateDeploymentResponse503
from ...types import Response


def _get_kwargs(*, body: CreateDeploymentData) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/deployments"}
    _kwargs["files"] = body.to_multipart()
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateDeploymentResponse200
    | CreateDeploymentResponse400
    | CreateDeploymentResponse503
    | None
):
    if response.status_code == 200:
        response_200 = CreateDeploymentResponse200.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = CreateDeploymentResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 503:
        response_503 = CreateDeploymentResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateDeploymentResponse200
    | CreateDeploymentResponse400
    | CreateDeploymentResponse503
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: CreateDeploymentData
) -> Response[
    CreateDeploymentResponse200
    | CreateDeploymentResponse400
    | CreateDeploymentResponse503
]:
    """Deploy resources

     Deploys one or more resources (e.g. processes, decision models, or forms).
    This is an atomic call, i.e. either all resources are deployed or none of them are.

    Args:
        body (CreateDeploymentData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDeploymentResponse200 | CreateDeploymentResponse400 | CreateDeploymentResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient | Client, body: CreateDeploymentData, **kwargs: Any
) -> CreateDeploymentResponse200:
    """Deploy resources

     Deploys one or more resources (e.g. processes, decision models, or forms).
    This is an atomic call, i.e. either all resources are deployed or none of them are.

    Args:
        body (CreateDeploymentData):

    Raises:
        errors.CreateDeploymentBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateDeploymentServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CreateDeploymentResponse200"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateDeploymentBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateDeploymentResponse400, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateDeploymentServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateDeploymentResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateDeploymentResponse200, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: CreateDeploymentData
) -> Response[
    CreateDeploymentResponse200
    | CreateDeploymentResponse400
    | CreateDeploymentResponse503
]:
    """Deploy resources

     Deploys one or more resources (e.g. processes, decision models, or forms).
    This is an atomic call, i.e. either all resources are deployed or none of them are.

    Args:
        body (CreateDeploymentData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateDeploymentResponse200 | CreateDeploymentResponse400 | CreateDeploymentResponse503]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient | Client, body: CreateDeploymentData, **kwargs: Any
) -> CreateDeploymentResponse200:
    """Deploy resources

     Deploys one or more resources (e.g. processes, decision models, or forms).
    This is an atomic call, i.e. either all resources are deployed or none of them are.

    Args:
        body (CreateDeploymentData):

    Raises:
        errors.CreateDeploymentBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateDeploymentServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CreateDeploymentResponse200"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateDeploymentBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateDeploymentResponse400, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateDeploymentServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(CreateDeploymentResponse503, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateDeploymentResponse200, response.parsed)
