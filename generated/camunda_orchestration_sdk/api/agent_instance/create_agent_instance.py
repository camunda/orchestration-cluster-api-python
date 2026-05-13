from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_instance_creation_request import AgentInstanceCreationRequest
from ...models.agent_instance_creation_result import AgentInstanceCreationResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(*, body: AgentInstanceCreationRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/agent-instances"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AgentInstanceCreationResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = AgentInstanceCreationResult.from_dict(response.json())
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
    if response.status_code == 503:
        response_503 = ProblemDetail.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentInstanceCreationResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: AgentInstanceCreationRequest
) -> Response[AgentInstanceCreationResult | ProblemDetail]:
    """Create agent instance

     Creates a new agent instance. The returned key identifies the instance and must
    be used in subsequent update and query calls.

    Args:
        body (AgentInstanceCreationRequest): Request to create a new agent instance.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentInstanceCreationResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: AgentInstanceCreationRequest,
    **kwargs: Any,
) -> AgentInstanceCreationResult:
    """Create agent instance

     Creates a new agent instance. The returned key identifies the instance and must
    be used in subsequent update and query calls.

    Args:
        body (AgentInstanceCreationRequest): Request to create a new agent instance.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. The elementInstanceKey does not correspond to an active element instance. More details are provided in the response body.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        AgentInstanceCreationResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="create_agent_instance"
        )
    assert response.parsed is not None
    return cast(AgentInstanceCreationResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: AgentInstanceCreationRequest
) -> Response[AgentInstanceCreationResult | ProblemDetail]:
    """Create agent instance

     Creates a new agent instance. The returned key identifies the instance and must
    be used in subsequent update and query calls.

    Args:
        body (AgentInstanceCreationRequest): Request to create a new agent instance.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentInstanceCreationResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AgentInstanceCreationRequest,
    **kwargs: Any,
) -> AgentInstanceCreationResult:
    """Create agent instance

     Creates a new agent instance. The returned key identifies the instance and must
    be used in subsequent update and query calls.

    Args:
        body (AgentInstanceCreationRequest): Request to create a new agent instance.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. The elementInstanceKey does not correspond to an active element instance. More details are provided in the response body.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        AgentInstanceCreationResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_agent_instance",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="create_agent_instance"
        )
    assert response.parsed is not None
    return cast(AgentInstanceCreationResult, response.parsed)
