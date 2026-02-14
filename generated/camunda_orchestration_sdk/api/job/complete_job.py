from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.complete_job_data import CompleteJobData
from ...models.problem_detail import ProblemDetail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    job_key: str, *, body: CompleteJobData | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/jobs/{job_key}/completion".format(
            job_key=quote(str(job_key), safe="")
        ),
    }
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProblemDetail | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = ProblemDetail.from_dict(response.json())
        return response_400
    if response.status_code == 404:
        response_404 = ProblemDetail.from_dict(response.json())
        return response_404
    if response.status_code == 409:
        response_409 = ProblemDetail.from_dict(response.json())
        return response_409
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = ProblemDetail.from_dict(response.json())
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProblemDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: CompleteJobData | Unset = UNSET,
) -> Response[Any | ProblemDetail]:
    """Complete job

     Complete a job with the given payload, which allows completing the associated service task.

    Args:
        job_key (str): System-generated key for a job. Example: 2251799813653498.
        body (CompleteJobData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(job_key=job_key, body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    job_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: CompleteJobData | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Complete job

     Complete a job with the given payload, which allows completing the associated service task.

    Args:
        job_key (str): System-generated key for a job. Example: 2251799813653498.
        body (CompleteJobData | Unset):

    Raises:
        errors.CompleteJobBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CompleteJobNotFound: If the response status code is 404. The job with the given key was not found.
        errors.CompleteJobConflict: If the response status code is 409. The job with the given key is in the wrong state currently. More details are provided in the response body.
        errors.CompleteJobInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CompleteJobServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = sync_detailed(job_key=job_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CompleteJobBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.CompleteJobNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 409:
            raise errors.CompleteJobConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CompleteJobInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CompleteJobServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


async def asyncio_detailed(
    job_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: CompleteJobData | Unset = UNSET,
) -> Response[Any | ProblemDetail]:
    """Complete job

     Complete a job with the given payload, which allows completing the associated service task.

    Args:
        job_key (str): System-generated key for a job. Example: 2251799813653498.
        body (CompleteJobData | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProblemDetail]
    """
    kwargs = _get_kwargs(job_key=job_key, body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    job_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: CompleteJobData | Unset = UNSET,
    **kwargs: Any,
) -> None:
    """Complete job

     Complete a job with the given payload, which allows completing the associated service task.

    Args:
        job_key (str): System-generated key for a job. Example: 2251799813653498.
        body (CompleteJobData | Unset):

    Raises:
        errors.CompleteJobBadRequest: If the response status code is 400. The provided data is not valid.
        errors.CompleteJobNotFound: If the response status code is 404. The job with the given key was not found.
        errors.CompleteJobConflict: If the response status code is 409. The job with the given key is in the wrong state currently. More details are provided in the response body.
        errors.CompleteJobInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
        errors.CompleteJobServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        None"""
    response = await asyncio_detailed(job_key=job_key, client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.CompleteJobBadRequest(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 404:
            raise errors.CompleteJobNotFound(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 409:
            raise errors.CompleteJobConflict(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 500:
            raise errors.CompleteJobInternalServerError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        if response.status_code == 503:
            raise errors.CompleteJobServiceUnavailable(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
            )
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None
