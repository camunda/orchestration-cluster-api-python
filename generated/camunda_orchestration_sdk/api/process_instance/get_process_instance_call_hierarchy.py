from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.process_instance_call_hierarchy_entry import (
    ProcessInstanceCallHierarchyEntry,
)
from ...types import Response


def _get_kwargs(process_instance_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/process-instances/{process_instance_key}/call-hierarchy".format(
            process_instance_key=quote(str(process_instance_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | list[ProcessInstanceCallHierarchyEntry] | None:
    if response.status_code == 200:
        response_200: list[ProcessInstanceCallHierarchyEntry] = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProcessInstanceCallHierarchyEntry.from_dict(
                response_200_item_data
            )
            response_200.append(response_200_item)
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
) -> Response[ProblemDetail | list[ProcessInstanceCallHierarchyEntry]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    process_instance_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | list[ProcessInstanceCallHierarchyEntry]]:
    """Get call hierarchy

     Returns the call hierarchy for a given process instance, showing its ancestry up to the root
    instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | list[ProcessInstanceCallHierarchyEntry]]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> list[Any]:
    """Get call hierarchy

     Returns the call hierarchy for a given process instance, showing its ancestry up to the root
    instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.GetProcessInstanceCallHierarchyBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessInstanceCallHierarchyUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessInstanceCallHierarchyForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessInstanceCallHierarchyNotFound: If the response status code is 404. The process instance is not found.
        errors.GetProcessInstanceCallHierarchyInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        list[Any]"""
    response = sync_detailed(process_instance_key=process_instance_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceCallHierarchyBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessInstanceCallHierarchyUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessInstanceCallHierarchyForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetProcessInstanceCallHierarchyNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessInstanceCallHierarchyInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(list[Any], response.parsed)


async def asyncio_detailed(
    process_instance_key: str, *, client: AuthenticatedClient | Client
) -> Response[ProblemDetail | list[ProcessInstanceCallHierarchyEntry]]:
    """Get call hierarchy

     Returns the call hierarchy for a given process instance, showing its ancestry up to the root
    instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | list[ProcessInstanceCallHierarchyEntry]]
    """
    kwargs = _get_kwargs(process_instance_key=process_instance_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    process_instance_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> list[Any]:
    """Get call hierarchy

     Returns the call hierarchy for a given process instance, showing its ancestry up to the root
    instance.

    Args:
        process_instance_key (str): System-generated key for a process instance. Example:
            2251799813690746.

    Raises:
        errors.GetProcessInstanceCallHierarchyBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessInstanceCallHierarchyUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessInstanceCallHierarchyForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessInstanceCallHierarchyNotFound: If the response status code is 404. The process instance is not found.
        errors.GetProcessInstanceCallHierarchyInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        list[Any]"""
    response = await asyncio_detailed(
        process_instance_key=process_instance_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessInstanceCallHierarchyBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessInstanceCallHierarchyUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessInstanceCallHierarchyForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetProcessInstanceCallHierarchyNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessInstanceCallHierarchyInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(list[Any], response.parsed)
