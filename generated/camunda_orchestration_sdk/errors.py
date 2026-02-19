"""Contains shared errors types that can be raised from API functions"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .models import (
        ProblemDetail,
    )


class ApiError(Exception):
    """Base class for API errors raised by convenience wrappers."""

    def __init__(self, *, status_code: int, content: bytes, parsed: Any | None = None):
        self.status_code = status_code
        self.content = content
        self.parsed = parsed

        super().__init__(self._build_message())

    def _build_message(self) -> str:
        parsed_name = type(self.parsed).__name__ if self.parsed is not None else "None"
        try:
            content_text = self.content.decode(errors="ignore")
        except Exception:
            content_text = "<binary>"
        return f"HTTP {self.status_code} ({parsed_name})\n\nResponse content:\n{content_text}"


class UnexpectedStatus(ApiError):
    """Raised when the server returns a status code that is not handled/parsed by the SDK."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(status_code=status_code, content=content, parsed=None)


class ActivateAdHocSubProcessActivitiesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesNotFound(ApiError):
    """Raised when the server returns HTTP 404. The ad-hoc sub-process instance is not found or the provided key does not identify an ad-hoc sub-process."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateJobsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateJobsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateJobsServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateJobsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupConflict(ApiError):
    """Raised when the server returns HTTP 409. The client with the given ID is already assigned to the group."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. The tenant was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or group was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupConflict(ApiError):
    """Raised when the server returns HTTP 409. The mapping rule with the given ID is already assigned to the group."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group or mapping rule with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or mapping rule was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientConflict(ApiError):
    """Raised when the server returns HTTP 409. The role was already assigned to the client with the given ID."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupConflict(ApiError):
    """Raised when the server returns HTTP 409. The role is already assigned to the group with the given ID."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleConflict(ApiError):
    """Raised when the server returns HTTP 409. The role is already assigned to the mapping rule with the given ID."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or mapping rule with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or role was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserConflict(ApiError):
    """Raised when the server returns HTTP 409. The role is already assigned to the user with the given ID."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or user with the given ID or username was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskConflict(ApiError):
    """Raised when the server returns HTTP 409. The user task with the given key is in the wrong state currently. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupConflict(ApiError):
    """Raised when the server returns HTTP 409. The user with the given ID is already assigned to the group."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group or user with the given ID or username was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or user was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class BroadcastSignalBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class BroadcastSignalInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class BroadcastSignalNotFound(ApiError):
    """Raised when the server returns HTTP 404. The signal is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class BroadcastSignalServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelBatchOperationNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The batch operation was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstancesBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstancesBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstancesBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstancesBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobConflict(ApiError):
    """Raised when the server returns HTTP 409. The job with the given key is in the wrong state currently. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobNotFound(ApiError):
    """Raised when the server returns HTTP 404. The job with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskConflict(ApiError):
    """Raised when the server returns HTTP 409. The user task with the given key is in the wrong state currently. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAdminUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAdminUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAdminUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAdminUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The owner was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDeploymentBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDeploymentServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentLinkBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentUnsupportedMediaType(ApiError):
    """Raised when the server returns HTTP 415. The server cannot process the request because the media type (Content-Type) of the request payload is not supported by the server for the requested resource and method."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentsUnsupportedMediaType(ApiError):
    """Raised when the server returns HTTP 415. The server cannot process the request because the media type (Content-Type) of the request payload is not supported by the server for the requested resource and method."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateElementInstanceVariablesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateElementInstanceVariablesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateElementInstanceVariablesServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalTaskListenerBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalTaskListenerConflict(ApiError):
    """Raised when the server returns HTTP 409. A global listener with this id already exists."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalTaskListenerForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalTaskListenerInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalTaskListenerServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalTaskListenerUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. The request to create a mapping rule was denied. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The request to create a mapping rule was denied."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateProcessInstanceGatewayTimeout(ApiError):
    """Raised when the server returns HTTP 504. The process instance creation request timed out in the gateway. This can happen if the `awaitCompletion` request parameter is set to `true` and the created process instance did not complete within the defined request timeout. This often happens when the created instance is not fully automated or contains wait states."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantConflict(ApiError):
    """Raised when the server returns HTTP 409. Tenant with this id already exists."""

    parsed: Any

    def __init__(self, *, status_code: int, content: bytes, parsed: Any):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The resource was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserConflict(ApiError):
    """Raised when the server returns HTTP 409. A user with this username already exists."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteAuthorizationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteAuthorizationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The authorization with the authorizationKey was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteAuthorizationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteAuthorizationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDecisionInstanceForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDecisionInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDecisionInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision instance is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDecisionInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDecisionInstanceUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDecisionInstancesBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The decision instance batch operation failed. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDecisionInstancesBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDecisionInstancesBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDecisionInstancesBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDocumentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDocumentNotFound(ApiError):
    """Raised when the server returns HTTP 404. The document with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalTaskListenerBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalTaskListenerForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalTaskListenerInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalTaskListenerNotFound(ApiError):
    """Raised when the server returns HTTP 404. The global user task listener was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalTaskListenerServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalTaskListenerUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The mapping rule with the mappingRuleId was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteMappingRuleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteMappingRuleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceConflict(ApiError):
    """Raised when the server returns HTTP 409. The process instance is not in a completed or terminated state and cannot be deleted."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstancesBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstancesBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstancesBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstancesBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteResourceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteResourceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteResourceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The resource is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteResourceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteRoleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsForbidden(ApiError):
    """Raised when the server returns HTTP 403. The client is not authorized to start process instances for the specified process definition. If a processDefinitionKey is not provided, this indicates that the client is not authorized to start process instances for at least one of the matched process definitions."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process definition was not found for the given processDefinitionKey."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateDecisionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateDecisionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateDecisionNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateDecisionServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateExpressionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateExpressionForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateExpressionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateExpressionUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobConflict(ApiError):
    """Raised when the server returns HTTP 409. The job with the given key is in the wrong state (i.e: not ACTIVATED or ACTIVATABLE). The job was failed by another worker with retries = 0, and the process is now in an incident state."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobNotFound(ApiError):
    """Raised when the server returns HTTP 404. The job with the given jobKey is not found. It was completed by another worker, or the process instance itself was canceled."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuditLogForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuditLogInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuditLogNotFound(ApiError):
    """Raised when the server returns HTTP 404. The audit log with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuditLogUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthenticationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthenticationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthenticationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthorizationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthorizationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthorizationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The authorization with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthorizationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetBatchOperationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The batch operation is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision definition with the given key was not found. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision definition with the given key was not found. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision instance with the given key was not found. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision requirements with the given key was not found. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision requirements with the given key was not found. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDocumentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDocumentNotFound(ApiError):
    """Raised when the server returns HTTP 404. The document with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The element instance with the given key was not found. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalJobStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalJobStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalJobStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalJobStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentNotFound(ApiError):
    """Raised when the server returns HTTP 404. The incident with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetJobTypeStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetJobTypeStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetJobTypeStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetJobTypeStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetLicenseInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The mapping rule with the mappingRuleId was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetMappingRuleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceVersionStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceVersionStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceVersionStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceVersionStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionMessageSubscriptionStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionMessageSubscriptionStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionMessageSubscriptionStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionMessageSubscriptionStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process definition with the given key was not found. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process definition with the given key was not found. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceSequenceFlowsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceSequenceFlowsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceSequenceFlowsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceSequenceFlowsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByDefinitionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByDefinitionForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByDefinitionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByDefinitionUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByErrorBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByErrorForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByErrorInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByErrorUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetResourceContentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetResourceContentNotFound(ApiError):
    """Raised when the server returns HTTP 404. A resource with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetResourceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetResourceNotFound(ApiError):
    """Raised when the server returns HTTP 404. A resource with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStatusServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The cluster is DOWN and does not have any partition with a healthy leader."""

    parsed: None

    def __init__(self, *, status_code: int, content: bytes, parsed: None):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Tenant not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTopologyInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTopologyUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUsageMetricsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUsageMetricsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUsageMetricsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUsageMetricsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user with the given username was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceConflict(ApiError):
    """Raised when the server returns HTTP 409. The process instance migration failed. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstancesBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstancesBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstancesBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstancesBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstancesBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstancesBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstancesBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstancesBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PinClockBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PinClockInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PinClockServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PublishMessageBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PublishMessageInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PublishMessageServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResetClockInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResetClockServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentNotFound(ApiError):
    """Raised when the server returns HTTP 404. The incident with the incidentKey is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentsBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentsBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentsBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentsBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The batch operation was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuditLogsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuditLogsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuditLogsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: Any

    def __init__(self, *, status_code: int, content: bytes, parsed: Any):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuditLogsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuthorizationsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuthorizationsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuthorizationsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuthorizationsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchBatchOperationItemsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchBatchOperationItemsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchBatchOperationsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchBatchOperationsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClusterVariablesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClusterVariablesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClusterVariablesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClusterVariablesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchCorrelatedMessageSubscriptionsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchCorrelatedMessageSubscriptionsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchCorrelatedMessageSubscriptionsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchCorrelatedMessageSubscriptionsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionDefinitionsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionDefinitionsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionDefinitionsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionDefinitionsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionInstancesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionInstancesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionInstancesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionInstancesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionRequirementsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionRequirementsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionRequirementsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionRequirementsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The element instance with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstancesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstancesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstancesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstancesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: Any

    def __init__(self, *, status_code: int, content: bytes, parsed: Any):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchIncidentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchIncidentsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchIncidentsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchIncidentsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchJobsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchJobsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchJobsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchJobsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRuleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMessageSubscriptionsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMessageSubscriptionsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMessageSubscriptionsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMessageSubscriptionsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessDefinitionsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessDefinitionsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessDefinitionsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessDefinitionsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstancesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstancesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstancesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstancesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTaskAuditLogsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTaskAuditLogsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTaskVariablesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTaskVariablesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTasksBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTasksForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTasksInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTasksUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchVariablesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchVariablesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchVariablesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchVariablesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The batch operation was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorConflict(ApiError):
    """Raised when the server returns HTTP 409. The job with the given key is in the wrong state currently. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorNotFound(ApiError):
    """Raised when the server returns HTTP 404. The job with the given key was not found or is not activated."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found, or the client is not assigned to this group."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. The tenant does not exist or the client was not assigned to it."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or group was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group or mapping rule with the given ID was not found, or the mapping rule is not assigned to this group."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or mapping rule was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or client with the given ID or username was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or mapping rule with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or role was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or user with the given ID or username was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group or user with the given ID was not found, or the user is not assigned to this group."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or user was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskConflict(ApiError):
    """Raised when the server returns HTTP 409. The user task with the given key is in the wrong state currently. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateAuthorizationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateAuthorizationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The authorization with the authorizationKey was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateAuthorizationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateAuthorizationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalTaskListenerBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalTaskListenerForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalTaskListenerInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalTaskListenerNotFound(ApiError):
    """Raised when the server returns HTTP 404. The global user task listener was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalTaskListenerServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGlobalTaskListenerUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobConflict(ApiError):
    """Raised when the server returns HTTP 409. The job with the given key is in the wrong state currently. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobNotFound(ApiError):
    """Raised when the server returns HTTP 404. The job with the jobKey is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. The request to update a mapping rule was denied. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The request to update a mapping rule was denied."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the ID is not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskConflict(ApiError):
    """Raised when the server returns HTTP 409. The user task with the given key is in the wrong state currently. More details are provided in the response body."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""

    parsed: ProblemDetail

    def __init__(self, *, status_code: int, content: bytes, parsed: ProblemDetail):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


__all__ = [
    "ActivateAdHocSubProcessActivitiesBadRequest",
    "ActivateAdHocSubProcessActivitiesForbidden",
    "ActivateAdHocSubProcessActivitiesInternalServerError",
    "ActivateAdHocSubProcessActivitiesNotFound",
    "ActivateAdHocSubProcessActivitiesServiceUnavailable",
    "ActivateAdHocSubProcessActivitiesUnauthorized",
    "ActivateJobsBadRequest",
    "ActivateJobsInternalServerError",
    "ActivateJobsServiceUnavailable",
    "ActivateJobsUnauthorized",
    "ApiError",
    "AssignClientToGroupBadRequest",
    "AssignClientToGroupConflict",
    "AssignClientToGroupForbidden",
    "AssignClientToGroupInternalServerError",
    "AssignClientToGroupNotFound",
    "AssignClientToGroupServiceUnavailable",
    "AssignClientToTenantBadRequest",
    "AssignClientToTenantForbidden",
    "AssignClientToTenantInternalServerError",
    "AssignClientToTenantNotFound",
    "AssignClientToTenantServiceUnavailable",
    "AssignGroupToTenantBadRequest",
    "AssignGroupToTenantForbidden",
    "AssignGroupToTenantInternalServerError",
    "AssignGroupToTenantNotFound",
    "AssignGroupToTenantServiceUnavailable",
    "AssignMappingRuleToGroupBadRequest",
    "AssignMappingRuleToGroupConflict",
    "AssignMappingRuleToGroupForbidden",
    "AssignMappingRuleToGroupInternalServerError",
    "AssignMappingRuleToGroupNotFound",
    "AssignMappingRuleToGroupServiceUnavailable",
    "AssignMappingRuleToTenantBadRequest",
    "AssignMappingRuleToTenantForbidden",
    "AssignMappingRuleToTenantInternalServerError",
    "AssignMappingRuleToTenantNotFound",
    "AssignMappingRuleToTenantServiceUnavailable",
    "AssignRoleToClientBadRequest",
    "AssignRoleToClientConflict",
    "AssignRoleToClientForbidden",
    "AssignRoleToClientInternalServerError",
    "AssignRoleToClientNotFound",
    "AssignRoleToClientServiceUnavailable",
    "AssignRoleToGroupBadRequest",
    "AssignRoleToGroupConflict",
    "AssignRoleToGroupForbidden",
    "AssignRoleToGroupInternalServerError",
    "AssignRoleToGroupNotFound",
    "AssignRoleToGroupServiceUnavailable",
    "AssignRoleToMappingRuleBadRequest",
    "AssignRoleToMappingRuleConflict",
    "AssignRoleToMappingRuleForbidden",
    "AssignRoleToMappingRuleInternalServerError",
    "AssignRoleToMappingRuleNotFound",
    "AssignRoleToMappingRuleServiceUnavailable",
    "AssignRoleToTenantBadRequest",
    "AssignRoleToTenantForbidden",
    "AssignRoleToTenantInternalServerError",
    "AssignRoleToTenantNotFound",
    "AssignRoleToTenantServiceUnavailable",
    "AssignRoleToUserBadRequest",
    "AssignRoleToUserConflict",
    "AssignRoleToUserForbidden",
    "AssignRoleToUserInternalServerError",
    "AssignRoleToUserNotFound",
    "AssignRoleToUserServiceUnavailable",
    "AssignUserTaskBadRequest",
    "AssignUserTaskConflict",
    "AssignUserTaskInternalServerError",
    "AssignUserTaskNotFound",
    "AssignUserTaskServiceUnavailable",
    "AssignUserToGroupBadRequest",
    "AssignUserToGroupConflict",
    "AssignUserToGroupForbidden",
    "AssignUserToGroupInternalServerError",
    "AssignUserToGroupNotFound",
    "AssignUserToGroupServiceUnavailable",
    "AssignUserToTenantBadRequest",
    "AssignUserToTenantForbidden",
    "AssignUserToTenantInternalServerError",
    "AssignUserToTenantNotFound",
    "AssignUserToTenantServiceUnavailable",
    "BroadcastSignalBadRequest",
    "BroadcastSignalInternalServerError",
    "BroadcastSignalNotFound",
    "BroadcastSignalServiceUnavailable",
    "CancelBatchOperationBadRequest",
    "CancelBatchOperationForbidden",
    "CancelBatchOperationInternalServerError",
    "CancelBatchOperationNotFound",
    "CancelProcessInstanceBadRequest",
    "CancelProcessInstanceInternalServerError",
    "CancelProcessInstanceNotFound",
    "CancelProcessInstanceServiceUnavailable",
    "CancelProcessInstancesBatchOperationBadRequest",
    "CancelProcessInstancesBatchOperationForbidden",
    "CancelProcessInstancesBatchOperationInternalServerError",
    "CancelProcessInstancesBatchOperationUnauthorized",
    "CompleteJobBadRequest",
    "CompleteJobConflict",
    "CompleteJobInternalServerError",
    "CompleteJobNotFound",
    "CompleteJobServiceUnavailable",
    "CompleteUserTaskBadRequest",
    "CompleteUserTaskConflict",
    "CompleteUserTaskInternalServerError",
    "CompleteUserTaskNotFound",
    "CompleteUserTaskServiceUnavailable",
    "CorrelateMessageBadRequest",
    "CorrelateMessageForbidden",
    "CorrelateMessageInternalServerError",
    "CorrelateMessageNotFound",
    "CorrelateMessageServiceUnavailable",
    "CreateAdminUserBadRequest",
    "CreateAdminUserForbidden",
    "CreateAdminUserInternalServerError",
    "CreateAdminUserServiceUnavailable",
    "CreateAuthorizationBadRequest",
    "CreateAuthorizationForbidden",
    "CreateAuthorizationInternalServerError",
    "CreateAuthorizationNotFound",
    "CreateAuthorizationServiceUnavailable",
    "CreateAuthorizationUnauthorized",
    "CreateDeploymentBadRequest",
    "CreateDeploymentServiceUnavailable",
    "CreateDocumentBadRequest",
    "CreateDocumentLinkBadRequest",
    "CreateDocumentUnsupportedMediaType",
    "CreateDocumentsBadRequest",
    "CreateDocumentsUnsupportedMediaType",
    "CreateElementInstanceVariablesBadRequest",
    "CreateElementInstanceVariablesInternalServerError",
    "CreateElementInstanceVariablesServiceUnavailable",
    "CreateGlobalClusterVariableBadRequest",
    "CreateGlobalClusterVariableForbidden",
    "CreateGlobalClusterVariableInternalServerError",
    "CreateGlobalClusterVariableUnauthorized",
    "CreateGlobalTaskListenerBadRequest",
    "CreateGlobalTaskListenerConflict",
    "CreateGlobalTaskListenerForbidden",
    "CreateGlobalTaskListenerInternalServerError",
    "CreateGlobalTaskListenerServiceUnavailable",
    "CreateGlobalTaskListenerUnauthorized",
    "CreateGroupBadRequest",
    "CreateGroupForbidden",
    "CreateGroupInternalServerError",
    "CreateGroupServiceUnavailable",
    "CreateGroupUnauthorized",
    "CreateMappingRuleBadRequest",
    "CreateMappingRuleForbidden",
    "CreateMappingRuleInternalServerError",
    "CreateMappingRuleNotFound",
    "CreateProcessInstanceBadRequest",
    "CreateProcessInstanceGatewayTimeout",
    "CreateProcessInstanceInternalServerError",
    "CreateProcessInstanceServiceUnavailable",
    "CreateRoleBadRequest",
    "CreateRoleForbidden",
    "CreateRoleInternalServerError",
    "CreateRoleServiceUnavailable",
    "CreateRoleUnauthorized",
    "CreateTenantBadRequest",
    "CreateTenantClusterVariableBadRequest",
    "CreateTenantClusterVariableForbidden",
    "CreateTenantClusterVariableInternalServerError",
    "CreateTenantClusterVariableUnauthorized",
    "CreateTenantConflict",
    "CreateTenantForbidden",
    "CreateTenantInternalServerError",
    "CreateTenantNotFound",
    "CreateTenantServiceUnavailable",
    "CreateUserBadRequest",
    "CreateUserConflict",
    "CreateUserForbidden",
    "CreateUserInternalServerError",
    "CreateUserServiceUnavailable",
    "CreateUserUnauthorized",
    "DeleteAuthorizationInternalServerError",
    "DeleteAuthorizationNotFound",
    "DeleteAuthorizationServiceUnavailable",
    "DeleteAuthorizationUnauthorized",
    "DeleteDecisionInstanceForbidden",
    "DeleteDecisionInstanceInternalServerError",
    "DeleteDecisionInstanceNotFound",
    "DeleteDecisionInstanceServiceUnavailable",
    "DeleteDecisionInstanceUnauthorized",
    "DeleteDecisionInstancesBatchOperationBadRequest",
    "DeleteDecisionInstancesBatchOperationForbidden",
    "DeleteDecisionInstancesBatchOperationInternalServerError",
    "DeleteDecisionInstancesBatchOperationUnauthorized",
    "DeleteDocumentInternalServerError",
    "DeleteDocumentNotFound",
    "DeleteGlobalClusterVariableBadRequest",
    "DeleteGlobalClusterVariableForbidden",
    "DeleteGlobalClusterVariableInternalServerError",
    "DeleteGlobalClusterVariableNotFound",
    "DeleteGlobalClusterVariableUnauthorized",
    "DeleteGlobalTaskListenerBadRequest",
    "DeleteGlobalTaskListenerForbidden",
    "DeleteGlobalTaskListenerInternalServerError",
    "DeleteGlobalTaskListenerNotFound",
    "DeleteGlobalTaskListenerServiceUnavailable",
    "DeleteGlobalTaskListenerUnauthorized",
    "DeleteGroupInternalServerError",
    "DeleteGroupNotFound",
    "DeleteGroupServiceUnavailable",
    "DeleteGroupUnauthorized",
    "DeleteMappingRuleInternalServerError",
    "DeleteMappingRuleNotFound",
    "DeleteMappingRuleServiceUnavailable",
    "DeleteMappingRuleUnauthorized",
    "DeleteProcessInstanceConflict",
    "DeleteProcessInstanceForbidden",
    "DeleteProcessInstanceInternalServerError",
    "DeleteProcessInstanceNotFound",
    "DeleteProcessInstanceServiceUnavailable",
    "DeleteProcessInstanceUnauthorized",
    "DeleteProcessInstancesBatchOperationBadRequest",
    "DeleteProcessInstancesBatchOperationForbidden",
    "DeleteProcessInstancesBatchOperationInternalServerError",
    "DeleteProcessInstancesBatchOperationUnauthorized",
    "DeleteResourceBadRequest",
    "DeleteResourceInternalServerError",
    "DeleteResourceNotFound",
    "DeleteResourceServiceUnavailable",
    "DeleteRoleInternalServerError",
    "DeleteRoleNotFound",
    "DeleteRoleServiceUnavailable",
    "DeleteRoleUnauthorized",
    "DeleteTenantBadRequest",
    "DeleteTenantClusterVariableBadRequest",
    "DeleteTenantClusterVariableForbidden",
    "DeleteTenantClusterVariableInternalServerError",
    "DeleteTenantClusterVariableNotFound",
    "DeleteTenantClusterVariableUnauthorized",
    "DeleteTenantForbidden",
    "DeleteTenantInternalServerError",
    "DeleteTenantNotFound",
    "DeleteTenantServiceUnavailable",
    "DeleteUserBadRequest",
    "DeleteUserInternalServerError",
    "DeleteUserNotFound",
    "DeleteUserServiceUnavailable",
    "EvaluateConditionalsBadRequest",
    "EvaluateConditionalsForbidden",
    "EvaluateConditionalsInternalServerError",
    "EvaluateConditionalsNotFound",
    "EvaluateConditionalsServiceUnavailable",
    "EvaluateDecisionBadRequest",
    "EvaluateDecisionInternalServerError",
    "EvaluateDecisionNotFound",
    "EvaluateDecisionServiceUnavailable",
    "EvaluateExpressionBadRequest",
    "EvaluateExpressionForbidden",
    "EvaluateExpressionInternalServerError",
    "EvaluateExpressionUnauthorized",
    "FailJobBadRequest",
    "FailJobConflict",
    "FailJobInternalServerError",
    "FailJobNotFound",
    "FailJobServiceUnavailable",
    "GetAuditLogForbidden",
    "GetAuditLogInternalServerError",
    "GetAuditLogNotFound",
    "GetAuditLogUnauthorized",
    "GetAuthenticationForbidden",
    "GetAuthenticationInternalServerError",
    "GetAuthenticationUnauthorized",
    "GetAuthorizationForbidden",
    "GetAuthorizationInternalServerError",
    "GetAuthorizationNotFound",
    "GetAuthorizationUnauthorized",
    "GetBatchOperationBadRequest",
    "GetBatchOperationInternalServerError",
    "GetBatchOperationNotFound",
    "GetDecisionDefinitionBadRequest",
    "GetDecisionDefinitionForbidden",
    "GetDecisionDefinitionInternalServerError",
    "GetDecisionDefinitionNotFound",
    "GetDecisionDefinitionUnauthorized",
    "GetDecisionDefinitionXmlBadRequest",
    "GetDecisionDefinitionXmlForbidden",
    "GetDecisionDefinitionXmlInternalServerError",
    "GetDecisionDefinitionXmlNotFound",
    "GetDecisionDefinitionXmlUnauthorized",
    "GetDecisionInstanceBadRequest",
    "GetDecisionInstanceForbidden",
    "GetDecisionInstanceInternalServerError",
    "GetDecisionInstanceNotFound",
    "GetDecisionInstanceUnauthorized",
    "GetDecisionRequirementsBadRequest",
    "GetDecisionRequirementsForbidden",
    "GetDecisionRequirementsInternalServerError",
    "GetDecisionRequirementsNotFound",
    "GetDecisionRequirementsUnauthorized",
    "GetDecisionRequirementsXmlBadRequest",
    "GetDecisionRequirementsXmlForbidden",
    "GetDecisionRequirementsXmlInternalServerError",
    "GetDecisionRequirementsXmlNotFound",
    "GetDecisionRequirementsXmlUnauthorized",
    "GetDocumentInternalServerError",
    "GetDocumentNotFound",
    "GetElementInstanceBadRequest",
    "GetElementInstanceForbidden",
    "GetElementInstanceInternalServerError",
    "GetElementInstanceNotFound",
    "GetElementInstanceUnauthorized",
    "GetGlobalClusterVariableBadRequest",
    "GetGlobalClusterVariableForbidden",
    "GetGlobalClusterVariableInternalServerError",
    "GetGlobalClusterVariableNotFound",
    "GetGlobalClusterVariableUnauthorized",
    "GetGlobalJobStatisticsBadRequest",
    "GetGlobalJobStatisticsForbidden",
    "GetGlobalJobStatisticsInternalServerError",
    "GetGlobalJobStatisticsUnauthorized",
    "GetGroupForbidden",
    "GetGroupInternalServerError",
    "GetGroupNotFound",
    "GetGroupUnauthorized",
    "GetIncidentBadRequest",
    "GetIncidentForbidden",
    "GetIncidentInternalServerError",
    "GetIncidentNotFound",
    "GetIncidentUnauthorized",
    "GetJobTypeStatisticsBadRequest",
    "GetJobTypeStatisticsForbidden",
    "GetJobTypeStatisticsInternalServerError",
    "GetJobTypeStatisticsUnauthorized",
    "GetLicenseInternalServerError",
    "GetMappingRuleInternalServerError",
    "GetMappingRuleNotFound",
    "GetMappingRuleUnauthorized",
    "GetProcessDefinitionBadRequest",
    "GetProcessDefinitionForbidden",
    "GetProcessDefinitionInstanceStatisticsBadRequest",
    "GetProcessDefinitionInstanceStatisticsForbidden",
    "GetProcessDefinitionInstanceStatisticsInternalServerError",
    "GetProcessDefinitionInstanceStatisticsUnauthorized",
    "GetProcessDefinitionInstanceVersionStatisticsBadRequest",
    "GetProcessDefinitionInstanceVersionStatisticsForbidden",
    "GetProcessDefinitionInstanceVersionStatisticsInternalServerError",
    "GetProcessDefinitionInstanceVersionStatisticsUnauthorized",
    "GetProcessDefinitionInternalServerError",
    "GetProcessDefinitionMessageSubscriptionStatisticsBadRequest",
    "GetProcessDefinitionMessageSubscriptionStatisticsForbidden",
    "GetProcessDefinitionMessageSubscriptionStatisticsInternalServerError",
    "GetProcessDefinitionMessageSubscriptionStatisticsUnauthorized",
    "GetProcessDefinitionNotFound",
    "GetProcessDefinitionStatisticsBadRequest",
    "GetProcessDefinitionStatisticsForbidden",
    "GetProcessDefinitionStatisticsInternalServerError",
    "GetProcessDefinitionStatisticsUnauthorized",
    "GetProcessDefinitionUnauthorized",
    "GetProcessDefinitionXmlBadRequest",
    "GetProcessDefinitionXmlForbidden",
    "GetProcessDefinitionXmlInternalServerError",
    "GetProcessDefinitionXmlNotFound",
    "GetProcessDefinitionXmlUnauthorized",
    "GetProcessInstanceBadRequest",
    "GetProcessInstanceCallHierarchyBadRequest",
    "GetProcessInstanceCallHierarchyForbidden",
    "GetProcessInstanceCallHierarchyInternalServerError",
    "GetProcessInstanceCallHierarchyNotFound",
    "GetProcessInstanceCallHierarchyUnauthorized",
    "GetProcessInstanceForbidden",
    "GetProcessInstanceInternalServerError",
    "GetProcessInstanceNotFound",
    "GetProcessInstanceSequenceFlowsBadRequest",
    "GetProcessInstanceSequenceFlowsForbidden",
    "GetProcessInstanceSequenceFlowsInternalServerError",
    "GetProcessInstanceSequenceFlowsUnauthorized",
    "GetProcessInstanceStatisticsBadRequest",
    "GetProcessInstanceStatisticsByDefinitionBadRequest",
    "GetProcessInstanceStatisticsByDefinitionForbidden",
    "GetProcessInstanceStatisticsByDefinitionInternalServerError",
    "GetProcessInstanceStatisticsByDefinitionUnauthorized",
    "GetProcessInstanceStatisticsByErrorBadRequest",
    "GetProcessInstanceStatisticsByErrorForbidden",
    "GetProcessInstanceStatisticsByErrorInternalServerError",
    "GetProcessInstanceStatisticsByErrorUnauthorized",
    "GetProcessInstanceStatisticsForbidden",
    "GetProcessInstanceStatisticsInternalServerError",
    "GetProcessInstanceStatisticsUnauthorized",
    "GetProcessInstanceUnauthorized",
    "GetResourceContentInternalServerError",
    "GetResourceContentNotFound",
    "GetResourceInternalServerError",
    "GetResourceNotFound",
    "GetRoleForbidden",
    "GetRoleInternalServerError",
    "GetRoleNotFound",
    "GetRoleUnauthorized",
    "GetStartProcessFormBadRequest",
    "GetStartProcessFormForbidden",
    "GetStartProcessFormInternalServerError",
    "GetStartProcessFormNotFound",
    "GetStartProcessFormUnauthorized",
    "GetStatusServiceUnavailable",
    "GetTenantBadRequest",
    "GetTenantClusterVariableBadRequest",
    "GetTenantClusterVariableForbidden",
    "GetTenantClusterVariableInternalServerError",
    "GetTenantClusterVariableNotFound",
    "GetTenantClusterVariableUnauthorized",
    "GetTenantForbidden",
    "GetTenantInternalServerError",
    "GetTenantNotFound",
    "GetTenantUnauthorized",
    "GetTopologyInternalServerError",
    "GetTopologyUnauthorized",
    "GetUsageMetricsBadRequest",
    "GetUsageMetricsForbidden",
    "GetUsageMetricsInternalServerError",
    "GetUsageMetricsUnauthorized",
    "GetUserForbidden",
    "GetUserInternalServerError",
    "GetUserNotFound",
    "GetUserTaskBadRequest",
    "GetUserTaskForbidden",
    "GetUserTaskFormBadRequest",
    "GetUserTaskFormForbidden",
    "GetUserTaskFormInternalServerError",
    "GetUserTaskFormNotFound",
    "GetUserTaskFormUnauthorized",
    "GetUserTaskInternalServerError",
    "GetUserTaskNotFound",
    "GetUserTaskUnauthorized",
    "GetUserUnauthorized",
    "GetVariableBadRequest",
    "GetVariableForbidden",
    "GetVariableInternalServerError",
    "GetVariableNotFound",
    "GetVariableUnauthorized",
    "MigrateProcessInstanceBadRequest",
    "MigrateProcessInstanceConflict",
    "MigrateProcessInstanceInternalServerError",
    "MigrateProcessInstanceNotFound",
    "MigrateProcessInstanceServiceUnavailable",
    "MigrateProcessInstancesBatchOperationBadRequest",
    "MigrateProcessInstancesBatchOperationForbidden",
    "MigrateProcessInstancesBatchOperationInternalServerError",
    "MigrateProcessInstancesBatchOperationUnauthorized",
    "ModifyProcessInstanceBadRequest",
    "ModifyProcessInstanceInternalServerError",
    "ModifyProcessInstanceNotFound",
    "ModifyProcessInstanceServiceUnavailable",
    "ModifyProcessInstancesBatchOperationBadRequest",
    "ModifyProcessInstancesBatchOperationForbidden",
    "ModifyProcessInstancesBatchOperationInternalServerError",
    "ModifyProcessInstancesBatchOperationUnauthorized",
    "PinClockBadRequest",
    "PinClockInternalServerError",
    "PinClockServiceUnavailable",
    "PublishMessageBadRequest",
    "PublishMessageInternalServerError",
    "PublishMessageServiceUnavailable",
    "ResetClockInternalServerError",
    "ResetClockServiceUnavailable",
    "ResolveIncidentBadRequest",
    "ResolveIncidentInternalServerError",
    "ResolveIncidentNotFound",
    "ResolveIncidentServiceUnavailable",
    "ResolveIncidentsBatchOperationBadRequest",
    "ResolveIncidentsBatchOperationForbidden",
    "ResolveIncidentsBatchOperationInternalServerError",
    "ResolveIncidentsBatchOperationUnauthorized",
    "ResolveProcessInstanceIncidentsBadRequest",
    "ResolveProcessInstanceIncidentsInternalServerError",
    "ResolveProcessInstanceIncidentsNotFound",
    "ResolveProcessInstanceIncidentsServiceUnavailable",
    "ResolveProcessInstanceIncidentsUnauthorized",
    "ResumeBatchOperationBadRequest",
    "ResumeBatchOperationForbidden",
    "ResumeBatchOperationInternalServerError",
    "ResumeBatchOperationNotFound",
    "ResumeBatchOperationServiceUnavailable",
    "SearchAuditLogsBadRequest",
    "SearchAuditLogsForbidden",
    "SearchAuditLogsInternalServerError",
    "SearchAuditLogsUnauthorized",
    "SearchAuthorizationsBadRequest",
    "SearchAuthorizationsForbidden",
    "SearchAuthorizationsInternalServerError",
    "SearchAuthorizationsUnauthorized",
    "SearchBatchOperationItemsBadRequest",
    "SearchBatchOperationItemsInternalServerError",
    "SearchBatchOperationsBadRequest",
    "SearchBatchOperationsInternalServerError",
    "SearchClientsForGroupBadRequest",
    "SearchClientsForGroupForbidden",
    "SearchClientsForGroupInternalServerError",
    "SearchClientsForGroupNotFound",
    "SearchClientsForGroupUnauthorized",
    "SearchClientsForRoleBadRequest",
    "SearchClientsForRoleForbidden",
    "SearchClientsForRoleInternalServerError",
    "SearchClientsForRoleNotFound",
    "SearchClientsForRoleUnauthorized",
    "SearchClusterVariablesBadRequest",
    "SearchClusterVariablesForbidden",
    "SearchClusterVariablesInternalServerError",
    "SearchClusterVariablesUnauthorized",
    "SearchCorrelatedMessageSubscriptionsBadRequest",
    "SearchCorrelatedMessageSubscriptionsForbidden",
    "SearchCorrelatedMessageSubscriptionsInternalServerError",
    "SearchCorrelatedMessageSubscriptionsUnauthorized",
    "SearchDecisionDefinitionsBadRequest",
    "SearchDecisionDefinitionsForbidden",
    "SearchDecisionDefinitionsInternalServerError",
    "SearchDecisionDefinitionsUnauthorized",
    "SearchDecisionInstancesBadRequest",
    "SearchDecisionInstancesForbidden",
    "SearchDecisionInstancesInternalServerError",
    "SearchDecisionInstancesUnauthorized",
    "SearchDecisionRequirementsBadRequest",
    "SearchDecisionRequirementsForbidden",
    "SearchDecisionRequirementsInternalServerError",
    "SearchDecisionRequirementsUnauthorized",
    "SearchElementInstanceIncidentsBadRequest",
    "SearchElementInstanceIncidentsForbidden",
    "SearchElementInstanceIncidentsInternalServerError",
    "SearchElementInstanceIncidentsNotFound",
    "SearchElementInstanceIncidentsUnauthorized",
    "SearchElementInstancesBadRequest",
    "SearchElementInstancesForbidden",
    "SearchElementInstancesInternalServerError",
    "SearchElementInstancesUnauthorized",
    "SearchGroupsBadRequest",
    "SearchGroupsForRoleBadRequest",
    "SearchGroupsForRoleForbidden",
    "SearchGroupsForRoleInternalServerError",
    "SearchGroupsForRoleNotFound",
    "SearchGroupsForRoleUnauthorized",
    "SearchGroupsForbidden",
    "SearchGroupsInternalServerError",
    "SearchGroupsUnauthorized",
    "SearchIncidentsBadRequest",
    "SearchIncidentsForbidden",
    "SearchIncidentsInternalServerError",
    "SearchIncidentsUnauthorized",
    "SearchJobsBadRequest",
    "SearchJobsForbidden",
    "SearchJobsInternalServerError",
    "SearchJobsUnauthorized",
    "SearchMappingRuleBadRequest",
    "SearchMappingRuleForbidden",
    "SearchMappingRuleInternalServerError",
    "SearchMappingRuleUnauthorized",
    "SearchMappingRulesForGroupBadRequest",
    "SearchMappingRulesForGroupForbidden",
    "SearchMappingRulesForGroupInternalServerError",
    "SearchMappingRulesForGroupNotFound",
    "SearchMappingRulesForGroupUnauthorized",
    "SearchMappingRulesForRoleBadRequest",
    "SearchMappingRulesForRoleForbidden",
    "SearchMappingRulesForRoleInternalServerError",
    "SearchMappingRulesForRoleNotFound",
    "SearchMappingRulesForRoleUnauthorized",
    "SearchMessageSubscriptionsBadRequest",
    "SearchMessageSubscriptionsForbidden",
    "SearchMessageSubscriptionsInternalServerError",
    "SearchMessageSubscriptionsUnauthorized",
    "SearchProcessDefinitionsBadRequest",
    "SearchProcessDefinitionsForbidden",
    "SearchProcessDefinitionsInternalServerError",
    "SearchProcessDefinitionsUnauthorized",
    "SearchProcessInstanceIncidentsBadRequest",
    "SearchProcessInstanceIncidentsForbidden",
    "SearchProcessInstanceIncidentsInternalServerError",
    "SearchProcessInstanceIncidentsNotFound",
    "SearchProcessInstanceIncidentsUnauthorized",
    "SearchProcessInstancesBadRequest",
    "SearchProcessInstancesForbidden",
    "SearchProcessInstancesInternalServerError",
    "SearchProcessInstancesUnauthorized",
    "SearchRolesBadRequest",
    "SearchRolesForGroupBadRequest",
    "SearchRolesForGroupForbidden",
    "SearchRolesForGroupInternalServerError",
    "SearchRolesForGroupNotFound",
    "SearchRolesForGroupUnauthorized",
    "SearchRolesForbidden",
    "SearchRolesInternalServerError",
    "SearchRolesUnauthorized",
    "SearchTenantsBadRequest",
    "SearchTenantsForbidden",
    "SearchTenantsInternalServerError",
    "SearchTenantsNotFound",
    "SearchTenantsUnauthorized",
    "SearchUserTaskAuditLogsBadRequest",
    "SearchUserTaskAuditLogsInternalServerError",
    "SearchUserTaskVariablesBadRequest",
    "SearchUserTaskVariablesInternalServerError",
    "SearchUserTasksBadRequest",
    "SearchUserTasksForbidden",
    "SearchUserTasksInternalServerError",
    "SearchUserTasksUnauthorized",
    "SearchUsersBadRequest",
    "SearchUsersForGroupBadRequest",
    "SearchUsersForGroupForbidden",
    "SearchUsersForGroupInternalServerError",
    "SearchUsersForGroupNotFound",
    "SearchUsersForGroupUnauthorized",
    "SearchUsersForRoleBadRequest",
    "SearchUsersForRoleForbidden",
    "SearchUsersForRoleInternalServerError",
    "SearchUsersForRoleNotFound",
    "SearchUsersForRoleUnauthorized",
    "SearchUsersForbidden",
    "SearchUsersInternalServerError",
    "SearchUsersUnauthorized",
    "SearchVariablesBadRequest",
    "SearchVariablesForbidden",
    "SearchVariablesInternalServerError",
    "SearchVariablesUnauthorized",
    "SuspendBatchOperationBadRequest",
    "SuspendBatchOperationForbidden",
    "SuspendBatchOperationInternalServerError",
    "SuspendBatchOperationNotFound",
    "SuspendBatchOperationServiceUnavailable",
    "ThrowJobErrorBadRequest",
    "ThrowJobErrorConflict",
    "ThrowJobErrorInternalServerError",
    "ThrowJobErrorNotFound",
    "ThrowJobErrorServiceUnavailable",
    "UnassignClientFromGroupBadRequest",
    "UnassignClientFromGroupForbidden",
    "UnassignClientFromGroupInternalServerError",
    "UnassignClientFromGroupNotFound",
    "UnassignClientFromGroupServiceUnavailable",
    "UnassignClientFromTenantBadRequest",
    "UnassignClientFromTenantForbidden",
    "UnassignClientFromTenantInternalServerError",
    "UnassignClientFromTenantNotFound",
    "UnassignClientFromTenantServiceUnavailable",
    "UnassignGroupFromTenantBadRequest",
    "UnassignGroupFromTenantForbidden",
    "UnassignGroupFromTenantInternalServerError",
    "UnassignGroupFromTenantNotFound",
    "UnassignGroupFromTenantServiceUnavailable",
    "UnassignMappingRuleFromGroupBadRequest",
    "UnassignMappingRuleFromGroupForbidden",
    "UnassignMappingRuleFromGroupInternalServerError",
    "UnassignMappingRuleFromGroupNotFound",
    "UnassignMappingRuleFromGroupServiceUnavailable",
    "UnassignMappingRuleFromTenantBadRequest",
    "UnassignMappingRuleFromTenantForbidden",
    "UnassignMappingRuleFromTenantInternalServerError",
    "UnassignMappingRuleFromTenantNotFound",
    "UnassignMappingRuleFromTenantServiceUnavailable",
    "UnassignRoleFromClientBadRequest",
    "UnassignRoleFromClientForbidden",
    "UnassignRoleFromClientInternalServerError",
    "UnassignRoleFromClientNotFound",
    "UnassignRoleFromClientServiceUnavailable",
    "UnassignRoleFromGroupBadRequest",
    "UnassignRoleFromGroupForbidden",
    "UnassignRoleFromGroupInternalServerError",
    "UnassignRoleFromGroupNotFound",
    "UnassignRoleFromGroupServiceUnavailable",
    "UnassignRoleFromMappingRuleBadRequest",
    "UnassignRoleFromMappingRuleForbidden",
    "UnassignRoleFromMappingRuleInternalServerError",
    "UnassignRoleFromMappingRuleNotFound",
    "UnassignRoleFromMappingRuleServiceUnavailable",
    "UnassignRoleFromTenantBadRequest",
    "UnassignRoleFromTenantForbidden",
    "UnassignRoleFromTenantInternalServerError",
    "UnassignRoleFromTenantNotFound",
    "UnassignRoleFromTenantServiceUnavailable",
    "UnassignRoleFromUserBadRequest",
    "UnassignRoleFromUserForbidden",
    "UnassignRoleFromUserInternalServerError",
    "UnassignRoleFromUserNotFound",
    "UnassignRoleFromUserServiceUnavailable",
    "UnassignUserFromGroupBadRequest",
    "UnassignUserFromGroupForbidden",
    "UnassignUserFromGroupInternalServerError",
    "UnassignUserFromGroupNotFound",
    "UnassignUserFromGroupServiceUnavailable",
    "UnassignUserFromTenantBadRequest",
    "UnassignUserFromTenantForbidden",
    "UnassignUserFromTenantInternalServerError",
    "UnassignUserFromTenantNotFound",
    "UnassignUserFromTenantServiceUnavailable",
    "UnassignUserTaskBadRequest",
    "UnassignUserTaskConflict",
    "UnassignUserTaskInternalServerError",
    "UnassignUserTaskNotFound",
    "UnassignUserTaskServiceUnavailable",
    "UnexpectedStatus",
    "UpdateAuthorizationInternalServerError",
    "UpdateAuthorizationNotFound",
    "UpdateAuthorizationServiceUnavailable",
    "UpdateAuthorizationUnauthorized",
    "UpdateGlobalClusterVariableBadRequest",
    "UpdateGlobalClusterVariableForbidden",
    "UpdateGlobalClusterVariableInternalServerError",
    "UpdateGlobalClusterVariableNotFound",
    "UpdateGlobalClusterVariableUnauthorized",
    "UpdateGlobalTaskListenerBadRequest",
    "UpdateGlobalTaskListenerForbidden",
    "UpdateGlobalTaskListenerInternalServerError",
    "UpdateGlobalTaskListenerNotFound",
    "UpdateGlobalTaskListenerServiceUnavailable",
    "UpdateGlobalTaskListenerUnauthorized",
    "UpdateGroupBadRequest",
    "UpdateGroupInternalServerError",
    "UpdateGroupNotFound",
    "UpdateGroupServiceUnavailable",
    "UpdateGroupUnauthorized",
    "UpdateJobBadRequest",
    "UpdateJobConflict",
    "UpdateJobInternalServerError",
    "UpdateJobNotFound",
    "UpdateJobServiceUnavailable",
    "UpdateMappingRuleBadRequest",
    "UpdateMappingRuleForbidden",
    "UpdateMappingRuleInternalServerError",
    "UpdateMappingRuleNotFound",
    "UpdateMappingRuleServiceUnavailable",
    "UpdateRoleBadRequest",
    "UpdateRoleInternalServerError",
    "UpdateRoleNotFound",
    "UpdateRoleServiceUnavailable",
    "UpdateRoleUnauthorized",
    "UpdateTenantBadRequest",
    "UpdateTenantClusterVariableBadRequest",
    "UpdateTenantClusterVariableForbidden",
    "UpdateTenantClusterVariableInternalServerError",
    "UpdateTenantClusterVariableNotFound",
    "UpdateTenantClusterVariableUnauthorized",
    "UpdateTenantForbidden",
    "UpdateTenantInternalServerError",
    "UpdateTenantNotFound",
    "UpdateTenantServiceUnavailable",
    "UpdateUserBadRequest",
    "UpdateUserForbidden",
    "UpdateUserInternalServerError",
    "UpdateUserNotFound",
    "UpdateUserServiceUnavailable",
    "UpdateUserTaskBadRequest",
    "UpdateUserTaskConflict",
    "UpdateUserTaskInternalServerError",
    "UpdateUserTaskNotFound",
    "UpdateUserTaskServiceUnavailable",
]
