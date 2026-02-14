from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_process_instance_result import CreateProcessInstanceResult
from ...models.problem_detail import ProblemDetail
from ...models.process_creation_by_id import ProcessCreationById
from ...models.process_creation_by_key import ProcessCreationByKey
from ...types import Response


def _get_kwargs(*, body: ProcessCreationById | ProcessCreationByKey) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/process-instances"}
    if isinstance(body, ProcessCreationById):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateProcessInstanceResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = CreateProcessInstanceResult.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = ProblemDetail.from_dict(response.json())
        return response_503
    if response.status_code == 504:
        response_504 = ProblemDetail.from_dict(response.json())
        return response_504
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CreateProcessInstanceResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ProcessCreationById | ProcessCreationByKey,
) -> Response[CreateProcessInstanceResult | ProblemDetail]:
    """Create process instance

     Creates and starts an instance of the specified process.
    The process definition to use to create the instance can be specified either using its unique key
    (as returned by Deploy resources), or using the BPMN process id and a version.

    Waits for the completion of the process instance before returning a result
    when awaitCompletion is enabled.

    Args:
        body (ProcessCreationById | ProcessCreationByKey): Instructions for creating a process
            instance. The process definition can be specified
            either by id or by key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateProcessInstanceResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ProcessCreationById | ProcessCreationByKey,
    **kwargs: Any,
) -> CreateProcessInstanceResult:
    """Create process instance

     Creates and starts an instance of the specified process.
    The process definition to use to create the instance can be specified either using its unique key
    (as returned by Deploy resources), or using the BPMN process id and a version.

    Waits for the completion of the process instance before returning a result
    when awaitCompletion is enabled.

    Args:
        body (ProcessCreationById | ProcessCreationByKey): Instructions for creating a process
            instance. The process definition can be specified
            either by id or by key.

    Raises:
        errors.CreateProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.CreateProcessInstanceGatewayTimeout: If the response status code is 504. The process instance creation request timed out in the gateway. This can happen if the `awaitCompletion` request parameter is set to `true` and the created process instance did not complete within the defined request timeout. This often happens when the created instance is not fully automated or contains wait states.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CreateProcessInstanceResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateProcessInstanceBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CreateProcessInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateProcessInstanceServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 504:
            raise errors.CreateProcessInstanceGatewayTimeout(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateProcessInstanceResult, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ProcessCreationById | ProcessCreationByKey,
) -> Response[CreateProcessInstanceResult | ProblemDetail]:
    """Create process instance

     Creates and starts an instance of the specified process.
    The process definition to use to create the instance can be specified either using its unique key
    (as returned by Deploy resources), or using the BPMN process id and a version.

    Waits for the completion of the process instance before returning a result
    when awaitCompletion is enabled.

    Args:
        body (ProcessCreationById | ProcessCreationByKey): Instructions for creating a process
            instance. The process definition can be specified
            either by id or by key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateProcessInstanceResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ProcessCreationById | ProcessCreationByKey,
    **kwargs: Any,
) -> CreateProcessInstanceResult:
    """Create process instance

     Creates and starts an instance of the specified process.
    The process definition to use to create the instance can be specified either using its unique key
    (as returned by Deploy resources), or using the BPMN process id and a version.

    Waits for the completion of the process instance before returning a result
    when awaitCompletion is enabled.

    Args:
        body (ProcessCreationById | ProcessCreationByKey): Instructions for creating a process
            instance. The process definition can be specified
            either by id or by key.

    Raises:
        errors.CreateProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CreateProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CreateProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.CreateProcessInstanceGatewayTimeout: If the response status code is 504. The process instance creation request timed out in the gateway. This can happen if the `awaitCompletion` request parameter is set to `true` and the created process instance did not complete within the defined request timeout. This often happens when the created instance is not fully automated or contains wait states.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CreateProcessInstanceResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CreateProcessInstanceBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CreateProcessInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CreateProcessInstanceServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 504:
            raise errors.CreateProcessInstanceGatewayTimeout(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CreateProcessInstanceResult, response.parsed)
