from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_decision_definition_xml_response_400 import GetDecisionDefinitionXMLResponse400
from ...models.get_decision_definition_xml_response_401 import GetDecisionDefinitionXMLResponse401
from ...models.get_decision_definition_xml_response_403 import GetDecisionDefinitionXMLResponse403
from ...models.get_decision_definition_xml_response_404 import GetDecisionDefinitionXMLResponse404
from ...models.get_decision_definition_xml_response_500 import GetDecisionDefinitionXMLResponse500
from ...types import Response

def _get_kwargs(decision_definition_key: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {'method': 'get', 'url': '/decision-definitions/{decision_definition_key}/xml'.format(decision_definition_key=quote(str(decision_definition_key), safe=''))}
    return _kwargs

def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetDecisionDefinitionXMLResponse400 | GetDecisionDefinitionXMLResponse401 | GetDecisionDefinitionXMLResponse403 | GetDecisionDefinitionXMLResponse404 | GetDecisionDefinitionXMLResponse500 | str | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200
    if response.status_code == 400:
        response_400 = GetDecisionDefinitionXMLResponse400.from_dict(response.json())
        return response_400
    if response.status_code == 401:
        response_401 = GetDecisionDefinitionXMLResponse401.from_dict(response.json())
        return response_401
    if response.status_code == 403:
        response_403 = GetDecisionDefinitionXMLResponse403.from_dict(response.json())
        return response_403
    if response.status_code == 404:
        response_404 = GetDecisionDefinitionXMLResponse404.from_dict(response.json())
        return response_404
    if response.status_code == 500:
        response_500 = GetDecisionDefinitionXMLResponse500.from_dict(response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None

def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetDecisionDefinitionXMLResponse400 | GetDecisionDefinitionXMLResponse401 | GetDecisionDefinitionXMLResponse403 | GetDecisionDefinitionXMLResponse404 | GetDecisionDefinitionXMLResponse500 | str]:
    return Response(status_code=HTTPStatus(response.status_code), content=response.content, headers=response.headers, parsed=_parse_response(client=client, response=response))

def sync_detailed(decision_definition_key: str, *, client: AuthenticatedClient | Client) -> Response[GetDecisionDefinitionXMLResponse400 | GetDecisionDefinitionXMLResponse401 | GetDecisionDefinitionXMLResponse403 | GetDecisionDefinitionXMLResponse404 | GetDecisionDefinitionXMLResponse500 | str]:
    """Get decision definition XML

     Returns decision definition as XML.

    Args:
        decision_definition_key (str): System-generated key for a decision definition. Example:
            2251799813326547.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDecisionDefinitionXMLResponse400 | GetDecisionDefinitionXMLResponse401 | GetDecisionDefinitionXMLResponse403 | GetDecisionDefinitionXMLResponse404 | GetDecisionDefinitionXMLResponse500 | str]
    """
    kwargs = _get_kwargs(decision_definition_key=decision_definition_key)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

def sync(decision_definition_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetDecisionDefinitionXMLResponse400:
    """Get decision definition XML

 Returns decision definition as XML.

Args:
    decision_definition_key (str): System-generated key for a decision definition. Example:
        2251799813326547.

Raises:
    errors.GetDecisionDefinitionXmlBadRequest: If the response status code is 400.
    errors.GetDecisionDefinitionXmlUnauthorized: If the response status code is 401.
    errors.GetDecisionDefinitionXmlForbidden: If the response status code is 403.
    errors.GetDecisionDefinitionXmlNotFound: If the response status code is 404.
    errors.GetDecisionDefinitionXmlInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetDecisionDefinitionXMLResponse400"""
    response = sync_detailed(decision_definition_key=decision_definition_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetDecisionDefinitionXmlBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetDecisionDefinitionXmlUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetDecisionDefinitionXmlForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetDecisionDefinitionXmlNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetDecisionDefinitionXmlInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed

async def asyncio_detailed(decision_definition_key: str, *, client: AuthenticatedClient | Client) -> Response[GetDecisionDefinitionXMLResponse400 | GetDecisionDefinitionXMLResponse401 | GetDecisionDefinitionXMLResponse403 | GetDecisionDefinitionXMLResponse404 | GetDecisionDefinitionXMLResponse500 | str]:
    """Get decision definition XML

     Returns decision definition as XML.

    Args:
        decision_definition_key (str): System-generated key for a decision definition. Example:
            2251799813326547.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDecisionDefinitionXMLResponse400 | GetDecisionDefinitionXMLResponse401 | GetDecisionDefinitionXMLResponse403 | GetDecisionDefinitionXMLResponse404 | GetDecisionDefinitionXMLResponse500 | str]
    """
    kwargs = _get_kwargs(decision_definition_key=decision_definition_key)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)

async def asyncio(decision_definition_key: str, *, client: AuthenticatedClient | Client, **kwargs) -> GetDecisionDefinitionXMLResponse400:
    """Get decision definition XML

 Returns decision definition as XML.

Args:
    decision_definition_key (str): System-generated key for a decision definition. Example:
        2251799813326547.

Raises:
    errors.GetDecisionDefinitionXmlBadRequest: If the response status code is 400.
    errors.GetDecisionDefinitionXmlUnauthorized: If the response status code is 401.
    errors.GetDecisionDefinitionXmlForbidden: If the response status code is 403.
    errors.GetDecisionDefinitionXmlNotFound: If the response status code is 404.
    errors.GetDecisionDefinitionXmlInternalServerError: If the response status code is 500.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetDecisionDefinitionXMLResponse400"""
    response = await asyncio_detailed(decision_definition_key=decision_definition_key, client=client)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.GetDecisionDefinitionXmlBadRequest(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse400, response.parsed))
        if response.status_code == 401:
            raise errors.GetDecisionDefinitionXmlUnauthorized(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse401, response.parsed))
        if response.status_code == 403:
            raise errors.GetDecisionDefinitionXmlForbidden(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse403, response.parsed))
        if response.status_code == 404:
            raise errors.GetDecisionDefinitionXmlNotFound(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse404, response.parsed))
        if response.status_code == 500:
            raise errors.GetDecisionDefinitionXmlInternalServerError(status_code=response.status_code, content=response.content, parsed=cast(GetDecisionDefinitionXMLResponse500, response.parsed))
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed