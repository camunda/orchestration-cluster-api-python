from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.mapping_rule_result import MappingRuleResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(mapping_rule_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/mapping-rules/{mapping_rule_id}".format(
            mapping_rule_id=quote(str(mapping_rule_id), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> MappingRuleResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = MappingRuleResult.from_dict(response.json())
        return response_200
    if response.status_code == 401:
        response_401 = ProblemDetail.from_dict(response.json())
        return response_401
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
) -> Response[MappingRuleResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    mapping_rule_id: str, *, client: AuthenticatedClient | Client
) -> Response[MappingRuleResult | ProblemDetail]:
    """Get a mapping rule

     Gets the mapping rule with the given ID.

    Args:
        mapping_rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MappingRuleResult | ProblemDetail]
    """
    kwargs = _get_kwargs(mapping_rule_id=mapping_rule_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    mapping_rule_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> MappingRuleResult:
    """Get a mapping rule

     Gets the mapping rule with the given ID.

    Args:
        mapping_rule_id (str):

    Raises:
        errors.GetMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetMappingRuleNotFound: If the response status code is 404. The mapping rule with the mappingRuleId was not found.
        errors.GetMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        MappingRuleResult"""
    response = sync_detailed(mapping_rule_id=mapping_rule_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetMappingRuleUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetMappingRuleNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetMappingRuleInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(MappingRuleResult, response.parsed)


async def asyncio_detailed(
    mapping_rule_id: str, *, client: AuthenticatedClient | Client
) -> Response[MappingRuleResult | ProblemDetail]:
    """Get a mapping rule

     Gets the mapping rule with the given ID.

    Args:
        mapping_rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MappingRuleResult | ProblemDetail]
    """
    kwargs = _get_kwargs(mapping_rule_id=mapping_rule_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    mapping_rule_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> MappingRuleResult:
    """Get a mapping rule

     Gets the mapping rule with the given ID.

    Args:
        mapping_rule_id (str):

    Raises:
        errors.GetMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetMappingRuleNotFound: If the response status code is 404. The mapping rule with the mappingRuleId was not found.
        errors.GetMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        MappingRuleResult"""
    response = await asyncio_detailed(mapping_rule_id=mapping_rule_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 401:
            raise errors.GetMappingRuleUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetMappingRuleNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetMappingRuleInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(MappingRuleResult, response.parsed)
