from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_instance_update_request import AgentInstanceUpdateRequest
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(
    agent_instance_key: str, *, body: AgentInstanceUpdateRequest
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/agent-instances/{agent_instance_key}".format(
            agent_instance_key=quote(str(agent_instance_key), safe="")
        ),
    }
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
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
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceUpdateRequest,
) -> Response[Any | ProblemDetail]:
    """Update agent instance

     Updates the mutable fields of an agent instance: status, metric counters, and
    tools. Metric values are treated as deltas and applied immediately to the
    aggregate counters. Tool updates replace the existing tool list.

    Args:
        agent_instance_key (str): System-generated key for an agent instance. Example:
            4503599627370496.
        body (AgentInstanceUpdateRequest): Request to update the mutable state of an agent
            instance.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(agent_instance_key=agent_instance_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceUpdateRequest,
    **kwargs: Any,
) -> None:
    """Update agent instance

     Updates the mutable fields of an agent instance: status, metric counters, and
    tools. Metric values are treated as deltas and applied immediately to the
    aggregate counters. Tool updates replace the existing tool list.

    Args:
        agent_instance_key (str): System-generated key for an agent instance. Example:
            4503599627370496.
        body (AgentInstanceUpdateRequest): Request to update the mutable state of an agent
            instance.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. The agent instance with the given key was not found. More details are provided in the response body.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(
        agent_instance_key=agent_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="update_agent_instance"
        )
    return None


async def asyncio_detailed(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceUpdateRequest,
) -> Response[Any | ProblemDetail]:
    """Update agent instance

     Updates the mutable fields of an agent instance: status, metric counters, and
    tools. Metric values are treated as deltas and applied immediately to the
    aggregate counters. Tool updates replace the existing tool list.

    Args:
        agent_instance_key (str): System-generated key for an agent instance. Example:
            4503599627370496.
        body (AgentInstanceUpdateRequest): Request to update the mutable state of an agent
            instance.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(agent_instance_key=agent_instance_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    agent_instance_key: str,
    *,
    client: AuthenticatedClient,
    body: AgentInstanceUpdateRequest,
    **kwargs: Any,
) -> None:
    """Update agent instance

     Updates the mutable fields of an agent instance: status, metric counters, and
    tools. Metric values are treated as deltas and applied immediately to the
    aggregate counters. Tool updates replace the existing tool list.

    Args:
        agent_instance_key (str): System-generated key for an agent instance. Example:
            4503599627370496.
        body (AgentInstanceUpdateRequest): Request to update the mutable state of an agent
            instance.

    Raises:
        errors.BadRequestError: If the response status code is 400. The provided data is not valid.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. The agent instance with the given key was not found. More details are provided in the response body.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(
        agent_instance_key=agent_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="update_agent_instance",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="update_agent_instance"
        )
    return None
