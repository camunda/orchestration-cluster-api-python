from __future__ import annotations

from typing import Any
from .models import ProblemDetail
class ApiError(Exception):
    def __init__(self, status_code: int, content: bytes, parsed: Any | None = None): ...
    def _build_message(self) -> str: ...
class UnexpectedStatus(ApiError):
    def __init__(self, status_code: int, content: bytes): ...
class ActivateAdHocSubProcessActivitiesBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ActivateAdHocSubProcessActivitiesForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ActivateAdHocSubProcessActivitiesInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ActivateAdHocSubProcessActivitiesNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ActivateAdHocSubProcessActivitiesServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ActivateAdHocSubProcessActivitiesUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ActivateJobsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ActivateJobsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ActivateJobsServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ActivateJobsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToGroupConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignClientToTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignGroupToTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignGroupToTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignGroupToTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignGroupToTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignGroupToTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToGroupConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignMappingRuleToTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToClientBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToClientConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToClientForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToClientInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToClientNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToClientServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToGroupConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToMappingRuleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToMappingRuleConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToMappingRuleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToMappingRuleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToMappingRuleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToMappingRuleServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToUserBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToUserConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToUserForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToUserInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToUserNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignRoleToUserServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserTaskBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserTaskConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserTaskInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserTaskNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserTaskServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToGroupConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class AssignUserToTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class BroadcastSignalBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class BroadcastSignalInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class BroadcastSignalNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class BroadcastSignalServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelBatchOperationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelBatchOperationNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelProcessInstanceBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelProcessInstanceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelProcessInstanceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelProcessInstanceServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelProcessInstancesBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelProcessInstancesBatchOperationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelProcessInstancesBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CancelProcessInstancesBatchOperationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteJobBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteJobConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteJobInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteJobNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteJobServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteUserTaskBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteUserTaskConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteUserTaskInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteUserTaskNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CompleteUserTaskServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CorrelateMessageBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CorrelateMessageForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CorrelateMessageInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CorrelateMessageNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CorrelateMessageServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAdminUserBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAdminUserForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAdminUserInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAdminUserServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAuthorizationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAuthorizationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAuthorizationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAuthorizationNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAuthorizationServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateAuthorizationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateDeploymentBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateDeploymentServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateDocumentBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateDocumentLinkBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateDocumentUnsupportedMediaType(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateDocumentsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateDocumentsUnsupportedMediaType(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateElementInstanceVariablesBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateElementInstanceVariablesInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateElementInstanceVariablesServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateGlobalClusterVariableBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateGlobalClusterVariableForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateGlobalClusterVariableInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateGlobalClusterVariableUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateGroupUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateMappingRuleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateMappingRuleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateMappingRuleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateMappingRuleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateProcessInstanceBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateProcessInstanceGatewayTimeout(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateProcessInstanceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateProcessInstanceServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateRoleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateRoleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateRoleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateRoleServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateRoleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateTenantClusterVariableBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateTenantClusterVariableForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateTenantClusterVariableInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateTenantClusterVariableUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateTenantConflict(ApiError):
    parsed: Any
    def __init__(self, status_code: int, content: bytes, parsed: Any): ...
class CreateTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateUserBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateUserConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateUserForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateUserInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateUserServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class CreateUserUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteAuthorizationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteAuthorizationNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteAuthorizationServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteAuthorizationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDecisionInstanceForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDecisionInstanceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDecisionInstanceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDecisionInstanceServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDecisionInstanceUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDecisionInstancesBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDecisionInstancesBatchOperationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDecisionInstancesBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDecisionInstancesBatchOperationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDocumentInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteDocumentNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteGlobalClusterVariableBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteGlobalClusterVariableForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteGlobalClusterVariableInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteGlobalClusterVariableNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteGlobalClusterVariableUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteGroupUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteMappingRuleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteMappingRuleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteMappingRuleServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteMappingRuleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstanceConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstanceForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstanceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstanceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstanceServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstanceUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstancesBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstancesBatchOperationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstancesBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteProcessInstancesBatchOperationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteResourceBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteResourceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteResourceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteResourceServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteRoleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteRoleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteRoleServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteRoleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantClusterVariableBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantClusterVariableForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantClusterVariableInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantClusterVariableNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantClusterVariableUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteUserBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteUserInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteUserNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class DeleteUserServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateConditionalsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateConditionalsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateConditionalsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateConditionalsNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateConditionalsServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateDecisionBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateDecisionInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateDecisionNotFound(ApiError):
    parsed: Any
    def __init__(self, status_code: int, content: bytes, parsed: Any): ...
class EvaluateDecisionServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateExpressionBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateExpressionForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateExpressionInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class EvaluateExpressionUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class FailJobBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class FailJobConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class FailJobInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class FailJobNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class FailJobServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuditLogForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuditLogInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuditLogNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuditLogUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuthenticationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuthenticationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuthenticationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuthorizationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuthorizationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuthorizationNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetAuthorizationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetBatchOperationNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionXmlBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionXmlForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionXmlInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionXmlNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionDefinitionXmlUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionInstanceBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionInstanceForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionInstanceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionInstanceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionInstanceUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsXmlBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsXmlForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsXmlInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsXmlNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDecisionRequirementsXmlUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDocumentInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetDocumentNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetElementInstanceBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetElementInstanceForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetElementInstanceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetElementInstanceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetElementInstanceUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGlobalClusterVariableBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGlobalClusterVariableForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGlobalClusterVariableInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGlobalClusterVariableNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGlobalClusterVariableUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGlobalJobStatisticsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGlobalJobStatisticsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGlobalJobStatisticsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGlobalJobStatisticsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetGroupUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetIncidentBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetIncidentForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetIncidentInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetIncidentNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetIncidentUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetLicenseInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetMappingRuleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetMappingRuleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetMappingRuleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionInstanceStatisticsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionInstanceStatisticsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionInstanceStatisticsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionInstanceStatisticsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionInstanceVersionStatisticsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionInstanceVersionStatisticsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionInstanceVersionStatisticsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionInstanceVersionStatisticsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionMessageSubscriptionStatisticsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionMessageSubscriptionStatisticsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionMessageSubscriptionStatisticsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionMessageSubscriptionStatisticsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionStatisticsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionStatisticsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionStatisticsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionStatisticsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionXmlBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionXmlForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionXmlInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionXmlNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessDefinitionXmlUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceCallHierarchyBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceCallHierarchyForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceCallHierarchyInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceCallHierarchyNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceCallHierarchyUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceSequenceFlowsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceSequenceFlowsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceSequenceFlowsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceSequenceFlowsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsByDefinitionBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsByDefinitionForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsByDefinitionInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsByDefinitionUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsByErrorBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsByErrorForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsByErrorInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsByErrorUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceStatisticsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetProcessInstanceUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetResourceContentInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetResourceContentNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetResourceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetResourceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetRoleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetRoleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetRoleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetRoleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetStartProcessFormBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetStartProcessFormForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetStartProcessFormInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetStartProcessFormNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetStartProcessFormUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetStatusServiceUnavailable(ApiError):
    parsed: None
    def __init__(self, status_code: int, content: bytes, parsed: None): ...
class GetTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTenantClusterVariableBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTenantClusterVariableForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTenantClusterVariableInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTenantClusterVariableNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTenantClusterVariableUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTenantUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTopologyInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetTopologyUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUsageMetricsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUsageMetricsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUsageMetricsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUsageMetricsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskFormBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskFormForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskFormInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskFormNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskFormUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserTaskUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetUserUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetVariableBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetVariableForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetVariableInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetVariableNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class GetVariableUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class MigrateProcessInstanceBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class MigrateProcessInstanceConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class MigrateProcessInstanceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class MigrateProcessInstanceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class MigrateProcessInstanceServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class MigrateProcessInstancesBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class MigrateProcessInstancesBatchOperationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class MigrateProcessInstancesBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class MigrateProcessInstancesBatchOperationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ModifyProcessInstanceBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ModifyProcessInstanceInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ModifyProcessInstanceNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ModifyProcessInstanceServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ModifyProcessInstancesBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ModifyProcessInstancesBatchOperationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ModifyProcessInstancesBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ModifyProcessInstancesBatchOperationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class PinClockBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class PinClockInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class PinClockServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class PublishMessageBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class PublishMessageInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class PublishMessageServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResetClockInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResetClockServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveIncidentBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveIncidentInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveIncidentNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveIncidentServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveIncidentsBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveIncidentsBatchOperationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveIncidentsBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveIncidentsBatchOperationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveProcessInstanceIncidentsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveProcessInstanceIncidentsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveProcessInstanceIncidentsNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveProcessInstanceIncidentsServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResolveProcessInstanceIncidentsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResumeBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResumeBatchOperationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResumeBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResumeBatchOperationNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ResumeBatchOperationServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchAuditLogsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchAuditLogsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchAuditLogsInternalServerError(ApiError):
    parsed: Any
    def __init__(self, status_code: int, content: bytes, parsed: Any): ...
class SearchAuditLogsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchAuthorizationsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchAuthorizationsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchAuthorizationsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchAuthorizationsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchBatchOperationItemsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchBatchOperationItemsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchBatchOperationsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchBatchOperationsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForGroupUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForRoleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForRoleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForRoleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForRoleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClientsForRoleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClusterVariablesBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClusterVariablesForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClusterVariablesInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchClusterVariablesUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchCorrelatedMessageSubscriptionsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchCorrelatedMessageSubscriptionsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchCorrelatedMessageSubscriptionsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchCorrelatedMessageSubscriptionsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionDefinitionsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionDefinitionsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionDefinitionsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionDefinitionsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionInstancesBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionInstancesForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionInstancesInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionInstancesUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionRequirementsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionRequirementsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionRequirementsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchDecisionRequirementsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchElementInstanceIncidentsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchElementInstanceIncidentsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchElementInstanceIncidentsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchElementInstanceIncidentsNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchElementInstanceIncidentsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchElementInstancesBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchElementInstancesForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchElementInstancesInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchElementInstancesUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchGroupsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchGroupsForRoleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchGroupsForRoleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchGroupsForRoleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchGroupsForRoleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchGroupsForRoleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchGroupsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchGroupsInternalServerError(ApiError):
    parsed: Any
    def __init__(self, status_code: int, content: bytes, parsed: Any): ...
class SearchGroupsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchIncidentsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchIncidentsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchIncidentsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchIncidentsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchJobsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchJobsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchJobsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchJobsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRuleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRuleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRuleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRuleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForGroupUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForRoleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForRoleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForRoleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForRoleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMappingRulesForRoleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMessageSubscriptionsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMessageSubscriptionsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMessageSubscriptionsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchMessageSubscriptionsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessDefinitionsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessDefinitionsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessDefinitionsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessDefinitionsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessInstanceIncidentsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessInstanceIncidentsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessInstanceIncidentsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessInstanceIncidentsNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessInstanceIncidentsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessInstancesBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessInstancesForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessInstancesInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchProcessInstancesUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchRolesBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchRolesForGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchRolesForGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchRolesForGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchRolesForGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchRolesForGroupUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchRolesForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchRolesInternalServerError(ApiError):
    parsed: Any
    def __init__(self, status_code: int, content: bytes, parsed: Any): ...
class SearchRolesUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchTenantsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchTenantsForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchTenantsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchTenantsNotFound(ApiError):
    parsed: Any
    def __init__(self, status_code: int, content: bytes, parsed: Any): ...
class SearchTenantsUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUserTaskAuditLogsBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUserTaskAuditLogsInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUserTaskVariablesBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUserTaskVariablesInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUserTasksBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUserTasksForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUserTasksInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUserTasksUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForGroupUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForRoleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForRoleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForRoleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForRoleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForRoleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchUsersUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchVariablesBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchVariablesForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchVariablesInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SearchVariablesUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SuspendBatchOperationBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SuspendBatchOperationForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SuspendBatchOperationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SuspendBatchOperationNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class SuspendBatchOperationServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ThrowJobErrorBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ThrowJobErrorConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ThrowJobErrorInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ThrowJobErrorNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class ThrowJobErrorServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignClientFromTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignGroupFromTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignGroupFromTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignGroupFromTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignGroupFromTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignGroupFromTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignMappingRuleFromTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromClientBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromClientForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromClientInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromClientNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromClientServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromMappingRuleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromMappingRuleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromMappingRuleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromMappingRuleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromMappingRuleServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromUserBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromUserForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromUserInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromUserNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignRoleFromUserServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromGroupForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserFromTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserTaskBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserTaskConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserTaskInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserTaskNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UnassignUserTaskServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateAuthorizationInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateAuthorizationNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateAuthorizationServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateAuthorizationUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGlobalClusterVariableBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGlobalClusterVariableForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGlobalClusterVariableInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGlobalClusterVariableNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGlobalClusterVariableUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGroupBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGroupInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGroupNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGroupServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateGroupUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateJobBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateJobConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateJobInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateJobNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateJobServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateMappingRuleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateMappingRuleForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateMappingRuleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateMappingRuleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateMappingRuleServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateRoleBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateRoleInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateRoleNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateRoleServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateRoleUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantClusterVariableBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantClusterVariableForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantClusterVariableInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantClusterVariableNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantClusterVariableUnauthorized(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateTenantServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserForbidden(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserTaskBadRequest(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserTaskConflict(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserTaskInternalServerError(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserTaskNotFound(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
class UpdateUserTaskServiceUnavailable(ApiError):
    parsed: ProblemDetail
    def __init__(self, status_code: int, content: bytes, parsed: ProblemDetail): ...
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
