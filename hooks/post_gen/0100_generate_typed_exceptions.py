from pathlib import Path


# Mapping from HTTP status code to (class name, human-readable reason).
_STATUS_CLASSES: dict[int, tuple[str, str]] = {
    400: ("BadRequestError", "The provided data is not valid."),
    401: ("UnauthorizedError", "Authentication credentials are missing or invalid."),
    402: ("PaymentRequiredError", "Payment is required."),
    403: ("ForbiddenError", "The request is not allowed."),
    404: ("NotFoundError", "The requested resource was not found."),
    405: ("MethodNotAllowedError", "The HTTP method is not allowed for this resource."),
    408: ("RequestTimeoutError", "The request timed out."),
    409: (
        "ConflictError",
        "The request conflicts with the current state of the resource.",
    ),
    410: ("GoneError", "The requested resource is no longer available."),
    412: ("PreconditionFailedError", "A precondition for the request was not met."),
    413: ("PayloadTooLargeError", "The payload is too large."),
    415: ("UnsupportedMediaTypeError", "The media type is not supported."),
    422: (
        "UnprocessableEntityError",
        "The request is syntactically correct but semantically invalid.",
    ),
    429: ("TooManyRequestsError", "Too many requests. Rate limit exceeded."),
    500: ("InternalServerErrorError", "An unexpected error occurred on the server."),
    501: ("NotImplementedError_", "The server does not support this operation."),
    502: ("BadGatewayError", "The upstream server returned an invalid response."),
    503: (
        "ServiceUnavailableError",
        "The server is temporarily unavailable (backpressure or maintenance).",
    ),
    504: ("GatewayTimeoutError", "The upstream server did not respond in time."),
}


def status_class_name(code: int) -> str:
    """Return the per-status exception class name for a given HTTP status code."""
    entry = _STATUS_CLASSES.get(code)
    if entry:
        return entry[0]
    return f"Http{code}Error"


def _generate_errors_py() -> str:
    lines: list[str] = []
    lines.append('"""Per-status error classes raised by SDK API methods."""')
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Any")
    lines.append("")
    lines.append("")

    # Base class
    lines.append("class ApiError(Exception):")
    lines.append('    """Base class for API errors raised by SDK methods.')
    lines.append("")
    lines.append("    Attributes:")
    lines.append("        status_code: The HTTP status code returned by the server.")
    lines.append("        content: The raw response body as bytes.")
    lines.append(
        "        parsed: The parsed error model (typically ProblemDetail), or None."
    )
    lines.append(
        "        operation_id: The SDK operation that raised this error (e.g. 'create_process_instance')."
    )
    lines.append('    """')
    lines.append("")
    lines.append("    def __init__(")
    lines.append("        self,")
    lines.append("        *,")
    lines.append("        status_code: int,")
    lines.append("        content: bytes,")
    lines.append("        parsed: Any | None = None,")
    lines.append("        operation_id: str | None = None,")
    lines.append("    ):")
    lines.append("        self.status_code = status_code")
    lines.append("        self.content = content")
    lines.append("        self.parsed = parsed")
    lines.append("        self.operation_id = operation_id")
    lines.append("")
    lines.append("        super().__init__(self._build_message())")
    lines.append("")
    lines.append("    def _build_message(self) -> str:")
    lines.append(
        "        parsed_name = type(self.parsed).__name__ if self.parsed is not None else 'None'"
    )
    lines.append("        op = f' [{self.operation_id}]' if self.operation_id else ''")
    lines.append("        try:")
    lines.append("            content_text = self.content.decode(errors='ignore')")
    lines.append("        except Exception:")
    lines.append("            content_text = '<binary>'")
    lines.append(
        "        return f'HTTP {self.status_code}{op} ({parsed_name})\\n\\nResponse content:\\n{content_text}'"
    )
    lines.append("")
    lines.append("")

    # UnexpectedStatus
    lines.append("class UnexpectedStatus(ApiError):")
    lines.append(
        '    """Raised when the server returns a status code that is not handled/parsed by the SDK."""'
    )
    lines.append("")
    lines.append(
        "    def __init__(self, status_code: int, content: bytes, *, operation_id: str | None = None):"
    )
    lines.append(
        "        super().__init__(status_code=status_code, content=content, parsed=None, operation_id=operation_id)"
    )
    lines.append("")
    lines.append("")

    exported: list[str] = ["ApiError", "UnexpectedStatus"]

    # Per-status classes
    for code in sorted(_STATUS_CLASSES.keys()):
        class_name, description = _STATUS_CLASSES[code]
        exported.append(class_name)

        lines.append(f"class {class_name}(ApiError):")
        lines.append(
            f'    """Raised when the server returns HTTP {code}. {description}"""'
        )
        lines.append("")
        lines.append("")

    lines.append(f"__all__ = {sorted(set(exported))!r}")
    lines.append("")

    return "\n".join(lines)


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"

    errors_py = package_dir / "errors.py"
    errors_py.write_text(_generate_errors_py())
    print(f"Generated {errors_py} with {len(_STATUS_CLASSES)} per-status error classes")
