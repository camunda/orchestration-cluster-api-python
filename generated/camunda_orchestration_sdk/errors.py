"""Per-status error classes raised by SDK API methods."""

from __future__ import annotations

from typing import Any


class ApiError(Exception):
    """Base class for API errors raised by SDK methods.

    Attributes:
        status_code: The HTTP status code returned by the server.
        content: The raw response body as bytes.
        parsed: The parsed error model (typically ProblemDetail), or None.
        operation_id: The SDK operation that raised this error (e.g. 'create_process_instance').
    """

    def __init__(
        self,
        *,
        status_code: int,
        content: bytes,
        parsed: Any | None = None,
        operation_id: str | None = None,
    ):
        self.status_code = status_code
        self.content = content
        self.parsed = parsed
        self.operation_id = operation_id

        super().__init__(self._build_message())

    def _build_message(self) -> str:
        parsed_name = type(self.parsed).__name__ if self.parsed is not None else "None"
        op = f" [{self.operation_id}]" if self.operation_id else ""
        try:
            content_text = self.content.decode(errors="ignore")
        except Exception:
            content_text = "<binary>"
        return f"HTTP {self.status_code}{op} ({parsed_name})\n\nResponse content:\n{content_text}"


class UnexpectedStatus(ApiError):
    """Raised when the server returns a status code that is not handled/parsed by the SDK."""

    def __init__(
        self, status_code: int, content: bytes, *, operation_id: str | None = None
    ):
        super().__init__(
            status_code=status_code,
            content=content,
            parsed=None,
            operation_id=operation_id,
        )


class BadRequestError(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""


class UnauthorizedError(ApiError):
    """Raised when the server returns HTTP 401. Authentication credentials are missing or invalid."""


class PaymentRequiredError(ApiError):
    """Raised when the server returns HTTP 402. Payment is required."""


class ForbiddenError(ApiError):
    """Raised when the server returns HTTP 403. The request is not allowed."""


class NotFoundError(ApiError):
    """Raised when the server returns HTTP 404. The requested resource was not found."""


class MethodNotAllowedError(ApiError):
    """Raised when the server returns HTTP 405. The HTTP method is not allowed for this resource."""


class RequestTimeoutError(ApiError):
    """Raised when the server returns HTTP 408. The request timed out."""


class ConflictError(ApiError):
    """Raised when the server returns HTTP 409. The request conflicts with the current state of the resource."""


class GoneError(ApiError):
    """Raised when the server returns HTTP 410. The requested resource is no longer available."""


class PreconditionFailedError(ApiError):
    """Raised when the server returns HTTP 412. A precondition for the request was not met."""


class PayloadTooLargeError(ApiError):
    """Raised when the server returns HTTP 413. The payload is too large."""


class UnsupportedMediaTypeError(ApiError):
    """Raised when the server returns HTTP 415. The media type is not supported."""


class UnprocessableEntityError(ApiError):
    """Raised when the server returns HTTP 422. The request is syntactically correct but semantically invalid."""


class TooManyRequestsError(ApiError):
    """Raised when the server returns HTTP 429. Too many requests. Rate limit exceeded."""


class InternalServerErrorError(ApiError):
    """Raised when the server returns HTTP 500. An unexpected error occurred on the server."""


class NotImplementedError_(ApiError):
    """Raised when the server returns HTTP 501. The server does not support this operation."""


class BadGatewayError(ApiError):
    """Raised when the server returns HTTP 502. The upstream server returned an invalid response."""


class ServiceUnavailableError(ApiError):
    """Raised when the server returns HTTP 503. The server is temporarily unavailable (backpressure or maintenance)."""


class GatewayTimeoutError(ApiError):
    """Raised when the server returns HTTP 504. The upstream server did not respond in time."""


__all__ = [
    "ApiError",
    "BadGatewayError",
    "BadRequestError",
    "ConflictError",
    "ForbiddenError",
    "GatewayTimeoutError",
    "GoneError",
    "InternalServerErrorError",
    "MethodNotAllowedError",
    "NotFoundError",
    "NotImplementedError_",
    "PayloadTooLargeError",
    "PaymentRequiredError",
    "PreconditionFailedError",
    "RequestTimeoutError",
    "ServiceUnavailableError",
    "TooManyRequestsError",
    "UnauthorizedError",
    "UnexpectedStatus",
    "UnprocessableEntityError",
    "UnsupportedMediaTypeError",
]
