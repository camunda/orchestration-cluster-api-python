from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.decision_instance_get_query_result import DecisionInstanceGetQueryResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(decision_evaluation_instance_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/decision-instances/{decision_evaluation_instance_key}".format(
            decision_evaluation_instance_key=quote(
                str(decision_evaluation_instance_key), safe=""
            )
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DecisionInstanceGetQueryResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = DecisionInstanceGetQueryResult.from_dict(response.json())
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
) -> Response[DecisionInstanceGetQueryResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    decision_evaluation_instance_key: str, *, client: AuthenticatedClient | Client
) -> Response[DecisionInstanceGetQueryResult | ProblemDetail]:
    """Get decision instance

     Returns a decision instance.

    Args:
        decision_evaluation_instance_key (str): System-generated key for a deployed decision
            instance. Example: 22517998136843567.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DecisionInstanceGetQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(
        decision_evaluation_instance_key=decision_evaluation_instance_key
    )
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    decision_evaluation_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    **kwargs: Any,
) -> DecisionInstanceGetQueryResult:
    """Get decision instance

     Returns a decision instance.

    Args:
        decision_evaluation_instance_key (str): System-generated key for a deployed decision
            instance. Example: 22517998136843567.

    Raises:
        errors.GetDecisionInstanceBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetDecisionInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetDecisionInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetDecisionInstanceNotFound: If the response status code is 404. The decision instance with the given key was not found. More details are provided in the response body.
        errors.GetDecisionInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        DecisionInstanceGetQueryResult"""
    response = sync_detailed(
        decision_evaluation_instance_key=decision_evaluation_instance_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetDecisionInstanceBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetDecisionInstanceUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetDecisionInstanceForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetDecisionInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetDecisionInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(DecisionInstanceGetQueryResult, response.parsed)


async def asyncio_detailed(
    decision_evaluation_instance_key: str, *, client: AuthenticatedClient | Client
) -> Response[DecisionInstanceGetQueryResult | ProblemDetail]:
    """Get decision instance

     Returns a decision instance.

    Args:
        decision_evaluation_instance_key (str): System-generated key for a deployed decision
            instance. Example: 22517998136843567.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DecisionInstanceGetQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(
        decision_evaluation_instance_key=decision_evaluation_instance_key
    )
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    decision_evaluation_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    **kwargs: Any,
) -> DecisionInstanceGetQueryResult:
    """Get decision instance

     Returns a decision instance.

    Args:
        decision_evaluation_instance_key (str): System-generated key for a deployed decision
            instance. Example: 22517998136843567.

    Raises:
        errors.GetDecisionInstanceBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetDecisionInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetDecisionInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetDecisionInstanceNotFound: If the response status code is 404. The decision instance with the given key was not found. More details are provided in the response body.
        errors.GetDecisionInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        DecisionInstanceGetQueryResult"""
    response = await asyncio_detailed(
        decision_evaluation_instance_key=decision_evaluation_instance_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetDecisionInstanceBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetDecisionInstanceUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetDecisionInstanceForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetDecisionInstanceNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetDecisionInstanceInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(DecisionInstanceGetQueryResult, response.parsed)
