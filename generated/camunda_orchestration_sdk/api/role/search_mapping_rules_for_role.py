from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.mapping_rule_search_query_request import MappingRuleSearchQueryRequest
from ...models.problem_detail import ProblemDetail
from ...models.search_query_response import SearchQueryResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    role_id: str, *, body: MappingRuleSearchQueryRequest | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/roles/{role_id}/mapping-rules/search".format(
            role_id=quote(str(role_id), safe="")
        ),
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | SearchQueryResponse | None:
    if response.status_code == 200:
        response_200 = SearchQueryResponse.from_dict(response.json())
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
) -> Response[ProblemDetail | SearchQueryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    role_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[ProblemDetail | SearchQueryResponse]:
    """Search role mapping rules

     Search mapping rules with assigned role.

    Args:
        role_id (str):
        body (MappingRuleSearchQueryRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | SearchQueryResponse]
    """
    kwargs = _get_kwargs(role_id=role_id, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    role_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse:
    """Search role mapping rules

     Search mapping rules with assigned role.

    Args:
        role_id (str):
        body (MappingRuleSearchQueryRequest | Unset):

    Raises:
        errors.SearchMappingRulesForRoleBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchMappingRulesForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchMappingRulesForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchMappingRulesForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
        errors.SearchMappingRulesForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SearchQueryResponse"""
    response = sync_detailed(role_id=role_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchMappingRulesForRoleBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchMappingRulesForRoleUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchMappingRulesForRoleForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.SearchMappingRulesForRoleNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchMappingRulesForRoleInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchQueryResponse, response.parsed)


async def asyncio_detailed(
    role_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
) -> Response[ProblemDetail | SearchQueryResponse]:
    """Search role mapping rules

     Search mapping rules with assigned role.

    Args:
        role_id (str):
        body (MappingRuleSearchQueryRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | SearchQueryResponse]
    """
    kwargs = _get_kwargs(role_id=role_id, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    role_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MappingRuleSearchQueryRequest | Unset = UNSET,
    **kwargs: Any,
) -> SearchQueryResponse:
    """Search role mapping rules

     Search mapping rules with assigned role.

    Args:
        role_id (str):
        body (MappingRuleSearchQueryRequest | Unset):

    Raises:
        errors.SearchMappingRulesForRoleBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchMappingRulesForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.SearchMappingRulesForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.SearchMappingRulesForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
        errors.SearchMappingRulesForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        SearchQueryResponse"""
    response = await asyncio_detailed(role_id=role_id, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchMappingRulesForRoleBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.SearchMappingRulesForRoleUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.SearchMappingRulesForRoleForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.SearchMappingRulesForRoleNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchMappingRulesForRoleInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(SearchQueryResponse, response.parsed)
