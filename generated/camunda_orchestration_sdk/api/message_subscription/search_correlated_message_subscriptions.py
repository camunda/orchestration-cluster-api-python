from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.correlated_message_subscription_search_query import (
    CorrelatedMessageSubscriptionSearchQuery,
)
from ...models.correlated_message_subscription_search_query_result import (
    CorrelatedMessageSubscriptionSearchQueryResult,
)
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: CorrelatedMessageSubscriptionSearchQuery | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/correlated-message-subscriptions/search",
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CorrelatedMessageSubscriptionSearchQueryResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = CorrelatedMessageSubscriptionSearchQueryResult.from_dict(
            response.json()
        )
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
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CorrelatedMessageSubscriptionSearchQueryResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CorrelatedMessageSubscriptionSearchQuery | Unset = UNSET,
) -> Response[CorrelatedMessageSubscriptionSearchQueryResult | ProblemDetail]:
    """Search correlated message subscriptions

     Search correlated message subscriptions based on given criteria.

    Args:
        body (CorrelatedMessageSubscriptionSearchQuery | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorrelatedMessageSubscriptionSearchQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: CorrelatedMessageSubscriptionSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> CorrelatedMessageSubscriptionSearchQueryResult:
    """Search correlated message subscriptions

     Search correlated message subscriptions based on given criteria.

    Args:
        body (CorrelatedMessageSubscriptionSearchQuery | Unset):

    Raises:
        errors.SearchCorrelatedMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchCorrelatedMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchCorrelatedMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchCorrelatedMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CorrelatedMessageSubscriptionSearchQueryResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchCorrelatedMessageSubscriptionsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchCorrelatedMessageSubscriptionsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchCorrelatedMessageSubscriptionsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchCorrelatedMessageSubscriptionsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CorrelatedMessageSubscriptionSearchQueryResult, response.parsed)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CorrelatedMessageSubscriptionSearchQuery | Unset = UNSET,
) -> Response[CorrelatedMessageSubscriptionSearchQueryResult | ProblemDetail]:
    """Search correlated message subscriptions

     Search correlated message subscriptions based on given criteria.

    Args:
        body (CorrelatedMessageSubscriptionSearchQuery | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CorrelatedMessageSubscriptionSearchQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CorrelatedMessageSubscriptionSearchQuery | Unset = UNSET,
    **kwargs: Any,
) -> CorrelatedMessageSubscriptionSearchQueryResult:
    """Search correlated message subscriptions

     Search correlated message subscriptions based on given criteria.

    Args:
        body (CorrelatedMessageSubscriptionSearchQuery | Unset):

    Raises:
        errors.SearchCorrelatedMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchCorrelatedMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchCorrelatedMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchCorrelatedMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        CorrelatedMessageSubscriptionSearchQueryResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchCorrelatedMessageSubscriptionsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchCorrelatedMessageSubscriptionsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchCorrelatedMessageSubscriptionsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchCorrelatedMessageSubscriptionsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(CorrelatedMessageSubscriptionSearchQueryResult, response.parsed)
