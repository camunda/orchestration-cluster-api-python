from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.incident_search_query import IncidentSearchQuery
from ...models.incident_search_query_result import IncidentSearchQueryResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(
    element_instance_key: str, *, body: IncidentSearchQuery
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/element-instances/{element_instance_key}/incidents/search".format(
            element_instance_key=quote(str(element_instance_key), safe="")
        ),
    }
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> IncidentSearchQueryResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = IncidentSearchQueryResult.from_dict(response.json())
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
) -> Response[IncidentSearchQueryResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    element_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: IncidentSearchQuery,
) -> Response[IncidentSearchQueryResult | ProblemDetail]:
    """Search for incidents of a specific element instance

     Search for incidents caused by the specified element instance, including incidents of any child
    instances created from this element instance.

    Although the `elementInstanceKey` is provided as a path parameter to indicate the root element
    instance,
    you may also include an `elementInstanceKey` within the filter object to narrow results to specific
    child element instances. This is useful, for example, if you want to isolate incidents associated
    with
    nested or subordinate elements within the given element instance while excluding incidents directly
    tied
    to the root element itself.

    Args:
        element_instance_key (str): System-generated key for a element instance. Example:
            2251799813686789.
        body (IncidentSearchQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IncidentSearchQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(element_instance_key=element_instance_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    element_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: IncidentSearchQuery,
    **kwargs: Any,
) -> IncidentSearchQueryResult:
    """Search for incidents of a specific element instance

     Search for incidents caused by the specified element instance, including incidents of any child
    instances created from this element instance.

    Although the `elementInstanceKey` is provided as a path parameter to indicate the root element
    instance,
    you may also include an `elementInstanceKey` within the filter object to narrow results to specific
    child element instances. This is useful, for example, if you want to isolate incidents associated
    with
    nested or subordinate elements within the given element instance while excluding incidents directly
    tied
    to the root element itself.

    Args:
        element_instance_key (str): System-generated key for a element instance. Example:
            2251799813686789.
        body (IncidentSearchQuery):

    Raises:
        errors.SearchElementInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchElementInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchElementInstanceIncidentsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchElementInstanceIncidentsNotFound: If the response status code is 404. The element instance with the given key was not found.
        errors.SearchElementInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        IncidentSearchQueryResult"""
    response = sync_detailed(
        element_instance_key=element_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchElementInstanceIncidentsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchElementInstanceIncidentsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchElementInstanceIncidentsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.SearchElementInstanceIncidentsNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchElementInstanceIncidentsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(IncidentSearchQueryResult, response.parsed)


async def asyncio_detailed(
    element_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: IncidentSearchQuery,
) -> Response[IncidentSearchQueryResult | ProblemDetail]:
    """Search for incidents of a specific element instance

     Search for incidents caused by the specified element instance, including incidents of any child
    instances created from this element instance.

    Although the `elementInstanceKey` is provided as a path parameter to indicate the root element
    instance,
    you may also include an `elementInstanceKey` within the filter object to narrow results to specific
    child element instances. This is useful, for example, if you want to isolate incidents associated
    with
    nested or subordinate elements within the given element instance while excluding incidents directly
    tied
    to the root element itself.

    Args:
        element_instance_key (str): System-generated key for a element instance. Example:
            2251799813686789.
        body (IncidentSearchQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IncidentSearchQueryResult | ProblemDetail]
    """
    kwargs = _get_kwargs(element_instance_key=element_instance_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    element_instance_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: IncidentSearchQuery,
    **kwargs: Any,
) -> IncidentSearchQueryResult:
    """Search for incidents of a specific element instance

     Search for incidents caused by the specified element instance, including incidents of any child
    instances created from this element instance.

    Although the `elementInstanceKey` is provided as a path parameter to indicate the root element
    instance,
    you may also include an `elementInstanceKey` within the filter object to narrow results to specific
    child element instances. This is useful, for example, if you want to isolate incidents associated
    with
    nested or subordinate elements within the given element instance while excluding incidents directly
    tied
    to the root element itself.

    Args:
        element_instance_key (str): System-generated key for a element instance. Example:
            2251799813686789.
        body (IncidentSearchQuery):

    Raises:
        errors.SearchElementInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchElementInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchElementInstanceIncidentsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchElementInstanceIncidentsNotFound: If the response status code is 404. The element instance with the given key was not found.
        errors.SearchElementInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        IncidentSearchQueryResult"""
    response = await asyncio_detailed(
        element_instance_key=element_instance_key, client=client, body=body
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchElementInstanceIncidentsBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchElementInstanceIncidentsUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchElementInstanceIncidentsForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.SearchElementInstanceIncidentsNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchElementInstanceIncidentsInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(IncidentSearchQueryResult, response.parsed)
