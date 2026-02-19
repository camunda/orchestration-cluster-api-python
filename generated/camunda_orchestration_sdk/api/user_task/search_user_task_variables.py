from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.problem_detail import ProblemDetail
from ...models.search_user_task_variables_data import SearchUserTaskVariablesData
from ...models.variable_search_query_result import VariableSearchQueryResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_task_key: str,
    *,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}
    params["truncateValues"] = truncate_values
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/user-tasks/{user_task_key}/variables/search".format(
            user_task_key=quote(str(user_task_key), safe="")
        ),
        "params": params,
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | VariableSearchQueryResult | None:
    if response.status_code == 200:
        response_200 = VariableSearchQueryResult.from_dict(response.json())
        return response_200
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | VariableSearchQueryResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableSearchQueryResult]:
    """Search user task variables

     Search for user task variables based on given criteria. This endpoint returns all variables
    visible from the user task's scope, including variables from parent scopes in the scope
    hierarchy. By default, long variable values in the response are truncated.

    Args:
        user_task_key (str): System-generated key for a user task.
        truncate_values (bool | Unset):
        body (SearchUserTaskVariablesData | Unset): User task search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | VariableSearchQueryResult]
    """
    kwargs = _get_kwargs(
        user_task_key=user_task_key, body=body, truncate_values=truncate_values
    )
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableSearchQueryResult:
    """Search user task variables

     Search for user task variables based on given criteria. This endpoint returns all variables
    visible from the user task's scope, including variables from parent scopes in the scope
    hierarchy. By default, long variable values in the response are truncated.

    Args:
        user_task_key (str): System-generated key for a user task.
        truncate_values (bool | Unset):
        body (SearchUserTaskVariablesData | Unset): User task search query request.

    Raises:
        errors.SearchUserTaskVariablesBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchUserTaskVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        VariableSearchQueryResult"""
    response = sync_detailed(
        user_task_key=user_task_key,
        client=client,
        body=body,
        truncate_values=truncate_values,
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchUserTaskVariablesBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchUserTaskVariablesInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(VariableSearchQueryResult, response.parsed)


async def asyncio_detailed(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
) -> Response[ProblemDetail | VariableSearchQueryResult]:
    """Search user task variables

     Search for user task variables based on given criteria. This endpoint returns all variables
    visible from the user task's scope, including variables from parent scopes in the scope
    hierarchy. By default, long variable values in the response are truncated.

    Args:
        user_task_key (str): System-generated key for a user task.
        truncate_values (bool | Unset):
        body (SearchUserTaskVariablesData | Unset): User task search query request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProblemDetail | VariableSearchQueryResult]
    """
    kwargs = _get_kwargs(
        user_task_key=user_task_key, body=body, truncate_values=truncate_values
    )
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    user_task_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SearchUserTaskVariablesData | Unset = UNSET,
    truncate_values: bool | Unset = UNSET,
    **kwargs: Any,
) -> VariableSearchQueryResult:
    """Search user task variables

     Search for user task variables based on given criteria. This endpoint returns all variables
    visible from the user task's scope, including variables from parent scopes in the scope
    hierarchy. By default, long variable values in the response are truncated.

    Args:
        user_task_key (str): System-generated key for a user task.
        truncate_values (bool | Unset):
        body (SearchUserTaskVariablesData | Unset): User task search query request.

    Raises:
        errors.SearchUserTaskVariablesBadRequest: If the response status code is 400. The provided data is not valid.
        errors.SearchUserTaskVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        VariableSearchQueryResult"""
    response = await asyncio_detailed(
        user_task_key=user_task_key,
        client=client,
        body=body,
        truncate_values=truncate_values,
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.SearchUserTaskVariablesBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.SearchUserTaskVariablesInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(VariableSearchQueryResult, response.parsed)
