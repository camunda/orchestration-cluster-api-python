"""Contains shared errors types that can be raised from API functions"""
from __future__ import annotations

from typing import Any


class ApiError(Exception):
    """Base class for API errors raised by convenience wrappers."""

    def __init__(self, *, status_code: int, content: bytes, parsed: Any | None = None):
        self.status_code = status_code
        self.content = content
        self.parsed = parsed

        super().__init__(self._build_message())

    def _build_message(self) -> str:
        parsed_name = type(self.parsed).__name__ if self.parsed is not None else 'None'
        try:
            content_text = self.content.decode(errors='ignore')
        except Exception:
            content_text = '<binary>'
        return f'HTTP {self.status_code} ({parsed_name})\n\nResponse content:\n{content_text}'


class UnexpectedStatus(ApiError):
    """Raised when the server returns a status code that is not handled/parsed by the SDK."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(status_code=status_code, content=content, parsed=None)


class ActivateAdHocSubProcessActivitiesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: ActivateAdHocSubProcessActivitiesResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateAdHocSubProcessActivitiesResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: ActivateAdHocSubProcessActivitiesResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateAdHocSubProcessActivitiesResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ActivateAdHocSubProcessActivitiesResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateAdHocSubProcessActivitiesResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesNotFound(ApiError):
    """Raised when the server returns HTTP 404. The ad-hoc sub-process instance is not found or the provided key does not identify an ad-hoc sub-process."""
    parsed: ActivateAdHocSubProcessActivitiesResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateAdHocSubProcessActivitiesResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: ActivateAdHocSubProcessActivitiesResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateAdHocSubProcessActivitiesResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateAdHocSubProcessActivitiesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: ActivateAdHocSubProcessActivitiesResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateAdHocSubProcessActivitiesResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateJobsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: ActivateJobsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateJobsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateJobsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ActivateJobsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateJobsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateJobsServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: ActivateJobsResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateJobsResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ActivateJobsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: ActivateJobsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: ActivateJobsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignClientToGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupConflict(ApiError):
    """Raised when the server returns HTTP 409. The client with the given ID is already assigned to the group."""
    parsed: AssignClientToGroupResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToGroupResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignClientToGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignClientToGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""
    parsed: AssignClientToGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignClientToGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignClientToTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignClientToTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignClientToTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. The tenant was not found."""
    parsed: AssignClientToTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignClientToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignClientToTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignClientToTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignGroupToTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignGroupToTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignGroupToTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignGroupToTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignGroupToTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignGroupToTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or group was not found."""
    parsed: AssignGroupToTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignGroupToTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignGroupToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignGroupToTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignGroupToTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignMappingRuleToGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupConflict(ApiError):
    """Raised when the server returns HTTP 409. The mapping rule with the given ID is already assigned to the group."""
    parsed: AssignMappingRuleToGroupResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToGroupResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignMappingRuleToGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignMappingRuleToGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group or mapping rule with the given ID was not found."""
    parsed: AssignMappingRuleToGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignMappingRuleToGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignMappingRuleToTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignMappingRuleToTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignMappingRuleToTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or mapping rule was not found."""
    parsed: AssignMappingRuleToTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignMappingRuleToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignMappingRuleToTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignMappingRuleToTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignRoleToClientResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToClientResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientConflict(ApiError):
    """Raised when the server returns HTTP 409. The role was already assigned to the client with the given ID."""
    parsed: AssignRoleToClientResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToClientResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignRoleToClientResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToClientResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignRoleToClientResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToClientResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""
    parsed: AssignRoleToClientResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToClientResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToClientServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignRoleToClientResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToClientResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignRoleToGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupConflict(ApiError):
    """Raised when the server returns HTTP 409. The role is already assigned to the group with the given ID."""
    parsed: AssignRoleToGroupResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToGroupResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignRoleToGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignRoleToGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or group with the given ID was not found."""
    parsed: AssignRoleToGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignRoleToGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignRoleToMappingRuleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToMappingRuleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleConflict(ApiError):
    """Raised when the server returns HTTP 409. The role is already assigned to the mapping rule with the given ID."""
    parsed: AssignRoleToMappingRuleResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToMappingRuleResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignRoleToMappingRuleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToMappingRuleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignRoleToMappingRuleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToMappingRuleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or mapping rule with the given ID was not found."""
    parsed: AssignRoleToMappingRuleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToMappingRuleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToMappingRuleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignRoleToMappingRuleResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToMappingRuleResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignRoleToTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignRoleToTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignRoleToTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or role was not found."""
    parsed: AssignRoleToTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignRoleToTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignRoleToUserResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToUserResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserConflict(ApiError):
    """Raised when the server returns HTTP 409. The role is already assigned to the user with the given ID."""
    parsed: AssignRoleToUserResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToUserResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignRoleToUserResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToUserResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignRoleToUserResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToUserResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or user with the given ID or username was not found."""
    parsed: AssignRoleToUserResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToUserResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignRoleToUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignRoleToUserResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignRoleToUserResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignUserTaskResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserTaskResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskConflict(ApiError):
    """Raised when the server returns HTTP 409. The user task with the given key is in the wrong state currently. More details are provided in the response body."""
    parsed: AssignUserTaskResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserTaskResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignUserTaskResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserTaskResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""
    parsed: AssignUserTaskResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserTaskResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserTaskServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignUserTaskResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserTaskResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignUserToGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupConflict(ApiError):
    """Raised when the server returns HTTP 409. The user with the given ID is already assigned to the group."""
    parsed: AssignUserToGroupResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToGroupResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignUserToGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignUserToGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group or user with the given ID or username was not found."""
    parsed: AssignUserToGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignUserToGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: AssignUserToTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: AssignUserToTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: AssignUserToTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or user was not found."""
    parsed: AssignUserToTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class AssignUserToTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: AssignUserToTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: AssignUserToTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class BroadcastSignalBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: BroadcastSignalResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: BroadcastSignalResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class BroadcastSignalInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: BroadcastSignalResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: BroadcastSignalResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class BroadcastSignalNotFound(ApiError):
    """Raised when the server returns HTTP 404. The signal is not found."""
    parsed: BroadcastSignalResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: BroadcastSignalResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class BroadcastSignalServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: BroadcastSignalResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: BroadcastSignalResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CancelBatchOperationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelBatchOperationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CancelBatchOperationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelBatchOperationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CancelBatchOperationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelBatchOperationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelBatchOperationNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The batch operation was not found."""
    parsed: CancelBatchOperationResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelBatchOperationResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CancelProcessInstanceResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelProcessInstanceResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CancelProcessInstanceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelProcessInstanceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""
    parsed: CancelProcessInstanceResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelProcessInstanceResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CancelProcessInstanceResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelProcessInstanceResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstancesBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""
    parsed: CancelProcessInstancesBatchOperationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelProcessInstancesBatchOperationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstancesBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CancelProcessInstancesBatchOperationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelProcessInstancesBatchOperationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstancesBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CancelProcessInstancesBatchOperationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelProcessInstancesBatchOperationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CancelProcessInstancesBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: CancelProcessInstancesBatchOperationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: CancelProcessInstancesBatchOperationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CompleteJobResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteJobResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobConflict(ApiError):
    """Raised when the server returns HTTP 409. The job with the given key is in the wrong state currently. More details are provided in the response body."""
    parsed: CompleteJobResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteJobResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CompleteJobResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteJobResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobNotFound(ApiError):
    """Raised when the server returns HTTP 404. The job with the given key was not found."""
    parsed: CompleteJobResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteJobResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteJobServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CompleteJobResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteJobResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CompleteUserTaskResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteUserTaskResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskConflict(ApiError):
    """Raised when the server returns HTTP 409. The user task with the given key is in the wrong state currently. More details are provided in the response body."""
    parsed: CompleteUserTaskResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteUserTaskResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CompleteUserTaskResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteUserTaskResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""
    parsed: CompleteUserTaskResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteUserTaskResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CompleteUserTaskServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CompleteUserTaskResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CompleteUserTaskResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CorrelateMessageResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CorrelateMessageResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CorrelateMessageResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CorrelateMessageResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CorrelateMessageResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CorrelateMessageResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""
    parsed: CorrelateMessageResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: CorrelateMessageResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CorrelateMessageServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CorrelateMessageResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CorrelateMessageResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAdminUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateAdminUserResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAdminUserResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAdminUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CreateAdminUserResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAdminUserResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAdminUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateAdminUserResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAdminUserResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAdminUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CreateAdminUserResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAdminUserResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateAuthorizationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAuthorizationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CreateAuthorizationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAuthorizationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateAuthorizationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAuthorizationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The owner was not found."""
    parsed: CreateAuthorizationResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAuthorizationResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CreateAuthorizationResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAuthorizationResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateAuthorizationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: CreateAuthorizationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateAuthorizationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDeploymentBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateDeploymentResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateDeploymentResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDeploymentServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CreateDeploymentResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateDeploymentResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateDocumentResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateDocumentResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentLinkBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateDocumentLinkResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateDocumentLinkResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentUnsupportedMediaType(ApiError):
    """Raised when the server returns HTTP 415. The server cannot process the request because the media type (Content-Type) of the request payload is not supported by the server for the requested resource and method."""
    parsed: CreateDocumentResponse415

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateDocumentResponse415):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateDocumentsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateDocumentsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateDocumentsUnsupportedMediaType(ApiError):
    """Raised when the server returns HTTP 415. The server cannot process the request because the media type (Content-Type) of the request payload is not supported by the server for the requested resource and method."""
    parsed: CreateDocumentsResponse415

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateDocumentsResponse415):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateElementInstanceVariablesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateElementInstanceVariablesResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateElementInstanceVariablesResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateElementInstanceVariablesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateElementInstanceVariablesResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateElementInstanceVariablesResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateElementInstanceVariablesServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CreateElementInstanceVariablesResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateElementInstanceVariablesResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateGlobalClusterVariableResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateGlobalClusterVariableResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CreateGlobalClusterVariableResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateGlobalClusterVariableResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateGlobalClusterVariableResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateGlobalClusterVariableResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGlobalClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: CreateGlobalClusterVariableResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateGlobalClusterVariableResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CreateGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CreateGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: CreateGroupResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateGroupResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateMappingRuleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateMappingRuleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. The request to create a mapping rule was denied. More details are provided in the response body."""
    parsed: CreateMappingRuleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateMappingRuleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateMappingRuleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateMappingRuleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The request to create a mapping rule was denied."""
    parsed: CreateMappingRuleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateMappingRuleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateProcessInstanceResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateProcessInstanceResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateProcessInstanceGatewayTimeout(ApiError):
    """Raised when the server returns HTTP 504. The process instance creation request timed out in the gateway. This can happen if the `awaitCompletion` request parameter is set to `true` and the created process instance did not complete within the defined request timeout. This often happens when the created instance is not fully automated or contains wait states."""
    parsed: CreateProcessInstanceResponse504

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateProcessInstanceResponse504):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateProcessInstanceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateProcessInstanceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CreateProcessInstanceResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateProcessInstanceResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateRoleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateRoleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CreateRoleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateRoleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateRoleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateRoleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CreateRoleResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateRoleResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: CreateRoleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateRoleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateTenantClusterVariableResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateTenantClusterVariableResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CreateTenantClusterVariableResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateTenantClusterVariableResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateTenantClusterVariableResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateTenantClusterVariableResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: CreateTenantClusterVariableResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateTenantClusterVariableResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantConflict(ApiError):
    """Raised when the server returns HTTP 409. Tenant with this id already exists."""
    parsed: Any

    def __init__(self, *, status_code: int, content: bytes, parsed: Any):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CreateTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The resource was not found."""
    parsed: CreateTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CreateTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: CreateUserResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateUserResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserConflict(ApiError):
    """Raised when the server returns HTTP 409. A user with this username already exists."""
    parsed: CreateUserResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateUserResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: CreateUserResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateUserResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: CreateUserResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateUserResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: CreateUserResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateUserResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class CreateUserUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: CreateUserResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: CreateUserResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteAuthorizationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteAuthorizationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteAuthorizationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteAuthorizationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The authorization with the authorizationKey was not found."""
    parsed: DeleteAuthorizationResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteAuthorizationResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteAuthorizationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: DeleteAuthorizationResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteAuthorizationResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteAuthorizationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: DeleteAuthorizationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteAuthorizationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDocumentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteDocumentResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteDocumentResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteDocumentNotFound(ApiError):
    """Raised when the server returns HTTP 404. The document with the given ID was not found."""
    parsed: DeleteDocumentResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteDocumentResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: DeleteGlobalClusterVariableResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteGlobalClusterVariableResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: DeleteGlobalClusterVariableResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteGlobalClusterVariableResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteGlobalClusterVariableResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteGlobalClusterVariableResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""
    parsed: DeleteGlobalClusterVariableResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteGlobalClusterVariableResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGlobalClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: DeleteGlobalClusterVariableResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteGlobalClusterVariableResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""
    parsed: DeleteGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: DeleteGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: DeleteGroupResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteGroupResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteMappingRuleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteMappingRuleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The mapping rule with the mappingRuleId was not found."""
    parsed: DeleteMappingRuleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteMappingRuleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteMappingRuleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: DeleteMappingRuleResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteMappingRuleResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteMappingRuleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: DeleteMappingRuleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteMappingRuleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceConflict(ApiError):
    """Raised when the server returns HTTP 409. The process instance is not in a completed or terminated state and cannot be deleted."""
    parsed: DeleteProcessInstanceResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstanceResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: DeleteProcessInstanceResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstanceResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteProcessInstanceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstanceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""
    parsed: DeleteProcessInstanceResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstanceResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: DeleteProcessInstanceResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstanceResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstanceUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: DeleteProcessInstanceResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstanceResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstancesBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""
    parsed: DeleteProcessInstancesBatchOperationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstancesBatchOperationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstancesBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: DeleteProcessInstancesBatchOperationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstancesBatchOperationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstancesBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteProcessInstancesBatchOperationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstancesBatchOperationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteProcessInstancesBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: DeleteProcessInstancesBatchOperationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteProcessInstancesBatchOperationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteResourceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: DeleteResourceResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteResourceResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteResourceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteResourceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteResourceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteResourceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The resource is not found."""
    parsed: DeleteResourceResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteResourceResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteResourceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: DeleteResourceResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteResourceResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteRoleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteRoleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the ID was not found."""
    parsed: DeleteRoleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteRoleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteRoleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: DeleteRoleResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteRoleResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: DeleteRoleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteRoleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: DeleteTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: DeleteTenantClusterVariableResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantClusterVariableResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: DeleteTenantClusterVariableResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantClusterVariableResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteTenantClusterVariableResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantClusterVariableResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""
    parsed: DeleteTenantClusterVariableResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantClusterVariableResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: DeleteTenantClusterVariableResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantClusterVariableResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: DeleteTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant was not found."""
    parsed: DeleteTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: DeleteTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: DeleteUserResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteUserResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: DeleteUserResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteUserResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user is not found."""
    parsed: DeleteUserResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteUserResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class DeleteUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: DeleteUserResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: DeleteUserResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: EvaluateConditionalsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateConditionalsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsForbidden(ApiError):
    """Raised when the server returns HTTP 403. The client is not authorized to start process instances for the specified process definition. If a processDefinitionKey is not provided, this indicates that the client is not authorized to start process instances for at least one of the matched process definitions."""
    parsed: EvaluateConditionalsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateConditionalsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: EvaluateConditionalsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateConditionalsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process definition was not found for the given processDefinitionKey."""
    parsed: EvaluateConditionalsResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateConditionalsResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateConditionalsServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: EvaluateConditionalsResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateConditionalsResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateDecisionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: EvaluateDecisionResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateDecisionResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateDecisionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: EvaluateDecisionResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateDecisionResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateDecisionNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision is not found."""
    parsed: Any

    def __init__(self, *, status_code: int, content: bytes, parsed: Any):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateDecisionServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: EvaluateDecisionResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateDecisionResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateExpressionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: EvaluateExpressionResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateExpressionResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateExpressionForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: EvaluateExpressionResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateExpressionResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateExpressionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: EvaluateExpressionResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateExpressionResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class EvaluateExpressionUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: EvaluateExpressionResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: EvaluateExpressionResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: FailJobResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: FailJobResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobConflict(ApiError):
    """Raised when the server returns HTTP 409. The job with the given key is in the wrong state (i.e: not ACTIVATED or ACTIVATABLE). The job was failed by another worker with retries = 0, and the process is now in an incident state."""
    parsed: FailJobResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: FailJobResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: FailJobResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: FailJobResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobNotFound(ApiError):
    """Raised when the server returns HTTP 404. The job with the given jobKey is not found. It was completed by another worker, or the process instance itself was canceled."""
    parsed: FailJobResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: FailJobResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class FailJobServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: FailJobResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: FailJobResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuditLogForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetAuditLogResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuditLogResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuditLogInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetAuditLogResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuditLogResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuditLogNotFound(ApiError):
    """Raised when the server returns HTTP 404. The audit log with the given key was not found."""
    parsed: GetAuditLogResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuditLogResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuditLogUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetAuditLogResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuditLogResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthenticationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetAuthenticationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuthenticationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthenticationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetAuthenticationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuthenticationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthenticationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetAuthenticationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuthenticationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthorizationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetAuthorizationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuthorizationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthorizationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetAuthorizationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuthorizationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthorizationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The authorization with the given key was not found."""
    parsed: GetAuthorizationResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuthorizationResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetAuthorizationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetAuthorizationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetAuthorizationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetBatchOperationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetBatchOperationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetBatchOperationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetBatchOperationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetBatchOperationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The batch operation is not found."""
    parsed: GetBatchOperationResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetBatchOperationResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetDecisionDefinitionResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetDecisionDefinitionResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetDecisionDefinitionResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision definition with the given key was not found. More details are provided in the response body."""
    parsed: GetDecisionDefinitionResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetDecisionDefinitionResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetDecisionDefinitionXMLResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionXMLResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetDecisionDefinitionXMLResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionXMLResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetDecisionDefinitionXMLResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionXMLResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision definition with the given key was not found. More details are provided in the response body."""
    parsed: GetDecisionDefinitionXMLResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionXMLResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionDefinitionXmlUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetDecisionDefinitionXMLResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionDefinitionXMLResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetDecisionInstanceResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionInstanceResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetDecisionInstanceResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionInstanceResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetDecisionInstanceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionInstanceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision instance with the given key was not found. More details are provided in the response body."""
    parsed: GetDecisionInstanceResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionInstanceResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionInstanceUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetDecisionInstanceResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionInstanceResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetDecisionRequirementsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetDecisionRequirementsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetDecisionRequirementsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision requirements with the given key was not found. More details are provided in the response body."""
    parsed: GetDecisionRequirementsResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetDecisionRequirementsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetDecisionRequirementsXMLResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsXMLResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetDecisionRequirementsXMLResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsXMLResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetDecisionRequirementsXMLResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsXMLResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlNotFound(ApiError):
    """Raised when the server returns HTTP 404. The decision requirements with the given key was not found. More details are provided in the response body."""
    parsed: GetDecisionRequirementsXMLResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsXMLResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDecisionRequirementsXmlUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetDecisionRequirementsXMLResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDecisionRequirementsXMLResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDocumentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetDocumentResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDocumentResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetDocumentNotFound(ApiError):
    """Raised when the server returns HTTP 404. The document with the given ID was not found."""
    parsed: GetDocumentResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetDocumentResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetElementInstanceResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetElementInstanceResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetElementInstanceResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetElementInstanceResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetElementInstanceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetElementInstanceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The element instance with the given key was not found. More details are provided in the response body."""
    parsed: GetElementInstanceResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetElementInstanceResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetElementInstanceUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetElementInstanceResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetElementInstanceResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetGlobalClusterVariableResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetGlobalClusterVariableResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetGlobalClusterVariableResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetGlobalClusterVariableResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetGlobalClusterVariableResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetGlobalClusterVariableResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""
    parsed: GetGlobalClusterVariableResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetGlobalClusterVariableResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGlobalClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetGlobalClusterVariableResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetGlobalClusterVariableResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""
    parsed: GetGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetGroupResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetGroupResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetIncidentResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetIncidentResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetIncidentResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetIncidentResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetIncidentResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetIncidentResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentNotFound(ApiError):
    """Raised when the server returns HTTP 404. The incident with the given key was not found."""
    parsed: GetIncidentResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetIncidentResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetIncidentUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetIncidentResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetIncidentResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetLicenseInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetLicenseResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetLicenseResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetMappingRuleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetMappingRuleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The mapping rule with the mappingRuleId was not found."""
    parsed: GetMappingRuleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetMappingRuleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetMappingRuleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetMappingRuleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetMappingRuleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessDefinitionResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessDefinitionResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessDefinitionInstanceStatisticsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionInstanceStatisticsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessDefinitionInstanceStatisticsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionInstanceStatisticsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessDefinitionInstanceStatisticsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionInstanceStatisticsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessDefinitionInstanceStatisticsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionInstanceStatisticsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceVersionStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessDefinitionInstanceVersionStatisticsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionInstanceVersionStatisticsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceVersionStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessDefinitionInstanceVersionStatisticsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionInstanceVersionStatisticsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceVersionStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessDefinitionInstanceVersionStatisticsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionInstanceVersionStatisticsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInstanceVersionStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessDefinitionInstanceVersionStatisticsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionInstanceVersionStatisticsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessDefinitionResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionMessageSubscriptionStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessDefinitionMessageSubscriptionStatisticsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionMessageSubscriptionStatisticsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionMessageSubscriptionStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessDefinitionMessageSubscriptionStatisticsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionMessageSubscriptionStatisticsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionMessageSubscriptionStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessDefinitionMessageSubscriptionStatisticsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionMessageSubscriptionStatisticsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionMessageSubscriptionStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessDefinitionMessageSubscriptionStatisticsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionMessageSubscriptionStatisticsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process definition with the given key was not found. More details are provided in the response body."""
    parsed: GetProcessDefinitionResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessDefinitionStatisticsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionStatisticsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessDefinitionStatisticsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionStatisticsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessDefinitionStatisticsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionStatisticsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessDefinitionStatisticsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionStatisticsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessDefinitionResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessDefinitionXMLResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionXMLResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessDefinitionXMLResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionXMLResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessDefinitionXMLResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionXMLResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process definition with the given key was not found. More details are provided in the response body."""
    parsed: GetProcessDefinitionXMLResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionXMLResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessDefinitionXmlUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessDefinitionXMLResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessDefinitionXMLResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessInstanceResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessInstanceCallHierarchyResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceCallHierarchyResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessInstanceCallHierarchyResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceCallHierarchyResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessInstanceCallHierarchyResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceCallHierarchyResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""
    parsed: GetProcessInstanceCallHierarchyResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceCallHierarchyResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceCallHierarchyUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessInstanceCallHierarchyResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceCallHierarchyResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessInstanceResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessInstanceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance with the given key was not found."""
    parsed: GetProcessInstanceResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceSequenceFlowsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessInstanceSequenceFlowsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceSequenceFlowsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceSequenceFlowsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessInstanceSequenceFlowsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceSequenceFlowsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceSequenceFlowsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessInstanceSequenceFlowsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceSequenceFlowsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceSequenceFlowsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessInstanceSequenceFlowsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceSequenceFlowsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessInstanceStatisticsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByDefinitionBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessInstanceStatisticsByDefinitionResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsByDefinitionResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByDefinitionForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessInstanceStatisticsByDefinitionResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsByDefinitionResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByDefinitionInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessInstanceStatisticsByDefinitionResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsByDefinitionResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByDefinitionUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessInstanceStatisticsByDefinitionResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsByDefinitionResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByErrorBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetProcessInstanceStatisticsByErrorResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsByErrorResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByErrorForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessInstanceStatisticsByErrorResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsByErrorResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByErrorInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessInstanceStatisticsByErrorResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsByErrorResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsByErrorUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessInstanceStatisticsByErrorResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsByErrorResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetProcessInstanceStatisticsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetProcessInstanceStatisticsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceStatisticsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessInstanceStatisticsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceStatisticsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetProcessInstanceUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetProcessInstanceResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetProcessInstanceResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetResourceContentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetResourceContentResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetResourceContentResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetResourceContentNotFound(ApiError):
    """Raised when the server returns HTTP 404. A resource with the given key was not found."""
    parsed: GetResourceContentResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetResourceContentResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetResourceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetResourceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetResourceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetResourceNotFound(ApiError):
    """Raised when the server returns HTTP 404. A resource with the given key was not found."""
    parsed: GetResourceResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetResourceResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetRoleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetRoleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetRoleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetRoleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""
    parsed: GetRoleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetRoleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetRoleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetRoleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetStartProcessFormResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetStartProcessFormResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetStartProcessFormResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetStartProcessFormResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetStartProcessFormResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetStartProcessFormResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""
    parsed: GetStartProcessFormResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetStartProcessFormResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStartProcessFormUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetStartProcessFormResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetStartProcessFormResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetStatusServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The cluster is DOWN and does not have any partition with a healthy leader."""
    parsed: None

    def __init__(self, *, status_code: int, content: bytes, parsed: None):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetTenantClusterVariableResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantClusterVariableResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetTenantClusterVariableResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantClusterVariableResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetTenantClusterVariableResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantClusterVariableResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Cluster variable not found"""
    parsed: GetTenantClusterVariableResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantClusterVariableResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantClusterVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetTenantClusterVariableResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantClusterVariableResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Tenant not found."""
    parsed: GetTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTenantUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetTenantResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTenantResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTopologyInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetTopologyResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTopologyResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetTopologyUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetTopologyResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetTopologyResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUsageMetricsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetUsageMetricsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUsageMetricsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUsageMetricsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetUsageMetricsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUsageMetricsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUsageMetricsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetUsageMetricsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUsageMetricsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUsageMetricsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetUsageMetricsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUsageMetricsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetUserResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetUserResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user with the given username was not found."""
    parsed: GetUserResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetUserTaskResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetUserTaskResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetUserTaskFormResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskFormResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetUserTaskFormResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskFormResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetUserTaskFormResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskFormResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""
    parsed: GetUserTaskFormResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskFormResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskFormUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetUserTaskFormResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskFormResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetUserTaskResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""
    parsed: GetUserTaskResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserTaskUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetUserTaskResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserTaskResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetUserUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetUserResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetUserResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: GetVariableResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: GetVariableResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: GetVariableResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: GetVariableResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: GetVariableResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: GetVariableResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""
    parsed: GetVariableResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: GetVariableResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class GetVariableUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: GetVariableResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: GetVariableResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: MigrateProcessInstanceResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: MigrateProcessInstanceResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceConflict(ApiError):
    """Raised when the server returns HTTP 409. The process instance migration failed. More details are provided in the response body."""
    parsed: MigrateProcessInstanceResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: MigrateProcessInstanceResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: MigrateProcessInstanceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: MigrateProcessInstanceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""
    parsed: MigrateProcessInstanceResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: MigrateProcessInstanceResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: MigrateProcessInstanceResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: MigrateProcessInstanceResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstancesBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""
    parsed: MigrateProcessInstancesBatchOperationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: MigrateProcessInstancesBatchOperationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstancesBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: MigrateProcessInstancesBatchOperationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: MigrateProcessInstancesBatchOperationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstancesBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: MigrateProcessInstancesBatchOperationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: MigrateProcessInstancesBatchOperationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class MigrateProcessInstancesBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: MigrateProcessInstancesBatchOperationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: MigrateProcessInstancesBatchOperationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstanceBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: ModifyProcessInstanceResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: ModifyProcessInstanceResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstanceInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ModifyProcessInstanceResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ModifyProcessInstanceResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstanceNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""
    parsed: ModifyProcessInstanceResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: ModifyProcessInstanceResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstanceServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: ModifyProcessInstanceResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: ModifyProcessInstanceResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstancesBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""
    parsed: ModifyProcessInstancesBatchOperationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: ModifyProcessInstancesBatchOperationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstancesBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: ModifyProcessInstancesBatchOperationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: ModifyProcessInstancesBatchOperationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstancesBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ModifyProcessInstancesBatchOperationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ModifyProcessInstancesBatchOperationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ModifyProcessInstancesBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: ModifyProcessInstancesBatchOperationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: ModifyProcessInstancesBatchOperationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PinClockBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: PinClockResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: PinClockResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PinClockInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: PinClockResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: PinClockResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PinClockServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: PinClockResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: PinClockResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PublishMessageBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: PublishMessageResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: PublishMessageResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PublishMessageInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: PublishMessageResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: PublishMessageResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class PublishMessageServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: PublishMessageResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: PublishMessageResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResetClockInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ResetClockResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ResetClockResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResetClockServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: ResetClockResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: ResetClockResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: ResolveIncidentResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveIncidentResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ResolveIncidentResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveIncidentResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentNotFound(ApiError):
    """Raised when the server returns HTTP 404. The incident with the incidentKey is not found."""
    parsed: ResolveIncidentResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveIncidentResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: ResolveIncidentResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveIncidentResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentsBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The process instance batch operation failed. More details are provided in the response body."""
    parsed: ResolveIncidentsBatchOperationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveIncidentsBatchOperationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentsBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: ResolveIncidentsBatchOperationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveIncidentsBatchOperationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentsBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ResolveIncidentsBatchOperationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveIncidentsBatchOperationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveIncidentsBatchOperationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: ResolveIncidentsBatchOperationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveIncidentsBatchOperationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: ResolveProcessInstanceIncidentsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveProcessInstanceIncidentsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ResolveProcessInstanceIncidentsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveProcessInstanceIncidentsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance is not found."""
    parsed: ResolveProcessInstanceIncidentsResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveProcessInstanceIncidentsResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: ResolveProcessInstanceIncidentsResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveProcessInstanceIncidentsResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResolveProcessInstanceIncidentsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: ResolveProcessInstanceIncidentsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: ResolveProcessInstanceIncidentsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: ResumeBatchOperationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: ResumeBatchOperationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: ResumeBatchOperationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: ResumeBatchOperationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ResumeBatchOperationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ResumeBatchOperationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The batch operation was not found."""
    parsed: ResumeBatchOperationResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: ResumeBatchOperationResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ResumeBatchOperationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: ResumeBatchOperationResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: ResumeBatchOperationResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuditLogsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchAuditLogsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchAuditLogsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuditLogsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchAuditLogsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchAuditLogsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuditLogsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: Any

    def __init__(self, *, status_code: int, content: bytes, parsed: Any):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuditLogsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchAuditLogsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchAuditLogsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuthorizationsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchAuthorizationsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchAuthorizationsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuthorizationsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchAuthorizationsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchAuthorizationsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuthorizationsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchAuthorizationsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchAuthorizationsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchAuthorizationsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchAuthorizationsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchAuthorizationsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchBatchOperationItemsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchBatchOperationItemsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchBatchOperationItemsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchBatchOperationItemsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchBatchOperationItemsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchBatchOperationItemsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchBatchOperationsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchBatchOperationsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchBatchOperationsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchBatchOperationsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchBatchOperationsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchBatchOperationsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchClientsForGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchClientsForGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchClientsForGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""
    parsed: SearchClientsForGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchClientsForGroupResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForGroupResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchClientsForRoleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForRoleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchClientsForRoleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForRoleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchClientsForRoleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForRoleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""
    parsed: SearchClientsForRoleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForRoleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClientsForRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchClientsForRoleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClientsForRoleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClusterVariablesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchClusterVariablesResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClusterVariablesResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClusterVariablesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchClusterVariablesResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClusterVariablesResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClusterVariablesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchClusterVariablesResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClusterVariablesResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchClusterVariablesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchClusterVariablesResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchClusterVariablesResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchCorrelatedMessageSubscriptionsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchCorrelatedMessageSubscriptionsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchCorrelatedMessageSubscriptionsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchCorrelatedMessageSubscriptionsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchCorrelatedMessageSubscriptionsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchCorrelatedMessageSubscriptionsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchCorrelatedMessageSubscriptionsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchCorrelatedMessageSubscriptionsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchCorrelatedMessageSubscriptionsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchCorrelatedMessageSubscriptionsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchCorrelatedMessageSubscriptionsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchCorrelatedMessageSubscriptionsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionDefinitionsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchDecisionDefinitionsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionDefinitionsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionDefinitionsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchDecisionDefinitionsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionDefinitionsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionDefinitionsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchDecisionDefinitionsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionDefinitionsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionDefinitionsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchDecisionDefinitionsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionDefinitionsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionInstancesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchDecisionInstancesResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionInstancesResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionInstancesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchDecisionInstancesResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionInstancesResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionInstancesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchDecisionInstancesResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionInstancesResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionInstancesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchDecisionInstancesResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionInstancesResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionRequirementsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchDecisionRequirementsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionRequirementsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionRequirementsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchDecisionRequirementsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionRequirementsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionRequirementsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchDecisionRequirementsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionRequirementsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchDecisionRequirementsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchDecisionRequirementsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchDecisionRequirementsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchElementInstanceIncidentsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchElementInstanceIncidentsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchElementInstanceIncidentsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchElementInstanceIncidentsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchElementInstanceIncidentsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchElementInstanceIncidentsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The element instance with the given key was not found."""
    parsed: SearchElementInstanceIncidentsResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchElementInstanceIncidentsResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstanceIncidentsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchElementInstanceIncidentsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchElementInstanceIncidentsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstancesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchElementInstancesResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchElementInstancesResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstancesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchElementInstancesResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchElementInstancesResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstancesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchElementInstancesResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchElementInstancesResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchElementInstancesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchElementInstancesResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchElementInstancesResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchGroupsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchGroupsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchGroupsForRoleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchGroupsForRoleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchGroupsForRoleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchGroupsForRoleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchGroupsForRoleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchGroupsForRoleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""
    parsed: SearchGroupsForRoleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchGroupsForRoleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchGroupsForRoleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchGroupsForRoleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchGroupsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchGroupsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: Any

    def __init__(self, *, status_code: int, content: bytes, parsed: Any):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchGroupsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchGroupsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchGroupsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchIncidentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchIncidentsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchIncidentsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchIncidentsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchIncidentsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchIncidentsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchIncidentsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchIncidentsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchIncidentsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchIncidentsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchIncidentsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchIncidentsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchJobsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchJobsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchJobsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchJobsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchJobsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchJobsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchJobsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchJobsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchJobsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchJobsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchJobsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchJobsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchMappingRuleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRuleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchMappingRuleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRuleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchMappingRuleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRuleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRuleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchMappingRuleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRuleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchMappingRulesForGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchMappingRulesForGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchMappingRulesForGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""
    parsed: SearchMappingRulesForGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchMappingRulesForGroupResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForGroupResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchMappingRulesForRoleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForRoleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchMappingRulesForRoleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForRoleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchMappingRulesForRoleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForRoleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""
    parsed: SearchMappingRulesForRoleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForRoleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMappingRulesForRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchMappingRulesForRoleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMappingRulesForRoleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMessageSubscriptionsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchMessageSubscriptionsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMessageSubscriptionsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMessageSubscriptionsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchMessageSubscriptionsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMessageSubscriptionsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMessageSubscriptionsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchMessageSubscriptionsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMessageSubscriptionsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchMessageSubscriptionsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchMessageSubscriptionsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchMessageSubscriptionsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessDefinitionsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchProcessDefinitionsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessDefinitionsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessDefinitionsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchProcessDefinitionsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessDefinitionsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessDefinitionsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchProcessDefinitionsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessDefinitionsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessDefinitionsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchProcessDefinitionsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessDefinitionsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchProcessInstanceIncidentsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessInstanceIncidentsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchProcessInstanceIncidentsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessInstanceIncidentsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchProcessInstanceIncidentsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessInstanceIncidentsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsNotFound(ApiError):
    """Raised when the server returns HTTP 404. The process instance with the given key was not found."""
    parsed: SearchProcessInstanceIncidentsResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessInstanceIncidentsResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstanceIncidentsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchProcessInstanceIncidentsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessInstanceIncidentsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstancesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchProcessInstancesResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessInstancesResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstancesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchProcessInstancesResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessInstancesResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstancesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchProcessInstancesResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessInstancesResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchProcessInstancesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchProcessInstancesResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchProcessInstancesResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchRolesResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchRolesResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchRolesForGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchRolesForGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchRolesForGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchRolesForGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchRolesForGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchRolesForGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""
    parsed: SearchRolesForGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchRolesForGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchRolesForGroupResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchRolesForGroupResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchRolesResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchRolesResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: Any

    def __init__(self, *, status_code: int, content: bytes, parsed: Any):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchRolesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchRolesResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchRolesResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchTenantsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchTenantsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchTenantsResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchTenantsResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchTenantsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchTenantsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found"""
    parsed: Any

    def __init__(self, *, status_code: int, content: bytes, parsed: Any):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchTenantsUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchTenantsResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchTenantsResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTaskAuditLogsBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchUserTaskAuditLogsResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUserTaskAuditLogsResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTaskAuditLogsInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchUserTaskAuditLogsResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUserTaskAuditLogsResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTaskVariablesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchUserTaskVariablesResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUserTaskVariablesResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTaskVariablesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchUserTaskVariablesResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUserTaskVariablesResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTasksBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchUserTasksResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUserTasksResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTasksForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchUserTasksResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUserTasksResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTasksInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchUserTasksResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUserTasksResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUserTasksUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchUserTasksResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUserTasksResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchUsersResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchUsersForGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchUsersForGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchUsersForGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""
    parsed: SearchUsersForGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchUsersForGroupResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForGroupResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchUsersForRoleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForRoleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchUsersForRoleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForRoleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchUsersForRoleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForRoleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the given ID was not found."""
    parsed: SearchUsersForRoleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForRoleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchUsersForRoleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersForRoleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchUsersResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchUsersResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchUsersUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchUsersResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchUsersResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchVariablesBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SearchVariablesResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchVariablesResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchVariablesForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SearchVariablesResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchVariablesResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchVariablesInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SearchVariablesResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchVariablesResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SearchVariablesUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: SearchVariablesResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: SearchVariablesResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: SuspendBatchOperationResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: SuspendBatchOperationResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: SuspendBatchOperationResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: SuspendBatchOperationResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: SuspendBatchOperationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: SuspendBatchOperationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The batch operation was not found."""
    parsed: SuspendBatchOperationResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: SuspendBatchOperationResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class SuspendBatchOperationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: SuspendBatchOperationResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: SuspendBatchOperationResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: ThrowJobErrorResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: ThrowJobErrorResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorConflict(ApiError):
    """Raised when the server returns HTTP 409. The job with the given key is in the wrong state currently. More details are provided in the response body."""
    parsed: ThrowJobErrorResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: ThrowJobErrorResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: ThrowJobErrorResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: ThrowJobErrorResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorNotFound(ApiError):
    """Raised when the server returns HTTP 404. The job with the given key was not found or is not activated."""
    parsed: ThrowJobErrorResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: ThrowJobErrorResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class ThrowJobErrorServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: ThrowJobErrorResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: ThrowJobErrorResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignClientFromGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignClientFromGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignClientFromGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found, or the client is not assigned to this group."""
    parsed: UnassignClientFromGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignClientFromGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignClientFromTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignClientFromTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignClientFromTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. The tenant does not exist or the client was not assigned to it."""
    parsed: UnassignClientFromTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignClientFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignClientFromTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignClientFromTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignGroupFromTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignGroupFromTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignGroupFromTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignGroupFromTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignGroupFromTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignGroupFromTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or group was not found."""
    parsed: UnassignGroupFromTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignGroupFromTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignGroupFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignGroupFromTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignGroupFromTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignMappingRuleFromGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignMappingRuleFromGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignMappingRuleFromGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group or mapping rule with the given ID was not found, or the mapping rule is not assigned to this group."""
    parsed: UnassignMappingRuleFromGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignMappingRuleFromGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignMappingRuleFromTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignMappingRuleFromTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignMappingRuleFromTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or mapping rule was not found."""
    parsed: UnassignMappingRuleFromTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignMappingRuleFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignMappingRuleFromTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignMappingRuleFromTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignRoleFromClientResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromClientResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignRoleFromClientResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromClientResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignRoleFromClientResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromClientResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or client with the given ID or username was not found."""
    parsed: UnassignRoleFromClientResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromClientResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromClientServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignRoleFromClientResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromClientResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignRoleFromGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignRoleFromGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignRoleFromGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or group with the given ID was not found."""
    parsed: UnassignRoleFromGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignRoleFromGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignRoleFromMappingRuleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromMappingRuleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignRoleFromMappingRuleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromMappingRuleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignRoleFromMappingRuleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromMappingRuleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or mapping rule with the given ID was not found."""
    parsed: UnassignRoleFromMappingRuleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromMappingRuleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromMappingRuleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignRoleFromMappingRuleResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromMappingRuleResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignRoleFromTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignRoleFromTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignRoleFromTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or role was not found."""
    parsed: UnassignRoleFromTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignRoleFromTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignRoleFromUserResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromUserResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignRoleFromUserResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromUserResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignRoleFromUserResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromUserResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role or user with the given ID or username was not found."""
    parsed: UnassignRoleFromUserResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromUserResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignRoleFromUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignRoleFromUserResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignRoleFromUserResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignUserFromGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignUserFromGroupResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromGroupResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignUserFromGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group or user with the given ID was not found, or the user is not assigned to this group."""
    parsed: UnassignUserFromGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignUserFromGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignUserFromTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UnassignUserFromTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignUserFromTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant or user was not found."""
    parsed: UnassignUserFromTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserFromTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignUserFromTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserFromTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UnassignUserTaskResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserTaskResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskConflict(ApiError):
    """Raised when the server returns HTTP 409. The user task with the given key is in the wrong state currently. More details are provided in the response body."""
    parsed: UnassignUserTaskResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserTaskResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UnassignUserTaskResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserTaskResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""
    parsed: UnassignUserTaskResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserTaskResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UnassignUserTaskServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UnassignUserTaskResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UnassignUserTaskResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateAuthorizationInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UpdateAuthorizationResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateAuthorizationResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateAuthorizationNotFound(ApiError):
    """Raised when the server returns HTTP 404. The authorization with the authorizationKey was not found."""
    parsed: UpdateAuthorizationResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateAuthorizationResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateAuthorizationServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UpdateAuthorizationResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateAuthorizationResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateAuthorizationUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: UpdateAuthorizationResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateAuthorizationResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UpdateGroupResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateGroupResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UpdateGroupResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateGroupResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupNotFound(ApiError):
    """Raised when the server returns HTTP 404. The group with the given ID was not found."""
    parsed: UpdateGroupResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateGroupResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UpdateGroupResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateGroupResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateGroupUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: UpdateGroupResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateGroupResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UpdateJobResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateJobResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobConflict(ApiError):
    """Raised when the server returns HTTP 409. The job with the given key is in the wrong state currently. More details are provided in the response body."""
    parsed: UpdateJobResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateJobResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UpdateJobResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateJobResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobNotFound(ApiError):
    """Raised when the server returns HTTP 404. The job with the jobKey is not found."""
    parsed: UpdateJobResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateJobResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateJobServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UpdateJobResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateJobResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UpdateMappingRuleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateMappingRuleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleForbidden(ApiError):
    """Raised when the server returns HTTP 403. The request to update a mapping rule was denied. More details are provided in the response body."""
    parsed: UpdateMappingRuleResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateMappingRuleResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UpdateMappingRuleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateMappingRuleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The request to update a mapping rule was denied."""
    parsed: UpdateMappingRuleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateMappingRuleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateMappingRuleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UpdateMappingRuleResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateMappingRuleResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UpdateRoleResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateRoleResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UpdateRoleResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateRoleResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleNotFound(ApiError):
    """Raised when the server returns HTTP 404. The role with the ID is not found."""
    parsed: UpdateRoleResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateRoleResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UpdateRoleResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateRoleResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateRoleUnauthorized(ApiError):
    """Raised when the server returns HTTP 401. The request lacks valid authentication credentials."""
    parsed: UpdateRoleResponse401

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateRoleResponse401):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UpdateTenantResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateTenantResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UpdateTenantResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateTenantResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UpdateTenantResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateTenantResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantNotFound(ApiError):
    """Raised when the server returns HTTP 404. Not found. The tenant was not found."""
    parsed: UpdateTenantResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateTenantResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateTenantServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UpdateTenantResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateTenantResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UpdateUserResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserForbidden(ApiError):
    """Raised when the server returns HTTP 403. Forbidden. The request is not allowed."""
    parsed: UpdateUserResponse403

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserResponse403):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UpdateUserResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user was not found."""
    parsed: UpdateUserResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UpdateUserResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskBadRequest(ApiError):
    """Raised when the server returns HTTP 400. The provided data is not valid."""
    parsed: UpdateUserTaskResponse400

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserTaskResponse400):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskConflict(ApiError):
    """Raised when the server returns HTTP 409. The user task with the given key is in the wrong state currently. More details are provided in the response body."""
    parsed: UpdateUserTaskResponse409

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserTaskResponse409):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskInternalServerError(ApiError):
    """Raised when the server returns HTTP 500. An internal error occurred while processing the request."""
    parsed: UpdateUserTaskResponse500

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserTaskResponse500):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskNotFound(ApiError):
    """Raised when the server returns HTTP 404. The user task with the given key was not found."""
    parsed: UpdateUserTaskResponse404

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserTaskResponse404):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


class UpdateUserTaskServiceUnavailable(ApiError):
    """Raised when the server returns HTTP 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure ."""
    parsed: UpdateUserTaskResponse503

    def __init__(self, *, status_code: int, content: bytes, parsed: UpdateUserTaskResponse503):
        super().__init__(status_code=status_code, content=content, parsed=parsed)


__all__ = ['ActivateAdHocSubProcessActivitiesBadRequest', 'ActivateAdHocSubProcessActivitiesForbidden', 'ActivateAdHocSubProcessActivitiesInternalServerError', 'ActivateAdHocSubProcessActivitiesNotFound', 'ActivateAdHocSubProcessActivitiesServiceUnavailable', 'ActivateAdHocSubProcessActivitiesUnauthorized', 'ActivateJobsBadRequest', 'ActivateJobsInternalServerError', 'ActivateJobsServiceUnavailable', 'ActivateJobsUnauthorized', 'ApiError', 'AssignClientToGroupBadRequest', 'AssignClientToGroupConflict', 'AssignClientToGroupForbidden', 'AssignClientToGroupInternalServerError', 'AssignClientToGroupNotFound', 'AssignClientToGroupServiceUnavailable', 'AssignClientToTenantBadRequest', 'AssignClientToTenantForbidden', 'AssignClientToTenantInternalServerError', 'AssignClientToTenantNotFound', 'AssignClientToTenantServiceUnavailable', 'AssignGroupToTenantBadRequest', 'AssignGroupToTenantForbidden', 'AssignGroupToTenantInternalServerError', 'AssignGroupToTenantNotFound', 'AssignGroupToTenantServiceUnavailable', 'AssignMappingRuleToGroupBadRequest', 'AssignMappingRuleToGroupConflict', 'AssignMappingRuleToGroupForbidden', 'AssignMappingRuleToGroupInternalServerError', 'AssignMappingRuleToGroupNotFound', 'AssignMappingRuleToGroupServiceUnavailable', 'AssignMappingRuleToTenantBadRequest', 'AssignMappingRuleToTenantForbidden', 'AssignMappingRuleToTenantInternalServerError', 'AssignMappingRuleToTenantNotFound', 'AssignMappingRuleToTenantServiceUnavailable', 'AssignRoleToClientBadRequest', 'AssignRoleToClientConflict', 'AssignRoleToClientForbidden', 'AssignRoleToClientInternalServerError', 'AssignRoleToClientNotFound', 'AssignRoleToClientServiceUnavailable', 'AssignRoleToGroupBadRequest', 'AssignRoleToGroupConflict', 'AssignRoleToGroupForbidden', 'AssignRoleToGroupInternalServerError', 'AssignRoleToGroupNotFound', 'AssignRoleToGroupServiceUnavailable', 'AssignRoleToMappingRuleBadRequest', 'AssignRoleToMappingRuleConflict', 'AssignRoleToMappingRuleForbidden', 'AssignRoleToMappingRuleInternalServerError', 'AssignRoleToMappingRuleNotFound', 'AssignRoleToMappingRuleServiceUnavailable', 'AssignRoleToTenantBadRequest', 'AssignRoleToTenantForbidden', 'AssignRoleToTenantInternalServerError', 'AssignRoleToTenantNotFound', 'AssignRoleToTenantServiceUnavailable', 'AssignRoleToUserBadRequest', 'AssignRoleToUserConflict', 'AssignRoleToUserForbidden', 'AssignRoleToUserInternalServerError', 'AssignRoleToUserNotFound', 'AssignRoleToUserServiceUnavailable', 'AssignUserTaskBadRequest', 'AssignUserTaskConflict', 'AssignUserTaskInternalServerError', 'AssignUserTaskNotFound', 'AssignUserTaskServiceUnavailable', 'AssignUserToGroupBadRequest', 'AssignUserToGroupConflict', 'AssignUserToGroupForbidden', 'AssignUserToGroupInternalServerError', 'AssignUserToGroupNotFound', 'AssignUserToGroupServiceUnavailable', 'AssignUserToTenantBadRequest', 'AssignUserToTenantForbidden', 'AssignUserToTenantInternalServerError', 'AssignUserToTenantNotFound', 'AssignUserToTenantServiceUnavailable', 'BroadcastSignalBadRequest', 'BroadcastSignalInternalServerError', 'BroadcastSignalNotFound', 'BroadcastSignalServiceUnavailable', 'CancelBatchOperationBadRequest', 'CancelBatchOperationForbidden', 'CancelBatchOperationInternalServerError', 'CancelBatchOperationNotFound', 'CancelProcessInstanceBadRequest', 'CancelProcessInstanceInternalServerError', 'CancelProcessInstanceNotFound', 'CancelProcessInstanceServiceUnavailable', 'CancelProcessInstancesBatchOperationBadRequest', 'CancelProcessInstancesBatchOperationForbidden', 'CancelProcessInstancesBatchOperationInternalServerError', 'CancelProcessInstancesBatchOperationUnauthorized', 'CompleteJobBadRequest', 'CompleteJobConflict', 'CompleteJobInternalServerError', 'CompleteJobNotFound', 'CompleteJobServiceUnavailable', 'CompleteUserTaskBadRequest', 'CompleteUserTaskConflict', 'CompleteUserTaskInternalServerError', 'CompleteUserTaskNotFound', 'CompleteUserTaskServiceUnavailable', 'CorrelateMessageBadRequest', 'CorrelateMessageForbidden', 'CorrelateMessageInternalServerError', 'CorrelateMessageNotFound', 'CorrelateMessageServiceUnavailable', 'CreateAdminUserBadRequest', 'CreateAdminUserForbidden', 'CreateAdminUserInternalServerError', 'CreateAdminUserServiceUnavailable', 'CreateAuthorizationBadRequest', 'CreateAuthorizationForbidden', 'CreateAuthorizationInternalServerError', 'CreateAuthorizationNotFound', 'CreateAuthorizationServiceUnavailable', 'CreateAuthorizationUnauthorized', 'CreateDeploymentBadRequest', 'CreateDeploymentServiceUnavailable', 'CreateDocumentBadRequest', 'CreateDocumentLinkBadRequest', 'CreateDocumentUnsupportedMediaType', 'CreateDocumentsBadRequest', 'CreateDocumentsUnsupportedMediaType', 'CreateElementInstanceVariablesBadRequest', 'CreateElementInstanceVariablesInternalServerError', 'CreateElementInstanceVariablesServiceUnavailable', 'CreateGlobalClusterVariableBadRequest', 'CreateGlobalClusterVariableForbidden', 'CreateGlobalClusterVariableInternalServerError', 'CreateGlobalClusterVariableUnauthorized', 'CreateGroupBadRequest', 'CreateGroupForbidden', 'CreateGroupInternalServerError', 'CreateGroupServiceUnavailable', 'CreateGroupUnauthorized', 'CreateMappingRuleBadRequest', 'CreateMappingRuleForbidden', 'CreateMappingRuleInternalServerError', 'CreateMappingRuleNotFound', 'CreateProcessInstanceBadRequest', 'CreateProcessInstanceGatewayTimeout', 'CreateProcessInstanceInternalServerError', 'CreateProcessInstanceServiceUnavailable', 'CreateRoleBadRequest', 'CreateRoleForbidden', 'CreateRoleInternalServerError', 'CreateRoleServiceUnavailable', 'CreateRoleUnauthorized', 'CreateTenantBadRequest', 'CreateTenantClusterVariableBadRequest', 'CreateTenantClusterVariableForbidden', 'CreateTenantClusterVariableInternalServerError', 'CreateTenantClusterVariableUnauthorized', 'CreateTenantConflict', 'CreateTenantForbidden', 'CreateTenantInternalServerError', 'CreateTenantNotFound', 'CreateTenantServiceUnavailable', 'CreateUserBadRequest', 'CreateUserConflict', 'CreateUserForbidden', 'CreateUserInternalServerError', 'CreateUserServiceUnavailable', 'CreateUserUnauthorized', 'DeleteAuthorizationInternalServerError', 'DeleteAuthorizationNotFound', 'DeleteAuthorizationServiceUnavailable', 'DeleteAuthorizationUnauthorized', 'DeleteDocumentInternalServerError', 'DeleteDocumentNotFound', 'DeleteGlobalClusterVariableBadRequest', 'DeleteGlobalClusterVariableForbidden', 'DeleteGlobalClusterVariableInternalServerError', 'DeleteGlobalClusterVariableNotFound', 'DeleteGlobalClusterVariableUnauthorized', 'DeleteGroupInternalServerError', 'DeleteGroupNotFound', 'DeleteGroupServiceUnavailable', 'DeleteGroupUnauthorized', 'DeleteMappingRuleInternalServerError', 'DeleteMappingRuleNotFound', 'DeleteMappingRuleServiceUnavailable', 'DeleteMappingRuleUnauthorized', 'DeleteProcessInstanceConflict', 'DeleteProcessInstanceForbidden', 'DeleteProcessInstanceInternalServerError', 'DeleteProcessInstanceNotFound', 'DeleteProcessInstanceServiceUnavailable', 'DeleteProcessInstanceUnauthorized', 'DeleteProcessInstancesBatchOperationBadRequest', 'DeleteProcessInstancesBatchOperationForbidden', 'DeleteProcessInstancesBatchOperationInternalServerError', 'DeleteProcessInstancesBatchOperationUnauthorized', 'DeleteResourceBadRequest', 'DeleteResourceInternalServerError', 'DeleteResourceNotFound', 'DeleteResourceServiceUnavailable', 'DeleteRoleInternalServerError', 'DeleteRoleNotFound', 'DeleteRoleServiceUnavailable', 'DeleteRoleUnauthorized', 'DeleteTenantBadRequest', 'DeleteTenantClusterVariableBadRequest', 'DeleteTenantClusterVariableForbidden', 'DeleteTenantClusterVariableInternalServerError', 'DeleteTenantClusterVariableNotFound', 'DeleteTenantClusterVariableUnauthorized', 'DeleteTenantForbidden', 'DeleteTenantInternalServerError', 'DeleteTenantNotFound', 'DeleteTenantServiceUnavailable', 'DeleteUserBadRequest', 'DeleteUserInternalServerError', 'DeleteUserNotFound', 'DeleteUserServiceUnavailable', 'EvaluateConditionalsBadRequest', 'EvaluateConditionalsForbidden', 'EvaluateConditionalsInternalServerError', 'EvaluateConditionalsNotFound', 'EvaluateConditionalsServiceUnavailable', 'EvaluateDecisionBadRequest', 'EvaluateDecisionInternalServerError', 'EvaluateDecisionNotFound', 'EvaluateDecisionServiceUnavailable', 'EvaluateExpressionBadRequest', 'EvaluateExpressionForbidden', 'EvaluateExpressionInternalServerError', 'EvaluateExpressionUnauthorized', 'FailJobBadRequest', 'FailJobConflict', 'FailJobInternalServerError', 'FailJobNotFound', 'FailJobServiceUnavailable', 'GetAuditLogForbidden', 'GetAuditLogInternalServerError', 'GetAuditLogNotFound', 'GetAuditLogUnauthorized', 'GetAuthenticationForbidden', 'GetAuthenticationInternalServerError', 'GetAuthenticationUnauthorized', 'GetAuthorizationForbidden', 'GetAuthorizationInternalServerError', 'GetAuthorizationNotFound', 'GetAuthorizationUnauthorized', 'GetBatchOperationBadRequest', 'GetBatchOperationInternalServerError', 'GetBatchOperationNotFound', 'GetDecisionDefinitionBadRequest', 'GetDecisionDefinitionForbidden', 'GetDecisionDefinitionInternalServerError', 'GetDecisionDefinitionNotFound', 'GetDecisionDefinitionUnauthorized', 'GetDecisionDefinitionXmlBadRequest', 'GetDecisionDefinitionXmlForbidden', 'GetDecisionDefinitionXmlInternalServerError', 'GetDecisionDefinitionXmlNotFound', 'GetDecisionDefinitionXmlUnauthorized', 'GetDecisionInstanceBadRequest', 'GetDecisionInstanceForbidden', 'GetDecisionInstanceInternalServerError', 'GetDecisionInstanceNotFound', 'GetDecisionInstanceUnauthorized', 'GetDecisionRequirementsBadRequest', 'GetDecisionRequirementsForbidden', 'GetDecisionRequirementsInternalServerError', 'GetDecisionRequirementsNotFound', 'GetDecisionRequirementsUnauthorized', 'GetDecisionRequirementsXmlBadRequest', 'GetDecisionRequirementsXmlForbidden', 'GetDecisionRequirementsXmlInternalServerError', 'GetDecisionRequirementsXmlNotFound', 'GetDecisionRequirementsXmlUnauthorized', 'GetDocumentInternalServerError', 'GetDocumentNotFound', 'GetElementInstanceBadRequest', 'GetElementInstanceForbidden', 'GetElementInstanceInternalServerError', 'GetElementInstanceNotFound', 'GetElementInstanceUnauthorized', 'GetGlobalClusterVariableBadRequest', 'GetGlobalClusterVariableForbidden', 'GetGlobalClusterVariableInternalServerError', 'GetGlobalClusterVariableNotFound', 'GetGlobalClusterVariableUnauthorized', 'GetGroupForbidden', 'GetGroupInternalServerError', 'GetGroupNotFound', 'GetGroupUnauthorized', 'GetIncidentBadRequest', 'GetIncidentForbidden', 'GetIncidentInternalServerError', 'GetIncidentNotFound', 'GetIncidentUnauthorized', 'GetLicenseInternalServerError', 'GetMappingRuleInternalServerError', 'GetMappingRuleNotFound', 'GetMappingRuleUnauthorized', 'GetProcessDefinitionBadRequest', 'GetProcessDefinitionForbidden', 'GetProcessDefinitionInstanceStatisticsBadRequest', 'GetProcessDefinitionInstanceStatisticsForbidden', 'GetProcessDefinitionInstanceStatisticsInternalServerError', 'GetProcessDefinitionInstanceStatisticsUnauthorized', 'GetProcessDefinitionInstanceVersionStatisticsBadRequest', 'GetProcessDefinitionInstanceVersionStatisticsForbidden', 'GetProcessDefinitionInstanceVersionStatisticsInternalServerError', 'GetProcessDefinitionInstanceVersionStatisticsUnauthorized', 'GetProcessDefinitionInternalServerError', 'GetProcessDefinitionMessageSubscriptionStatisticsBadRequest', 'GetProcessDefinitionMessageSubscriptionStatisticsForbidden', 'GetProcessDefinitionMessageSubscriptionStatisticsInternalServerError', 'GetProcessDefinitionMessageSubscriptionStatisticsUnauthorized', 'GetProcessDefinitionNotFound', 'GetProcessDefinitionStatisticsBadRequest', 'GetProcessDefinitionStatisticsForbidden', 'GetProcessDefinitionStatisticsInternalServerError', 'GetProcessDefinitionStatisticsUnauthorized', 'GetProcessDefinitionUnauthorized', 'GetProcessDefinitionXmlBadRequest', 'GetProcessDefinitionXmlForbidden', 'GetProcessDefinitionXmlInternalServerError', 'GetProcessDefinitionXmlNotFound', 'GetProcessDefinitionXmlUnauthorized', 'GetProcessInstanceBadRequest', 'GetProcessInstanceCallHierarchyBadRequest', 'GetProcessInstanceCallHierarchyForbidden', 'GetProcessInstanceCallHierarchyInternalServerError', 'GetProcessInstanceCallHierarchyNotFound', 'GetProcessInstanceCallHierarchyUnauthorized', 'GetProcessInstanceForbidden', 'GetProcessInstanceInternalServerError', 'GetProcessInstanceNotFound', 'GetProcessInstanceSequenceFlowsBadRequest', 'GetProcessInstanceSequenceFlowsForbidden', 'GetProcessInstanceSequenceFlowsInternalServerError', 'GetProcessInstanceSequenceFlowsUnauthorized', 'GetProcessInstanceStatisticsBadRequest', 'GetProcessInstanceStatisticsByDefinitionBadRequest', 'GetProcessInstanceStatisticsByDefinitionForbidden', 'GetProcessInstanceStatisticsByDefinitionInternalServerError', 'GetProcessInstanceStatisticsByDefinitionUnauthorized', 'GetProcessInstanceStatisticsByErrorBadRequest', 'GetProcessInstanceStatisticsByErrorForbidden', 'GetProcessInstanceStatisticsByErrorInternalServerError', 'GetProcessInstanceStatisticsByErrorUnauthorized', 'GetProcessInstanceStatisticsForbidden', 'GetProcessInstanceStatisticsInternalServerError', 'GetProcessInstanceStatisticsUnauthorized', 'GetProcessInstanceUnauthorized', 'GetResourceContentInternalServerError', 'GetResourceContentNotFound', 'GetResourceInternalServerError', 'GetResourceNotFound', 'GetRoleForbidden', 'GetRoleInternalServerError', 'GetRoleNotFound', 'GetRoleUnauthorized', 'GetStartProcessFormBadRequest', 'GetStartProcessFormForbidden', 'GetStartProcessFormInternalServerError', 'GetStartProcessFormNotFound', 'GetStartProcessFormUnauthorized', 'GetStatusServiceUnavailable', 'GetTenantBadRequest', 'GetTenantClusterVariableBadRequest', 'GetTenantClusterVariableForbidden', 'GetTenantClusterVariableInternalServerError', 'GetTenantClusterVariableNotFound', 'GetTenantClusterVariableUnauthorized', 'GetTenantForbidden', 'GetTenantInternalServerError', 'GetTenantNotFound', 'GetTenantUnauthorized', 'GetTopologyInternalServerError', 'GetTopologyUnauthorized', 'GetUsageMetricsBadRequest', 'GetUsageMetricsForbidden', 'GetUsageMetricsInternalServerError', 'GetUsageMetricsUnauthorized', 'GetUserForbidden', 'GetUserInternalServerError', 'GetUserNotFound', 'GetUserTaskBadRequest', 'GetUserTaskForbidden', 'GetUserTaskFormBadRequest', 'GetUserTaskFormForbidden', 'GetUserTaskFormInternalServerError', 'GetUserTaskFormNotFound', 'GetUserTaskFormUnauthorized', 'GetUserTaskInternalServerError', 'GetUserTaskNotFound', 'GetUserTaskUnauthorized', 'GetUserUnauthorized', 'GetVariableBadRequest', 'GetVariableForbidden', 'GetVariableInternalServerError', 'GetVariableNotFound', 'GetVariableUnauthorized', 'MigrateProcessInstanceBadRequest', 'MigrateProcessInstanceConflict', 'MigrateProcessInstanceInternalServerError', 'MigrateProcessInstanceNotFound', 'MigrateProcessInstanceServiceUnavailable', 'MigrateProcessInstancesBatchOperationBadRequest', 'MigrateProcessInstancesBatchOperationForbidden', 'MigrateProcessInstancesBatchOperationInternalServerError', 'MigrateProcessInstancesBatchOperationUnauthorized', 'ModifyProcessInstanceBadRequest', 'ModifyProcessInstanceInternalServerError', 'ModifyProcessInstanceNotFound', 'ModifyProcessInstanceServiceUnavailable', 'ModifyProcessInstancesBatchOperationBadRequest', 'ModifyProcessInstancesBatchOperationForbidden', 'ModifyProcessInstancesBatchOperationInternalServerError', 'ModifyProcessInstancesBatchOperationUnauthorized', 'PinClockBadRequest', 'PinClockInternalServerError', 'PinClockServiceUnavailable', 'PublishMessageBadRequest', 'PublishMessageInternalServerError', 'PublishMessageServiceUnavailable', 'ResetClockInternalServerError', 'ResetClockServiceUnavailable', 'ResolveIncidentBadRequest', 'ResolveIncidentInternalServerError', 'ResolveIncidentNotFound', 'ResolveIncidentServiceUnavailable', 'ResolveIncidentsBatchOperationBadRequest', 'ResolveIncidentsBatchOperationForbidden', 'ResolveIncidentsBatchOperationInternalServerError', 'ResolveIncidentsBatchOperationUnauthorized', 'ResolveProcessInstanceIncidentsBadRequest', 'ResolveProcessInstanceIncidentsInternalServerError', 'ResolveProcessInstanceIncidentsNotFound', 'ResolveProcessInstanceIncidentsServiceUnavailable', 'ResolveProcessInstanceIncidentsUnauthorized', 'ResumeBatchOperationBadRequest', 'ResumeBatchOperationForbidden', 'ResumeBatchOperationInternalServerError', 'ResumeBatchOperationNotFound', 'ResumeBatchOperationServiceUnavailable', 'SearchAuditLogsBadRequest', 'SearchAuditLogsForbidden', 'SearchAuditLogsInternalServerError', 'SearchAuditLogsUnauthorized', 'SearchAuthorizationsBadRequest', 'SearchAuthorizationsForbidden', 'SearchAuthorizationsInternalServerError', 'SearchAuthorizationsUnauthorized', 'SearchBatchOperationItemsBadRequest', 'SearchBatchOperationItemsInternalServerError', 'SearchBatchOperationsBadRequest', 'SearchBatchOperationsInternalServerError', 'SearchClientsForGroupBadRequest', 'SearchClientsForGroupForbidden', 'SearchClientsForGroupInternalServerError', 'SearchClientsForGroupNotFound', 'SearchClientsForGroupUnauthorized', 'SearchClientsForRoleBadRequest', 'SearchClientsForRoleForbidden', 'SearchClientsForRoleInternalServerError', 'SearchClientsForRoleNotFound', 'SearchClientsForRoleUnauthorized', 'SearchClusterVariablesBadRequest', 'SearchClusterVariablesForbidden', 'SearchClusterVariablesInternalServerError', 'SearchClusterVariablesUnauthorized', 'SearchCorrelatedMessageSubscriptionsBadRequest', 'SearchCorrelatedMessageSubscriptionsForbidden', 'SearchCorrelatedMessageSubscriptionsInternalServerError', 'SearchCorrelatedMessageSubscriptionsUnauthorized', 'SearchDecisionDefinitionsBadRequest', 'SearchDecisionDefinitionsForbidden', 'SearchDecisionDefinitionsInternalServerError', 'SearchDecisionDefinitionsUnauthorized', 'SearchDecisionInstancesBadRequest', 'SearchDecisionInstancesForbidden', 'SearchDecisionInstancesInternalServerError', 'SearchDecisionInstancesUnauthorized', 'SearchDecisionRequirementsBadRequest', 'SearchDecisionRequirementsForbidden', 'SearchDecisionRequirementsInternalServerError', 'SearchDecisionRequirementsUnauthorized', 'SearchElementInstanceIncidentsBadRequest', 'SearchElementInstanceIncidentsForbidden', 'SearchElementInstanceIncidentsInternalServerError', 'SearchElementInstanceIncidentsNotFound', 'SearchElementInstanceIncidentsUnauthorized', 'SearchElementInstancesBadRequest', 'SearchElementInstancesForbidden', 'SearchElementInstancesInternalServerError', 'SearchElementInstancesUnauthorized', 'SearchGroupsBadRequest', 'SearchGroupsForRoleBadRequest', 'SearchGroupsForRoleForbidden', 'SearchGroupsForRoleInternalServerError', 'SearchGroupsForRoleNotFound', 'SearchGroupsForRoleUnauthorized', 'SearchGroupsForbidden', 'SearchGroupsInternalServerError', 'SearchGroupsUnauthorized', 'SearchIncidentsBadRequest', 'SearchIncidentsForbidden', 'SearchIncidentsInternalServerError', 'SearchIncidentsUnauthorized', 'SearchJobsBadRequest', 'SearchJobsForbidden', 'SearchJobsInternalServerError', 'SearchJobsUnauthorized', 'SearchMappingRuleBadRequest', 'SearchMappingRuleForbidden', 'SearchMappingRuleInternalServerError', 'SearchMappingRuleUnauthorized', 'SearchMappingRulesForGroupBadRequest', 'SearchMappingRulesForGroupForbidden', 'SearchMappingRulesForGroupInternalServerError', 'SearchMappingRulesForGroupNotFound', 'SearchMappingRulesForGroupUnauthorized', 'SearchMappingRulesForRoleBadRequest', 'SearchMappingRulesForRoleForbidden', 'SearchMappingRulesForRoleInternalServerError', 'SearchMappingRulesForRoleNotFound', 'SearchMappingRulesForRoleUnauthorized', 'SearchMessageSubscriptionsBadRequest', 'SearchMessageSubscriptionsForbidden', 'SearchMessageSubscriptionsInternalServerError', 'SearchMessageSubscriptionsUnauthorized', 'SearchProcessDefinitionsBadRequest', 'SearchProcessDefinitionsForbidden', 'SearchProcessDefinitionsInternalServerError', 'SearchProcessDefinitionsUnauthorized', 'SearchProcessInstanceIncidentsBadRequest', 'SearchProcessInstanceIncidentsForbidden', 'SearchProcessInstanceIncidentsInternalServerError', 'SearchProcessInstanceIncidentsNotFound', 'SearchProcessInstanceIncidentsUnauthorized', 'SearchProcessInstancesBadRequest', 'SearchProcessInstancesForbidden', 'SearchProcessInstancesInternalServerError', 'SearchProcessInstancesUnauthorized', 'SearchRolesBadRequest', 'SearchRolesForGroupBadRequest', 'SearchRolesForGroupForbidden', 'SearchRolesForGroupInternalServerError', 'SearchRolesForGroupNotFound', 'SearchRolesForGroupUnauthorized', 'SearchRolesForbidden', 'SearchRolesInternalServerError', 'SearchRolesUnauthorized', 'SearchTenantsBadRequest', 'SearchTenantsForbidden', 'SearchTenantsInternalServerError', 'SearchTenantsNotFound', 'SearchTenantsUnauthorized', 'SearchUserTaskAuditLogsBadRequest', 'SearchUserTaskAuditLogsInternalServerError', 'SearchUserTaskVariablesBadRequest', 'SearchUserTaskVariablesInternalServerError', 'SearchUserTasksBadRequest', 'SearchUserTasksForbidden', 'SearchUserTasksInternalServerError', 'SearchUserTasksUnauthorized', 'SearchUsersBadRequest', 'SearchUsersForGroupBadRequest', 'SearchUsersForGroupForbidden', 'SearchUsersForGroupInternalServerError', 'SearchUsersForGroupNotFound', 'SearchUsersForGroupUnauthorized', 'SearchUsersForRoleBadRequest', 'SearchUsersForRoleForbidden', 'SearchUsersForRoleInternalServerError', 'SearchUsersForRoleNotFound', 'SearchUsersForRoleUnauthorized', 'SearchUsersForbidden', 'SearchUsersInternalServerError', 'SearchUsersUnauthorized', 'SearchVariablesBadRequest', 'SearchVariablesForbidden', 'SearchVariablesInternalServerError', 'SearchVariablesUnauthorized', 'SuspendBatchOperationBadRequest', 'SuspendBatchOperationForbidden', 'SuspendBatchOperationInternalServerError', 'SuspendBatchOperationNotFound', 'SuspendBatchOperationServiceUnavailable', 'ThrowJobErrorBadRequest', 'ThrowJobErrorConflict', 'ThrowJobErrorInternalServerError', 'ThrowJobErrorNotFound', 'ThrowJobErrorServiceUnavailable', 'UnassignClientFromGroupBadRequest', 'UnassignClientFromGroupForbidden', 'UnassignClientFromGroupInternalServerError', 'UnassignClientFromGroupNotFound', 'UnassignClientFromGroupServiceUnavailable', 'UnassignClientFromTenantBadRequest', 'UnassignClientFromTenantForbidden', 'UnassignClientFromTenantInternalServerError', 'UnassignClientFromTenantNotFound', 'UnassignClientFromTenantServiceUnavailable', 'UnassignGroupFromTenantBadRequest', 'UnassignGroupFromTenantForbidden', 'UnassignGroupFromTenantInternalServerError', 'UnassignGroupFromTenantNotFound', 'UnassignGroupFromTenantServiceUnavailable', 'UnassignMappingRuleFromGroupBadRequest', 'UnassignMappingRuleFromGroupForbidden', 'UnassignMappingRuleFromGroupInternalServerError', 'UnassignMappingRuleFromGroupNotFound', 'UnassignMappingRuleFromGroupServiceUnavailable', 'UnassignMappingRuleFromTenantBadRequest', 'UnassignMappingRuleFromTenantForbidden', 'UnassignMappingRuleFromTenantInternalServerError', 'UnassignMappingRuleFromTenantNotFound', 'UnassignMappingRuleFromTenantServiceUnavailable', 'UnassignRoleFromClientBadRequest', 'UnassignRoleFromClientForbidden', 'UnassignRoleFromClientInternalServerError', 'UnassignRoleFromClientNotFound', 'UnassignRoleFromClientServiceUnavailable', 'UnassignRoleFromGroupBadRequest', 'UnassignRoleFromGroupForbidden', 'UnassignRoleFromGroupInternalServerError', 'UnassignRoleFromGroupNotFound', 'UnassignRoleFromGroupServiceUnavailable', 'UnassignRoleFromMappingRuleBadRequest', 'UnassignRoleFromMappingRuleForbidden', 'UnassignRoleFromMappingRuleInternalServerError', 'UnassignRoleFromMappingRuleNotFound', 'UnassignRoleFromMappingRuleServiceUnavailable', 'UnassignRoleFromTenantBadRequest', 'UnassignRoleFromTenantForbidden', 'UnassignRoleFromTenantInternalServerError', 'UnassignRoleFromTenantNotFound', 'UnassignRoleFromTenantServiceUnavailable', 'UnassignRoleFromUserBadRequest', 'UnassignRoleFromUserForbidden', 'UnassignRoleFromUserInternalServerError', 'UnassignRoleFromUserNotFound', 'UnassignRoleFromUserServiceUnavailable', 'UnassignUserFromGroupBadRequest', 'UnassignUserFromGroupForbidden', 'UnassignUserFromGroupInternalServerError', 'UnassignUserFromGroupNotFound', 'UnassignUserFromGroupServiceUnavailable', 'UnassignUserFromTenantBadRequest', 'UnassignUserFromTenantForbidden', 'UnassignUserFromTenantInternalServerError', 'UnassignUserFromTenantNotFound', 'UnassignUserFromTenantServiceUnavailable', 'UnassignUserTaskBadRequest', 'UnassignUserTaskConflict', 'UnassignUserTaskInternalServerError', 'UnassignUserTaskNotFound', 'UnassignUserTaskServiceUnavailable', 'UnexpectedStatus', 'UpdateAuthorizationInternalServerError', 'UpdateAuthorizationNotFound', 'UpdateAuthorizationServiceUnavailable', 'UpdateAuthorizationUnauthorized', 'UpdateGroupBadRequest', 'UpdateGroupInternalServerError', 'UpdateGroupNotFound', 'UpdateGroupServiceUnavailable', 'UpdateGroupUnauthorized', 'UpdateJobBadRequest', 'UpdateJobConflict', 'UpdateJobInternalServerError', 'UpdateJobNotFound', 'UpdateJobServiceUnavailable', 'UpdateMappingRuleBadRequest', 'UpdateMappingRuleForbidden', 'UpdateMappingRuleInternalServerError', 'UpdateMappingRuleNotFound', 'UpdateMappingRuleServiceUnavailable', 'UpdateRoleBadRequest', 'UpdateRoleInternalServerError', 'UpdateRoleNotFound', 'UpdateRoleServiceUnavailable', 'UpdateRoleUnauthorized', 'UpdateTenantBadRequest', 'UpdateTenantForbidden', 'UpdateTenantInternalServerError', 'UpdateTenantNotFound', 'UpdateTenantServiceUnavailable', 'UpdateUserBadRequest', 'UpdateUserForbidden', 'UpdateUserInternalServerError', 'UpdateUserNotFound', 'UpdateUserServiceUnavailable', 'UpdateUserTaskBadRequest', 'UpdateUserTaskConflict', 'UpdateUserTaskInternalServerError', 'UpdateUserTaskNotFound', 'UpdateUserTaskServiceUnavailable']
