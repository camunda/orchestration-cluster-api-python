from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.form_result import FormResult
from ...models.problem_detail import ProblemDetail
from ...types import Response


def _get_kwargs(process_definition_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/process-definitions/{process_definition_key}/form".format(
            process_definition_key=quote(str(process_definition_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | FormResult | ProblemDetail | None:
    if response.status_code == 200:
        response_200 = FormResult.from_dict(response.json())
        return response_200
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
) -> Response[Any | FormResult | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    process_definition_key: str, *, client: AuthenticatedClient | Client
) -> Response[Any | FormResult | ProblemDetail]:
    """Get process start form

     Get the start form of a process.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | FormResult | ProblemDetail]
    """
    kwargs = _get_kwargs(process_definition_key=process_definition_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    process_definition_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> FormResult:
    """Get process start form

     Get the start form of a process.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.GetStartProcessFormBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetStartProcessFormUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetStartProcessFormForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetStartProcessFormNotFound: If the response status code is 404. Not found
        errors.GetStartProcessFormInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        FormResult"""
    response = sync_detailed(
        process_definition_key=process_definition_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetStartProcessFormBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetStartProcessFormUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetStartProcessFormForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetStartProcessFormNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetStartProcessFormInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(FormResult, response.parsed)


async def asyncio_detailed(
    process_definition_key: str, *, client: AuthenticatedClient | Client
) -> Response[Any | FormResult | ProblemDetail]:
    """Get process start form

     Get the start form of a process.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | FormResult | ProblemDetail]
    """
    kwargs = _get_kwargs(process_definition_key=process_definition_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    process_definition_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> FormResult:
    """Get process start form

     Get the start form of a process.
    Note that this endpoint will only return linked forms. This endpoint does not support embedded
    forms.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.GetStartProcessFormBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetStartProcessFormUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetStartProcessFormForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetStartProcessFormNotFound: If the response status code is 404. Not found
        errors.GetStartProcessFormInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        FormResult"""
    response = await asyncio_detailed(
        process_definition_key=process_definition_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetStartProcessFormBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetStartProcessFormUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetStartProcessFormForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetStartProcessFormNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetStartProcessFormInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(FormResult, response.parsed)
