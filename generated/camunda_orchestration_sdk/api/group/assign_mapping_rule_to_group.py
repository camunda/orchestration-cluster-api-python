from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assign_mapping_rule_to_group_response_400 import AssignMappingRuleToGroupResponse400
from ...models.assign_mapping_rule_to_group_response_403 import AssignMappingRuleToGroupResponse403
from ...models.assign_mapping_rule_to_group_response_404 import AssignMappingRuleToGroupResponse404
from ...models.assign_mapping_rule_to_group_response_409 import AssignMappingRuleToGroupResponse409
from ...models.assign_mapping_rule_to_group_response_500 import AssignMappingRuleToGroupResponse500
from ...models.assign_mapping_rule_to_group_response_503 import AssignMappingRuleToGroupResponse503
from ...types import Response

def _get_kwargs(group_id: str, mapping_rule_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'put', 'url': '/groups/{group_id}/mapping-rules/{mapping_rule_id}'.format(group_id=quote(str(group_id), safe=''), mapping_rule_id=quote(str(mapping_rule_id), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AssignMappingRuleToGroupResponse400 | AssignMappingRuleToGroupResponse403 | AssignMappingRuleToGroupResponse404 | AssignMappingRuleToGroupResponse409 | AssignMappingRuleToGroupResponse500 | AssignMappingRuleToGroupResponse503 | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = AssignMappingRuleToGroupResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 403:
        response_403 = AssignMappingRuleToGroupResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = AssignMappingRuleToGroupResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = AssignMappingRuleToGroupResponse409.from_dict(response.json())
        return response_409
    if response.status_code == 500:
        response_500 = AssignMappingRuleToGroupResponse500.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = AssignMappingRuleToGroupResponse503.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AssignMappingRuleToGroupResponse400 | AssignMappingRuleToGroupResponse403 | AssignMappingRuleToGroupResponse404 | AssignMappingRuleToGroupResponse409 | AssignMappingRuleToGroupResponse500 | AssignMappingRuleToGroupResponse503]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(group_id: str, mapping_rule_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | AssignMappingRuleToGroupResponse400 | AssignMappingRuleToGroupResponse403 | AssignMappingRuleToGroupResponse404 | AssignMappingRuleToGroupResponse409 | AssignMappingRuleToGroupResponse500 | AssignMappingRuleToGroupResponse503]:
    """Assign a mapping rule to a group

     Assigns a mapping rule to a group.

    Args:
        group_id (str):
        mapping_rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AssignMappingRuleToGroupResponse400 | AssignMappingRuleToGroupResponse403 | AssignMappingRuleToGroupResponse404 | AssignMappingRuleToGroupResponse409 | AssignMappingRuleToGroupResponse500 | AssignMappingRuleToGroupResponse503]
    """
    kwargs = _get_kwargs(group_id=group_id, mapping_rule_id=mapping_rule_id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(group_id: str, mapping_rule_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any) -> None:
    """Assign a mapping rule to a group

 Assigns a mapping rule to a group.

Args:
    group_id (str):
    mapping_rule_id (str):

Raises:
    errors.AssignMappingRuleToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignMappingRuleToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignMappingRuleToGroupNotFound: If the response status code is 404. The group or mapping rule with the given ID was not found.
    errors.AssignMappingRuleToGroupConflict: If the response status code is 409. The mapping rule with the given ID is already assigned to the group.
    errors.AssignMappingRuleToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignMappingRuleToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
    response = sync_detailed(group_id=group_id, mapping_rule_id=mapping_rule_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.AssignMappingRuleToGroupBadRequest(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.AssignMappingRuleToGroupForbidden(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.AssignMappingRuleToGroupNotFound(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse404, response.parsed))
        if response.status_code == 409:
            raise errors.AssignMappingRuleToGroupConflict(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse409, response.parsed))
        if response.status_code == 500:
            raise errors.AssignMappingRuleToGroupInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.AssignMappingRuleToGroupServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None

async def asyncio_detailed(group_id: str, mapping_rule_id: str, *, client: AuthenticatedClient | Client) -> Response[Any | AssignMappingRuleToGroupResponse400 | AssignMappingRuleToGroupResponse403 | AssignMappingRuleToGroupResponse404 | AssignMappingRuleToGroupResponse409 | AssignMappingRuleToGroupResponse500 | AssignMappingRuleToGroupResponse503]:
    """Assign a mapping rule to a group

     Assigns a mapping rule to a group.

    Args:
        group_id (str):
        mapping_rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AssignMappingRuleToGroupResponse400 | AssignMappingRuleToGroupResponse403 | AssignMappingRuleToGroupResponse404 | AssignMappingRuleToGroupResponse409 | AssignMappingRuleToGroupResponse500 | AssignMappingRuleToGroupResponse503]
    """
    kwargs = _get_kwargs(group_id=group_id, mapping_rule_id=mapping_rule_id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(group_id: str, mapping_rule_id: str, *, client: AuthenticatedClient | Client, **kwargs: Any) -> None:
    """Assign a mapping rule to a group

 Assigns a mapping rule to a group.

Args:
    group_id (str):
    mapping_rule_id (str):

Raises:
    errors.AssignMappingRuleToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignMappingRuleToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignMappingRuleToGroupNotFound: If the response status code is 404. The group or mapping rule with the given ID was not found.
    errors.AssignMappingRuleToGroupConflict: If the response status code is 409. The mapping rule with the given ID is already assigned to the group.
    errors.AssignMappingRuleToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignMappingRuleToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
    response = await asyncio_detailed(group_id=group_id, mapping_rule_id=mapping_rule_id, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.AssignMappingRuleToGroupBadRequest(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse400, response.parsed))
        if response.status_code == 403:
            raise errors.AssignMappingRuleToGroupForbidden(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.AssignMappingRuleToGroupNotFound(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse404, response.parsed))
        if response.status_code == 409:
            raise errors.AssignMappingRuleToGroupConflict(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse409, response.parsed))
        if response.status_code == 500:
            raise errors.AssignMappingRuleToGroupInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse500, response.parsed))
        if response.status_code == 503:
            raise errors.AssignMappingRuleToGroupServiceUnavailable(status_code=response.status_code, content=response.content, parsed=cast(AssignMappingRuleToGroupResponse503, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None