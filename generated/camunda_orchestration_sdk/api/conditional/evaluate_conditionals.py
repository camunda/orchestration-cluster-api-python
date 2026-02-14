from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.conditional_evaluation_instruction import (
    ConditionalEvaluationInstruction,
)
from ...models.evaluate_conditional_result import EvaluateConditionalResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(*, body: ConditionalEvaluationInstruction) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/conditionals/evaluation"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EvaluateConditionalResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = EvaluateConditionalResult.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
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
) -> Response[EvaluateConditionalResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient | Client, body: ConditionalEvaluationInstruction
) -> Response[EvaluateConditionalResult | ProblemDetail]:
    """Evaluate root level conditional start events

     Evaluates root-level conditional start events for process definitions.
    If the evaluation is successful, it will return the keys of all created process instances, along
    with their associated process definition key.
    Multiple root-level conditional start events of the same process definition can trigger if their
    conditions evaluate to true.

    Args:
        body (ConditionalEvaluationInstruction):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EvaluateConditionalResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ConditionalEvaluationInstruction,
    **kwargs: Any,
) -> EvaluateConditionalResult:
    """Evaluate root level conditional start events

     Evaluates root-level conditional start events for process definitions.
    If the evaluation is successful, it will return the keys of all created process instances, along
    with their associated process definition key.
    Multiple root-level conditional start events of the same process definition can trigger if their
    conditions evaluate to true.

    Args:
        body (ConditionalEvaluationInstruction):

    Raises:
        errors.EvaluateConditionalsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.EvaluateConditionalsForbidden: If the response status code is 403. The client is not authorized to start process instances for the specified process definition. If a processDefinitionKey is not provided, this indicates that the client is not authorized to start process instances for at least one of the matched process definitions.
        errors.EvaluateConditionalsNotFound: If the response status code is 404. The process definition was not found for the given processDefinitionKey.
        errors.EvaluateConditionalsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.EvaluateConditionalsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        EvaluateConditionalResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.EvaluateConditionalsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.EvaluateConditionalsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.EvaluateConditionalsNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.EvaluateConditionalsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.EvaluateConditionalsServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(EvaluateConditionalResult, response.parsed)


async def asyncio_detailed(
    *, client: AuthenticatedClient | Client, body: ConditionalEvaluationInstruction
) -> Response[EvaluateConditionalResult | ProblemDetail]:
    """Evaluate root level conditional start events

     Evaluates root-level conditional start events for process definitions.
    If the evaluation is successful, it will return the keys of all created process instances, along
    with their associated process definition key.
    Multiple root-level conditional start events of the same process definition can trigger if their
    conditions evaluate to true.

    Args:
        body (ConditionalEvaluationInstruction):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EvaluateConditionalResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ConditionalEvaluationInstruction,
    **kwargs: Any,
) -> EvaluateConditionalResult:
    """Evaluate root level conditional start events

     Evaluates root-level conditional start events for process definitions.
    If the evaluation is successful, it will return the keys of all created process instances, along
    with their associated process definition key.
    Multiple root-level conditional start events of the same process definition can trigger if their
    conditions evaluate to true.

    Args:
        body (ConditionalEvaluationInstruction):

    Raises:
        errors.EvaluateConditionalsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.EvaluateConditionalsForbidden: If the response status code is 403. The client is not authorized to start process instances for the specified process definition. If a processDefinitionKey is not provided, this indicates that the client is not authorized to start process instances for at least one of the matched process definitions.
        errors.EvaluateConditionalsNotFound: If the response status code is 404. The process definition was not found for the given processDefinitionKey.
        errors.EvaluateConditionalsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.EvaluateConditionalsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        EvaluateConditionalResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.EvaluateConditionalsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.EvaluateConditionalsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.EvaluateConditionalsNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.EvaluateConditionalsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.EvaluateConditionalsServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(EvaluateConditionalResult, response.parsed)
