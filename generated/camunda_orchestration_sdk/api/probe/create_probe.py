from http import HTTPStatus
from typing import Any, cast
import httpx
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_probe_result import ErrorProbeResult
from ...models.ok_probe_result import OKProbeResult
from ...models.probe_creation_request import ProbeCreationRequest
from ...models.problem_detail import ProblemDetail
from ...models.unsupported_probe_result import UnsupportedProbeResult
from ...types import Response


def _get_kwargs(*, body: ProbeCreationRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    _kwargs: dict[str, Any] = {"method": "post", "url": "/probes"}
    _kwargs["json"] = body.to_dict()
    headers["Content-Type"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail | None:
    if response.status_code == 200:

        def _parse_response_200(
            data: object,
        ) -> ErrorProbeResult | OKProbeResult | UnsupportedProbeResult:
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_probe_result_type_0 = OKProbeResult.from_dict(data)
                return componentsschemas_probe_result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_probe_result_type_1 = (
                    UnsupportedProbeResult.from_dict(data)
                )
                return componentsschemas_probe_result_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            componentsschemas_probe_result_type_2 = ErrorProbeResult.from_dict(data)
            return componentsschemas_probe_result_type_2

        response_200 = _parse_response_200(response.json())
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
    if response.status_code == 413:
        response_413 = ProblemDetail.from_dict(response.json())
        return response_413
    if response.status_code == 500:
        response_500 = ProblemDetail.from_dict(response.json())
        return response_500
    if response.status_code == 503:
        response_503 = ProblemDetail.from_dict(response.json())
        return response_503
    if response.status_code == 504:
        response_504 = ProblemDetail.from_dict(response.json())
        return response_504
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, body: ProbeCreationRequest
) -> Response[
    ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail
]:
    """Create probe (alpha)

     Asks a worker a short question and waits for its answer in the same request.

    The probe is routed on `probeId`: a worker that polls for this probe ID with
    `POST /v2/probes/activation` collects it and answers with
    `POST /v2/probes/{probeKey}/answer`. The engine evaluates `input` when the probe is
    created and injects the values of the secrets it references before a worker collects it.

    The probe ends at its deadline, `requestTimeout` after the gateway received the request.
    Wait at least `requestTimeout` plus one second for the HTTP response, so that you get the
    reason the probe ended instead of a client-side timeout. With `requestTimeout` absent or
    `0`, the deadline uses the cluster's request timeout, capped at 30 seconds.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Args:
        body (ProbeCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, body: ProbeCreationRequest, **kwargs: Any
) -> ErrorProbeResult | OKProbeResult | UnsupportedProbeResult:
    """Create probe (alpha)

     Asks a worker a short question and waits for its answer in the same request.

    The probe is routed on `probeId`: a worker that polls for this probe ID with
    `POST /v2/probes/activation` collects it and answers with
    `POST /v2/probes/{probeKey}/answer`. The engine evaluates `input` when the probe is
    created and injects the values of the secrets it references before a worker collects it.

    The probe ends at its deadline, `requestTimeout` after the gateway received the request.
    Wait at least `requestTimeout` plus one second for the HTTP response, so that you get the
    reason the probe ended instead of a client-side timeout. With `requestTimeout` absent or
    `0`, the deadline uses the cluster's request timeout, capped at 30 seconds.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Args:
        body (ProbeCreationRequest):

    Raises:
        errors.BadRequestError: If the response status code is 400. The request is invalid, or the probe ended because of its secrets. The title of the problem tells the two apart: - `INVALID_ARGUMENT`: the body is invalid, for example a blank input, a probe ID that is not valid, a `requestTimeout` out of range, or an input that is not a valid expression or does not evaluate to a context. - `SECRET_RESOLUTION_ERROR`: a secret that the input references could not be resolved, or its value could not be injected into the input.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. No worker collected the probe before its deadline: no worker polls this probe ID, or the workers that poll it lack the `ANSWER` permission on it. The title is `NO_WORKER`.
        errors.PayloadTooLargeError: If the response status code is 413. The request is too large to be written to the log. The title is `PAYLOAD_TOO_LARGE`.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.GatewayTimeoutError: If the response status code is 504. The probe got no answer in time. The title of the problem tells why: - `WORKER_DID_NOT_ANSWER`: a worker collected the probe but did not answer before its deadline. - `SECRET_RESOLUTION_TIMEOUT`: the probe still waited for the values of its secrets at its deadline. - `DEADLINE_EXCEEDED`: the gateway timed out before the engine answered, for example after a leader change.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ErrorProbeResult | OKProbeResult | UnsupportedProbeResult"""
    response = sync_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 413:
            raise errors.PayloadTooLargeError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="create_probe"
        )
    assert response.parsed is not None
    return cast(
        ErrorProbeResult | OKProbeResult | UnsupportedProbeResult, response.parsed
    )


async def asyncio_detailed(
    *, client: AuthenticatedClient, body: ProbeCreationRequest
) -> Response[
    ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail
]:
    """Create probe (alpha)

     Asks a worker a short question and waits for its answer in the same request.

    The probe is routed on `probeId`: a worker that polls for this probe ID with
    `POST /v2/probes/activation` collects it and answers with
    `POST /v2/probes/{probeKey}/answer`. The engine evaluates `input` when the probe is
    created and injects the values of the secrets it references before a worker collects it.

    The probe ends at its deadline, `requestTimeout` after the gateway received the request.
    Wait at least `requestTimeout` plus one second for the HTTP response, so that you get the
    reason the probe ended instead of a client-side timeout. With `requestTimeout` absent or
    `0`, the deadline uses the cluster's request timeout, capped at 30 seconds.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Args:
        body (ProbeCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorProbeResult | OKProbeResult | UnsupportedProbeResult | ProblemDetail]
    """
    kwargs = _get_kwargs(body=body)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, body: ProbeCreationRequest, **kwargs: Any
) -> ErrorProbeResult | OKProbeResult | UnsupportedProbeResult:
    """Create probe (alpha)

     Asks a worker a short question and waits for its answer in the same request.

    The probe is routed on `probeId`: a worker that polls for this probe ID with
    `POST /v2/probes/activation` collects it and answers with
    `POST /v2/probes/{probeKey}/answer`. The engine evaluates `input` when the probe is
    created and injects the values of the secrets it references before a worker collects it.

    The probe ends at its deadline, `requestTimeout` after the gateway received the request.
    Wait at least `requestTimeout` plus one second for the HTTP response, so that you get the
    reason the probe ended instead of a client-side timeout. With `requestTimeout` absent or
    `0`, the deadline uses the cluster's request timeout, capped at 30 seconds.

    This endpoint is an alpha feature and may be subject to change
    in future releases.

    Args:
        body (ProbeCreationRequest):

    Raises:
        errors.BadRequestError: If the response status code is 400. The request is invalid, or the probe ended because of its secrets. The title of the problem tells the two apart: - `INVALID_ARGUMENT`: the body is invalid, for example a blank input, a probe ID that is not valid, a `requestTimeout` out of range, or an input that is not a valid expression or does not evaluate to a context. - `SECRET_RESOLUTION_ERROR`: a secret that the input references could not be resolved, or its value could not be injected into the input.
        errors.UnauthorizedError: If the response status code is 401. The request lacks valid authentication credentials.
        errors.ForbiddenError: If the response status code is 403. Forbidden. The request is not allowed.
        errors.NotFoundError: If the response status code is 404. No worker collected the probe before its deadline: no worker polls this probe ID, or the workers that poll it lack the `ANSWER` permission on it. The title is `NO_WORKER`.
        errors.PayloadTooLargeError: If the response status code is 413. The request is too large to be written to the log. The title is `PAYLOAD_TOO_LARGE`.
        errors.InternalServerErrorError: If the response status code is 500. An internal error occurred while processing the request.
        errors.ServiceUnavailableError: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
        errors.GatewayTimeoutError: If the response status code is 504. The probe got no answer in time. The title of the problem tells why: - `WORKER_DID_NOT_ANSWER`: a worker collected the probe but did not answer before its deadline. - `SECRET_RESOLUTION_TIMEOUT`: the probe still waited for the values of its secrets at its deadline. - `DEADLINE_EXCEEDED`: the gateway timed out before the engine answered, for example after a leader change.
        errors.UnexpectedStatus: If the response status code is not documented.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    Returns:
        ErrorProbeResult | OKProbeResult | UnsupportedProbeResult"""
    response = await asyncio_detailed(client=client, body=body)
    if response.status_code < 200 or response.status_code >= 300:
        if response.status_code == 400:
            raise errors.BadRequestError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 401:
            raise errors.UnauthorizedError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 403:
            raise errors.ForbiddenError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 404:
            raise errors.NotFoundError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 413:
            raise errors.PayloadTooLargeError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 500:
            raise errors.InternalServerErrorError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 503:
            raise errors.ServiceUnavailableError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        if response.status_code == 504:
            raise errors.GatewayTimeoutError(
                status_code=response.status_code,
                content=response.content,
                parsed=cast(ProblemDetail, response.parsed),
                operation_id="create_probe",
            )
        raise errors.UnexpectedStatus(
            response.status_code, response.content, operation_id="create_probe"
        )
    assert response.parsed is not None
    return cast(
        ErrorProbeResult | OKProbeResult | UnsupportedProbeResult, response.parsed
    )
