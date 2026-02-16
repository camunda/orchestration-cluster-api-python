from __future__ import annotations

import ssl
from typing import Any
import httpx
from attrs import define, field
from .types import UNSET, Unset, str_any_dict_factory, str_str_dict_factory
from .runtime.job_worker import JobWorker, WorkerConfig, JobHandler
from .runtime.configuration_resolver import (
    CamundaSdkConfigPartial,
    CamundaSdkConfiguration,
)
from .runtime.auth import AuthProvider
from .runtime.logging import CamundaLogger
from pathlib import Path
from .models.create_deployment_response_200 import CreateDeploymentResponse200
from .models.deployment_process_result import DeploymentProcessResult
from .models.deployment_decision_result import DeploymentDecisionResult
from .models.deployment_decision_requirements_result import (
    DeploymentDecisionRequirementsResult,
)
from .models.deployment_form_result import DeploymentFormResult
from .models.activate_jobs_response_200 import ActivateJobsResponse200
from .models.ad_hoc_sub_process_activate_activities_instruction import (
    AdHocSubProcessActivateActivitiesInstruction,
)
from .models.audit_log_search_query_request import AuditLogSearchQueryRequest
from .models.authorization_create_result import AuthorizationCreateResult
from .models.authorization_id_based_request import AuthorizationIdBasedRequest
from .models.authorization_property_based_request import (
    AuthorizationPropertyBasedRequest,
)
from .models.authorization_result import AuthorizationResult
from .models.authorization_search_query import AuthorizationSearchQuery
from .models.authorization_search_result import AuthorizationSearchResult
from .models.batch_operation_created_result import BatchOperationCreatedResult
from .models.batch_operation_item_search_query_result import (
    BatchOperationItemSearchQueryResult,
)
from .models.batch_operation_response import BatchOperationResponse
from .models.batch_operation_search_query_result import BatchOperationSearchQueryResult
from .models.camunda_user_result import CamundaUserResult
from .models.cancel_process_instance_data_type_0 import CancelProcessInstanceDataType0
from .models.cancel_process_instances_batch_operation_data import (
    CancelProcessInstancesBatchOperationData,
)
from .models.clock_pin_request import ClockPinRequest
from .models.cluster_variable_result import ClusterVariableResult
from .models.cluster_variable_search_query_request import (
    ClusterVariableSearchQueryRequest,
)
from .models.cluster_variable_search_query_result import (
    ClusterVariableSearchQueryResult,
)
from .models.complete_job_data import CompleteJobData
from .models.conditional_evaluation_instruction import ConditionalEvaluationInstruction
from .models.correlated_message_subscription_search_query import (
    CorrelatedMessageSubscriptionSearchQuery,
)
from .models.correlated_message_subscription_search_query_result import (
    CorrelatedMessageSubscriptionSearchQueryResult,
)
from .models.create_cluster_variable_request import CreateClusterVariableRequest
from .models.create_deployment_data import CreateDeploymentData
from .models.create_document_data import CreateDocumentData
from .models.create_documents_data import CreateDocumentsData
from .models.create_process_instance_result import CreateProcessInstanceResult
from .models.decision_definition_result import DecisionDefinitionResult
from .models.decision_definition_search_query import DecisionDefinitionSearchQuery
from .models.decision_definition_search_query_result import (
    DecisionDefinitionSearchQueryResult,
)
from .models.decision_evaluation_by_id import DecisionEvaluationByID
from .models.decision_evaluation_by_key import DecisionEvaluationByKey
from .models.decision_instance_deletion_batch_operation_request import (
    DecisionInstanceDeletionBatchOperationRequest,
)
from .models.decision_instance_get_query_result import DecisionInstanceGetQueryResult
from .models.decision_instance_search_query import DecisionInstanceSearchQuery
from .models.decision_instance_search_query_result import (
    DecisionInstanceSearchQueryResult,
)
from .models.decision_requirements_result import DecisionRequirementsResult
from .models.decision_requirements_search_query import DecisionRequirementsSearchQuery
from .models.decision_requirements_search_query_result import (
    DecisionRequirementsSearchQueryResult,
)
from .models.delete_process_instance_data_type_0 import DeleteProcessInstanceDataType0
from .models.delete_process_instance_request_type_0 import (
    DeleteProcessInstanceRequestType0,
)
from .models.delete_process_instances_batch_operation_data import (
    DeleteProcessInstancesBatchOperationData,
)
from .models.delete_resource_data_type_0 import DeleteResourceDataType0
from .models.delete_resource_response import DeleteResourceResponse
from .models.document_creation_batch_response import DocumentCreationBatchResponse
from .models.document_link import DocumentLink
from .models.document_link_request import DocumentLinkRequest
from .models.document_reference import DocumentReference
from .models.element_instance_result import ElementInstanceResult
from .models.element_instance_search_query import ElementInstanceSearchQuery
from .models.element_instance_search_query_result import (
    ElementInstanceSearchQueryResult,
)
from .models.evaluate_conditional_result import EvaluateConditionalResult
from .models.evaluate_decision_result import EvaluateDecisionResult
from .models.expression_evaluation_request import ExpressionEvaluationRequest
from .models.expression_evaluation_result import ExpressionEvaluationResult
from .models.get_audit_log_response_200 import GetAuditLogResponse200
from .models.get_process_definition_statistics_data import (
    GetProcessDefinitionStatisticsData,
)
from .models.get_process_definition_statistics_response_200 import (
    GetProcessDefinitionStatisticsResponse200,
)
from .models.get_process_instance_response_200 import GetProcessInstanceResponse200
from .models.get_process_instance_sequence_flows_response_200 import (
    GetProcessInstanceSequenceFlowsResponse200,
)
from .models.get_process_instance_statistics_response_200 import (
    GetProcessInstanceStatisticsResponse200,
)
from .models.get_start_process_form_response_200 import GetStartProcessFormResponse200
from .models.get_user_task_form_response_200 import GetUserTaskFormResponse200
from .models.get_user_task_response_200 import GetUserTaskResponse200
from .models.global_job_statistics_query_result import GlobalJobStatisticsQueryResult
from .models.group_create_request import GroupCreateRequest
from .models.group_create_result import GroupCreateResult
from .models.group_result import GroupResult
from .models.group_search_query_request import GroupSearchQueryRequest
from .models.group_search_query_result import GroupSearchQueryResult
from .models.group_update_request import GroupUpdateRequest
from .models.group_update_result import GroupUpdateResult
from .models.incident_process_instance_statistics_by_definition_query import (
    IncidentProcessInstanceStatisticsByDefinitionQuery,
)
from .models.incident_process_instance_statistics_by_definition_query_result import (
    IncidentProcessInstanceStatisticsByDefinitionQueryResult,
)
from .models.incident_process_instance_statistics_by_error_query import (
    IncidentProcessInstanceStatisticsByErrorQuery,
)
from .models.incident_process_instance_statistics_by_error_query_result import (
    IncidentProcessInstanceStatisticsByErrorQueryResult,
)
from .models.incident_resolution_request import IncidentResolutionRequest
from .models.incident_result import IncidentResult
from .models.incident_search_query import IncidentSearchQuery
from .models.incident_search_query_result import IncidentSearchQueryResult
from .models.job_activation_request import JobActivationRequest
from .models.job_error_request import JobErrorRequest
from .models.job_fail_request import JobFailRequest
from .models.job_search_query import JobSearchQuery
from .models.job_update_request import JobUpdateRequest
from .models.license_response import LicenseResponse
from .models.mapping_rule_create_request import MappingRuleCreateRequest
from .models.mapping_rule_result import MappingRuleResult
from .models.mapping_rule_search_query_request import MappingRuleSearchQueryRequest
from .models.mapping_rule_search_query_result import MappingRuleSearchQueryResult
from .models.mapping_rule_update_request import MappingRuleUpdateRequest
from .models.mapping_rule_update_result import MappingRuleUpdateResult
from .models.message_correlation_request import MessageCorrelationRequest
from .models.message_correlation_result import MessageCorrelationResult
from .models.message_publication_request import MessagePublicationRequest
from .models.migrate_process_instance_data import MigrateProcessInstanceData
from .models.migrate_process_instances_batch_operation_data import (
    MigrateProcessInstancesBatchOperationData,
)
from .models.modify_process_instance_data import ModifyProcessInstanceData
from .models.modify_process_instances_batch_operation_data import (
    ModifyProcessInstancesBatchOperationData,
)
from .models.process_creation_by_id import ProcessCreationById
from .models.process_creation_by_key import ProcessCreationByKey
from .models.process_definition_instance_statistics_query import (
    ProcessDefinitionInstanceStatisticsQuery,
)
from .models.process_definition_instance_statistics_query_result import (
    ProcessDefinitionInstanceStatisticsQueryResult,
)
from .models.process_definition_instance_version_statistics_query import (
    ProcessDefinitionInstanceVersionStatisticsQuery,
)
from .models.process_definition_instance_version_statistics_query_result import (
    ProcessDefinitionInstanceVersionStatisticsQueryResult,
)
from .models.process_definition_message_subscription_statistics_query import (
    ProcessDefinitionMessageSubscriptionStatisticsQuery,
)
from .models.process_definition_message_subscription_statistics_query_result import (
    ProcessDefinitionMessageSubscriptionStatisticsQueryResult,
)
from .models.process_definition_result import ProcessDefinitionResult
from .models.process_definition_search_query_result import (
    ProcessDefinitionSearchQueryResult,
)
from .models.publish_message_response_200 import PublishMessageResponse200
from .models.resolve_incidents_batch_operation_data import (
    ResolveIncidentsBatchOperationData,
)
from .models.resource_result import ResourceResult
from .models.role_create_request import RoleCreateRequest
from .models.role_create_result import RoleCreateResult
from .models.role_group_search_result import RoleGroupSearchResult
from .models.role_result import RoleResult
from .models.role_search_query_request import RoleSearchQueryRequest
from .models.role_search_query_result import RoleSearchQueryResult
from .models.role_update_request import RoleUpdateRequest
from .models.role_update_result import RoleUpdateResult
from .models.search_audit_logs_response_200 import SearchAuditLogsResponse200
from .models.search_batch_operation_items_data import SearchBatchOperationItemsData
from .models.search_batch_operations_data import SearchBatchOperationsData
from .models.search_clients_for_group_data import SearchClientsForGroupData
from .models.search_clients_for_role_data import SearchClientsForRoleData
from .models.search_clients_for_tenant_data import SearchClientsForTenantData
from .models.search_group_ids_for_tenant_data import SearchGroupIdsForTenantData
from .models.search_groups_for_role_data import SearchGroupsForRoleData
from .models.search_jobs_response_200 import SearchJobsResponse200
from .models.search_message_subscriptions_data import SearchMessageSubscriptionsData
from .models.search_message_subscriptions_response_200 import (
    SearchMessageSubscriptionsResponse200,
)
from .models.search_process_definitions_data import SearchProcessDefinitionsData
from .models.search_process_instances_data import SearchProcessInstancesData
from .models.search_process_instances_response_200 import (
    SearchProcessInstancesResponse200,
)
from .models.search_query_response import SearchQueryResponse
from .models.search_tenants_data import SearchTenantsData
from .models.search_user_task_audit_logs_data import SearchUserTaskAuditLogsData
from .models.search_user_task_audit_logs_response_200 import (
    SearchUserTaskAuditLogsResponse200,
)
from .models.search_user_task_variables_data import SearchUserTaskVariablesData
from .models.search_user_tasks_data import SearchUserTasksData
from .models.search_user_tasks_response_200 import SearchUserTasksResponse200
from .models.search_users_data import SearchUsersData
from .models.search_users_for_group_data import SearchUsersForGroupData
from .models.search_users_for_role_data import SearchUsersForRoleData
from .models.search_users_for_tenant_data import SearchUsersForTenantData
from .models.search_variables_data import SearchVariablesData
from .models.set_variable_request import SetVariableRequest
from .models.signal_broadcast_request import SignalBroadcastRequest
from .models.signal_broadcast_result import SignalBroadcastResult
from .models.tenant_client_search_result import TenantClientSearchResult
from .models.tenant_create_request import TenantCreateRequest
from .models.tenant_create_result import TenantCreateResult
from .models.tenant_group_search_result import TenantGroupSearchResult
from .models.tenant_result import TenantResult
from .models.tenant_search_query_result import TenantSearchQueryResult
from .models.tenant_update_request import TenantUpdateRequest
from .models.tenant_update_result import TenantUpdateResult
from .models.tenant_user_search_result import TenantUserSearchResult
from .models.topology_response import TopologyResponse
from .models.update_cluster_variable_request import UpdateClusterVariableRequest
from .models.usage_metrics_response import UsageMetricsResponse
from .models.user_create_result import UserCreateResult
from .models.user_request import UserRequest
from .models.user_result import UserResult
from .models.user_search_result import UserSearchResult
from .models.user_task_assignment_request import UserTaskAssignmentRequest
from .models.user_task_completion_request import UserTaskCompletionRequest
from .models.user_task_update_request import UserTaskUpdateRequest
from .models.user_update_request import UserUpdateRequest
from .models.variable_result import VariableResult
from .models.variable_search_query_result import VariableSearchQueryResult
from .semantic_types import (
    AuditLogKey,
    AuthorizationKey,
    BatchOperationKey,
    DecisionDefinitionKey,
    DecisionEvaluationInstanceKey,
    DecisionInstanceKey,
    DecisionRequirementsKey,
    DocumentId,
    ElementInstanceKey,
    IncidentKey,
    JobKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    UserTaskKey,
    Username,
    VariableKey,
)
from .types import File
import datetime

@define
class Client:
    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str = field(alias="base_url")
    _cookies: dict[str, str] = field(
        factory=str_str_dict_factory, kw_only=True, alias="cookies"
    )
    _headers: dict[str, str] = field(
        factory=str_str_dict_factory, kw_only=True, alias="headers"
    )
    _timeout: httpx.Timeout | None = field(default=None, kw_only=True, alias="timeout")
    _verify_ssl: str | bool | ssl.SSLContext = field(
        default=True, kw_only=True, alias="verify_ssl"
    )
    _follow_redirects: bool = field(
        default=False, kw_only=True, alias="follow_redirects"
    )
    _httpx_args: dict[str, Any] = field(
        factory=str_any_dict_factory, kw_only=True, alias="httpx_args"
    )
    _client: httpx.Client | None = field(default=None, init=False)
    _async_client: httpx.AsyncClient | None = field(default=None, init=False)
    def with_headers(self, headers: dict[str, str]) -> "Client": ...
    def with_cookies(self, cookies: dict[str, str]) -> "Client": ...
    def with_timeout(self, timeout: httpx.Timeout) -> "Client": ...
    def set_httpx_client(self, client: httpx.Client) -> "Client": ...
    def get_httpx_client(self) -> httpx.Client: ...
    def __enter__(self) -> "Client": ...
    def __exit__(self, *args: Any, **kwargs: Any) -> None: ...
    def set_async_httpx_client(self, async_client: httpx.AsyncClient) -> "Client": ...
    def get_async_httpx_client(self) -> httpx.AsyncClient: ...
    async def __aenter__(self) -> "Client": ...
    async def __aexit__(self, *args: Any, **kwargs: Any) -> None: ...

@define
class AuthenticatedClient:
    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str = field(alias="base_url")
    _cookies: dict[str, str] = field(
        factory=str_str_dict_factory, kw_only=True, alias="cookies"
    )
    _headers: dict[str, str] = field(
        factory=str_str_dict_factory, kw_only=True, alias="headers"
    )
    _timeout: httpx.Timeout | None = field(default=None, kw_only=True, alias="timeout")
    _verify_ssl: str | bool | ssl.SSLContext = field(
        default=True, kw_only=True, alias="verify_ssl"
    )
    _follow_redirects: bool = field(
        default=False, kw_only=True, alias="follow_redirects"
    )
    _httpx_args: dict[str, Any] = field(
        factory=str_any_dict_factory, kw_only=True, alias="httpx_args"
    )
    _client: httpx.Client | None = field(default=None, init=False)
    _async_client: httpx.AsyncClient | None = field(default=None, init=False)
    token: str
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"
    def with_headers(self, headers: dict[str, str]) -> "AuthenticatedClient": ...
    def with_cookies(self, cookies: dict[str, str]) -> "AuthenticatedClient": ...
    def with_timeout(self, timeout: httpx.Timeout) -> "AuthenticatedClient": ...
    def set_httpx_client(self, client: httpx.Client) -> "AuthenticatedClient": ...
    def get_httpx_client(self) -> httpx.Client: ...
    def __enter__(self) -> "AuthenticatedClient": ...
    def __exit__(self, *args: Any, **kwargs: Any) -> None: ...
    def set_async_httpx_client(
        self, async_client: httpx.AsyncClient
    ) -> "AuthenticatedClient": ...
    def get_async_httpx_client(self) -> httpx.AsyncClient: ...
    async def __aenter__(self) -> "AuthenticatedClient": ...
    async def __aexit__(self, *args: Any, **kwargs: Any) -> None: ...

class ExtendedDeploymentResult(CreateDeploymentResponse200):
    processes: list[DeploymentProcessResult]
    decisions: list[DeploymentDecisionResult]
    decision_requirements: list[DeploymentDecisionRequirementsResult]
    forms: list[DeploymentFormResult]
    def __init__(self, response: CreateDeploymentResponse200) -> None: ...

class CamundaClient:
    client: Client | AuthenticatedClient
    configuration: CamundaSdkConfiguration
    auth_provider: AuthProvider
    def __init__(
        self,
        configuration: CamundaSdkConfigPartial | None = None,
        auth_provider: AuthProvider | None = None,
        logger: CamundaLogger | None = None,
        **kwargs: Any,
    ) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, *args: Any, **kwargs: Any) -> None: ...
    def close(self) -> None: ...
    def deploy_resources_from_files(
        self, files: list[str | Path], tenant_id: str | None = None
    ) -> ExtendedDeploymentResult: ...
    def delete_tenant(self, tenant_id: TenantId, **kwargs: Any) -> None: ...
    def assign_group_to_tenant(
        self, tenant_id: TenantId, group_id: str, **kwargs: Any
    ) -> None: ...
    def unassign_role_from_tenant(
        self, tenant_id: TenantId, role_id: str, **kwargs: Any
    ) -> None: ...
    def search_group_ids_for_tenant(
        self,
        tenant_id: TenantId,
        data: SearchGroupIdsForTenantData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantGroupSearchResult: ...
    def search_users_for_tenant(
        self,
        tenant_id: TenantId,
        data: SearchUsersForTenantData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantUserSearchResult: ...
    def unassign_client_from_tenant(
        self, tenant_id: TenantId, client_id: str, **kwargs: Any
    ) -> None: ...
    def unassign_user_from_tenant(
        self, tenant_id: TenantId, username: Username, **kwargs: Any
    ) -> None: ...
    def search_roles_for_tenant(
        self,
        tenant_id: TenantId,
        data: RoleSearchQueryRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchQueryResponse: ...
    def unassign_group_from_tenant(
        self, tenant_id: TenantId, group_id: str, **kwargs: Any
    ) -> None: ...
    def search_clients_for_tenant(
        self,
        tenant_id: TenantId,
        data: SearchClientsForTenantData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantClientSearchResult: ...
    def search_tenants(
        self, data: SearchTenantsData | Unset = UNSET, **kwargs: Any
    ) -> TenantSearchQueryResult: ...
    def assign_user_to_tenant(
        self, tenant_id: TenantId, username: Username, **kwargs: Any
    ) -> None: ...
    def assign_role_to_tenant(
        self, tenant_id: TenantId, role_id: str, **kwargs: Any
    ) -> None: ...
    def search_mapping_rules_for_tenant(
        self,
        tenant_id: TenantId,
        data: MappingRuleSearchQueryRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchQueryResponse: ...
    def assign_mapping_rule_to_tenant(
        self, tenant_id: TenantId, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    def update_tenant(
        self, tenant_id: TenantId, data: TenantUpdateRequest, **kwargs: Any
    ) -> TenantUpdateResult: ...
    def assign_client_to_tenant(
        self, tenant_id: TenantId, client_id: str, **kwargs: Any
    ) -> None: ...
    def get_tenant(self, tenant_id: TenantId, **kwargs: Any) -> TenantResult: ...
    def create_tenant(
        self, data: TenantCreateRequest, **kwargs: Any
    ) -> TenantCreateResult: ...
    def unassign_mapping_rule_from_tenant(
        self, tenant_id: TenantId, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    def cancel_batch_operation(
        self,
        batch_operation_key: BatchOperationKey,
        data: Any | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    def resume_batch_operation(
        self,
        batch_operation_key: BatchOperationKey,
        data: Any | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    def suspend_batch_operation(
        self,
        batch_operation_key: BatchOperationKey,
        data: Any | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    def search_batch_operations(
        self, data: SearchBatchOperationsData | Unset = UNSET, **kwargs: Any
    ) -> BatchOperationSearchQueryResult: ...
    def get_batch_operation(
        self, batch_operation_key: BatchOperationKey, **kwargs: Any
    ) -> BatchOperationResponse: ...
    def search_batch_operation_items(
        self, data: SearchBatchOperationItemsData | Unset = UNSET, **kwargs: Any
    ) -> BatchOperationItemSearchQueryResult: ...
    def get_topology(self, **kwargs: Any) -> TopologyResponse: ...
    def unassign_role_from_group(
        self, role_id: str, group_id: str, **kwargs: Any
    ) -> None: ...
    def search_users_for_role(
        self, role_id: str, data: SearchUsersForRoleData | Unset = UNSET, **kwargs: Any
    ) -> TenantUserSearchResult: ...
    def unassign_role_from_mapping_rule(
        self, role_id: str, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    def search_roles(
        self, data: RoleSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> RoleSearchQueryResult: ...
    def unassign_role_from_client(
        self, role_id: str, client_id: str, **kwargs: Any
    ) -> None: ...
    def unassign_role_from_user(
        self, role_id: str, username: Username, **kwargs: Any
    ) -> None: ...
    def create_role(
        self, data: RoleCreateRequest | Unset = UNSET, **kwargs: Any
    ) -> RoleCreateResult: ...
    def search_clients_for_role(
        self,
        role_id: str,
        data: SearchClientsForRoleData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantClientSearchResult: ...
    def assign_role_to_user(
        self, role_id: str, username: Username, **kwargs: Any
    ) -> None: ...
    def search_groups_for_role(
        self, role_id: str, data: SearchGroupsForRoleData | Unset = UNSET, **kwargs: Any
    ) -> RoleGroupSearchResult: ...
    def update_role(
        self, role_id: str, data: RoleUpdateRequest, **kwargs: Any
    ) -> RoleUpdateResult: ...
    def assign_role_to_group(
        self, role_id: str, group_id: str, **kwargs: Any
    ) -> None: ...
    def search_mapping_rules_for_role(
        self,
        role_id: str,
        data: MappingRuleSearchQueryRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchQueryResponse: ...
    def assign_role_to_client(
        self, role_id: str, client_id: str, **kwargs: Any
    ) -> None: ...
    def delete_role(self, role_id: str, **kwargs: Any) -> None: ...
    def assign_role_to_mapping_rule(
        self, role_id: str, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    def get_role(self, role_id: str, **kwargs: Any) -> RoleResult: ...
    def evaluate_conditionals(
        self, data: ConditionalEvaluationInstruction, **kwargs: Any
    ) -> EvaluateConditionalResult: ...
    def get_license(self, **kwargs: Any) -> LicenseResponse: ...
    def search_decision_instances(
        self, data: DecisionInstanceSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> DecisionInstanceSearchQueryResult: ...
    def get_decision_instance(
        self,
        decision_evaluation_instance_key: DecisionEvaluationInstanceKey,
        **kwargs: Any,
    ) -> DecisionInstanceGetQueryResult: ...
    def delete_decision_instance(
        self,
        decision_instance_key: DecisionInstanceKey,
        data: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
        **kwargs: Any,
    ) -> BatchOperationCreatedResult: ...
    def delete_decision_instances_batch_operation(
        self, data: DecisionInstanceDeletionBatchOperationRequest, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    def get_variable(
        self, variable_key: VariableKey, **kwargs: Any
    ) -> VariableResult: ...
    def search_variables(
        self,
        data: SearchVariablesData | Unset = UNSET,
        truncate_values: bool | Unset = UNSET,
        **kwargs: Any,
    ) -> VariableSearchQueryResult: ...
    def get_tenant_cluster_variable(
        self, tenant_id: TenantId, name: str, **kwargs: Any
    ) -> ClusterVariableResult: ...
    def search_cluster_variables(
        self,
        data: ClusterVariableSearchQueryRequest | Unset = UNSET,
        truncate_values: bool | Unset = UNSET,
        **kwargs: Any,
    ) -> ClusterVariableSearchQueryResult: ...
    def create_global_cluster_variable(
        self, data: CreateClusterVariableRequest, **kwargs: Any
    ) -> ClusterVariableResult: ...
    def update_tenant_cluster_variable(
        self,
        tenant_id: TenantId,
        name: str,
        data: UpdateClusterVariableRequest,
        **kwargs: Any,
    ) -> ClusterVariableResult: ...
    def delete_global_cluster_variable(self, name: str, **kwargs: Any) -> None: ...
    def delete_tenant_cluster_variable(
        self, tenant_id: TenantId, name: str, **kwargs: Any
    ) -> None: ...
    def update_global_cluster_variable(
        self, name: str, data: UpdateClusterVariableRequest, **kwargs: Any
    ) -> ClusterVariableResult: ...
    def create_tenant_cluster_variable(
        self, tenant_id: TenantId, data: CreateClusterVariableRequest, **kwargs: Any
    ) -> ClusterVariableResult: ...
    def get_global_cluster_variable(
        self, name: str, **kwargs: Any
    ) -> ClusterVariableResult: ...
    def unassign_mapping_rule_from_group(
        self, group_id: str, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    def search_roles_for_group(
        self, group_id: str, data: RoleSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> SearchQueryResponse: ...
    def assign_client_to_group(
        self, group_id: str, client_id: str, **kwargs: Any
    ) -> None: ...
    def unassign_user_from_group(
        self, group_id: str, username: Username, **kwargs: Any
    ) -> None: ...
    def search_users_for_group(
        self,
        group_id: str,
        data: SearchUsersForGroupData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantUserSearchResult: ...
    def get_group(self, group_id: str, **kwargs: Any) -> GroupResult: ...
    def unassign_client_from_group(
        self, group_id: str, client_id: str, **kwargs: Any
    ) -> None: ...
    def update_group(
        self, group_id: str, data: GroupUpdateRequest, **kwargs: Any
    ) -> GroupUpdateResult: ...
    def search_groups(
        self, data: GroupSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> GroupSearchQueryResult: ...
    def assign_mapping_rule_to_group(
        self, group_id: str, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    def search_mapping_rules_for_group(
        self,
        group_id: str,
        data: MappingRuleSearchQueryRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchQueryResponse: ...
    def create_group(
        self, data: GroupCreateRequest | Unset = UNSET, **kwargs: Any
    ) -> GroupCreateResult: ...
    def delete_group(self, group_id: str, **kwargs: Any) -> None: ...
    def assign_user_to_group(
        self, group_id: str, username: Username, **kwargs: Any
    ) -> None: ...
    def search_clients_for_group(
        self,
        group_id: str,
        data: SearchClientsForGroupData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantClientSearchResult: ...
    def search_correlated_message_subscriptions(
        self,
        data: CorrelatedMessageSubscriptionSearchQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> CorrelatedMessageSubscriptionSearchQueryResult: ...
    def search_message_subscriptions(
        self, data: SearchMessageSubscriptionsData | Unset = UNSET, **kwargs: Any
    ) -> SearchMessageSubscriptionsResponse200: ...
    def create_admin_user(self, data: UserRequest, **kwargs: Any) -> None: ...
    def publish_message(
        self, data: MessagePublicationRequest, **kwargs: Any
    ) -> PublishMessageResponse200: ...
    def correlate_message(
        self, data: MessageCorrelationRequest, **kwargs: Any
    ) -> MessageCorrelationResult: ...
    def create_user(self, data: UserRequest, **kwargs: Any) -> UserCreateResult: ...
    def search_users(
        self, data: SearchUsersData | Unset = UNSET, **kwargs: Any
    ) -> UserSearchResult: ...
    def delete_user(self, username: Username, **kwargs: Any) -> None: ...
    def get_user(self, username: Username, **kwargs: Any) -> UserResult: ...
    def update_user(
        self, username: Username, data: UserUpdateRequest, **kwargs: Any
    ) -> UserResult: ...
    def get_document(
        self,
        document_id: DocumentId,
        store_id: str | Unset = UNSET,
        content_hash: str | Unset = UNSET,
        **kwargs: Any,
    ) -> File: ...
    def create_documents(
        self, data: CreateDocumentsData, store_id: str | Unset = UNSET, **kwargs: Any
    ) -> DocumentCreationBatchResponse: ...
    def create_document_link(
        self,
        document_id: DocumentId,
        data: DocumentLinkRequest | Unset = UNSET,
        store_id: str | Unset = UNSET,
        content_hash: str | Unset = UNSET,
        **kwargs: Any,
    ) -> DocumentLink: ...
    def delete_document(
        self, document_id: DocumentId, store_id: str | Unset = UNSET, **kwargs: Any
    ) -> None: ...
    def create_document(
        self,
        data: CreateDocumentData,
        store_id: str | Unset = UNSET,
        document_id: str | Unset = UNSET,
        **kwargs: Any,
    ) -> DocumentReference: ...
    def get_audit_log(
        self, audit_log_key: AuditLogKey, **kwargs: Any
    ) -> GetAuditLogResponse200: ...
    def search_audit_logs(
        self, data: AuditLogSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> SearchAuditLogsResponse200: ...
    def get_usage_metrics(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        tenant_id: str | Unset = UNSET,
        with_tenants: bool | Unset = False,
        **kwargs: Any,
    ) -> UsageMetricsResponse: ...
    def search_element_instance_incidents(
        self,
        element_instance_key: ElementInstanceKey,
        data: IncidentSearchQuery,
        **kwargs: Any,
    ) -> IncidentSearchQueryResult: ...
    def get_element_instance(
        self, element_instance_key: ElementInstanceKey, **kwargs: Any
    ) -> ElementInstanceResult: ...
    def create_element_instance_variables(
        self,
        element_instance_key: ElementInstanceKey,
        data: SetVariableRequest,
        **kwargs: Any,
    ) -> None: ...
    def search_element_instances(
        self, data: ElementInstanceSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> ElementInstanceSearchQueryResult: ...
    def activate_ad_hoc_sub_process_activities(
        self,
        ad_hoc_sub_process_instance_key: str,
        data: AdHocSubProcessActivateActivitiesInstruction,
        **kwargs: Any,
    ) -> None: ...
    def fail_job(
        self, job_key: JobKey, data: JobFailRequest | Unset = UNSET, **kwargs: Any
    ) -> None: ...
    def search_jobs(
        self, data: JobSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> SearchJobsResponse200: ...
    def activate_jobs(
        self, data: JobActivationRequest, **kwargs: Any
    ) -> ActivateJobsResponse200: ...
    def get_global_job_statistics(
        self,
        from_: datetime.datetime,
        to: datetime.datetime,
        job_type: str | Unset = UNSET,
        **kwargs: Any,
    ) -> GlobalJobStatisticsQueryResult: ...
    def throw_job_error(
        self, job_key: JobKey, data: JobErrorRequest, **kwargs: Any
    ) -> None: ...
    def complete_job(
        self, job_key: JobKey, data: CompleteJobData | Unset = UNSET, **kwargs: Any
    ) -> None: ...
    def update_job(
        self, job_key: JobKey, data: JobUpdateRequest, **kwargs: Any
    ) -> None: ...
    def get_process_instance_statistics_by_definition(
        self, data: IncidentProcessInstanceStatisticsByDefinitionQuery, **kwargs: Any
    ) -> IncidentProcessInstanceStatisticsByDefinitionQueryResult: ...
    def resolve_incident(
        self,
        incident_key: IncidentKey,
        data: IncidentResolutionRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    def search_incidents(
        self, data: IncidentSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> IncidentSearchQueryResult: ...
    def get_process_instance_statistics_by_error(
        self,
        data: IncidentProcessInstanceStatisticsByErrorQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> IncidentProcessInstanceStatisticsByErrorQueryResult: ...
    def get_incident(
        self, incident_key: IncidentKey, **kwargs: Any
    ) -> IncidentResult: ...
    def get_decision_definition(
        self, decision_definition_key: DecisionDefinitionKey, **kwargs: Any
    ) -> DecisionDefinitionResult: ...
    def evaluate_decision(
        self, data: DecisionEvaluationByID | DecisionEvaluationByKey, **kwargs: Any
    ) -> EvaluateDecisionResult: ...
    def search_decision_definitions(
        self, data: DecisionDefinitionSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> DecisionDefinitionSearchQueryResult: ...
    def get_decision_definition_xml(
        self, decision_definition_key: DecisionDefinitionKey, **kwargs: Any
    ) -> str: ...
    def evaluate_expression(
        self, data: ExpressionEvaluationRequest, **kwargs: Any
    ) -> ExpressionEvaluationResult: ...
    def unassign_user_task(self, user_task_key: UserTaskKey, **kwargs: Any) -> None: ...
    def search_user_task_variables(
        self,
        user_task_key: UserTaskKey,
        data: SearchUserTaskVariablesData | Unset = UNSET,
        truncate_values: bool | Unset = UNSET,
        **kwargs: Any,
    ) -> VariableSearchQueryResult: ...
    def assign_user_task(
        self, user_task_key: UserTaskKey, data: UserTaskAssignmentRequest, **kwargs: Any
    ) -> None: ...
    def update_user_task(
        self,
        user_task_key: UserTaskKey,
        data: UserTaskUpdateRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    def get_user_task_form(
        self, user_task_key: UserTaskKey, **kwargs: Any
    ) -> GetUserTaskFormResponse200: ...
    def get_user_task(
        self, user_task_key: UserTaskKey, **kwargs: Any
    ) -> GetUserTaskResponse200: ...
    def search_user_task_audit_logs(
        self,
        user_task_key: UserTaskKey,
        data: SearchUserTaskAuditLogsData | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchUserTaskAuditLogsResponse200: ...
    def search_user_tasks(
        self, data: SearchUserTasksData | Unset = UNSET, **kwargs: Any
    ) -> SearchUserTasksResponse200: ...
    def complete_user_task(
        self,
        user_task_key: UserTaskKey,
        data: UserTaskCompletionRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    def delete_resource(
        self,
        resource_key: str,
        data: DeleteResourceDataType0 | None | Unset = UNSET,
        **kwargs: Any,
    ) -> DeleteResourceResponse: ...
    def get_resource_content(self, resource_key: str, **kwargs: Any) -> File: ...
    def create_deployment(
        self, data: CreateDeploymentData, **kwargs: Any
    ) -> CreateDeploymentResponse200: ...
    def get_resource(self, resource_key: str, **kwargs: Any) -> ResourceResult: ...
    def update_authorization(
        self,
        authorization_key: AuthorizationKey,
        data: AuthorizationIdBasedRequest | AuthorizationPropertyBasedRequest,
        **kwargs: Any,
    ) -> None: ...
    def create_authorization(
        self,
        data: AuthorizationIdBasedRequest | AuthorizationPropertyBasedRequest,
        **kwargs: Any,
    ) -> AuthorizationCreateResult: ...
    def search_authorizations(
        self, data: AuthorizationSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> AuthorizationSearchResult: ...
    def get_authorization(
        self, authorization_key: AuthorizationKey, **kwargs: Any
    ) -> AuthorizationResult: ...
    def delete_authorization(
        self, authorization_key: AuthorizationKey, **kwargs: Any
    ) -> None: ...
    def get_decision_requirements_xml(
        self, decision_requirements_key: DecisionRequirementsKey, **kwargs: Any
    ) -> str: ...
    def search_decision_requirements(
        self, data: DecisionRequirementsSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> DecisionRequirementsSearchQueryResult: ...
    def get_decision_requirements(
        self, decision_requirements_key: DecisionRequirementsKey, **kwargs: Any
    ) -> DecisionRequirementsResult: ...
    def get_authentication(self, **kwargs: Any) -> CamundaUserResult: ...
    def broadcast_signal(
        self, data: SignalBroadcastRequest, **kwargs: Any
    ) -> SignalBroadcastResult: ...
    def update_mapping_rule(
        self,
        mapping_rule_id: str,
        data: MappingRuleUpdateRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> MappingRuleUpdateResult: ...
    def delete_mapping_rule(self, mapping_rule_id: str, **kwargs: Any) -> None: ...
    def create_mapping_rule(
        self, data: MappingRuleCreateRequest | Unset = UNSET, **kwargs: Any
    ) -> MappingRuleUpdateResult: ...
    def search_mapping_rule(
        self, data: MappingRuleSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> MappingRuleSearchQueryResult: ...
    def get_mapping_rule(
        self, mapping_rule_id: str, **kwargs: Any
    ) -> MappingRuleResult: ...
    def get_process_instance_sequence_flows(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> GetProcessInstanceSequenceFlowsResponse200: ...
    def get_process_instance_call_hierarchy(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> list[Any]: ...
    def modify_process_instance(
        self,
        process_instance_key: ProcessInstanceKey,
        data: ModifyProcessInstanceData,
        **kwargs: Any,
    ) -> None: ...
    def get_process_instance_statistics(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> GetProcessInstanceStatisticsResponse200: ...
    def migrate_process_instances_batch_operation(
        self, data: MigrateProcessInstancesBatchOperationData, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    def get_process_instance(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> GetProcessInstanceResponse200: ...
    def resolve_incidents_batch_operation(
        self, data: ResolveIncidentsBatchOperationData | Unset = UNSET, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    def modify_process_instances_batch_operation(
        self, data: ModifyProcessInstancesBatchOperationData, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    def delete_process_instance(
        self,
        process_instance_key: ProcessInstanceKey,
        data: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
        **kwargs: Any,
    ) -> BatchOperationCreatedResult: ...
    def delete_process_instances_batch_operation(
        self, data: DeleteProcessInstancesBatchOperationData, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    def cancel_process_instances_batch_operation(
        self, data: CancelProcessInstancesBatchOperationData, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    def create_process_instance(
        self, data: ProcessCreationById | ProcessCreationByKey, **kwargs: Any
    ) -> CreateProcessInstanceResult: ...
    def cancel_process_instance(
        self,
        process_instance_key: ProcessInstanceKey,
        data: CancelProcessInstanceDataType0 | None | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    def search_process_instance_incidents(
        self,
        process_instance_key: ProcessInstanceKey,
        data: IncidentSearchQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> IncidentSearchQueryResult: ...
    def migrate_process_instance(
        self,
        process_instance_key: ProcessInstanceKey,
        data: MigrateProcessInstanceData,
        **kwargs: Any,
    ) -> None: ...
    def search_process_instances(
        self, data: SearchProcessInstancesData | Unset = UNSET, **kwargs: Any
    ) -> SearchProcessInstancesResponse200: ...
    def resolve_process_instance_incidents(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    def pin_clock(self, data: ClockPinRequest, **kwargs: Any) -> None: ...
    def reset_clock(self, **kwargs: Any) -> None: ...
    def get_process_definition_instance_version_statistics(
        self,
        process_definition_id: ProcessDefinitionId,
        data: ProcessDefinitionInstanceVersionStatisticsQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> ProcessDefinitionInstanceVersionStatisticsQueryResult: ...
    def get_process_definition_instance_statistics(
        self,
        data: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> ProcessDefinitionInstanceStatisticsQueryResult: ...
    def search_process_definitions(
        self, data: SearchProcessDefinitionsData | Unset = UNSET, **kwargs: Any
    ) -> ProcessDefinitionSearchQueryResult: ...
    def get_process_definition_message_subscription_statistics(
        self,
        data: ProcessDefinitionMessageSubscriptionStatisticsQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> ProcessDefinitionMessageSubscriptionStatisticsQueryResult: ...
    def get_start_process_form(
        self, process_definition_key: ProcessDefinitionKey, **kwargs: Any
    ) -> GetStartProcessFormResponse200: ...
    def get_process_definition_xml(
        self, process_definition_key: ProcessDefinitionKey, **kwargs: Any
    ) -> str: ...
    def get_process_definition(
        self, process_definition_key: ProcessDefinitionKey, **kwargs: Any
    ) -> ProcessDefinitionResult: ...
    def get_process_definition_statistics(
        self,
        process_definition_key: ProcessDefinitionKey,
        data: GetProcessDefinitionStatisticsData | Unset = UNSET,
        **kwargs: Any,
    ) -> GetProcessDefinitionStatisticsResponse200: ...

class CamundaAsyncClient:
    client: Client | AuthenticatedClient
    configuration: CamundaSdkConfiguration
    auth_provider: AuthProvider
    _workers: list[JobWorker]
    def __init__(
        self,
        configuration: CamundaSdkConfigPartial | None = None,
        auth_provider: AuthProvider | None = None,
        logger: CamundaLogger | None = None,
        **kwargs: Any,
    ) -> None: ...
    async def __aenter__(self) -> "CamundaAsyncClient": ...
    async def __aexit__(self, *args: Any, **kwargs: Any) -> None: ...
    async def aclose(self) -> None: ...
    def create_job_worker(
        self, config: WorkerConfig, callback: JobHandler, auto_start: bool = True
    ) -> JobWorker: ...
    async def run_workers(self) -> None: ...
    async def deploy_resources_from_files(
        self, files: list[str | Path], tenant_id: str | None = None
    ) -> ExtendedDeploymentResult: ...
    async def delete_tenant(self, tenant_id: TenantId, **kwargs: Any) -> None: ...
    async def assign_group_to_tenant(
        self, tenant_id: TenantId, group_id: str, **kwargs: Any
    ) -> None: ...
    async def unassign_role_from_tenant(
        self, tenant_id: TenantId, role_id: str, **kwargs: Any
    ) -> None: ...
    async def search_group_ids_for_tenant(
        self,
        tenant_id: TenantId,
        data: SearchGroupIdsForTenantData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantGroupSearchResult: ...
    async def search_users_for_tenant(
        self,
        tenant_id: TenantId,
        data: SearchUsersForTenantData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantUserSearchResult: ...
    async def unassign_client_from_tenant(
        self, tenant_id: TenantId, client_id: str, **kwargs: Any
    ) -> None: ...
    async def unassign_user_from_tenant(
        self, tenant_id: TenantId, username: Username, **kwargs: Any
    ) -> None: ...
    async def search_roles_for_tenant(
        self,
        tenant_id: TenantId,
        data: RoleSearchQueryRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchQueryResponse: ...
    async def unassign_group_from_tenant(
        self, tenant_id: TenantId, group_id: str, **kwargs: Any
    ) -> None: ...
    async def search_clients_for_tenant(
        self,
        tenant_id: TenantId,
        data: SearchClientsForTenantData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantClientSearchResult: ...
    async def search_tenants(
        self, data: SearchTenantsData | Unset = UNSET, **kwargs: Any
    ) -> TenantSearchQueryResult: ...
    async def assign_user_to_tenant(
        self, tenant_id: TenantId, username: Username, **kwargs: Any
    ) -> None: ...
    async def assign_role_to_tenant(
        self, tenant_id: TenantId, role_id: str, **kwargs: Any
    ) -> None: ...
    async def search_mapping_rules_for_tenant(
        self,
        tenant_id: TenantId,
        data: MappingRuleSearchQueryRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchQueryResponse: ...
    async def assign_mapping_rule_to_tenant(
        self, tenant_id: TenantId, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    async def update_tenant(
        self, tenant_id: TenantId, data: TenantUpdateRequest, **kwargs: Any
    ) -> TenantUpdateResult: ...
    async def assign_client_to_tenant(
        self, tenant_id: TenantId, client_id: str, **kwargs: Any
    ) -> None: ...
    async def get_tenant(self, tenant_id: TenantId, **kwargs: Any) -> TenantResult: ...
    async def create_tenant(
        self, data: TenantCreateRequest, **kwargs: Any
    ) -> TenantCreateResult: ...
    async def unassign_mapping_rule_from_tenant(
        self, tenant_id: TenantId, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    async def cancel_batch_operation(
        self,
        batch_operation_key: BatchOperationKey,
        data: Any | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    async def resume_batch_operation(
        self,
        batch_operation_key: BatchOperationKey,
        data: Any | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    async def suspend_batch_operation(
        self,
        batch_operation_key: BatchOperationKey,
        data: Any | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    async def search_batch_operations(
        self, data: SearchBatchOperationsData | Unset = UNSET, **kwargs: Any
    ) -> BatchOperationSearchQueryResult: ...
    async def get_batch_operation(
        self, batch_operation_key: BatchOperationKey, **kwargs: Any
    ) -> BatchOperationResponse: ...
    async def search_batch_operation_items(
        self, data: SearchBatchOperationItemsData | Unset = UNSET, **kwargs: Any
    ) -> BatchOperationItemSearchQueryResult: ...
    async def get_topology(self, **kwargs: Any) -> TopologyResponse: ...
    async def unassign_role_from_group(
        self, role_id: str, group_id: str, **kwargs: Any
    ) -> None: ...
    async def search_users_for_role(
        self, role_id: str, data: SearchUsersForRoleData | Unset = UNSET, **kwargs: Any
    ) -> TenantUserSearchResult: ...
    async def unassign_role_from_mapping_rule(
        self, role_id: str, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    async def search_roles(
        self, data: RoleSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> RoleSearchQueryResult: ...
    async def unassign_role_from_client(
        self, role_id: str, client_id: str, **kwargs: Any
    ) -> None: ...
    async def unassign_role_from_user(
        self, role_id: str, username: Username, **kwargs: Any
    ) -> None: ...
    async def create_role(
        self, data: RoleCreateRequest | Unset = UNSET, **kwargs: Any
    ) -> RoleCreateResult: ...
    async def search_clients_for_role(
        self,
        role_id: str,
        data: SearchClientsForRoleData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantClientSearchResult: ...
    async def assign_role_to_user(
        self, role_id: str, username: Username, **kwargs: Any
    ) -> None: ...
    async def search_groups_for_role(
        self, role_id: str, data: SearchGroupsForRoleData | Unset = UNSET, **kwargs: Any
    ) -> RoleGroupSearchResult: ...
    async def update_role(
        self, role_id: str, data: RoleUpdateRequest, **kwargs: Any
    ) -> RoleUpdateResult: ...
    async def assign_role_to_group(
        self, role_id: str, group_id: str, **kwargs: Any
    ) -> None: ...
    async def search_mapping_rules_for_role(
        self,
        role_id: str,
        data: MappingRuleSearchQueryRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchQueryResponse: ...
    async def assign_role_to_client(
        self, role_id: str, client_id: str, **kwargs: Any
    ) -> None: ...
    async def delete_role(self, role_id: str, **kwargs: Any) -> None: ...
    async def assign_role_to_mapping_rule(
        self, role_id: str, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    async def get_role(self, role_id: str, **kwargs: Any) -> RoleResult: ...
    async def evaluate_conditionals(
        self, data: ConditionalEvaluationInstruction, **kwargs: Any
    ) -> EvaluateConditionalResult: ...
    async def get_license(self, **kwargs: Any) -> LicenseResponse: ...
    async def search_decision_instances(
        self, data: DecisionInstanceSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> DecisionInstanceSearchQueryResult: ...
    async def get_decision_instance(
        self,
        decision_evaluation_instance_key: DecisionEvaluationInstanceKey,
        **kwargs: Any,
    ) -> DecisionInstanceGetQueryResult: ...
    async def delete_decision_instance(
        self,
        decision_instance_key: DecisionInstanceKey,
        data: DeleteProcessInstanceRequestType0 | None | Unset = UNSET,
        **kwargs: Any,
    ) -> BatchOperationCreatedResult: ...
    async def delete_decision_instances_batch_operation(
        self, data: DecisionInstanceDeletionBatchOperationRequest, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    async def get_variable(
        self, variable_key: VariableKey, **kwargs: Any
    ) -> VariableResult: ...
    async def search_variables(
        self,
        data: SearchVariablesData | Unset = UNSET,
        truncate_values: bool | Unset = UNSET,
        **kwargs: Any,
    ) -> VariableSearchQueryResult: ...
    async def get_tenant_cluster_variable(
        self, tenant_id: TenantId, name: str, **kwargs: Any
    ) -> ClusterVariableResult: ...
    async def search_cluster_variables(
        self,
        data: ClusterVariableSearchQueryRequest | Unset = UNSET,
        truncate_values: bool | Unset = UNSET,
        **kwargs: Any,
    ) -> ClusterVariableSearchQueryResult: ...
    async def create_global_cluster_variable(
        self, data: CreateClusterVariableRequest, **kwargs: Any
    ) -> ClusterVariableResult: ...
    async def update_tenant_cluster_variable(
        self,
        tenant_id: TenantId,
        name: str,
        data: UpdateClusterVariableRequest,
        **kwargs: Any,
    ) -> ClusterVariableResult: ...
    async def delete_global_cluster_variable(
        self, name: str, **kwargs: Any
    ) -> None: ...
    async def delete_tenant_cluster_variable(
        self, tenant_id: TenantId, name: str, **kwargs: Any
    ) -> None: ...
    async def update_global_cluster_variable(
        self, name: str, data: UpdateClusterVariableRequest, **kwargs: Any
    ) -> ClusterVariableResult: ...
    async def create_tenant_cluster_variable(
        self, tenant_id: TenantId, data: CreateClusterVariableRequest, **kwargs: Any
    ) -> ClusterVariableResult: ...
    async def get_global_cluster_variable(
        self, name: str, **kwargs: Any
    ) -> ClusterVariableResult: ...
    async def unassign_mapping_rule_from_group(
        self, group_id: str, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    async def search_roles_for_group(
        self, group_id: str, data: RoleSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> SearchQueryResponse: ...
    async def assign_client_to_group(
        self, group_id: str, client_id: str, **kwargs: Any
    ) -> None: ...
    async def unassign_user_from_group(
        self, group_id: str, username: Username, **kwargs: Any
    ) -> None: ...
    async def search_users_for_group(
        self,
        group_id: str,
        data: SearchUsersForGroupData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantUserSearchResult: ...
    async def get_group(self, group_id: str, **kwargs: Any) -> GroupResult: ...
    async def unassign_client_from_group(
        self, group_id: str, client_id: str, **kwargs: Any
    ) -> None: ...
    async def update_group(
        self, group_id: str, data: GroupUpdateRequest, **kwargs: Any
    ) -> GroupUpdateResult: ...
    async def search_groups(
        self, data: GroupSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> GroupSearchQueryResult: ...
    async def assign_mapping_rule_to_group(
        self, group_id: str, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    async def search_mapping_rules_for_group(
        self,
        group_id: str,
        data: MappingRuleSearchQueryRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchQueryResponse: ...
    async def create_group(
        self, data: GroupCreateRequest | Unset = UNSET, **kwargs: Any
    ) -> GroupCreateResult: ...
    async def delete_group(self, group_id: str, **kwargs: Any) -> None: ...
    async def assign_user_to_group(
        self, group_id: str, username: Username, **kwargs: Any
    ) -> None: ...
    async def search_clients_for_group(
        self,
        group_id: str,
        data: SearchClientsForGroupData | Unset = UNSET,
        **kwargs: Any,
    ) -> TenantClientSearchResult: ...
    async def search_correlated_message_subscriptions(
        self,
        data: CorrelatedMessageSubscriptionSearchQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> CorrelatedMessageSubscriptionSearchQueryResult: ...
    async def search_message_subscriptions(
        self, data: SearchMessageSubscriptionsData | Unset = UNSET, **kwargs: Any
    ) -> SearchMessageSubscriptionsResponse200: ...
    async def create_admin_user(self, data: UserRequest, **kwargs: Any) -> None: ...
    async def publish_message(
        self, data: MessagePublicationRequest, **kwargs: Any
    ) -> PublishMessageResponse200: ...
    async def correlate_message(
        self, data: MessageCorrelationRequest, **kwargs: Any
    ) -> MessageCorrelationResult: ...
    async def create_user(
        self, data: UserRequest, **kwargs: Any
    ) -> UserCreateResult: ...
    async def search_users(
        self, data: SearchUsersData | Unset = UNSET, **kwargs: Any
    ) -> UserSearchResult: ...
    async def delete_user(self, username: Username, **kwargs: Any) -> None: ...
    async def get_user(self, username: Username, **kwargs: Any) -> UserResult: ...
    async def update_user(
        self, username: Username, data: UserUpdateRequest, **kwargs: Any
    ) -> UserResult: ...
    async def get_document(
        self,
        document_id: DocumentId,
        store_id: str | Unset = UNSET,
        content_hash: str | Unset = UNSET,
        **kwargs: Any,
    ) -> File: ...
    async def create_documents(
        self, data: CreateDocumentsData, store_id: str | Unset = UNSET, **kwargs: Any
    ) -> DocumentCreationBatchResponse: ...
    async def create_document_link(
        self,
        document_id: DocumentId,
        data: DocumentLinkRequest | Unset = UNSET,
        store_id: str | Unset = UNSET,
        content_hash: str | Unset = UNSET,
        **kwargs: Any,
    ) -> DocumentLink: ...
    async def delete_document(
        self, document_id: DocumentId, store_id: str | Unset = UNSET, **kwargs: Any
    ) -> None: ...
    async def create_document(
        self,
        data: CreateDocumentData,
        store_id: str | Unset = UNSET,
        document_id: str | Unset = UNSET,
        **kwargs: Any,
    ) -> DocumentReference: ...
    async def get_audit_log(
        self, audit_log_key: AuditLogKey, **kwargs: Any
    ) -> GetAuditLogResponse200: ...
    async def search_audit_logs(
        self, data: AuditLogSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> SearchAuditLogsResponse200: ...
    async def get_usage_metrics(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        tenant_id: str | Unset = UNSET,
        with_tenants: bool | Unset = False,
        **kwargs: Any,
    ) -> UsageMetricsResponse: ...
    async def search_element_instance_incidents(
        self,
        element_instance_key: ElementInstanceKey,
        data: IncidentSearchQuery,
        **kwargs: Any,
    ) -> IncidentSearchQueryResult: ...
    async def get_element_instance(
        self, element_instance_key: ElementInstanceKey, **kwargs: Any
    ) -> ElementInstanceResult: ...
    async def create_element_instance_variables(
        self,
        element_instance_key: ElementInstanceKey,
        data: SetVariableRequest,
        **kwargs: Any,
    ) -> None: ...
    async def search_element_instances(
        self, data: ElementInstanceSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> ElementInstanceSearchQueryResult: ...
    async def activate_ad_hoc_sub_process_activities(
        self,
        ad_hoc_sub_process_instance_key: str,
        data: AdHocSubProcessActivateActivitiesInstruction,
        **kwargs: Any,
    ) -> None: ...
    async def fail_job(
        self, job_key: JobKey, data: JobFailRequest | Unset = UNSET, **kwargs: Any
    ) -> None: ...
    async def search_jobs(
        self, data: JobSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> SearchJobsResponse200: ...
    async def activate_jobs(
        self, data: JobActivationRequest, **kwargs: Any
    ) -> ActivateJobsResponse200: ...
    async def get_global_job_statistics(
        self,
        from_: datetime.datetime,
        to: datetime.datetime,
        job_type: str | Unset = UNSET,
        **kwargs: Any,
    ) -> GlobalJobStatisticsQueryResult: ...
    async def throw_job_error(
        self, job_key: JobKey, data: JobErrorRequest, **kwargs: Any
    ) -> None: ...
    async def complete_job(
        self, job_key: JobKey, data: CompleteJobData | Unset = UNSET, **kwargs: Any
    ) -> None: ...
    async def update_job(
        self, job_key: JobKey, data: JobUpdateRequest, **kwargs: Any
    ) -> None: ...
    async def get_process_instance_statistics_by_definition(
        self, data: IncidentProcessInstanceStatisticsByDefinitionQuery, **kwargs: Any
    ) -> IncidentProcessInstanceStatisticsByDefinitionQueryResult: ...
    async def resolve_incident(
        self,
        incident_key: IncidentKey,
        data: IncidentResolutionRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    async def search_incidents(
        self, data: IncidentSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> IncidentSearchQueryResult: ...
    async def get_process_instance_statistics_by_error(
        self,
        data: IncidentProcessInstanceStatisticsByErrorQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> IncidentProcessInstanceStatisticsByErrorQueryResult: ...
    async def get_incident(
        self, incident_key: IncidentKey, **kwargs: Any
    ) -> IncidentResult: ...
    async def get_decision_definition(
        self, decision_definition_key: DecisionDefinitionKey, **kwargs: Any
    ) -> DecisionDefinitionResult: ...
    async def evaluate_decision(
        self, data: DecisionEvaluationByID | DecisionEvaluationByKey, **kwargs: Any
    ) -> EvaluateDecisionResult: ...
    async def search_decision_definitions(
        self, data: DecisionDefinitionSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> DecisionDefinitionSearchQueryResult: ...
    async def get_decision_definition_xml(
        self, decision_definition_key: DecisionDefinitionKey, **kwargs: Any
    ) -> str: ...
    async def evaluate_expression(
        self, data: ExpressionEvaluationRequest, **kwargs: Any
    ) -> ExpressionEvaluationResult: ...
    async def unassign_user_task(
        self, user_task_key: UserTaskKey, **kwargs: Any
    ) -> None: ...
    async def search_user_task_variables(
        self,
        user_task_key: UserTaskKey,
        data: SearchUserTaskVariablesData | Unset = UNSET,
        truncate_values: bool | Unset = UNSET,
        **kwargs: Any,
    ) -> VariableSearchQueryResult: ...
    async def assign_user_task(
        self, user_task_key: UserTaskKey, data: UserTaskAssignmentRequest, **kwargs: Any
    ) -> None: ...
    async def update_user_task(
        self,
        user_task_key: UserTaskKey,
        data: UserTaskUpdateRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    async def get_user_task_form(
        self, user_task_key: UserTaskKey, **kwargs: Any
    ) -> GetUserTaskFormResponse200: ...
    async def get_user_task(
        self, user_task_key: UserTaskKey, **kwargs: Any
    ) -> GetUserTaskResponse200: ...
    async def search_user_task_audit_logs(
        self,
        user_task_key: UserTaskKey,
        data: SearchUserTaskAuditLogsData | Unset = UNSET,
        **kwargs: Any,
    ) -> SearchUserTaskAuditLogsResponse200: ...
    async def search_user_tasks(
        self, data: SearchUserTasksData | Unset = UNSET, **kwargs: Any
    ) -> SearchUserTasksResponse200: ...
    async def complete_user_task(
        self,
        user_task_key: UserTaskKey,
        data: UserTaskCompletionRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    async def delete_resource(
        self,
        resource_key: str,
        data: DeleteResourceDataType0 | None | Unset = UNSET,
        **kwargs: Any,
    ) -> DeleteResourceResponse: ...
    async def get_resource_content(self, resource_key: str, **kwargs: Any) -> File: ...
    async def create_deployment(
        self, data: CreateDeploymentData, **kwargs: Any
    ) -> CreateDeploymentResponse200: ...
    async def get_resource(
        self, resource_key: str, **kwargs: Any
    ) -> ResourceResult: ...
    async def update_authorization(
        self,
        authorization_key: AuthorizationKey,
        data: AuthorizationIdBasedRequest | AuthorizationPropertyBasedRequest,
        **kwargs: Any,
    ) -> None: ...
    async def create_authorization(
        self,
        data: AuthorizationIdBasedRequest | AuthorizationPropertyBasedRequest,
        **kwargs: Any,
    ) -> AuthorizationCreateResult: ...
    async def search_authorizations(
        self, data: AuthorizationSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> AuthorizationSearchResult: ...
    async def get_authorization(
        self, authorization_key: AuthorizationKey, **kwargs: Any
    ) -> AuthorizationResult: ...
    async def delete_authorization(
        self, authorization_key: AuthorizationKey, **kwargs: Any
    ) -> None: ...
    async def get_decision_requirements_xml(
        self, decision_requirements_key: DecisionRequirementsKey, **kwargs: Any
    ) -> str: ...
    async def search_decision_requirements(
        self, data: DecisionRequirementsSearchQuery | Unset = UNSET, **kwargs: Any
    ) -> DecisionRequirementsSearchQueryResult: ...
    async def get_decision_requirements(
        self, decision_requirements_key: DecisionRequirementsKey, **kwargs: Any
    ) -> DecisionRequirementsResult: ...
    async def get_authentication(self, **kwargs: Any) -> CamundaUserResult: ...
    async def broadcast_signal(
        self, data: SignalBroadcastRequest, **kwargs: Any
    ) -> SignalBroadcastResult: ...
    async def update_mapping_rule(
        self,
        mapping_rule_id: str,
        data: MappingRuleUpdateRequest | Unset = UNSET,
        **kwargs: Any,
    ) -> MappingRuleUpdateResult: ...
    async def delete_mapping_rule(
        self, mapping_rule_id: str, **kwargs: Any
    ) -> None: ...
    async def create_mapping_rule(
        self, data: MappingRuleCreateRequest | Unset = UNSET, **kwargs: Any
    ) -> MappingRuleUpdateResult: ...
    async def search_mapping_rule(
        self, data: MappingRuleSearchQueryRequest | Unset = UNSET, **kwargs: Any
    ) -> MappingRuleSearchQueryResult: ...
    async def get_mapping_rule(
        self, mapping_rule_id: str, **kwargs: Any
    ) -> MappingRuleResult: ...
    async def get_process_instance_sequence_flows(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> GetProcessInstanceSequenceFlowsResponse200: ...
    async def get_process_instance_call_hierarchy(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> list[Any]: ...
    async def modify_process_instance(
        self,
        process_instance_key: ProcessInstanceKey,
        data: ModifyProcessInstanceData,
        **kwargs: Any,
    ) -> None: ...
    async def get_process_instance_statistics(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> GetProcessInstanceStatisticsResponse200: ...
    async def migrate_process_instances_batch_operation(
        self, data: MigrateProcessInstancesBatchOperationData, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    async def get_process_instance(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> GetProcessInstanceResponse200: ...
    async def resolve_incidents_batch_operation(
        self, data: ResolveIncidentsBatchOperationData | Unset = UNSET, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    async def modify_process_instances_batch_operation(
        self, data: ModifyProcessInstancesBatchOperationData, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    async def delete_process_instance(
        self,
        process_instance_key: ProcessInstanceKey,
        data: DeleteProcessInstanceDataType0 | None | Unset = UNSET,
        **kwargs: Any,
    ) -> BatchOperationCreatedResult: ...
    async def delete_process_instances_batch_operation(
        self, data: DeleteProcessInstancesBatchOperationData, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    async def cancel_process_instances_batch_operation(
        self, data: CancelProcessInstancesBatchOperationData, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    async def create_process_instance(
        self, data: ProcessCreationById | ProcessCreationByKey, **kwargs: Any
    ) -> CreateProcessInstanceResult: ...
    async def cancel_process_instance(
        self,
        process_instance_key: ProcessInstanceKey,
        data: CancelProcessInstanceDataType0 | None | Unset = UNSET,
        **kwargs: Any,
    ) -> None: ...
    async def search_process_instance_incidents(
        self,
        process_instance_key: ProcessInstanceKey,
        data: IncidentSearchQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> IncidentSearchQueryResult: ...
    async def migrate_process_instance(
        self,
        process_instance_key: ProcessInstanceKey,
        data: MigrateProcessInstanceData,
        **kwargs: Any,
    ) -> None: ...
    async def search_process_instances(
        self, data: SearchProcessInstancesData | Unset = UNSET, **kwargs: Any
    ) -> SearchProcessInstancesResponse200: ...
    async def resolve_process_instance_incidents(
        self, process_instance_key: ProcessInstanceKey, **kwargs: Any
    ) -> BatchOperationCreatedResult: ...
    async def pin_clock(self, data: ClockPinRequest, **kwargs: Any) -> None: ...
    async def reset_clock(self, **kwargs: Any) -> None: ...
    async def get_process_definition_instance_version_statistics(
        self,
        process_definition_id: ProcessDefinitionId,
        data: ProcessDefinitionInstanceVersionStatisticsQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> ProcessDefinitionInstanceVersionStatisticsQueryResult: ...
    async def get_process_definition_instance_statistics(
        self,
        data: ProcessDefinitionInstanceStatisticsQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> ProcessDefinitionInstanceStatisticsQueryResult: ...
    async def search_process_definitions(
        self, data: SearchProcessDefinitionsData | Unset = UNSET, **kwargs: Any
    ) -> ProcessDefinitionSearchQueryResult: ...
    async def get_process_definition_message_subscription_statistics(
        self,
        data: ProcessDefinitionMessageSubscriptionStatisticsQuery | Unset = UNSET,
        **kwargs: Any,
    ) -> ProcessDefinitionMessageSubscriptionStatisticsQueryResult: ...
    async def get_start_process_form(
        self, process_definition_key: ProcessDefinitionKey, **kwargs: Any
    ) -> GetStartProcessFormResponse200: ...
    async def get_process_definition_xml(
        self, process_definition_key: ProcessDefinitionKey, **kwargs: Any
    ) -> str: ...
    async def get_process_definition(
        self, process_definition_key: ProcessDefinitionKey, **kwargs: Any
    ) -> ProcessDefinitionResult: ...
    async def get_process_definition_statistics(
        self,
        process_definition_key: ProcessDefinitionKey,
        data: GetProcessDefinitionStatisticsData | Unset = UNSET,
        **kwargs: Any,
    ) -> GetProcessDefinitionStatisticsResponse200: ...
