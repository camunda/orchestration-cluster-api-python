from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_process_definition_xml_response_400 import (
    GetProcessDefinitionXMLResponse400,
)
from ...models.get_process_definition_xml_response_401 import (
    GetProcessDefinitionXMLResponse401,
)
from ...models.get_process_definition_xml_response_403 import (
    GetProcessDefinitionXMLResponse403,
)
from ...models.get_process_definition_xml_response_404 import (
    GetProcessDefinitionXMLResponse404,
)
from ...models.get_process_definition_xml_response_500 import (
    GetProcessDefinitionXMLResponse500,
)
from ...types import Response


def _get_kwargs(process_definition_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/process-definitions/{process_definition_key}/xml".format(
            process_definition_key=quote(str(process_definition_key), safe="")
        ),
    }
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetProcessDefinitionXMLResponse400
    | GetProcessDefinitionXMLResponse401
    | GetProcessDefinitionXMLResponse403
    | GetProcessDefinitionXMLResponse404
    | GetProcessDefinitionXMLResponse500
    | str
    | None
):
    if response.status_code == 200:
        response_200 = response.text
        return response_200
    if response.status_code == 204:
        response_204 = response.text
        return response_204
    if response.status_code == 400:
        response_400 = GetProcessDefinitionXMLResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetProcessDefinitionXMLResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetProcessDefinitionXMLResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetProcessDefinitionXMLResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetProcessDefinitionXMLResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    GetProcessDefinitionXMLResponse400
    | GetProcessDefinitionXMLResponse401
    | GetProcessDefinitionXMLResponse403
    | GetProcessDefinitionXMLResponse404
    | GetProcessDefinitionXMLResponse500
    | str
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    process_definition_key: str, *, client: AuthenticatedClient | Client
) -> Response[
    GetProcessDefinitionXMLResponse400
    | GetProcessDefinitionXMLResponse401
    | GetProcessDefinitionXMLResponse403
    | GetProcessDefinitionXMLResponse404
    | GetProcessDefinitionXMLResponse500
    | str
]:
    """Get process definition XML

     Returns process definition as XML.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessDefinitionXMLResponse400 | GetProcessDefinitionXMLResponse401 | GetProcessDefinitionXMLResponse403 | GetProcessDefinitionXMLResponse404 | GetProcessDefinitionXMLResponse500 | str]
    """
    kwargs = _get_kwargs(process_definition_key=process_definition_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    process_definition_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> str:
    """Get process definition XML

     Returns process definition as XML.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.GetProcessDefinitionXmlBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessDefinitionXmlUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessDefinitionXmlForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessDefinitionXmlNotFound: If the response status code is 404. The process definition with the given key was not found. More details are provided in the response body.
        errors.GetProcessDefinitionXmlInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        str"""
    response = sync_detailed(
        process_definition_key=process_definition_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessDefinitionXmlBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessDefinitionXmlUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessDefinitionXmlForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetProcessDefinitionXmlNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessDefinitionXmlInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(str, response.parsed)


async def asyncio_detailed(
    process_definition_key: str, *, client: AuthenticatedClient | Client
) -> Response[
    GetProcessDefinitionXMLResponse400
    | GetProcessDefinitionXMLResponse401
    | GetProcessDefinitionXMLResponse403
    | GetProcessDefinitionXMLResponse404
    | GetProcessDefinitionXMLResponse500
    | str
]:
    """Get process definition XML

     Returns process definition as XML.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetProcessDefinitionXMLResponse400 | GetProcessDefinitionXMLResponse401 | GetProcessDefinitionXMLResponse403 | GetProcessDefinitionXMLResponse404 | GetProcessDefinitionXMLResponse500 | str]
    """
    kwargs = _get_kwargs(process_definition_key=process_definition_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    process_definition_key: str, *, client: AuthenticatedClient | Client, **kwargs: Any
) -> str:
    """Get process definition XML

     Returns process definition as XML.

    Args:
        process_definition_key (str): System-generated key for a deployed process definition.
            Example: 2251799813686749.

    Raises:
        errors.GetProcessDefinitionXmlBadRequest: If the response status code is 400. The provided data is not valid.
        errors.GetProcessDefinitionXmlUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
        errors.GetProcessDefinitionXmlForbidden: If the response status code is 403. Forbidden. The request is not allowed.
        errors.GetProcessDefinitionXmlNotFound: If the response status code is 404. The process definition with the given key was not found. More details are provided in the response body.
        errors.GetProcessDefinitionXmlInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        str"""
    response = await asyncio_detailed(
        process_definition_key=process_definition_key, client=client
    )
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetProcessDefinitionXmlBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse400, response.parsed),
            )
        if response.status_code == 401:
            raise errors.GetProcessDefinitionXmlUnauthorized(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse401, response.parsed),
            )
        if response.status_code == 403:
            raise errors.GetProcessDefinitionXmlForbidden(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse403, response.parsed),
            )
        if response.status_code == 404:
            raise errors.GetProcessDefinitionXmlNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse404, response.parsed),
            )
        if response.status_code == 500:
            raise errors.GetProcessDefinitionXmlInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(GetProcessDefinitionXMLResponse500, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    assert response.parsed is not None
    return cast(str, response.parsed)
