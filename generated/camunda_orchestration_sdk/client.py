from __future__ import annotations
import ssl
from typing import Any

import httpx
from attrs import define, evolve, field


from .types import UNSET, Unset, str_any_dict_factory, str_str_dict_factory
from typing import TYPE_CHECKING
import asyncio
from .runtime.job_worker import JobWorker, WorkerConfig, JobHandler
from .runtime.configuration_resolver import CamundaSdkConfigPartial, CamundaSdkConfiguration, ConfigurationResolver, read_environment
from .runtime.auth import AuthProvider, BasicAuthProvider, NullAuthProvider, OAuthClientCredentialsAuthProvider, AsyncOAuthClientCredentialsAuthProvider, inject_auth_event_hooks
from pathlib import Path
from .models.create_deployment_response_200 import CreateDeploymentResponse200
from .models.create_deployment_response_200_deployments_item_process_definition import CreateDeploymentResponse200DeploymentsItemProcessDefinition
from .models.create_deployment_response_200_deployments_item_decision_definition import CreateDeploymentResponse200DeploymentsItemDecisionDefinition
from .models.create_deployment_response_200_deployments_item_decision_requirements import CreateDeploymentResponse200DeploymentsItemDecisionRequirements
from .models.create_deployment_response_200_deployments_item_form import CreateDeploymentResponse200DeploymentsItemForm

if TYPE_CHECKING:
    from .models.activate_ad_hoc_sub_process_activities_data import ActivateAdHocSubProcessActivitiesData
    from .models.activate_jobs_data import ActivateJobsData
    from .models.activate_jobs_response_200 import ActivateJobsResponse200
    from .models.assign_user_task_data import AssignUserTaskData
    from .models.broadcast_signal_data import BroadcastSignalData
    from .models.broadcast_signal_response_200 import BroadcastSignalResponse200
    from .models.cancel_process_instance_data_type_0 import CancelProcessInstanceDataType0
    from .models.cancel_process_instances_batch_operation_data import CancelProcessInstancesBatchOperationData
    from .models.cancel_process_instances_batch_operation_response_200 import CancelProcessInstancesBatchOperationResponse200
    from .models.complete_job_data import CompleteJobData
    from .models.complete_user_task_data import CompleteUserTaskData
    from .models.correlate_message_data import CorrelateMessageData
    from .models.correlate_message_response_200 import CorrelateMessageResponse200
    from .models.create_admin_user_data import CreateAdminUserData
    from .models.create_authorization_response_201 import CreateAuthorizationResponse201
    from .models.create_deployment_data import CreateDeploymentData
    from .models.create_deployment_response_200 import CreateDeploymentResponse200
    from .models.create_document_data import CreateDocumentData
    from .models.create_document_link_data import CreateDocumentLinkData
    from .models.create_document_link_response_201 import CreateDocumentLinkResponse201
    from .models.create_document_response_201 import CreateDocumentResponse201
    from .models.create_documents_data import CreateDocumentsData
    from .models.create_documents_response_201 import CreateDocumentsResponse201
    from .models.create_element_instance_variables_data import CreateElementInstanceVariablesData
    from .models.create_global_cluster_variable_data import CreateGlobalClusterVariableData
    from .models.create_global_cluster_variable_response_200 import CreateGlobalClusterVariableResponse200
    from .models.create_group_data import CreateGroupData
    from .models.create_group_response_201 import CreateGroupResponse201
    from .models.create_mapping_rule_data import CreateMappingRuleData
    from .models.create_mapping_rule_response_201 import CreateMappingRuleResponse201
    from .models.create_process_instance_response_200 import CreateProcessInstanceResponse200
    from .models.create_role_data import CreateRoleData
    from .models.create_role_response_201 import CreateRoleResponse201
    from .models.create_tenant_cluster_variable_data import CreateTenantClusterVariableData
    from .models.create_tenant_cluster_variable_response_200 import CreateTenantClusterVariableResponse200
    from .models.create_tenant_data import CreateTenantData
    from .models.create_tenant_response_201 import CreateTenantResponse201
    from .models.create_user_data import CreateUserData
    from .models.create_user_response_201 import CreateUserResponse201
    from .models.decisionevaluationby_id import DecisionevaluationbyID
    from .models.decisionevaluationbykey import Decisionevaluationbykey
    from .models.delete_decision_instance_data_type_0 import DeleteDecisionInstanceDataType0
    from .models.delete_decision_instance_response_200 import DeleteDecisionInstanceResponse200
    from .models.delete_decision_instances_batch_operation_data import DeleteDecisionInstancesBatchOperationData
    from .models.delete_decision_instances_batch_operation_response_200 import DeleteDecisionInstancesBatchOperationResponse200
    from .models.delete_process_instance_data_type_0 import DeleteProcessInstanceDataType0
    from .models.delete_process_instance_response_200 import DeleteProcessInstanceResponse200
    from .models.delete_process_instances_batch_operation_data import DeleteProcessInstancesBatchOperationData
    from .models.delete_process_instances_batch_operation_response_200 import DeleteProcessInstancesBatchOperationResponse200
    from .models.delete_resource_data_type_0 import DeleteResourceDataType0
    from .models.delete_resource_response_200 import DeleteResourceResponse200
    from .models.evaluate_conditionals_data import EvaluateConditionalsData
    from .models.evaluate_conditionals_response_200 import EvaluateConditionalsResponse200
    from .models.evaluate_decision_response_200 import EvaluateDecisionResponse200
    from .models.evaluate_expression_data import EvaluateExpressionData
    from .models.evaluate_expression_response_200 import EvaluateExpressionResponse200
    from .models.fail_job_data import FailJobData
    from .models.get_audit_log_response_200 import GetAuditLogResponse200
    from .models.get_authentication_response_200 import GetAuthenticationResponse200
    from .models.get_authorization_response_200 import GetAuthorizationResponse200
    from .models.get_batch_operation_response_200 import GetBatchOperationResponse200
    from .models.get_decision_definition_response_200 import GetDecisionDefinitionResponse200
    from .models.get_decision_instance_response_200 import GetDecisionInstanceResponse200
    from .models.get_decision_requirements_response_200 import GetDecisionRequirementsResponse200
    from .models.get_element_instance_response_200 import GetElementInstanceResponse200
    from .models.get_global_cluster_variable_response_200 import GetGlobalClusterVariableResponse200
    from .models.get_global_job_statistics_response_200 import GetGlobalJobStatisticsResponse200
    from .models.get_group_response_200 import GetGroupResponse200
    from .models.get_incident_response_200 import GetIncidentResponse200
    from .models.get_license_response_200 import GetLicenseResponse200
    from .models.get_mapping_rule_response_200 import GetMappingRuleResponse200
    from .models.get_process_definition_instance_statistics_data import GetProcessDefinitionInstanceStatisticsData
    from .models.get_process_definition_instance_statistics_response_200 import GetProcessDefinitionInstanceStatisticsResponse200
    from .models.get_process_definition_instance_version_statistics_data import GetProcessDefinitionInstanceVersionStatisticsData
    from .models.get_process_definition_instance_version_statistics_response_200 import GetProcessDefinitionInstanceVersionStatisticsResponse200
    from .models.get_process_definition_message_subscription_statistics_data import GetProcessDefinitionMessageSubscriptionStatisticsData
    from .models.get_process_definition_message_subscription_statistics_response_200 import GetProcessDefinitionMessageSubscriptionStatisticsResponse200
    from .models.get_process_definition_response_200 import GetProcessDefinitionResponse200
    from .models.get_process_definition_statistics_data import GetProcessDefinitionStatisticsData
    from .models.get_process_definition_statistics_response_200 import GetProcessDefinitionStatisticsResponse200
    from .models.get_process_instance_response_200 import GetProcessInstanceResponse200
    from .models.get_process_instance_sequence_flows_response_200 import GetProcessInstanceSequenceFlowsResponse200
    from .models.get_process_instance_statistics_by_definition_data import GetProcessInstanceStatisticsByDefinitionData
    from .models.get_process_instance_statistics_by_definition_response_200 import GetProcessInstanceStatisticsByDefinitionResponse200
    from .models.get_process_instance_statistics_by_error_data import GetProcessInstanceStatisticsByErrorData
    from .models.get_process_instance_statistics_by_error_response_200 import GetProcessInstanceStatisticsByErrorResponse200
    from .models.get_process_instance_statistics_response_200 import GetProcessInstanceStatisticsResponse200
    from .models.get_resource_response_200 import GetResourceResponse200
    from .models.get_role_response_200 import GetRoleResponse200
    from .models.get_start_process_form_response_200 import GetStartProcessFormResponse200
    from .models.get_tenant_cluster_variable_response_200 import GetTenantClusterVariableResponse200
    from .models.get_tenant_response_200 import GetTenantResponse200
    from .models.get_topology_response_200 import GetTopologyResponse200
    from .models.get_usage_metrics_response_200 import GetUsageMetricsResponse200
    from .models.get_user_response_200 import GetUserResponse200
    from .models.get_user_task_form_response_200 import GetUserTaskFormResponse200
    from .models.get_user_task_response_200 import GetUserTaskResponse200
    from .models.get_variable_response_200 import GetVariableResponse200
    from .models.migrate_process_instance_data import MigrateProcessInstanceData
    from .models.migrate_process_instances_batch_operation_data import MigrateProcessInstancesBatchOperationData
    from .models.migrate_process_instances_batch_operation_response_200 import MigrateProcessInstancesBatchOperationResponse200
    from .models.modify_process_instance_data import ModifyProcessInstanceData
    from .models.modify_process_instances_batch_operation_data import ModifyProcessInstancesBatchOperationData
    from .models.modify_process_instances_batch_operation_response_200 import ModifyProcessInstancesBatchOperationResponse200
    from .models.object_ import Object
    from .models.object_1 import Object1
    from .models.pin_clock_data import PinClockData
    from .models.processcreationbyid import Processcreationbyid
    from .models.processcreationbykey import Processcreationbykey
    from .models.publish_message_data import PublishMessageData
    from .models.publish_message_response_200 import PublishMessageResponse200
    from .models.resolve_incident_data import ResolveIncidentData
    from .models.resolve_incidents_batch_operation_data import ResolveIncidentsBatchOperationData
    from .models.resolve_incidents_batch_operation_response_200 import ResolveIncidentsBatchOperationResponse200
    from .models.resolve_process_instance_incidents_response_200 import ResolveProcessInstanceIncidentsResponse200
    from .models.search_audit_logs_data import SearchAuditLogsData
    from .models.search_audit_logs_response_200 import SearchAuditLogsResponse200
    from .models.search_authorizations_data import SearchAuthorizationsData
    from .models.search_authorizations_response_200 import SearchAuthorizationsResponse200
    from .models.search_batch_operation_items_data import SearchBatchOperationItemsData
    from .models.search_batch_operation_items_response_200 import SearchBatchOperationItemsResponse200
    from .models.search_batch_operations_data import SearchBatchOperationsData
    from .models.search_batch_operations_response_200 import SearchBatchOperationsResponse200
    from .models.search_clients_for_group_data import SearchClientsForGroupData
    from .models.search_clients_for_group_response_200 import SearchClientsForGroupResponse200
    from .models.search_clients_for_role_data import SearchClientsForRoleData
    from .models.search_clients_for_role_response_200 import SearchClientsForRoleResponse200
    from .models.search_clients_for_tenant_data import SearchClientsForTenantData
    from .models.search_clients_for_tenant_response_200 import SearchClientsForTenantResponse200
    from .models.search_cluster_variables_data import SearchClusterVariablesData
    from .models.search_cluster_variables_response_200 import SearchClusterVariablesResponse200
    from .models.search_correlated_message_subscriptions_data import SearchCorrelatedMessageSubscriptionsData
    from .models.search_correlated_message_subscriptions_response_200 import SearchCorrelatedMessageSubscriptionsResponse200
    from .models.search_decision_definitions_data import SearchDecisionDefinitionsData
    from .models.search_decision_definitions_response_200 import SearchDecisionDefinitionsResponse200
    from .models.search_decision_instances_data import SearchDecisionInstancesData
    from .models.search_decision_instances_response_200 import SearchDecisionInstancesResponse200
    from .models.search_decision_requirements_data import SearchDecisionRequirementsData
    from .models.search_decision_requirements_response_200 import SearchDecisionRequirementsResponse200
    from .models.search_element_instance_incidents_data import SearchElementInstanceIncidentsData
    from .models.search_element_instance_incidents_response_200 import SearchElementInstanceIncidentsResponse200
    from .models.search_element_instances_data import SearchElementInstancesData
    from .models.search_element_instances_response_200 import SearchElementInstancesResponse200
    from .models.search_group_ids_for_tenant_data import SearchGroupIdsForTenantData
    from .models.search_group_ids_for_tenant_response_200 import SearchGroupIdsForTenantResponse200
    from .models.search_groups_data import SearchGroupsData
    from .models.search_groups_for_role_data import SearchGroupsForRoleData
    from .models.search_groups_for_role_response_200 import SearchGroupsForRoleResponse200
    from .models.search_groups_response_200 import SearchGroupsResponse200
    from .models.search_incidents_data import SearchIncidentsData
    from .models.search_incidents_response_200 import SearchIncidentsResponse200
    from .models.search_jobs_data import SearchJobsData
    from .models.search_jobs_response_200 import SearchJobsResponse200
    from .models.search_mapping_rule_data import SearchMappingRuleData
    from .models.search_mapping_rule_response_200 import SearchMappingRuleResponse200
    from .models.search_mapping_rules_for_group_data import SearchMappingRulesForGroupData
    from .models.search_mapping_rules_for_group_response_200 import SearchMappingRulesForGroupResponse200
    from .models.search_mapping_rules_for_role_data import SearchMappingRulesForRoleData
    from .models.search_mapping_rules_for_role_response_200 import SearchMappingRulesForRoleResponse200
    from .models.search_mapping_rules_for_tenant_data import SearchMappingRulesForTenantData
    from .models.search_mapping_rules_for_tenant_response_200 import SearchMappingRulesForTenantResponse200
    from .models.search_message_subscriptions_data import SearchMessageSubscriptionsData
    from .models.search_message_subscriptions_response_200 import SearchMessageSubscriptionsResponse200
    from .models.search_process_definitions_data import SearchProcessDefinitionsData
    from .models.search_process_definitions_response_200 import SearchProcessDefinitionsResponse200
    from .models.search_process_instance_incidents_data import SearchProcessInstanceIncidentsData
    from .models.search_process_instance_incidents_response_200 import SearchProcessInstanceIncidentsResponse200
    from .models.search_process_instances_data import SearchProcessInstancesData
    from .models.search_process_instances_response_200 import SearchProcessInstancesResponse200
    from .models.search_roles_data import SearchRolesData
    from .models.search_roles_for_group_data import SearchRolesForGroupData
    from .models.search_roles_for_group_response_200 import SearchRolesForGroupResponse200
    from .models.search_roles_for_tenant_data import SearchRolesForTenantData
    from .models.search_roles_for_tenant_response_200 import SearchRolesForTenantResponse200
    from .models.search_roles_response_200 import SearchRolesResponse200
    from .models.search_tenants_data import SearchTenantsData
    from .models.search_tenants_response_200 import SearchTenantsResponse200
    from .models.search_user_task_audit_logs_data import SearchUserTaskAuditLogsData
    from .models.search_user_task_audit_logs_response_200 import SearchUserTaskAuditLogsResponse200
    from .models.search_user_task_variables_data import SearchUserTaskVariablesData
    from .models.search_user_task_variables_response_200 import SearchUserTaskVariablesResponse200
    from .models.search_user_tasks_data import SearchUserTasksData
    from .models.search_user_tasks_response_200 import SearchUserTasksResponse200
    from .models.search_users_data import SearchUsersData
    from .models.search_users_for_group_data import SearchUsersForGroupData
    from .models.search_users_for_group_response_200 import SearchUsersForGroupResponse200
    from .models.search_users_for_role_data import SearchUsersForRoleData
    from .models.search_users_for_role_response_200 import SearchUsersForRoleResponse200
    from .models.search_users_for_tenant_data import SearchUsersForTenantData
    from .models.search_users_for_tenant_response_200 import SearchUsersForTenantResponse200
    from .models.search_users_response_200 import SearchUsersResponse200
    from .models.search_variables_data import SearchVariablesData
    from .models.search_variables_response_200 import SearchVariablesResponse200
    from .models.throw_job_error_data import ThrowJobErrorData
    from .models.update_global_cluster_variable_data import UpdateGlobalClusterVariableData
    from .models.update_global_cluster_variable_response_200 import UpdateGlobalClusterVariableResponse200
    from .models.update_group_data import UpdateGroupData
    from .models.update_group_response_200 import UpdateGroupResponse200
    from .models.update_job_data import UpdateJobData
    from .models.update_mapping_rule_data import UpdateMappingRuleData
    from .models.update_mapping_rule_response_200 import UpdateMappingRuleResponse200
    from .models.update_role_data import UpdateRoleData
    from .models.update_role_response_200 import UpdateRoleResponse200
    from .models.update_tenant_cluster_variable_data import UpdateTenantClusterVariableData
    from .models.update_tenant_cluster_variable_response_200 import UpdateTenantClusterVariableResponse200
    from .models.update_tenant_data import UpdateTenantData
    from .models.update_tenant_response_200 import UpdateTenantResponse200
    from .models.update_user_data import UpdateUserData
    from .models.update_user_response_200 import UpdateUserResponse200
    from .models.update_user_task_data import UpdateUserTaskData
    from .types import File
    from .types import File
    import datetime

@define
class Client:
    """A class for keeping track of data related to the API

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``timeout``: The maximum amount of a time a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

        ``httpx_args``: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.


    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
    """

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str = field(alias="base_url")
    _cookies: dict[str, str] = field(factory=str_str_dict_factory, kw_only=True, alias="cookies")
    _headers: dict[str, str] = field(factory=str_str_dict_factory, kw_only=True, alias="headers")
    _timeout: httpx.Timeout | None = field(default=None, kw_only=True, alias="timeout")
    _verify_ssl: str | bool | ssl.SSLContext = field(
        default=True, kw_only=True, alias="verify_ssl"
    )
    _follow_redirects: bool = field(
        default=False, kw_only=True, alias="follow_redirects"
    )
    _httpx_args: dict[str, Any] = field(factory=str_any_dict_factory, kw_only=True, alias="httpx_args")
    _client: httpx.Client | None = field(default=None, init=False)
    _async_client: httpx.AsyncClient | None = field(default=None, init=False)

    def with_headers(self, headers: dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: httpx.Timeout) -> "Client":
        """Get a new client matching this one with a new timeout configuration"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return evolve(self, timeout=timeout)

    def set_httpx_client(self, client: httpx.Client) -> "Client":
        """Manually set the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._client = client
        return self

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._client

    def __enter__(self) -> "Client":
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        self.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for internal httpx.Client (see httpx docs)"""
        self.get_httpx_client().__exit__(*args, **kwargs)

    def set_async_httpx_client(self, async_client: httpx.AsyncClient) -> "Client":
        """Manually set the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._async_client = async_client
        return self

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._async_client

    async def __aenter__(self) -> "Client":
        """Enter a context manager for underlying httpx.AsyncClient—you cannot enter twice (see httpx docs)"""
        await self.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for underlying httpx.AsyncClient (see httpx docs)"""
        await self.get_async_httpx_client().__aexit__(*args, **kwargs)


@define
class AuthenticatedClient:
    """A Client which has been authenticated for use on secured endpoints

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``timeout``: The maximum amount of a time a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

        ``httpx_args``: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.


    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
        token: The token to use for authentication
        prefix: The prefix to use for the Authorization header
        auth_header_name: The name of the Authorization header
    """

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str = field(alias="base_url")
    _cookies: dict[str, str] = field(factory=str_str_dict_factory, kw_only=True, alias="cookies")
    _headers: dict[str, str] = field(factory=str_str_dict_factory, kw_only=True, alias="headers")
    _timeout: httpx.Timeout | None = field(default=None, kw_only=True, alias="timeout")
    _verify_ssl: str | bool | ssl.SSLContext = field(
        default=True, kw_only=True, alias="verify_ssl"
    )
    _follow_redirects: bool = field(
        default=False, kw_only=True, alias="follow_redirects"
    )
    _httpx_args: dict[str, Any] = field(factory=str_any_dict_factory, kw_only=True, alias="httpx_args")
    _client: httpx.Client | None = field(default=None, init=False)
    _async_client: httpx.AsyncClient | None = field(default=None, init=False)

    token: str
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"

    def with_headers(self, headers: dict[str, str]) -> "AuthenticatedClient":
        """Get a new client matching this one with additional headers"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: dict[str, str]) -> "AuthenticatedClient":
        """Get a new client matching this one with additional cookies"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: httpx.Timeout) -> "AuthenticatedClient":
        """Get a new client matching this one with a new timeout configuration"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return evolve(self, timeout=timeout)

    def set_httpx_client(self, client: httpx.Client) -> "AuthenticatedClient":
        """Manually set the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._client = client
        return self

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            self._headers[self.auth_header_name] = (
                f"{self.prefix} {self.token}" if self.prefix else self.token
            )
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._client

    def __enter__(self) -> "AuthenticatedClient":
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        self.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for internal httpx.Client (see httpx docs)"""
        self.get_httpx_client().__exit__(*args, **kwargs)

    def set_async_httpx_client(
        self, async_client: httpx.AsyncClient
    ) -> "AuthenticatedClient":
        """Manually set the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._async_client = async_client
        return self

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        if self._async_client is None:
            self._headers[self.auth_header_name] = (
                f"{self.prefix} {self.token}" if self.prefix else self.token
            )
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._async_client

    async def __aenter__(self) -> "AuthenticatedClient":
        """Enter a context manager for underlying httpx.AsyncClient—you cannot enter twice (see httpx docs)"""
        await self.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for underlying httpx.AsyncClient (see httpx docs)"""
        await self.get_async_httpx_client().__aexit__(*args, **kwargs)

class ExtendedDeploymentResult(CreateDeploymentResponse200):
    processes: list[CreateDeploymentResponse200DeploymentsItemProcessDefinition]
    decisions: list[CreateDeploymentResponse200DeploymentsItemDecisionDefinition]
    decision_requirements: list[CreateDeploymentResponse200DeploymentsItemDecisionRequirements]
    forms: list[CreateDeploymentResponse200DeploymentsItemForm]
    
    def __init__(self, response: CreateDeploymentResponse200):
        self.deployment_key = response.deployment_key
        self.tenant_id = response.tenant_id
        self.deployments = response.deployments
        self.additional_properties = response.additional_properties
        
        self.processes = [d.process_definition for d in self.deployments if not isinstance(d.process_definition, Unset)]
        self.decisions = [d.decision_definition for d in self.deployments if not isinstance(d.decision_definition, Unset)]
        self.decision_requirements = [d.decision_requirements for d in self.deployments if not isinstance(d.decision_requirements, Unset)]
        self.forms = [d.form for d in self.deployments if not isinstance(d.form, Unset)]


class CamundaClient:
    client: Client | AuthenticatedClient
    configuration: CamundaSdkConfiguration
    auth_provider: AuthProvider

    def __init__(self, configuration: CamundaSdkConfigPartial | None = None, auth_provider: AuthProvider | None = None, **kwargs: Any):
        resolved = ConfigurationResolver(
            environment=read_environment(),
            explicit_configuration=configuration,
        ).resolve()
        self.configuration = resolved.effective

        if "base_url" in kwargs:
            raise TypeError(
                "CamundaClient no longer accepts base_url; set CAMUNDA_REST_ADDRESS (or ZEEBE_REST_ADDRESS) via configuration/environment instead."
            )
        if "token" in kwargs:
            raise TypeError(
                "CamundaClient no longer accepts token; use configuration-based auth (CAMUNDA_AUTH_STRATEGY) instead."
            )

        if auth_provider is None:
            if self.configuration.CAMUNDA_AUTH_STRATEGY == "NONE":
                auth_provider = NullAuthProvider()
            elif self.configuration.CAMUNDA_AUTH_STRATEGY == "BASIC":
                auth_provider = BasicAuthProvider(
                    username=self.configuration.CAMUNDA_BASIC_AUTH_USERNAME or "",
                    password=self.configuration.CAMUNDA_BASIC_AUTH_PASSWORD or "",
                )
            elif self.configuration.CAMUNDA_AUTH_STRATEGY == "OAUTH":
                httpx_args: dict[str, Any] = kwargs.get("httpx_args") or {}
                transport: Any = httpx_args.get("transport")
                auth_provider = OAuthClientCredentialsAuthProvider(
                    oauth_url=self.configuration.CAMUNDA_OAUTH_URL,
                    client_id=self.configuration.CAMUNDA_CLIENT_ID or "",
                    client_secret=self.configuration.CAMUNDA_CLIENT_SECRET or "",
                    audience=self.configuration.CAMUNDA_TOKEN_AUDIENCE,
                    cache_dir=self.configuration.CAMUNDA_TOKEN_CACHE_DIR,
                    disk_cache_disable=self.configuration.CAMUNDA_TOKEN_DISK_CACHE_DISABLE,
                    transport=transport,
                )
            else:
                auth_provider = NullAuthProvider()

        self.auth_provider = auth_provider

        # Ensure every request gets auth headers via httpx event hooks.
        kwargs["httpx_args"] = inject_auth_event_hooks(
            kwargs.get("httpx_args"),
            auth_provider,
            async_client=False,
            log_level=self.configuration.CAMUNDA_SDK_LOG_LEVEL,
        )

        self.client = Client(base_url=self.configuration.CAMUNDA_REST_ADDRESS, **kwargs)

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any):
        try:
            return self.client.__exit__(*args, **kwargs)
        finally:
            close = getattr(self.auth_provider, "close", None)
            if callable(close):
                close()

    def close(self) -> None:
        """Close underlying HTTP clients.

        This closes both the API client's httpx client and, when available, the
        auth provider's token client.
        """

        try:
            close = getattr(self.auth_provider, "close", None)
            if callable(close):
                close()
        finally:
            try:
                self.client.get_httpx_client().close()
            except Exception:
                return

    def deploy_resources_from_files(self, files: list[str | Path], tenant_id: str | None = None) -> ExtendedDeploymentResult:
        """Deploy BPMN/DMN/Form resources from local files.

        This is a convenience wrapper around :meth:`create_deployment` that:

        - Reads each path in ``files`` as bytes.
        - Wraps the bytes in :class:`camunda_orchestration_sdk.types.File` using the file's basename
          as ``file_name``.
        - Builds :class:`camunda_orchestration_sdk.models.CreateDeploymentData` and calls
          :meth:`create_deployment`.
        - Returns an :class:`ExtendedDeploymentResult`, which is the deployment response plus
          convenience lists (``processes``, ``decisions``, ``decision_requirements``, ``forms``).

        Args:
            files: File paths (``str`` or ``Path``) to deploy.
            tenant_id: Optional tenant identifier. If not provided, the default tenant is used.

        Returns:
            ExtendedDeploymentResult: The deployment result with extracted resource lists.

        Raises:
            FileNotFoundError: If any file path does not exist.
            PermissionError: If any file path cannot be read.
            IsADirectoryError: If any file path is a directory.
            OSError: For other I/O failures while reading files.
            Exception: Propagates any exception raised by :meth:`create_deployment` (including
                typed API errors in :mod:`camunda_orchestration_sdk.errors` and ``httpx.TimeoutException``).
        """
        from .models.create_deployment_data import CreateDeploymentData
        from .semantic_types import TenantId
        from .types import File, UNSET
        import io
        import os

        resources: list[File] = []
        for file_path in files:
            file_path = str(file_path)
            with open(file_path, "rb") as f:
                content = f.read()
            resources.append(File(payload=io.BytesIO(content), file_name=os.path.basename(file_path)))

        data = CreateDeploymentData(resources=resources, tenant_id=TenantId(tenant_id) if tenant_id is not None else UNSET)
        return ExtendedDeploymentResult(self.create_deployment(data=data))


    def get_audit_log(self, audit_log_key: str, **kwargs: Any) -> GetAuditLogResponse200:
        """Get audit log

 Get an audit log entry by auditLogKey.

Args:
    audit_log_key (str): System-generated key for an audit log entry. Example:
        22517998136843567.

Raises:
    errors.GetAuditLogUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetAuditLogForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetAuditLogNotFound: If the response status code is 404. The audit log with the given key was not found.
    errors.GetAuditLogInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetAuditLogResponse200"""
        from .api.audit_log.get_audit_log import sync as get_audit_log_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_audit_log_sync(**_kwargs)


    def search_audit_logs(self, *, data: SearchAuditLogsData | Unset = UNSET, **kwargs: Any) -> SearchAuditLogsResponse200:
        """Search audit logs

 Search for audit logs based on given criteria.

Args:
    body (SearchAuditLogsData | Unset): Audit log search request.

Raises:
    errors.SearchAuditLogsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchAuditLogsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchAuditLogsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchAuditLogsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchAuditLogsResponse200"""
        from .api.audit_log.search_audit_logs import sync as search_audit_logs_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_audit_logs_sync(**_kwargs)


    def cancel_batch_operation(self, batch_operation_key: str, *, data: Any | Unset = UNSET, **kwargs: Any) -> None:
        """Cancel Batch operation

 Cancels a running batch operation.
This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/{batchOperationKey}).

Args:
    batch_operation_key (str): System-generated key for an batch operation. Example:
        2251799813684321.
    body (Any | Unset):

Raises:
    errors.CancelBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CancelBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CancelBatchOperationNotFound: If the response status code is 404. Not found. The batch operation was not found.
    errors.CancelBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.batch_operation.cancel_batch_operation import sync as cancel_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return cancel_batch_operation_sync(**_kwargs)


    def suspend_batch_operation(self, batch_operation_key: str, *, data: Any | Unset = UNSET, **kwargs: Any) -> None:
        """Suspend Batch operation

 Suspends a running batch operation.
This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/{batchOperationKey}).

Args:
    batch_operation_key (str): System-generated key for an batch operation. Example:
        2251799813684321.
    body (Any | Unset):

Raises:
    errors.SuspendBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SuspendBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SuspendBatchOperationNotFound: If the response status code is 404. Not found. The batch operation was not found.
    errors.SuspendBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.SuspendBatchOperationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.batch_operation.suspend_batch_operation import sync as suspend_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return suspend_batch_operation_sync(**_kwargs)


    def search_batch_operations(self, *, data: SearchBatchOperationsData | Unset = UNSET, **kwargs: Any) -> SearchBatchOperationsResponse200:
        """Search batch operations

 Search for batch operations based on given criteria.

Args:
    body (SearchBatchOperationsData | Unset): Batch operation search request.

Raises:
    errors.SearchBatchOperationsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchBatchOperationsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchBatchOperationsResponse200"""
        from .api.batch_operation.search_batch_operations import sync as search_batch_operations_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_batch_operations_sync(**_kwargs)


    def resume_batch_operation(self, batch_operation_key: str, *, data: Any | Unset = UNSET, **kwargs: Any) -> None:
        """Resume Batch operation

 Resumes a suspended batch operation.
This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/{batchOperationKey}).

Args:
    batch_operation_key (str): System-generated key for an batch operation. Example:
        2251799813684321.
    body (Any | Unset):

Raises:
    errors.ResumeBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ResumeBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.ResumeBatchOperationNotFound: If the response status code is 404. Not found. The batch operation was not found.
    errors.ResumeBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResumeBatchOperationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.batch_operation.resume_batch_operation import sync as resume_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return resume_batch_operation_sync(**_kwargs)


    def get_batch_operation(self, batch_operation_key: str, **kwargs: Any) -> GetBatchOperationResponse200:
        """Get batch operation

 Get batch operation by key.

Args:
    batch_operation_key (str): System-generated key for an batch operation. Example:
        2251799813684321.

Raises:
    errors.GetBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetBatchOperationNotFound: If the response status code is 404. The batch operation is not found.
    errors.GetBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetBatchOperationResponse200"""
        from .api.batch_operation.get_batch_operation import sync as get_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_batch_operation_sync(**_kwargs)


    def search_batch_operation_items(self, *, data: SearchBatchOperationItemsData | Unset = UNSET, **kwargs: Any) -> SearchBatchOperationItemsResponse200:
        """Search batch operation items

 Search for batch operation items based on given criteria.

Args:
    body (SearchBatchOperationItemsData | Unset): Batch operation item search request.

Raises:
    errors.SearchBatchOperationItemsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchBatchOperationItemsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchBatchOperationItemsResponse200"""
        from .api.batch_operation.search_batch_operation_items import sync as search_batch_operation_items_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_batch_operation_items_sync(**_kwargs)


    def get_start_process_form(self, process_definition_key: str, **kwargs: Any) -> GetStartProcessFormResponse200:
        """Get process start form

 Get the start form of a process.
Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

Args:
    process_definition_key (str): System-generated key for a deployed process definition.
        Example: 2251799813686749.

Raises:
    errors.GetStartProcessFormBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetStartProcessFormUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetStartProcessFormForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetStartProcessFormNotFound: If the response status code is 404. Not found
    errors.GetStartProcessFormInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetStartProcessFormResponse200"""
        from .api.process_definition.get_start_process_form import sync as get_start_process_form_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_start_process_form_sync(**_kwargs)


    def search_process_definitions(self, *, data: SearchProcessDefinitionsData | Unset = UNSET, **kwargs: Any) -> SearchProcessDefinitionsResponse200:
        """Search process definitions

 Search for process definitions based on given criteria.

Args:
    body (SearchProcessDefinitionsData | Unset):

Raises:
    errors.SearchProcessDefinitionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchProcessDefinitionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchProcessDefinitionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchProcessDefinitionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchProcessDefinitionsResponse200"""
        from .api.process_definition.search_process_definitions import sync as search_process_definitions_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_process_definitions_sync(**_kwargs)


    def get_process_definition_statistics(self, process_definition_key: str, *, data: GetProcessDefinitionStatisticsData | Unset = UNSET, **kwargs: Any) -> GetProcessDefinitionStatisticsResponse200:
        """Get process definition statistics

 Get statistics about elements in currently running process instances by process definition key and
search filter.

Args:
    process_definition_key (str): System-generated key for a deployed process definition.
        Example: 2251799813686749.
    body (GetProcessDefinitionStatisticsData | Unset): Process definition element statistics
        request.

Raises:
    errors.GetProcessDefinitionStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionStatisticsResponse200"""
        from .api.process_definition.get_process_definition_statistics import sync as get_process_definition_statistics_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_definition_statistics_sync(**_kwargs)


    def get_process_definition_message_subscription_statistics(self, *, data: GetProcessDefinitionMessageSubscriptionStatisticsData | Unset = UNSET, **kwargs: Any) -> GetProcessDefinitionMessageSubscriptionStatisticsResponse200:
        """Get message subscription statistics

 Get message subscription statistics, grouped by process definition.

Args:
    body (GetProcessDefinitionMessageSubscriptionStatisticsData | Unset):

Raises:
    errors.GetProcessDefinitionMessageSubscriptionStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionMessageSubscriptionStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionMessageSubscriptionStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionMessageSubscriptionStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionMessageSubscriptionStatisticsResponse200"""
        from .api.process_definition.get_process_definition_message_subscription_statistics import sync as get_process_definition_message_subscription_statistics_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_definition_message_subscription_statistics_sync(**_kwargs)


    def get_process_definition_instance_statistics(self, *, data: GetProcessDefinitionInstanceStatisticsData | Unset = UNSET, **kwargs: Any) -> GetProcessDefinitionInstanceStatisticsResponse200:
        """Get process instance statistics

 Get statistics about process instances, grouped by process definition and tenant.

Args:
    body (GetProcessDefinitionInstanceStatisticsData | Unset):

Raises:
    errors.GetProcessDefinitionInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionInstanceStatisticsResponse200"""
        from .api.process_definition.get_process_definition_instance_statistics import sync as get_process_definition_instance_statistics_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_definition_instance_statistics_sync(**_kwargs)


    def get_process_definition(self, process_definition_key: str, **kwargs: Any) -> GetProcessDefinitionResponse200:
        """Get process definition

 Returns process definition as JSON.

Args:
    process_definition_key (str): System-generated key for a deployed process definition.
        Example: 2251799813686749.

Raises:
    errors.GetProcessDefinitionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionNotFound: If the response status code is 404. The process definition with the given key was not found. More details are provided in the response body.
    errors.GetProcessDefinitionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionResponse200"""
        from .api.process_definition.get_process_definition import sync as get_process_definition_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_definition_sync(**_kwargs)


    def get_process_definition_instance_version_statistics(self, process_definition_id: str, *, data: GetProcessDefinitionInstanceVersionStatisticsData | Unset = UNSET, **kwargs: Any) -> GetProcessDefinitionInstanceVersionStatisticsResponse200:
        """Get process instance statistics by version

 Get statistics about process instances, grouped by version for a given process definition.

Args:
    process_definition_id (str): Id of a process definition, from the model. Only ids of
        process definitions that are deployed are useful. Example: new-account-onboarding-
        workflow.
    body (GetProcessDefinitionInstanceVersionStatisticsData | Unset):

Raises:
    errors.GetProcessDefinitionInstanceVersionStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionInstanceVersionStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionInstanceVersionStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionInstanceVersionStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionInstanceVersionStatisticsResponse200"""
        from .api.process_definition.get_process_definition_instance_version_statistics import sync as get_process_definition_instance_version_statistics_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_definition_instance_version_statistics_sync(**_kwargs)


    def get_process_definition_xml(self, process_definition_key: str, **kwargs: Any) -> str:
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
        from .api.process_definition.get_process_definition_xml import sync as get_process_definition_xml_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_definition_xml_sync(**_kwargs)


    def search_roles_for_group(self, group_id: str, *, data: SearchRolesForGroupData | Unset = UNSET, **kwargs: Any) -> SearchRolesForGroupResponse200:
        """Search group roles

 Search roles assigned to a group.

Args:
    group_id (str):
    body (SearchRolesForGroupData | Unset): Role search request.

Raises:
    errors.SearchRolesForGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchRolesForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchRolesForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchRolesForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.SearchRolesForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchRolesForGroupResponse200"""
        from .api.group.search_roles_for_group import sync as search_roles_for_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_roles_for_group_sync(**_kwargs)


    def unassign_user_from_group(self, group_id: str, username: str, **kwargs: Any) -> None:
        """Unassign a user from a group

 Unassigns a user from a group.
The user is removed as a group member, with associated authorizations, roles, and tenant assignments
no longer applied.

Args:
    group_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.UnassignUserFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignUserFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignUserFromGroupNotFound: If the response status code is 404. The group or user with the given ID was not found, or the user is not assigned to this group.
    errors.UnassignUserFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignUserFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.unassign_user_from_group import sync as unassign_user_from_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_user_from_group_sync(**_kwargs)


    def search_users_for_group(self, group_id: str, *, data: SearchUsersForGroupData | Unset = UNSET, **kwargs: Any) -> SearchUsersForGroupResponse200:
        """Search group users

 Search users assigned to a group.

Args:
    group_id (str):
    body (SearchUsersForGroupData | Unset):

Raises:
    errors.SearchUsersForGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUsersForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchUsersForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchUsersForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.SearchUsersForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUsersForGroupResponse200"""
        from .api.group.search_users_for_group import sync as search_users_for_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_users_for_group_sync(**_kwargs)


    def unassign_client_from_group(self, group_id: str, client_id: str, **kwargs: Any) -> None:
        """Unassign a client from a group

 Unassigns a client from a group.
The client is removed as a group member, with associated authorizations, roles, and tenant
assignments no longer applied.

Args:
    group_id (str):
    client_id (str):

Raises:
    errors.UnassignClientFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignClientFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignClientFromGroupNotFound: If the response status code is 404. The group with the given ID was not found, or the client is not assigned to this group.
    errors.UnassignClientFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignClientFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.unassign_client_from_group import sync as unassign_client_from_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_client_from_group_sync(**_kwargs)


    def assign_user_to_group(self, group_id: str, username: str, **kwargs: Any) -> None:
        """Assign a user to a group

 Assigns a user to a group, making the user a member of the group.
Group members inherit the group authorizations, roles, and tenant assignments.

Args:
    group_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.AssignUserToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignUserToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignUserToGroupNotFound: If the response status code is 404. The group or user with the given ID or username was not found.
    errors.AssignUserToGroupConflict: If the response status code is 409. The user with the given ID is already assigned to the group.
    errors.AssignUserToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignUserToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.assign_user_to_group import sync as assign_user_to_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_user_to_group_sync(**_kwargs)


    def search_clients_for_group(self, group_id: str, *, data: SearchClientsForGroupData | Unset = UNSET, **kwargs: Any) -> SearchClientsForGroupResponse200:
        """Search group clients

 Search clients assigned to a group.

Args:
    group_id (str):
    body (SearchClientsForGroupData | Unset):

Raises:
    errors.SearchClientsForGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchClientsForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchClientsForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchClientsForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.SearchClientsForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClientsForGroupResponse200"""
        from .api.group.search_clients_for_group import sync as search_clients_for_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_clients_for_group_sync(**_kwargs)


    def assign_mapping_rule_to_group(self, group_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Assign a mapping rule to a group

 Assigns a mapping rule to a group.

Args:
    group_id (str):
    mapping_rule_id (str):

Raises:
    errors.AssignMappingRuleToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignMappingRuleToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignMappingRuleToGroupNotFound: If the response status code is 404. The group or mapping rule with the given ID was not found.
    errors.AssignMappingRuleToGroupConflict: If the response status code is 409. The mapping rule with the given ID is already assigned to the group.
    errors.AssignMappingRuleToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignMappingRuleToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.assign_mapping_rule_to_group import sync as assign_mapping_rule_to_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_mapping_rule_to_group_sync(**_kwargs)


    def search_mapping_rules_for_group(self, group_id: str, *, data: SearchMappingRulesForGroupData | Unset = UNSET, **kwargs: Any) -> SearchMappingRulesForGroupResponse200:
        """Search group mapping rules

 Search mapping rules assigned to a group.

Args:
    group_id (str):
    body (SearchMappingRulesForGroupData | Unset):

Raises:
    errors.SearchMappingRulesForGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMappingRulesForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMappingRulesForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMappingRulesForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.SearchMappingRulesForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMappingRulesForGroupResponse200"""
        from .api.group.search_mapping_rules_for_group import sync as search_mapping_rules_for_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_mapping_rules_for_group_sync(**_kwargs)


    def search_groups(self, *, data: SearchGroupsData | Unset = UNSET, **kwargs: Any) -> SearchGroupsResponse200:
        """Search groups

 Search for groups based on given criteria.

Args:
    body (SearchGroupsData | Unset): Group search request.

Raises:
    errors.SearchGroupsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchGroupsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchGroupsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchGroupsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchGroupsResponse200"""
        from .api.group.search_groups import sync as search_groups_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_groups_sync(**_kwargs)


    def get_group(self, group_id: str, **kwargs: Any) -> GetGroupResponse200:
        """Get group

 Get a group by its ID.

Args:
    group_id (str):

Raises:
    errors.GetGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.GetGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetGroupResponse200"""
        from .api.group.get_group import sync as get_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_group_sync(**_kwargs)


    def delete_group(self, group_id: str, **kwargs: Any) -> None:
        """Delete group

 Deletes the group with the given ID.

Args:
    group_id (str):

Raises:
    errors.DeleteGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.DeleteGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.delete_group import sync as delete_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_group_sync(**_kwargs)


    def assign_client_to_group(self, group_id: str, client_id: str, **kwargs: Any) -> None:
        """Assign a client to a group

 Assigns a client to a group, making it a member of the group.
Members of the group inherit the group authorizations, roles, and tenant assignments.

Args:
    group_id (str):
    client_id (str):

Raises:
    errors.AssignClientToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignClientToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignClientToGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.AssignClientToGroupConflict: If the response status code is 409. The client with the given ID is already assigned to the group.
    errors.AssignClientToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignClientToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.assign_client_to_group import sync as assign_client_to_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_client_to_group_sync(**_kwargs)


    def update_group(self, group_id: str, *, data: UpdateGroupData, **kwargs: Any) -> UpdateGroupResponse200:
        """Update group

 Update a group with the given ID.

Args:
    group_id (str):
    body (UpdateGroupData):

Raises:
    errors.UpdateGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.UpdateGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateGroupResponse200"""
        from .api.group.update_group import sync as update_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_group_sync(**_kwargs)


    def unassign_mapping_rule_from_group(self, group_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Unassign a mapping rule from a group

 Unassigns a mapping rule from a group.

Args:
    group_id (str):
    mapping_rule_id (str):

Raises:
    errors.UnassignMappingRuleFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignMappingRuleFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignMappingRuleFromGroupNotFound: If the response status code is 404. The group or mapping rule with the given ID was not found, or the mapping rule is not assigned to this group.
    errors.UnassignMappingRuleFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignMappingRuleFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.unassign_mapping_rule_from_group import sync as unassign_mapping_rule_from_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_mapping_rule_from_group_sync(**_kwargs)


    def create_group(self, *, data: CreateGroupData | Unset = UNSET, **kwargs: Any) -> CreateGroupResponse201:
        """Create group

 Create a new group.

Args:
    body (CreateGroupData | Unset):

Raises:
    errors.CreateGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateGroupResponse201"""
        from .api.group.create_group import sync as create_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_group_sync(**_kwargs)


    def get_variable(self, variable_key: str, **kwargs: Any) -> GetVariableResponse200:
        """Get variable

 Get the variable by the variable key.

Args:
    variable_key (str): System-generated key for a variable. Example: 2251799813683287.

Raises:
    errors.GetVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetVariableNotFound: If the response status code is 404. Not found
    errors.GetVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetVariableResponse200"""
        from .api.variable.get_variable import sync as get_variable_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_variable_sync(**_kwargs)


    def search_variables(self, *, data: SearchVariablesData | Unset = UNSET, truncate_values: bool | Unset = UNSET, **kwargs: Any) -> SearchVariablesResponse200:
        """Search variables

 Search for process and local variables based on given criteria. By default, long variable values in
the response are truncated.

Args:
    truncate_values (bool | Unset):
    body (SearchVariablesData | Unset): Variable search query request.

Raises:
    errors.SearchVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchVariablesResponse200"""
        from .api.variable.search_variables import sync as search_variables_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_variables_sync(**_kwargs)


    def create_admin_user(self, *, data: CreateAdminUserData, **kwargs: Any) -> None:
        """Create admin user

 Creates a new user and assigns the admin role to it. This endpoint is only usable when users are
managed in the Orchestration Cluster and while no user is assigned to the admin role.

Args:
    body (CreateAdminUserData):

Raises:
    errors.CreateAdminUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateAdminUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateAdminUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateAdminUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.setup.create_admin_user import sync as create_admin_user_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_admin_user_sync(**_kwargs)


    def delete_decision_instances_batch_operation(self, *, data: DeleteDecisionInstancesBatchOperationData, **kwargs: Any) -> DeleteDecisionInstancesBatchOperationResponse200:
        """Delete decision instances (batch)

 Delete multiple decision instances. This will delete the historic data from secondary storage.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (DeleteDecisionInstancesBatchOperationData): The decision instance filter that
        defines which decision instances should be deleted.

Raises:
    errors.DeleteDecisionInstancesBatchOperationBadRequest: If the response status code is 400. The decision instance batch operation failed. More details are provided in the response body.
    errors.DeleteDecisionInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteDecisionInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteDecisionInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteDecisionInstancesBatchOperationResponse200"""
        from .api.decision_instance.delete_decision_instances_batch_operation import sync as delete_decision_instances_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_decision_instances_batch_operation_sync(**_kwargs)


    def delete_decision_instance(self, decision_instance_key: str, *, data: DeleteDecisionInstanceDataType0 | None | Unset = UNSET, **kwargs: Any) -> DeleteDecisionInstanceResponse200:
        """Delete decision instance

 Delete all associated decision evaluations based on provided key.

Args:
    decision_instance_key (str): System-generated key for a deployed decision instance.
        Example: 22517998136843567.
    body (DeleteDecisionInstanceDataType0 | None | Unset):

Raises:
    errors.DeleteDecisionInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteDecisionInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteDecisionInstanceNotFound: If the response status code is 404. The decision instance is not found.
    errors.DeleteDecisionInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteDecisionInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteDecisionInstanceResponse200"""
        from .api.decision_instance.delete_decision_instance import sync as delete_decision_instance_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_decision_instance_sync(**_kwargs)


    def get_decision_instance(self, decision_evaluation_instance_key: str, **kwargs: Any) -> GetDecisionInstanceResponse200:
        """Get decision instance

 Returns a decision instance.

Args:
    decision_evaluation_instance_key (str): System-generated key for a deployed decision
        instance. Example: 22517998136843567.

Raises:
    errors.GetDecisionInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionInstanceNotFound: If the response status code is 404. The decision instance with the given key was not found. More details are provided in the response body.
    errors.GetDecisionInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetDecisionInstanceResponse200"""
        from .api.decision_instance.get_decision_instance import sync as get_decision_instance_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_decision_instance_sync(**_kwargs)


    def search_decision_instances(self, *, data: SearchDecisionInstancesData | Unset = UNSET, **kwargs: Any) -> SearchDecisionInstancesResponse200:
        """Search decision instances

 Search for decision instances based on given criteria.

Args:
    body (SearchDecisionInstancesData | Unset):

Raises:
    errors.SearchDecisionInstancesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchDecisionInstancesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchDecisionInstancesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchDecisionInstancesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchDecisionInstancesResponse200"""
        from .api.decision_instance.search_decision_instances import sync as search_decision_instances_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_decision_instances_sync(**_kwargs)


    def activate_jobs(self, *, data: ActivateJobsData, **kwargs: Any) -> ActivateJobsResponse200:
        """Activate jobs

 Iterate through all known partitions and activate jobs up to the requested maximum.

Args:
    body (ActivateJobsData):

Raises:
    errors.ActivateJobsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ActivateJobsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ActivateJobsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ActivateJobsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ActivateJobsResponse200"""
        from .api.job.activate_jobs import sync as activate_jobs_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return activate_jobs_sync(**_kwargs)


    def complete_job(self, job_key: str, *, data: CompleteJobData | Unset = UNSET, **kwargs: Any) -> None:
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
        from .api.job.complete_job import sync as complete_job_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return complete_job_sync(**_kwargs)


    def fail_job(self, job_key: str, *, data: FailJobData | Unset = UNSET, **kwargs: Any) -> None:
        """Fail job

 Mark the job as failed.

Args:
    job_key (str): System-generated key for a job. Example: 2251799813653498.
    body (FailJobData | Unset):

Raises:
    errors.FailJobBadRequest: If the response status code is 400. The provided data is not valid.
    errors.FailJobNotFound: If the response status code is 404. The job with the given jobKey is not found. It was completed by another worker, or the process instance itself was canceled.
    errors.FailJobConflict: If the response status code is 409. The job with the given key is in the wrong state (i.e: not ACTIVATED or ACTIVATABLE). The job was failed by another worker with retries = 0, and the process is now in an incident state.
    errors.FailJobInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.FailJobServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.job.fail_job import sync as fail_job_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return fail_job_sync(**_kwargs)


    def throw_job_error(self, job_key: str, *, data: ThrowJobErrorData, **kwargs: Any) -> None:
        """Throw error for job

 Reports a business error (i.e. non-technical) that occurs while processing a job.

Args:
    job_key (str): System-generated key for a job. Example: 2251799813653498.
    body (ThrowJobErrorData):

Raises:
    errors.ThrowJobErrorBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ThrowJobErrorNotFound: If the response status code is 404. The job with the given key was not found or is not activated.
    errors.ThrowJobErrorConflict: If the response status code is 409. The job with the given key is in the wrong state currently. More details are provided in the response body.
    errors.ThrowJobErrorInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ThrowJobErrorServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.job.throw_job_error import sync as throw_job_error_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return throw_job_error_sync(**_kwargs)


    def update_job(self, job_key: str, *, data: UpdateJobData, **kwargs: Any) -> None:
        """Update job

 Update a job with the given key.

Args:
    job_key (str): System-generated key for a job. Example: 2251799813653498.
    body (UpdateJobData):

Raises:
    errors.UpdateJobBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateJobNotFound: If the response status code is 404. The job with the jobKey is not found.
    errors.UpdateJobConflict: If the response status code is 409. The job with the given key is in the wrong state currently. More details are provided in the response body.
    errors.UpdateJobInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateJobServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.job.update_job import sync as update_job_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_job_sync(**_kwargs)


    def search_jobs(self, *, data: SearchJobsData | Unset = UNSET, **kwargs: Any) -> SearchJobsResponse200:
        """Search jobs

 Search for jobs based on given criteria.

Args:
    body (SearchJobsData | Unset): Job search request.

Raises:
    errors.SearchJobsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchJobsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchJobsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchJobsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchJobsResponse200"""
        from .api.job.search_jobs import sync as search_jobs_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_jobs_sync(**_kwargs)


    def get_global_job_statistics(self, *, from_: datetime.datetime, to: datetime.datetime, job_type: str | Unset = UNSET, **kwargs: Any) -> GetGlobalJobStatisticsResponse200:
        """Global job statistics

 Returns global aggregated counts for jobs. Optionally filter by the creation time window and/or
jobType.

Args:
    from_ (datetime.datetime):
    to (datetime.datetime):
    job_type (str | Unset):

Raises:
    errors.GetGlobalJobStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetGlobalJobStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetGlobalJobStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetGlobalJobStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetGlobalJobStatisticsResponse200"""
        from .api.job.get_global_job_statistics import sync as get_global_job_statistics_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_global_job_statistics_sync(**_kwargs)


    def get_topology(self, **kwargs: Any) -> GetTopologyResponse200:
        """Get cluster topology

 Obtains the current topology of the cluster the gateway is part of.

Raises:
    errors.GetTopologyUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetTopologyInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetTopologyResponse200"""
        from .api.cluster.get_topology import sync as get_topology_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_topology_sync(**_kwargs)


    def correlate_message(self, *, data: CorrelateMessageData, **kwargs: Any) -> CorrelateMessageResponse200:
        """Correlate message

 Publishes a message and correlates it to a subscription.
If correlation is successful it will return the first process instance key the message correlated
with.
The message is not buffered.
Use the publish message endpoint to send messages that can be buffered.

Args:
    body (CorrelateMessageData):

Raises:
    errors.CorrelateMessageBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CorrelateMessageForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CorrelateMessageNotFound: If the response status code is 404. Not found
    errors.CorrelateMessageInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CorrelateMessageServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CorrelateMessageResponse200"""
        from .api.message.correlate_message import sync as correlate_message_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return correlate_message_sync(**_kwargs)


    def publish_message(self, *, data: PublishMessageData, **kwargs: Any) -> PublishMessageResponse200:
        """Publish message

 Publishes a single message.
Messages are published to specific partitions computed from their correlation keys.
Messages can be buffered.
The endpoint does not wait for a correlation result.
Use the message correlation endpoint for such use cases.

Args:
    body (PublishMessageData):

Raises:
    errors.PublishMessageBadRequest: If the response status code is 400. The provided data is not valid.
    errors.PublishMessageInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.PublishMessageServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    PublishMessageResponse200"""
        from .api.message.publish_message import sync as publish_message_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return publish_message_sync(**_kwargs)


    def delete_process_instances_batch_operation(self, *, data: DeleteProcessInstancesBatchOperationData, **kwargs: Any) -> DeleteProcessInstancesBatchOperationResponse200:
        """Delete process instances (batch)

 Delete multiple process instances. This will delete the historic data from secondary storage.
Only process instances in a final state (COMPLETED or TERMINATED) can be deleted.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (DeleteProcessInstancesBatchOperationData): The process instance filter that defines
        which process instances should be deleted.

Raises:
    errors.DeleteProcessInstancesBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.DeleteProcessInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteProcessInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteProcessInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteProcessInstancesBatchOperationResponse200"""
        from .api.process_instance.delete_process_instances_batch_operation import sync as delete_process_instances_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_process_instances_batch_operation_sync(**_kwargs)


    def migrate_process_instances_batch_operation(self, *, data: MigrateProcessInstancesBatchOperationData, **kwargs: Any) -> MigrateProcessInstancesBatchOperationResponse200:
        """Migrate process instances (batch)

 Migrate multiple process instances.
Since only process instances with ACTIVE state can be migrated, any given
filters for state are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (MigrateProcessInstancesBatchOperationData):

Raises:
    errors.MigrateProcessInstancesBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.MigrateProcessInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.MigrateProcessInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.MigrateProcessInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    MigrateProcessInstancesBatchOperationResponse200"""
        from .api.process_instance.migrate_process_instances_batch_operation import sync as migrate_process_instances_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return migrate_process_instances_batch_operation_sync(**_kwargs)


    def modify_process_instances_batch_operation(self, *, data: ModifyProcessInstancesBatchOperationData, **kwargs: Any) -> ModifyProcessInstancesBatchOperationResponse200:
        """Modify process instances (batch)

 Modify multiple process instances.
Since only process instances with ACTIVE state can be modified, any given
filters for state are ignored and overridden during this batch operation.
In contrast to single modification operation, it is not possible to add variable instructions or
modify by element key.
It is only possible to use the element id of the source and target.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (ModifyProcessInstancesBatchOperationData): The process instance filter to define on
        which process instances tokens should be moved,
        and new element instances should be activated or terminated.

Raises:
    errors.ModifyProcessInstancesBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.ModifyProcessInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ModifyProcessInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.ModifyProcessInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ModifyProcessInstancesBatchOperationResponse200"""
        from .api.process_instance.modify_process_instances_batch_operation import sync as modify_process_instances_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return modify_process_instances_batch_operation_sync(**_kwargs)


    def migrate_process_instance(self, process_instance_key: str, *, data: MigrateProcessInstanceData, **kwargs: Any) -> None:
        """Migrate process instance

 Migrates a process instance to a new process definition.
This request can contain multiple mapping instructions to define mapping between the active
process instance's elements and target process definition elements.

Use this to upgrade a process instance to a new version of a process or to
a different process definition, e.g. to keep your running instances up-to-date with the
latest process improvements.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (MigrateProcessInstanceData): The migration instructions describe how to migrate a
        process instance from one process definition to another.

Raises:
    errors.MigrateProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.MigrateProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
    errors.MigrateProcessInstanceConflict: If the response status code is 409. The process instance migration failed. More details are provided in the response body.
    errors.MigrateProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.MigrateProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.process_instance.migrate_process_instance import sync as migrate_process_instance_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return migrate_process_instance_sync(**_kwargs)


    def resolve_process_instance_incidents(self, process_instance_key: str, **kwargs: Any) -> ResolveProcessInstanceIncidentsResponse200:
        """Resolve related incidents

 Creates a batch operation to resolve multiple incidents of a process instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.ResolveProcessInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ResolveProcessInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ResolveProcessInstanceIncidentsNotFound: If the response status code is 404. The process instance is not found.
    errors.ResolveProcessInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResolveProcessInstanceIncidentsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ResolveProcessInstanceIncidentsResponse200"""
        from .api.process_instance.resolve_process_instance_incidents import sync as resolve_process_instance_incidents_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return resolve_process_instance_incidents_sync(**_kwargs)


    def resolve_incidents_batch_operation(self, *, data: ResolveIncidentsBatchOperationData | Unset = UNSET, **kwargs: Any) -> ResolveIncidentsBatchOperationResponse200:
        """Resolve related incidents (batch)

 Resolves multiple instances of process instances.
Since only process instances with ACTIVE state can have unresolved incidents, any given
filters for state are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (ResolveIncidentsBatchOperationData | Unset): The process instance filter that
        defines which process instances should have their incidents resolved.

Raises:
    errors.ResolveIncidentsBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.ResolveIncidentsBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ResolveIncidentsBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.ResolveIncidentsBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ResolveIncidentsBatchOperationResponse200"""
        from .api.process_instance.resolve_incidents_batch_operation import sync as resolve_incidents_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return resolve_incidents_batch_operation_sync(**_kwargs)


    def create_process_instance(self, *, data: Processcreationbyid | Processcreationbykey, **kwargs: Any) -> CreateProcessInstanceResponse200:
        """Create process instance

 Creates and starts an instance of the specified process.
The process definition to use to create the instance can be specified either using its unique key
(as returned by Deploy resources), or using the BPMN process id and a version.

Waits for the completion of the process instance before returning a result
when awaitCompletion is enabled.

Args:
    body (Processcreationbyid | Processcreationbykey): Instructions for creating a process
        instance. The process definition can be specified
        either by id or by key.

Raises:
    errors.CreateProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.CreateProcessInstanceGatewayTimeout: If the response status code is 504. The process instance creation request timed out in the gateway. This can happen if the `awaitCompletion` request parameter is set to `true` and the created process instance did not complete within the defined request timeout. This often happens when the created instance is not fully automated or contains wait states.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateProcessInstanceResponse200"""
        from .api.process_instance.create_process_instance import sync as create_process_instance_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_process_instance_sync(**_kwargs)


    def cancel_process_instance(self, process_instance_key: str, *, data: CancelProcessInstanceDataType0 | None | Unset = UNSET, **kwargs: Any) -> None:
        """Cancel process instance

 Cancels a running process instance. As a cancellation includes more than just the removal of the
process instance resource, the cancellation resource must be posted.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (CancelProcessInstanceDataType0 | None | Unset):

Raises:
    errors.CancelProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CancelProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
    errors.CancelProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CancelProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.process_instance.cancel_process_instance import sync as cancel_process_instance_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return cancel_process_instance_sync(**_kwargs)


    def get_process_instance_sequence_flows(self, process_instance_key: str, **kwargs: Any) -> GetProcessInstanceSequenceFlowsResponse200:
        """Get sequence flows

 Get sequence flows taken by the process instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceSequenceFlowsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceSequenceFlowsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceSequenceFlowsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceSequenceFlowsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceSequenceFlowsResponse200"""
        from .api.process_instance.get_process_instance_sequence_flows import sync as get_process_instance_sequence_flows_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_instance_sequence_flows_sync(**_kwargs)


    def delete_process_instance(self, process_instance_key: str, *, data: DeleteProcessInstanceDataType0 | None | Unset = UNSET, **kwargs: Any) -> DeleteProcessInstanceResponse200:
        """Delete process instance

 Deletes a process instance. Only instances that are completed or terminated can be deleted.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (DeleteProcessInstanceDataType0 | None | Unset):

Raises:
    errors.DeleteProcessInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteProcessInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
    errors.DeleteProcessInstanceConflict: If the response status code is 409. The process instance is not in a completed or terminated state and cannot be deleted.
    errors.DeleteProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteProcessInstanceResponse200"""
        from .api.process_instance.delete_process_instance import sync as delete_process_instance_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_process_instance_sync(**_kwargs)


    def search_process_instance_incidents(self, process_instance_key: str, *, data: SearchProcessInstanceIncidentsData | Unset = UNSET, **kwargs: Any) -> SearchProcessInstanceIncidentsResponse200:
        """Search related incidents

 Search for incidents caused by the process instance or any of its called process or decision
instances.

Although the `processInstanceKey` is provided as a path parameter to indicate the root process
instance,
you may also include a `processInstanceKey` within the filter object to narrow results to specific
child process instances. This is useful, for example, if you want to isolate incidents associated
with
subprocesses or called processes under the root instance while excluding incidents directly tied to
the root.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (SearchProcessInstanceIncidentsData | Unset):

Raises:
    errors.SearchProcessInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchProcessInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchProcessInstanceIncidentsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchProcessInstanceIncidentsNotFound: If the response status code is 404. The process instance with the given key was not found.
    errors.SearchProcessInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchProcessInstanceIncidentsResponse200"""
        from .api.process_instance.search_process_instance_incidents import sync as search_process_instance_incidents_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_process_instance_incidents_sync(**_kwargs)


    def get_process_instance_statistics(self, process_instance_key: str, **kwargs: Any) -> GetProcessInstanceStatisticsResponse200:
        """Get element instance statistics

 Get statistics about elements by the process instance key.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsResponse200"""
        from .api.process_instance.get_process_instance_statistics import sync as get_process_instance_statistics_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_instance_statistics_sync(**_kwargs)


    def search_process_instances(self, *, data: SearchProcessInstancesData | Unset = UNSET, **kwargs: Any) -> SearchProcessInstancesResponse200:
        """Search process instances

 Search for process instances based on given criteria.

Args:
    body (SearchProcessInstancesData | Unset): Process instance search request.

Raises:
    errors.SearchProcessInstancesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchProcessInstancesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchProcessInstancesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchProcessInstancesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchProcessInstancesResponse200"""
        from .api.process_instance.search_process_instances import sync as search_process_instances_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_process_instances_sync(**_kwargs)


    def cancel_process_instances_batch_operation(self, *, data: CancelProcessInstancesBatchOperationData, **kwargs: Any) -> CancelProcessInstancesBatchOperationResponse200:
        """Cancel process instances (batch)

 Cancels multiple running process instances.
Since only ACTIVE root instances can be cancelled, any given filters for state and
parentProcessInstanceKey are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (CancelProcessInstancesBatchOperationData): The process instance filter that defines
        which process instances should be canceled.

Raises:
    errors.CancelProcessInstancesBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.CancelProcessInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CancelProcessInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CancelProcessInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CancelProcessInstancesBatchOperationResponse200"""
        from .api.process_instance.cancel_process_instances_batch_operation import sync as cancel_process_instances_batch_operation_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return cancel_process_instances_batch_operation_sync(**_kwargs)


    def get_process_instance(self, process_instance_key: str, **kwargs: Any) -> GetProcessInstanceResponse200:
        """Get process instance

 Get the process instance by the process instance key.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceNotFound: If the response status code is 404. The process instance with the given key was not found.
    errors.GetProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceResponse200"""
        from .api.process_instance.get_process_instance import sync as get_process_instance_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_instance_sync(**_kwargs)


    def get_process_instance_call_hierarchy(self, process_instance_key: str, **kwargs: Any) -> list[Any]:
        """Get call hierarchy

 Returns the call hierarchy for a given process instance, showing its ancestry up to the root
instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceCallHierarchyBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceCallHierarchyUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceCallHierarchyForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceCallHierarchyNotFound: If the response status code is 404. The process instance is not found.
    errors.GetProcessInstanceCallHierarchyInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    list[Any]"""
        from .api.process_instance.get_process_instance_call_hierarchy import sync as get_process_instance_call_hierarchy_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_instance_call_hierarchy_sync(**_kwargs)


    def modify_process_instance(self, process_instance_key: str, *, data: ModifyProcessInstanceData, **kwargs: Any) -> None:
        """Modify process instance

 Modifies a running process instance.
This request can contain multiple instructions to activate an element of the process or
to terminate an active instance of an element.

Use this to repair a process instance that is stuck on an element or took an unintended path.
For example, because an external system is not available or doesn't respond as expected.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (ModifyProcessInstanceData):

Raises:
    errors.ModifyProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ModifyProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
    errors.ModifyProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ModifyProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.process_instance.modify_process_instance import sync as modify_process_instance_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return modify_process_instance_sync(**_kwargs)


    def get_authentication(self, **kwargs: Any) -> GetAuthenticationResponse200:
        """Get current user

 Retrieves the current authenticated user.

Raises:
    errors.GetAuthenticationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetAuthenticationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetAuthenticationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetAuthenticationResponse200"""
        from .api.authentication.get_authentication import sync as get_authentication_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_authentication_sync(**_kwargs)


    def assign_group_to_tenant(self, tenant_id: str, group_id: str, **kwargs: Any) -> None:
        """Assign a group to a tenant

 Assigns a group to a specified tenant.
Group members (users, clients) can then access tenant data and perform authorized actions.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    group_id (str):

Raises:
    errors.AssignGroupToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignGroupToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignGroupToTenantNotFound: If the response status code is 404. Not found. The tenant or group was not found.
    errors.AssignGroupToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignGroupToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_group_to_tenant import sync as assign_group_to_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_group_to_tenant_sync(**_kwargs)


    def search_group_ids_for_tenant(self, tenant_id: str, *, data: SearchGroupIdsForTenantData | Unset = UNSET, **kwargs: Any) -> SearchGroupIdsForTenantResponse200:
        """Search groups for tenant

 Retrieves a filtered and sorted list of groups for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchGroupIdsForTenantData | Unset):

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchGroupIdsForTenantResponse200"""
        from .api.tenant.search_group_ids_for_tenant import sync as search_group_ids_for_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_group_ids_for_tenant_sync(**_kwargs)


    def unassign_client_from_tenant(self, tenant_id: str, client_id: str, **kwargs: Any) -> None:
        """Unassign a client from a tenant

 Unassigns the client from the specified tenant.
The client can no longer access tenant data.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    client_id (str):

Raises:
    errors.UnassignClientFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignClientFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignClientFromTenantNotFound: If the response status code is 404. The tenant does not exist or the client was not assigned to it.
    errors.UnassignClientFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignClientFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_client_from_tenant import sync as unassign_client_from_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_client_from_tenant_sync(**_kwargs)


    def get_tenant(self, tenant_id: str, **kwargs: Any) -> GetTenantResponse200:
        """Get tenant

 Retrieves a single tenant by tenant ID.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.

Raises:
    errors.GetTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetTenantUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetTenantNotFound: If the response status code is 404. Tenant not found.
    errors.GetTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetTenantResponse200"""
        from .api.tenant.get_tenant import sync as get_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_tenant_sync(**_kwargs)


    def assign_mapping_rule_to_tenant(self, tenant_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Assign a mapping rule to a tenant

 Assign a single mapping rule to a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    mapping_rule_id (str):

Raises:
    errors.AssignMappingRuleToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignMappingRuleToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignMappingRuleToTenantNotFound: If the response status code is 404. Not found. The tenant or mapping rule was not found.
    errors.AssignMappingRuleToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignMappingRuleToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_mapping_rule_to_tenant import sync as assign_mapping_rule_to_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_mapping_rule_to_tenant_sync(**_kwargs)


    def search_tenants(self, *, data: SearchTenantsData | Unset = UNSET, **kwargs: Any) -> SearchTenantsResponse200:
        """Search tenants

 Retrieves a filtered and sorted list of tenants.

Args:
    body (SearchTenantsData | Unset): Tenant search request

Raises:
    errors.SearchTenantsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchTenantsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchTenantsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchTenantsNotFound: If the response status code is 404. Not found
    errors.SearchTenantsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchTenantsResponse200"""
        from .api.tenant.search_tenants import sync as search_tenants_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_tenants_sync(**_kwargs)


    def delete_tenant(self, tenant_id: str, **kwargs: Any) -> None:
        """Delete tenant

 Deletes an existing tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.

Raises:
    errors.DeleteTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteTenantNotFound: If the response status code is 404. Not found. The tenant was not found.
    errors.DeleteTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.delete_tenant import sync as delete_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_tenant_sync(**_kwargs)


    def assign_client_to_tenant(self, tenant_id: str, client_id: str, **kwargs: Any) -> None:
        """Assign a client to a tenant

 Assign the client to the specified tenant.
The client can then access tenant data and perform authorized actions.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    client_id (str):

Raises:
    errors.AssignClientToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignClientToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignClientToTenantNotFound: If the response status code is 404. The tenant was not found.
    errors.AssignClientToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignClientToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_client_to_tenant import sync as assign_client_to_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_client_to_tenant_sync(**_kwargs)


    def search_roles_for_tenant(self, tenant_id: str, *, data: SearchRolesForTenantData | Unset = UNSET, **kwargs: Any) -> SearchRolesForTenantResponse200:
        """Search roles for tenant

 Retrieves a filtered and sorted list of roles for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchRolesForTenantData | Unset): Role search request.

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchRolesForTenantResponse200"""
        from .api.tenant.search_roles_for_tenant import sync as search_roles_for_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_roles_for_tenant_sync(**_kwargs)


    def unassign_role_from_tenant(self, tenant_id: str, role_id: str, **kwargs: Any) -> None:
        """Unassign a role from a tenant

 Unassigns a role from a specified tenant.
Users, Clients or Groups, that have the role assigned, will no longer have access to the
tenant's data - unless they are assigned directly to the tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    role_id (str):

Raises:
    errors.UnassignRoleFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromTenantNotFound: If the response status code is 404. Not found. The tenant or role was not found.
    errors.UnassignRoleFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_role_from_tenant import sync as unassign_role_from_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_role_from_tenant_sync(**_kwargs)


    def unassign_mapping_rule_from_tenant(self, tenant_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Unassign a mapping rule from a tenant

 Unassigns a single mapping rule from a specified tenant without deleting the rule.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    mapping_rule_id (str):

Raises:
    errors.UnassignMappingRuleFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignMappingRuleFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignMappingRuleFromTenantNotFound: If the response status code is 404. Not found. The tenant or mapping rule was not found.
    errors.UnassignMappingRuleFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignMappingRuleFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_mapping_rule_from_tenant import sync as unassign_mapping_rule_from_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_mapping_rule_from_tenant_sync(**_kwargs)


    def search_users_for_tenant(self, tenant_id: str, *, data: SearchUsersForTenantData | Unset = UNSET, **kwargs: Any) -> SearchUsersForTenantResponse200:
        """Search users for tenant

 Retrieves a filtered and sorted list of users for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchUsersForTenantData | Unset):

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUsersForTenantResponse200"""
        from .api.tenant.search_users_for_tenant import sync as search_users_for_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_users_for_tenant_sync(**_kwargs)


    def assign_user_to_tenant(self, tenant_id: str, username: str, **kwargs: Any) -> None:
        """Assign a user to a tenant

 Assign a single user to a specified tenant. The user can then access tenant data and perform
authorized actions.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.AssignUserToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignUserToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignUserToTenantNotFound: If the response status code is 404. Not found. The tenant or user was not found.
    errors.AssignUserToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignUserToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_user_to_tenant import sync as assign_user_to_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_user_to_tenant_sync(**_kwargs)


    def assign_role_to_tenant(self, tenant_id: str, role_id: str, **kwargs: Any) -> None:
        """Assign a role to a tenant

 Assigns a role to a specified tenant.
Users, Clients or Groups, that have the role assigned, will get access to the tenant's data and can
perform actions according to their authorizations.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    role_id (str):

Raises:
    errors.AssignRoleToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToTenantNotFound: If the response status code is 404. Not found. The tenant or role was not found.
    errors.AssignRoleToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_role_to_tenant import sync as assign_role_to_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_role_to_tenant_sync(**_kwargs)


    def create_tenant(self, *, data: CreateTenantData, **kwargs: Any) -> CreateTenantResponse201:
        """Create tenant

 Creates a new tenant.

Args:
    body (CreateTenantData):

Raises:
    errors.CreateTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateTenantNotFound: If the response status code is 404. Not found. The resource was not found.
    errors.CreateTenantConflict: If the response status code is 409. Tenant with this id already exists.
    errors.CreateTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateTenantResponse201"""
        from .api.tenant.create_tenant import sync as create_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_tenant_sync(**_kwargs)


    def unassign_group_from_tenant(self, tenant_id: str, group_id: str, **kwargs: Any) -> None:
        """Unassign a group from a tenant

 Unassigns a group from a specified tenant.
Members of the group (users, clients) will no longer have access to the tenant's data - except they
are assigned directly to the tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    group_id (str):

Raises:
    errors.UnassignGroupFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignGroupFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignGroupFromTenantNotFound: If the response status code is 404. Not found. The tenant or group was not found.
    errors.UnassignGroupFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignGroupFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_group_from_tenant import sync as unassign_group_from_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_group_from_tenant_sync(**_kwargs)


    def search_clients_for_tenant(self, tenant_id: str, *, data: SearchClientsForTenantData | Unset = UNSET, **kwargs: Any) -> SearchClientsForTenantResponse200:
        """Search clients for tenant

 Retrieves a filtered and sorted list of clients for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchClientsForTenantData | Unset):

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClientsForTenantResponse200"""
        from .api.tenant.search_clients_for_tenant import sync as search_clients_for_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_clients_for_tenant_sync(**_kwargs)


    def unassign_user_from_tenant(self, tenant_id: str, username: str, **kwargs: Any) -> None:
        """Unassign a user from a tenant

 Unassigns the user from the specified tenant.
The user can no longer access tenant data.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.UnassignUserFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignUserFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignUserFromTenantNotFound: If the response status code is 404. Not found. The tenant or user was not found.
    errors.UnassignUserFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignUserFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_user_from_tenant import sync as unassign_user_from_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_user_from_tenant_sync(**_kwargs)


    def update_tenant(self, tenant_id: str, *, data: UpdateTenantData, **kwargs: Any) -> UpdateTenantResponse200:
        """Update tenant

 Updates an existing tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (UpdateTenantData):

Raises:
    errors.UpdateTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateTenantNotFound: If the response status code is 404. Not found. The tenant was not found.
    errors.UpdateTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateTenantResponse200"""
        from .api.tenant.update_tenant import sync as update_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_tenant_sync(**_kwargs)


    def search_mapping_rules_for_tenant(self, tenant_id: str, *, data: SearchMappingRulesForTenantData | Unset = UNSET, **kwargs: Any) -> SearchMappingRulesForTenantResponse200:
        """Search mapping rules for tenant

 Retrieves a filtered and sorted list of MappingRules for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchMappingRulesForTenantData | Unset):

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMappingRulesForTenantResponse200"""
        from .api.tenant.search_mapping_rules_for_tenant import sync as search_mapping_rules_for_tenant_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_mapping_rules_for_tenant_sync(**_kwargs)


    def update_global_cluster_variable(self, name: str, *, data: UpdateGlobalClusterVariableData, **kwargs: Any) -> UpdateGlobalClusterVariableResponse200:
        """Update a global-scoped cluster variable

 Updates the value of an existing global cluster variable.
The variable must exist, otherwise a 404 error is returned.

Args:
    name (str):
    body (UpdateGlobalClusterVariableData):

Raises:
    errors.UpdateGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.UpdateGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateGlobalClusterVariableResponse200"""
        from .api.cluster_variable.update_global_cluster_variable import sync as update_global_cluster_variable_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_global_cluster_variable_sync(**_kwargs)


    def get_global_cluster_variable(self, name: str, **kwargs: Any) -> GetGlobalClusterVariableResponse200:
        """Get a global-scoped cluster variable

Args:
    name (str):

Raises:
    errors.GetGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.GetGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetGlobalClusterVariableResponse200"""
        from .api.cluster_variable.get_global_cluster_variable import sync as get_global_cluster_variable_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_global_cluster_variable_sync(**_kwargs)


    def update_tenant_cluster_variable(self, tenant_id: str, name: str, *, data: UpdateTenantClusterVariableData, **kwargs: Any) -> UpdateTenantClusterVariableResponse200:
        """Update a tenant-scoped cluster variable

 Updates the value of an existing tenant-scoped cluster variable.
The variable must exist, otherwise a 404 error is returned.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    name (str):
    body (UpdateTenantClusterVariableData):

Raises:
    errors.UpdateTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.UpdateTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateTenantClusterVariableResponse200"""
        from .api.cluster_variable.update_tenant_cluster_variable import sync as update_tenant_cluster_variable_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_tenant_cluster_variable_sync(**_kwargs)


    def delete_global_cluster_variable(self, name: str, **kwargs: Any) -> None:
        """Delete a global-scoped cluster variable

Args:
    name (str):

Raises:
    errors.DeleteGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.DeleteGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.cluster_variable.delete_global_cluster_variable import sync as delete_global_cluster_variable_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_global_cluster_variable_sync(**_kwargs)


    def get_tenant_cluster_variable(self, tenant_id: str, name: str, **kwargs: Any) -> GetTenantClusterVariableResponse200:
        """Get a tenant-scoped cluster variable

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    name (str):

Raises:
    errors.GetTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.GetTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetTenantClusterVariableResponse200"""
        from .api.cluster_variable.get_tenant_cluster_variable import sync as get_tenant_cluster_variable_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_tenant_cluster_variable_sync(**_kwargs)


    def create_tenant_cluster_variable(self, tenant_id: str, *, data: CreateTenantClusterVariableData, **kwargs: Any) -> CreateTenantClusterVariableResponse200:
        """Create a tenant-scoped cluster variable

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (CreateTenantClusterVariableData):

Raises:
    errors.CreateTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateTenantClusterVariableResponse200"""
        from .api.cluster_variable.create_tenant_cluster_variable import sync as create_tenant_cluster_variable_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_tenant_cluster_variable_sync(**_kwargs)


    def delete_tenant_cluster_variable(self, tenant_id: str, name: str, **kwargs: Any) -> None:
        """Delete a tenant-scoped cluster variable

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    name (str):

Raises:
    errors.DeleteTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.DeleteTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.cluster_variable.delete_tenant_cluster_variable import sync as delete_tenant_cluster_variable_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_tenant_cluster_variable_sync(**_kwargs)


    def search_cluster_variables(self, *, data: SearchClusterVariablesData | Unset = UNSET, truncate_values: bool | Unset = UNSET, **kwargs: Any) -> SearchClusterVariablesResponse200:
        """Search for cluster variables based on given criteria. By default, long variable values in the
response are truncated.

Args:
    truncate_values (bool | Unset):
    body (SearchClusterVariablesData | Unset): Cluster variable search query request.

Raises:
    errors.SearchClusterVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchClusterVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchClusterVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchClusterVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClusterVariablesResponse200"""
        from .api.cluster_variable.search_cluster_variables import sync as search_cluster_variables_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_cluster_variables_sync(**_kwargs)


    def create_global_cluster_variable(self, *, data: CreateGlobalClusterVariableData, **kwargs: Any) -> CreateGlobalClusterVariableResponse200:
        """Create a global-scoped cluster variable

Args:
    body (CreateGlobalClusterVariableData):

Raises:
    errors.CreateGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateGlobalClusterVariableResponse200"""
        from .api.cluster_variable.create_global_cluster_variable import sync as create_global_cluster_variable_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_global_cluster_variable_sync(**_kwargs)


    def get_document(self, document_id: str, *, store_id: str | Unset = UNSET, content_hash: str | Unset = UNSET, **kwargs: Any) -> File:
        """Download document

 Download a document from the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

Args:
    document_id (str): Document Id that uniquely identifies a document.
    store_id (str | Unset):
    content_hash (str | Unset):

Raises:
    errors.GetDocumentNotFound: If the response status code is 404. The document with the given ID was not found.
    errors.GetDocumentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    File"""
        from .api.document.get_document import sync as get_document_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_document_sync(**_kwargs)


    def create_documents(self, *, data: CreateDocumentsData, store_id: str | Unset = UNSET, **kwargs: Any) -> CreateDocumentsResponse201:
        """Upload multiple documents

 Upload multiple documents to the Camunda 8 cluster.

The caller must provide a file name for each document, which will be used in case of a multi-status
response
to identify which documents failed to upload. The file name can be provided in the `Content-
Disposition` header
of the file part or in the `fileName` field of the metadata. You can add a parallel array of
metadata objects. These
are matched with the files based on index, and must have the same length as the files array.
To pass homogenous metadata for all files, spread the metadata over the metadata array.
A filename value provided explicitly via the metadata array in the request overrides the `Content-
Disposition` header
of the file part.

In case of a multi-status response, the response body will contain a list of
`DocumentBatchProblemDetail` objects,
each of which contains the file name of the document that failed to upload and the reason for the
failure.
The client can choose to retry the whole batch or individual documents based on the response.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

Args:
    store_id (str | Unset):
    body (CreateDocumentsData):

Raises:
    errors.CreateDocumentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateDocumentsUnsupportedMediaType: If the response status code is 415. The server cannot process the request because the media type (Content-Type) of the request payload is not supported by the server for the requested resource and method.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateDocumentsResponse201"""
        from .api.document.create_documents import sync as create_documents_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_documents_sync(**_kwargs)


    def create_document_link(self, document_id: str, *, data: CreateDocumentLinkData | Unset = UNSET, store_id: str | Unset = UNSET, content_hash: str | Unset = UNSET, **kwargs: Any) -> CreateDocumentLinkResponse201:
        """Create document link

 Create a link to a document in the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP

Args:
    document_id (str): Document Id that uniquely identifies a document.
    store_id (str | Unset):
    content_hash (str | Unset):
    body (CreateDocumentLinkData | Unset):

Raises:
    errors.CreateDocumentLinkBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateDocumentLinkResponse201"""
        from .api.document.create_document_link import sync as create_document_link_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_document_link_sync(**_kwargs)


    def create_document(self, *, data: CreateDocumentData, store_id: str | Unset = UNSET, document_id: str | Unset = UNSET, **kwargs: Any) -> CreateDocumentResponse201:
        """Upload document

 Upload a document to the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

Args:
    store_id (str | Unset):
    document_id (str | Unset): Document Id that uniquely identifies a document.
    body (CreateDocumentData):

Raises:
    errors.CreateDocumentBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateDocumentUnsupportedMediaType: If the response status code is 415. The server cannot process the request because the media type (Content-Type) of the request payload is not supported by the server for the requested resource and method.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateDocumentResponse201"""
        from .api.document.create_document import sync as create_document_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_document_sync(**_kwargs)


    def delete_document(self, document_id: str, *, store_id: str | Unset = UNSET, **kwargs: Any) -> None:
        """Delete document

 Delete a document from the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

Args:
    document_id (str): Document Id that uniquely identifies a document.
    store_id (str | Unset):

Raises:
    errors.DeleteDocumentNotFound: If the response status code is 404. The document with the given ID was not found.
    errors.DeleteDocumentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.document.delete_document import sync as delete_document_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_document_sync(**_kwargs)


    def delete_resource(self, resource_key: str, *, data: DeleteResourceDataType0 | None | Unset = UNSET, **kwargs: Any) -> DeleteResourceResponse200:
        """Delete resource

 Deletes a deployed resource. This can be a process definition, decision requirements
definition, or form definition deployed using the deploy resources endpoint. Specify the
resource you want to delete in the `resourceKey` parameter.

Once a resource has been deleted it cannot be recovered. If the resource needs to be
available again, a new deployment of the resource is required.

By default, only the resource itself is deleted from the runtime state. To also delete the
historic data associated with a resource, set the `deleteHistory` flag in the request body
to `true`. The historic data is deleted asynchronously via a batch operation. The details of
the created batch operation are included in the response. Note that history deletion is only
supported for process resources; for other resource types this flag is ignored and no history
will be deleted.

Args:
    resource_key (str): The system-assigned key for this resource.
    body (DeleteResourceDataType0 | None | Unset):

Raises:
    errors.DeleteResourceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteResourceNotFound: If the response status code is 404. The resource is not found.
    errors.DeleteResourceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteResourceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteResourceResponse200"""
        from .api.resource.delete_resource import sync as delete_resource_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_resource_sync(**_kwargs)


    def create_deployment(self, *, data: CreateDeploymentData, **kwargs: Any) -> CreateDeploymentResponse200:
        """Deploy resources

 Deploys one or more resources (e.g. processes, decision models, or forms).
This is an atomic call, i.e. either all resources are deployed or none of them are.

Args:
    body (CreateDeploymentData):

Raises:
    errors.CreateDeploymentBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateDeploymentServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateDeploymentResponse200"""
        from .api.resource.create_deployment import sync as create_deployment_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_deployment_sync(**_kwargs)


    def get_resource(self, resource_key: str, **kwargs: Any) -> GetResourceResponse200:
        """Get resource

 Returns a deployed resource.
:::info
Currently, this endpoint only supports RPA resources.
:::

Args:
    resource_key (str): The system-assigned key for this resource.

Raises:
    errors.GetResourceNotFound: If the response status code is 404. A resource with the given key was not found.
    errors.GetResourceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetResourceResponse200"""
        from .api.resource.get_resource import sync as get_resource_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_resource_sync(**_kwargs)


    def get_resource_content(self, resource_key: str, **kwargs: Any) -> File:
        """Get resource content

 Returns the content of a deployed resource.
:::info
Currently, this endpoint only supports RPA resources.
:::

Args:
    resource_key (str): The system-assigned key for this resource.

Raises:
    errors.GetResourceContentNotFound: If the response status code is 404. A resource with the given key was not found.
    errors.GetResourceContentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    File"""
        from .api.resource.get_resource_content import sync as get_resource_content_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_resource_content_sync(**_kwargs)


    def pin_clock(self, *, data: PinClockData, **kwargs: Any) -> None:
        """Pin internal clock (alpha)

 Set a precise, static time for the Zeebe engine's internal clock.
When the clock is pinned, it remains at the specified time and does not advance.
To change the time, the clock must be pinned again with a new timestamp.

This endpoint is an alpha feature and may be subject to change
in future releases.

Args:
    body (PinClockData):

Raises:
    errors.PinClockBadRequest: If the response status code is 400. The provided data is not valid.
    errors.PinClockInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.PinClockServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.clock.pin_clock import sync as pin_clock_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return pin_clock_sync(**_kwargs)


    def reset_clock(self, **kwargs: Any) -> None:
        """Reset internal clock (alpha)

 Resets the Zeebe engine's internal clock to the current system time, enabling it to tick in real-
time.
This operation is useful for returning the clock to
normal behavior after it has been pinned to a specific time.

This endpoint is an alpha feature and may be subject to change
in future releases.

Raises:
    errors.ResetClockInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResetClockServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.clock.reset_clock import sync as reset_clock_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return reset_clock_sync(**_kwargs)


    def activate_ad_hoc_sub_process_activities(self, ad_hoc_sub_process_instance_key: str, *, data: ActivateAdHocSubProcessActivitiesData, **kwargs: Any) -> None:
        """Activate activities within an ad-hoc sub-process

 Activates selected activities within an ad-hoc sub-process identified by element ID.
The provided element IDs must exist within the ad-hoc sub-process instance identified by the
provided adHocSubProcessInstanceKey.

Args:
    ad_hoc_sub_process_instance_key (str): System-generated key for a element instance.
        Example: 2251799813686789.
    body (ActivateAdHocSubProcessActivitiesData):

Raises:
    errors.ActivateAdHocSubProcessActivitiesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ActivateAdHocSubProcessActivitiesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ActivateAdHocSubProcessActivitiesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.ActivateAdHocSubProcessActivitiesNotFound: If the response status code is 404. The ad-hoc sub-process instance is not found or the provided key does not identify an ad-hoc sub-process.
    errors.ActivateAdHocSubProcessActivitiesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ActivateAdHocSubProcessActivitiesServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.ad_hoc_sub_process.activate_ad_hoc_sub_process_activities import sync as activate_ad_hoc_sub_process_activities_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return activate_ad_hoc_sub_process_activities_sync(**_kwargs)


    def get_decision_requirements_xml(self, decision_requirements_key: str, **kwargs: Any) -> str:
        """Get decision requirements XML

 Returns decision requirements as XML.

Args:
    decision_requirements_key (str): System-generated key for a deployed decision requirements
        definition. Example: 2251799813683346.

Raises:
    errors.GetDecisionRequirementsXmlBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionRequirementsXmlUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionRequirementsXmlForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionRequirementsXmlNotFound: If the response status code is 404. The decision requirements with the given key was not found. More details are provided in the response body.
    errors.GetDecisionRequirementsXmlInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    str"""
        from .api.decision_requirements.get_decision_requirements_xml import sync as get_decision_requirements_xml_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_decision_requirements_xml_sync(**_kwargs)


    def search_decision_requirements(self, *, data: SearchDecisionRequirementsData | Unset = UNSET, **kwargs: Any) -> SearchDecisionRequirementsResponse200:
        """Search decision requirements

 Search for decision requirements based on given criteria.

Args:
    body (SearchDecisionRequirementsData | Unset):

Raises:
    errors.SearchDecisionRequirementsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchDecisionRequirementsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchDecisionRequirementsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchDecisionRequirementsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchDecisionRequirementsResponse200"""
        from .api.decision_requirements.search_decision_requirements import sync as search_decision_requirements_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_decision_requirements_sync(**_kwargs)


    def get_decision_requirements(self, decision_requirements_key: str, **kwargs: Any) -> GetDecisionRequirementsResponse200:
        """Get decision requirements

 Returns Decision Requirements as JSON.

Args:
    decision_requirements_key (str): System-generated key for a deployed decision requirements
        definition. Example: 2251799813683346.

Raises:
    errors.GetDecisionRequirementsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionRequirementsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionRequirementsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionRequirementsNotFound: If the response status code is 404. The decision requirements with the given key was not found. More details are provided in the response body.
    errors.GetDecisionRequirementsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetDecisionRequirementsResponse200"""
        from .api.decision_requirements.get_decision_requirements import sync as get_decision_requirements_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_decision_requirements_sync(**_kwargs)


    def create_mapping_rule(self, *, data: CreateMappingRuleData | Unset = UNSET, **kwargs: Any) -> CreateMappingRuleResponse201:
        """Create mapping rule

 Create a new mapping rule

Args:
    body (CreateMappingRuleData | Unset):

Raises:
    errors.CreateMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateMappingRuleForbidden: If the response status code is 403. The request to create a mapping rule was denied. More details are provided in the response body.
    errors.CreateMappingRuleNotFound: If the response status code is 404. The request to create a mapping rule was denied.
    errors.CreateMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateMappingRuleResponse201"""
        from .api.mapping_rule.create_mapping_rule import sync as create_mapping_rule_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_mapping_rule_sync(**_kwargs)


    def search_mapping_rule(self, *, data: SearchMappingRuleData | Unset = UNSET, **kwargs: Any) -> SearchMappingRuleResponse200:
        """Search mapping rules

 Search for mapping rules based on given criteria.

Args:
    body (SearchMappingRuleData | Unset):

Raises:
    errors.SearchMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMappingRuleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMappingRuleResponse200"""
        from .api.mapping_rule.search_mapping_rule import sync as search_mapping_rule_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_mapping_rule_sync(**_kwargs)


    def delete_mapping_rule(self, mapping_rule_id: str, **kwargs: Any) -> None:
        """Delete a mapping rule

 Deletes the mapping rule with the given ID.

Args:
    mapping_rule_id (str):

Raises:
    errors.DeleteMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteMappingRuleNotFound: If the response status code is 404. The mapping rule with the mappingRuleId was not found.
    errors.DeleteMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.mapping_rule.delete_mapping_rule import sync as delete_mapping_rule_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_mapping_rule_sync(**_kwargs)


    def get_mapping_rule(self, mapping_rule_id: str, **kwargs: Any) -> GetMappingRuleResponse200:
        """Get a mapping rule

 Gets the mapping rule with the given ID.

Args:
    mapping_rule_id (str):

Raises:
    errors.GetMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetMappingRuleNotFound: If the response status code is 404. The mapping rule with the mappingRuleId was not found.
    errors.GetMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetMappingRuleResponse200"""
        from .api.mapping_rule.get_mapping_rule import sync as get_mapping_rule_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_mapping_rule_sync(**_kwargs)


    def update_mapping_rule(self, mapping_rule_id: str, *, data: UpdateMappingRuleData | Unset = UNSET, **kwargs: Any) -> UpdateMappingRuleResponse200:
        """Update mapping rule

 Update a mapping rule.

Args:
    mapping_rule_id (str):
    body (UpdateMappingRuleData | Unset):

Raises:
    errors.UpdateMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateMappingRuleForbidden: If the response status code is 403. The request to update a mapping rule was denied. More details are provided in the response body.
    errors.UpdateMappingRuleNotFound: If the response status code is 404. The request to update a mapping rule was denied.
    errors.UpdateMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateMappingRuleResponse200"""
        from .api.mapping_rule.update_mapping_rule import sync as update_mapping_rule_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_mapping_rule_sync(**_kwargs)


    def evaluate_expression(self, *, data: EvaluateExpressionData, **kwargs: Any) -> EvaluateExpressionResponse200:
        """Evaluate an expression

 Evaluates a FEEL expression and returns the result. Supports references to tenant scoped cluster
variables when a tenant ID is provided.

Args:
    body (EvaluateExpressionData):

Raises:
    errors.EvaluateExpressionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.EvaluateExpressionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.EvaluateExpressionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.EvaluateExpressionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    EvaluateExpressionResponse200"""
        from .api.expression.evaluate_expression import sync as evaluate_expression_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return evaluate_expression_sync(**_kwargs)


    def get_element_instance(self, element_instance_key: str, **kwargs: Any) -> GetElementInstanceResponse200:
        """Get element instance

 Returns element instance as JSON.

Args:
    element_instance_key (str): System-generated key for a element instance. Example:
        2251799813686789.

Raises:
    errors.GetElementInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetElementInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetElementInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetElementInstanceNotFound: If the response status code is 404. The element instance with the given key was not found. More details are provided in the response body.
    errors.GetElementInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetElementInstanceResponse200"""
        from .api.element_instance.get_element_instance import sync as get_element_instance_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_element_instance_sync(**_kwargs)


    def search_element_instances(self, *, data: SearchElementInstancesData | Unset = UNSET, **kwargs: Any) -> SearchElementInstancesResponse200:
        """Search element instances

 Search for element instances based on given criteria.

Args:
    body (SearchElementInstancesData | Unset): Element instance search request.

Raises:
    errors.SearchElementInstancesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchElementInstancesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchElementInstancesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchElementInstancesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchElementInstancesResponse200"""
        from .api.element_instance.search_element_instances import sync as search_element_instances_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_element_instances_sync(**_kwargs)


    def create_element_instance_variables(self, element_instance_key: str, *, data: CreateElementInstanceVariablesData, **kwargs: Any) -> None:
        """Update element instance variables

 Updates all the variables of a particular scope (for example, process instance, element instance)
with the given variable data.
Specify the element instance in the `elementInstanceKey` parameter.

Args:
    element_instance_key (str): System-generated key for a element instance. Example:
        2251799813686789.
    body (CreateElementInstanceVariablesData):

Raises:
    errors.CreateElementInstanceVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateElementInstanceVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateElementInstanceVariablesServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.element_instance.create_element_instance_variables import sync as create_element_instance_variables_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_element_instance_variables_sync(**_kwargs)


    def search_element_instance_incidents(self, element_instance_key: str, *, data: SearchElementInstanceIncidentsData, **kwargs: Any) -> SearchElementInstanceIncidentsResponse200:
        """Search for incidents of a specific element instance

 Search for incidents caused by the specified element instance, including incidents of any child
instances created from this element instance.

Although the `elementInstanceKey` is provided as a path parameter to indicate the root element
instance,
you may also include an `elementInstanceKey` within the filter object to narrow results to specific
child element instances. This is useful, for example, if you want to isolate incidents associated
with
nested or subordinate elements within the given element instance while excluding incidents directly
tied
to the root element itself.

Args:
    element_instance_key (str): System-generated key for a element instance. Example:
        2251799813686789.
    body (SearchElementInstanceIncidentsData):

Raises:
    errors.SearchElementInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchElementInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchElementInstanceIncidentsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchElementInstanceIncidentsNotFound: If the response status code is 404. The element instance with the given key was not found.
    errors.SearchElementInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchElementInstanceIncidentsResponse200"""
        from .api.element_instance.search_element_instance_incidents import sync as search_element_instance_incidents_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_element_instance_incidents_sync(**_kwargs)


    def unassign_user_task(self, user_task_key: str, **kwargs: Any) -> None:
        """Unassign user task

 Removes the assignee of a task with the given key.

Args:
    user_task_key (str): System-generated key for a user task.

Raises:
    errors.UnassignUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.UnassignUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.UnassignUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user_task.unassign_user_task import sync as unassign_user_task_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_user_task_sync(**_kwargs)


    def search_user_task_variables(self, user_task_key: str, *, data: SearchUserTaskVariablesData | Unset = UNSET, truncate_values: bool | Unset = UNSET, **kwargs: Any) -> SearchUserTaskVariablesResponse200:
        """Search user task variables

 Search for user task variables based on given criteria. By default, long variable values in the
response are truncated.

Args:
    user_task_key (str): System-generated key for a user task.
    truncate_values (bool | Unset):
    body (SearchUserTaskVariablesData | Unset): User task search query request.

Raises:
    errors.SearchUserTaskVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUserTaskVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUserTaskVariablesResponse200"""
        from .api.user_task.search_user_task_variables import sync as search_user_task_variables_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_user_task_variables_sync(**_kwargs)


    def update_user_task(self, user_task_key: str, *, data: UpdateUserTaskData | Unset = UNSET, **kwargs: Any) -> None:
        """Update user task

 Update a user task with the given key.

Args:
    user_task_key (str): System-generated key for a user task.
    body (UpdateUserTaskData | Unset):

Raises:
    errors.UpdateUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.UpdateUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.UpdateUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user_task.update_user_task import sync as update_user_task_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_user_task_sync(**_kwargs)


    def get_user_task_form(self, user_task_key: str, **kwargs: Any) -> GetUserTaskFormResponse200:
        """Get user task form

 Get the form of a user task.
Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

Args:
    user_task_key (str): System-generated key for a user task.

Raises:
    errors.GetUserTaskFormBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetUserTaskFormUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUserTaskFormForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUserTaskFormNotFound: If the response status code is 404. Not found
    errors.GetUserTaskFormInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUserTaskFormResponse200"""
        from .api.user_task.get_user_task_form import sync as get_user_task_form_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_user_task_form_sync(**_kwargs)


    def get_user_task(self, user_task_key: str, **kwargs: Any) -> GetUserTaskResponse200:
        """Get user task

 Get the user task by the user task key.

Args:
    user_task_key (str): System-generated key for a user task.

Raises:
    errors.GetUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetUserTaskUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUserTaskForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.GetUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUserTaskResponse200"""
        from .api.user_task.get_user_task import sync as get_user_task_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_user_task_sync(**_kwargs)


    def complete_user_task(self, user_task_key: str, *, data: CompleteUserTaskData | Unset = UNSET, **kwargs: Any) -> None:
        """Complete user task

 Completes a user task with the given key.

Args:
    user_task_key (str): System-generated key for a user task.
    body (CompleteUserTaskData | Unset):

Raises:
    errors.CompleteUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CompleteUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.CompleteUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.CompleteUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CompleteUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user_task.complete_user_task import sync as complete_user_task_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return complete_user_task_sync(**_kwargs)


    def search_user_task_audit_logs(self, user_task_key: str, *, data: SearchUserTaskAuditLogsData | Unset = UNSET, **kwargs: Any) -> SearchUserTaskAuditLogsResponse200:
        """Search user task audit logs

 Search for user task audit logs based on given criteria.

Args:
    user_task_key (str): System-generated key for a user task.
    body (SearchUserTaskAuditLogsData | Unset): User task search query request.

Raises:
    errors.SearchUserTaskAuditLogsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUserTaskAuditLogsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUserTaskAuditLogsResponse200"""
        from .api.user_task.search_user_task_audit_logs import sync as search_user_task_audit_logs_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_user_task_audit_logs_sync(**_kwargs)


    def search_user_tasks(self, *, data: SearchUserTasksData | Unset = UNSET, **kwargs: Any) -> SearchUserTasksResponse200:
        """Search user tasks

 Search for user tasks based on given criteria.

Args:
    body (SearchUserTasksData | Unset): User task search query request.

Raises:
    errors.SearchUserTasksBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUserTasksUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchUserTasksForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchUserTasksInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUserTasksResponse200"""
        from .api.user_task.search_user_tasks import sync as search_user_tasks_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_user_tasks_sync(**_kwargs)


    def assign_user_task(self, user_task_key: str, *, data: AssignUserTaskData, **kwargs: Any) -> None:
        """Assign user task

 Assigns a user task with the given key to the given assignee.

Args:
    user_task_key (str): System-generated key for a user task.
    body (AssignUserTaskData):

Raises:
    errors.AssignUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.AssignUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.AssignUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user_task.assign_user_task import sync as assign_user_task_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_user_task_sync(**_kwargs)


    def search_correlated_message_subscriptions(self, *, data: SearchCorrelatedMessageSubscriptionsData | Unset = UNSET, **kwargs: Any) -> SearchCorrelatedMessageSubscriptionsResponse200:
        """Search correlated message subscriptions

 Search correlated message subscriptions based on given criteria.

Args:
    body (SearchCorrelatedMessageSubscriptionsData | Unset):

Raises:
    errors.SearchCorrelatedMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchCorrelatedMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchCorrelatedMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchCorrelatedMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchCorrelatedMessageSubscriptionsResponse200"""
        from .api.message_subscription.search_correlated_message_subscriptions import sync as search_correlated_message_subscriptions_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_correlated_message_subscriptions_sync(**_kwargs)


    def search_message_subscriptions(self, *, data: SearchMessageSubscriptionsData | Unset = UNSET, **kwargs: Any) -> SearchMessageSubscriptionsResponse200:
        """Search message subscriptions

 Search for message subscriptions based on given criteria.

Args:
    body (SearchMessageSubscriptionsData | Unset):

Raises:
    errors.SearchMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMessageSubscriptionsResponse200"""
        from .api.message_subscription.search_message_subscriptions import sync as search_message_subscriptions_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_message_subscriptions_sync(**_kwargs)


    def get_decision_definition(self, decision_definition_key: str, **kwargs: Any) -> GetDecisionDefinitionResponse200:
        """Get decision definition

 Returns a decision definition by key.

Args:
    decision_definition_key (str): System-generated key for a decision definition. Example:
        2251799813326547.

Raises:
    errors.GetDecisionDefinitionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionDefinitionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionDefinitionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionDefinitionNotFound: If the response status code is 404. The decision definition with the given key was not found. More details are provided in the response body.
    errors.GetDecisionDefinitionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetDecisionDefinitionResponse200"""
        from .api.decision_definition.get_decision_definition import sync as get_decision_definition_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_decision_definition_sync(**_kwargs)


    def evaluate_decision(self, *, data: DecisionevaluationbyID | Decisionevaluationbykey, **kwargs: Any) -> EvaluateDecisionResponse200:
        """Evaluate decision

 Evaluates a decision.
You specify the decision to evaluate either by using its unique key (as returned by
DeployResource), or using the decision ID. When using the decision ID, the latest deployed
version of the decision is used.

Args:
    body (DecisionevaluationbyID | Decisionevaluationbykey):

Raises:
    errors.EvaluateDecisionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.EvaluateDecisionNotFound: If the response status code is 404. The decision is not found.
    errors.EvaluateDecisionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.EvaluateDecisionServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    EvaluateDecisionResponse200"""
        from .api.decision_definition.evaluate_decision import sync as evaluate_decision_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return evaluate_decision_sync(**_kwargs)


    def search_decision_definitions(self, *, data: SearchDecisionDefinitionsData | Unset = UNSET, **kwargs: Any) -> SearchDecisionDefinitionsResponse200:
        """Search decision definitions

 Search for decision definitions based on given criteria.

Args:
    body (SearchDecisionDefinitionsData | Unset):

Raises:
    errors.SearchDecisionDefinitionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchDecisionDefinitionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchDecisionDefinitionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchDecisionDefinitionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchDecisionDefinitionsResponse200"""
        from .api.decision_definition.search_decision_definitions import sync as search_decision_definitions_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_decision_definitions_sync(**_kwargs)


    def get_decision_definition_xml(self, decision_definition_key: str, **kwargs: Any) -> str:
        """Get decision definition XML

 Returns decision definition as XML.

Args:
    decision_definition_key (str): System-generated key for a decision definition. Example:
        2251799813326547.

Raises:
    errors.GetDecisionDefinitionXmlBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionDefinitionXmlUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionDefinitionXmlForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionDefinitionXmlNotFound: If the response status code is 404. The decision definition with the given key was not found. More details are provided in the response body.
    errors.GetDecisionDefinitionXmlInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    str"""
        from .api.decision_definition.get_decision_definition_xml import sync as get_decision_definition_xml_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_decision_definition_xml_sync(**_kwargs)


    def create_authorization(self, *, data: Object | Object1, **kwargs: Any) -> CreateAuthorizationResponse201:
        """Create authorization

 Create the authorization.

Args:
    body (Object | Object1): Defines an authorization request.
        Either an id-based or a property-based authorization can be provided.

Raises:
    errors.CreateAuthorizationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateAuthorizationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateAuthorizationNotFound: If the response status code is 404. The owner was not found.
    errors.CreateAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateAuthorizationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateAuthorizationResponse201"""
        from .api.authorization.create_authorization import sync as create_authorization_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_authorization_sync(**_kwargs)


    def get_authorization(self, authorization_key: str, **kwargs: Any) -> GetAuthorizationResponse200:
        """Get authorization

 Get authorization by the given key.

Args:
    authorization_key (str): System-generated key for an authorization. Example:
        2251799813684332.

Raises:
    errors.GetAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetAuthorizationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetAuthorizationNotFound: If the response status code is 404. The authorization with the given key was not found.
    errors.GetAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetAuthorizationResponse200"""
        from .api.authorization.get_authorization import sync as get_authorization_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_authorization_sync(**_kwargs)


    def update_authorization(self, authorization_key: str, *, data: Object | Object1, **kwargs: Any) -> None:
        """Update authorization

 Update the authorization with the given key.

Args:
    authorization_key (str): System-generated key for an authorization. Example:
        2251799813684332.
    body (Object | Object1): Defines an authorization request.
        Either an id-based or a property-based authorization can be provided.

Raises:
    errors.UpdateAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateAuthorizationNotFound: If the response status code is 404. The authorization with the authorizationKey was not found.
    errors.UpdateAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateAuthorizationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.authorization.update_authorization import sync as update_authorization_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_authorization_sync(**_kwargs)


    def search_authorizations(self, *, data: SearchAuthorizationsData | Unset = UNSET, **kwargs: Any) -> SearchAuthorizationsResponse200:
        """Search authorizations

 Search for authorizations based on given criteria.

Args:
    body (SearchAuthorizationsData | Unset):

Raises:
    errors.SearchAuthorizationsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchAuthorizationsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchAuthorizationsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchAuthorizationsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchAuthorizationsResponse200"""
        from .api.authorization.search_authorizations import sync as search_authorizations_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_authorizations_sync(**_kwargs)


    def delete_authorization(self, authorization_key: str, **kwargs: Any) -> None:
        """Delete authorization

 Deletes the authorization with the given key.

Args:
    authorization_key (str): System-generated key for an authorization. Example:
        2251799813684332.

Raises:
    errors.DeleteAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteAuthorizationNotFound: If the response status code is 404. The authorization with the authorizationKey was not found.
    errors.DeleteAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteAuthorizationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.authorization.delete_authorization import sync as delete_authorization_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_authorization_sync(**_kwargs)


    def search_incidents(self, *, data: SearchIncidentsData | Unset = UNSET, **kwargs: Any) -> SearchIncidentsResponse200:
        """Search incidents

 Search for incidents based on given criteria.

Args:
    body (SearchIncidentsData | Unset):

Raises:
    errors.SearchIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchIncidentsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchIncidentsResponse200"""
        from .api.incident.search_incidents import sync as search_incidents_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_incidents_sync(**_kwargs)


    def get_process_instance_statistics_by_definition(self, *, data: GetProcessInstanceStatisticsByDefinitionData, **kwargs: Any) -> GetProcessInstanceStatisticsByDefinitionResponse200:
        """Get process instance statistics by definition

 Returns statistics for active process instances with incidents, grouped by process
definition. The result set is scoped to a specific incident error hash code, which must be
provided as a filter in the request body.

Args:
    body (GetProcessInstanceStatisticsByDefinitionData):

Raises:
    errors.GetProcessInstanceStatisticsByDefinitionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsByDefinitionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsByDefinitionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsByDefinitionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsByDefinitionResponse200"""
        from .api.incident.get_process_instance_statistics_by_definition import sync as get_process_instance_statistics_by_definition_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_instance_statistics_by_definition_sync(**_kwargs)


    def get_incident(self, incident_key: str, **kwargs: Any) -> GetIncidentResponse200:
        """Get incident

 Returns incident as JSON.

Args:
    incident_key (str): System-generated key for a incident. Example: 2251799813689432.

Raises:
    errors.GetIncidentBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetIncidentUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetIncidentForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetIncidentNotFound: If the response status code is 404. The incident with the given key was not found.
    errors.GetIncidentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetIncidentResponse200"""
        from .api.incident.get_incident import sync as get_incident_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_incident_sync(**_kwargs)


    def resolve_incident(self, incident_key: str, *, data: ResolveIncidentData | Unset = UNSET, **kwargs: Any) -> None:
        """Resolve incident

 Marks the incident as resolved; most likely a call to Update job will be necessary
to reset the job's retries, followed by this call.

Args:
    incident_key (str): System-generated key for a incident. Example: 2251799813689432.
    body (ResolveIncidentData | Unset):

Raises:
    errors.ResolveIncidentBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ResolveIncidentNotFound: If the response status code is 404. The incident with the incidentKey is not found.
    errors.ResolveIncidentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResolveIncidentServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.incident.resolve_incident import sync as resolve_incident_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return resolve_incident_sync(**_kwargs)


    def get_process_instance_statistics_by_error(self, *, data: GetProcessInstanceStatisticsByErrorData | Unset = UNSET, **kwargs: Any) -> GetProcessInstanceStatisticsByErrorResponse200:
        """Get process instance statistics by error

 Returns statistics for active process instances that currently have active incidents,
grouped by incident error hash code.

Args:
    body (GetProcessInstanceStatisticsByErrorData | Unset):

Raises:
    errors.GetProcessInstanceStatisticsByErrorBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsByErrorUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsByErrorForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsByErrorInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsByErrorResponse200"""
        from .api.incident.get_process_instance_statistics_by_error import sync as get_process_instance_statistics_by_error_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_process_instance_statistics_by_error_sync(**_kwargs)


    def get_user(self, username: str, **kwargs: Any) -> GetUserResponse200:
        """Get user

 Get a user by its username.

Args:
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.GetUserUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUserNotFound: If the response status code is 404. The user with the given username was not found.
    errors.GetUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUserResponse200"""
        from .api.user.get_user import sync as get_user_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_user_sync(**_kwargs)


    def delete_user(self, username: str, **kwargs: Any) -> None:
        """Delete user

 Deletes a user.

Args:
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.DeleteUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteUserNotFound: If the response status code is 404. The user is not found.
    errors.DeleteUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user.delete_user import sync as delete_user_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_user_sync(**_kwargs)


    def create_user(self, *, data: CreateUserData, **kwargs: Any) -> CreateUserResponse201:
        """Create user

 Create a new user.

Args:
    body (CreateUserData):

Raises:
    errors.CreateUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateUserUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateUserConflict: If the response status code is 409. A user with this username already exists.
    errors.CreateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateUserResponse201"""
        from .api.user.create_user import sync as create_user_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_user_sync(**_kwargs)


    def search_users(self, *, data: SearchUsersData | Unset = UNSET, **kwargs: Any) -> SearchUsersResponse200:
        """Search users

 Search for users based on given criteria.

Args:
    body (SearchUsersData | Unset):

Raises:
    errors.SearchUsersBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUsersUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchUsersForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchUsersInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUsersResponse200"""
        from .api.user.search_users import sync as search_users_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_users_sync(**_kwargs)


    def update_user(self, username: str, *, data: UpdateUserData, **kwargs: Any) -> UpdateUserResponse200:
        """Update user

 Updates a user.

Args:
    username (str): The unique name of a user. Example: swillis.
    body (UpdateUserData):

Raises:
    errors.UpdateUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateUserNotFound: If the response status code is 404. The user was not found.
    errors.UpdateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateUserResponse200"""
        from .api.user.update_user import sync as update_user_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_user_sync(**_kwargs)


    def get_usage_metrics(self, *, start_time: datetime.datetime, end_time: datetime.datetime, tenant_id: str | Unset = UNSET, with_tenants: bool | Unset = False, **kwargs: Any) -> GetUsageMetricsResponse200:
        """Get usage metrics

 Retrieve the usage metrics based on given criteria.

Args:
    start_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
    end_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
    tenant_id (str | Unset): The unique identifier of the tenant. Example: customer-service.
    with_tenants (bool | Unset):  Default: False.

Raises:
    errors.GetUsageMetricsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetUsageMetricsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUsageMetricsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUsageMetricsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUsageMetricsResponse200"""
        from .api.system.get_usage_metrics import sync as get_usage_metrics_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_usage_metrics_sync(**_kwargs)


    def update_role(self, role_id: str, *, data: UpdateRoleData, **kwargs: Any) -> UpdateRoleResponse200:
        """Update role

 Update a role with the given ID.

Args:
    role_id (str):
    body (UpdateRoleData):

Raises:
    errors.UpdateRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateRoleNotFound: If the response status code is 404. The role with the ID is not found.
    errors.UpdateRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateRoleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateRoleResponse200"""
        from .api.role.update_role import sync as update_role_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return update_role_sync(**_kwargs)


    def assign_role_to_client(self, role_id: str, client_id: str, **kwargs: Any) -> None:
        """Assign a role to a client

 Assigns the specified role to the client. The client will inherit the authorizations associated with
this role.

Args:
    role_id (str):
    client_id (str):

Raises:
    errors.AssignRoleToClientBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToClientForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToClientNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.AssignRoleToClientConflict: If the response status code is 409. The role was already assigned to the client with the given ID.
    errors.AssignRoleToClientInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToClientServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.assign_role_to_client import sync as assign_role_to_client_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_role_to_client_sync(**_kwargs)


    def get_role(self, role_id: str, **kwargs: Any) -> GetRoleResponse200:
        """Get role

 Get a role by its ID.

Args:
    role_id (str):

Raises:
    errors.GetRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.GetRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetRoleResponse200"""
        from .api.role.get_role import sync as get_role_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_role_sync(**_kwargs)


    def unassign_role_from_mapping_rule(self, role_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Unassign a role from a mapping rule

 Unassigns a role from a mapping rule.

Args:
    role_id (str):
    mapping_rule_id (str):

Raises:
    errors.UnassignRoleFromMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromMappingRuleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromMappingRuleNotFound: If the response status code is 404. The role or mapping rule with the given ID was not found.
    errors.UnassignRoleFromMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.unassign_role_from_mapping_rule import sync as unassign_role_from_mapping_rule_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_role_from_mapping_rule_sync(**_kwargs)


    def search_users_for_role(self, role_id: str, *, data: SearchUsersForRoleData | Unset = UNSET, **kwargs: Any) -> SearchUsersForRoleResponse200:
        """Search role users

 Search users with assigned role.

Args:
    role_id (str):
    body (SearchUsersForRoleData | Unset):

Raises:
    errors.SearchUsersForRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUsersForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchUsersForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchUsersForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.SearchUsersForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUsersForRoleResponse200"""
        from .api.role.search_users_for_role import sync as search_users_for_role_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_users_for_role_sync(**_kwargs)


    def search_mapping_rules_for_role(self, role_id: str, *, data: SearchMappingRulesForRoleData | Unset = UNSET, **kwargs: Any) -> SearchMappingRulesForRoleResponse200:
        """Search role mapping rules

 Search mapping rules with assigned role.

Args:
    role_id (str):
    body (SearchMappingRulesForRoleData | Unset):

Raises:
    errors.SearchMappingRulesForRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMappingRulesForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMappingRulesForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMappingRulesForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.SearchMappingRulesForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMappingRulesForRoleResponse200"""
        from .api.role.search_mapping_rules_for_role import sync as search_mapping_rules_for_role_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_mapping_rules_for_role_sync(**_kwargs)


    def search_groups_for_role(self, role_id: str, *, data: SearchGroupsForRoleData | Unset = UNSET, **kwargs: Any) -> SearchGroupsForRoleResponse200:
        """Search role groups

 Search groups with assigned role.

Args:
    role_id (str):
    body (SearchGroupsForRoleData | Unset):

Raises:
    errors.SearchGroupsForRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchGroupsForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchGroupsForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchGroupsForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.SearchGroupsForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchGroupsForRoleResponse200"""
        from .api.role.search_groups_for_role import sync as search_groups_for_role_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_groups_for_role_sync(**_kwargs)


    def search_roles(self, *, data: SearchRolesData | Unset = UNSET, **kwargs: Any) -> SearchRolesResponse200:
        """Search roles

 Search for roles based on given criteria.

Args:
    body (SearchRolesData | Unset): Role search request.

Raises:
    errors.SearchRolesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchRolesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchRolesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchRolesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchRolesResponse200"""
        from .api.role.search_roles import sync as search_roles_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_roles_sync(**_kwargs)


    def search_clients_for_role(self, role_id: str, *, data: SearchClientsForRoleData | Unset = UNSET, **kwargs: Any) -> SearchClientsForRoleResponse200:
        """Search role clients

 Search clients with assigned role.

Args:
    role_id (str):
    body (SearchClientsForRoleData | Unset):

Raises:
    errors.SearchClientsForRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchClientsForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchClientsForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchClientsForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.SearchClientsForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClientsForRoleResponse200"""
        from .api.role.search_clients_for_role import sync as search_clients_for_role_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return search_clients_for_role_sync(**_kwargs)


    def create_role(self, *, data: CreateRoleData | Unset = UNSET, **kwargs: Any) -> CreateRoleResponse201:
        """Create role

 Create a new role.

Args:
    body (CreateRoleData | Unset):

Raises:
    errors.CreateRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateRoleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateRoleResponse201"""
        from .api.role.create_role import sync as create_role_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return create_role_sync(**_kwargs)


    def assign_role_to_group(self, role_id: str, group_id: str, **kwargs: Any) -> None:
        """Assign a role to a group

 Assigns the specified role to the group. Every member of the group (user or client) will inherit the
authorizations associated with this role.

Args:
    role_id (str):
    group_id (str):

Raises:
    errors.AssignRoleToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToGroupNotFound: If the response status code is 404. The role or group with the given ID was not found.
    errors.AssignRoleToGroupConflict: If the response status code is 409. The role is already assigned to the group with the given ID.
    errors.AssignRoleToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.assign_role_to_group import sync as assign_role_to_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_role_to_group_sync(**_kwargs)


    def assign_role_to_mapping_rule(self, role_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Assign a role to a mapping rule

 Assigns a role to a mapping rule.

Args:
    role_id (str):
    mapping_rule_id (str):

Raises:
    errors.AssignRoleToMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToMappingRuleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToMappingRuleNotFound: If the response status code is 404. The role or mapping rule with the given ID was not found.
    errors.AssignRoleToMappingRuleConflict: If the response status code is 409. The role is already assigned to the mapping rule with the given ID.
    errors.AssignRoleToMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.assign_role_to_mapping_rule import sync as assign_role_to_mapping_rule_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_role_to_mapping_rule_sync(**_kwargs)


    def unassign_role_from_client(self, role_id: str, client_id: str, **kwargs: Any) -> None:
        """Unassign a role from a client

 Unassigns the specified role from the client. The client will no longer inherit the authorizations
associated with this role.

Args:
    role_id (str):
    client_id (str):

Raises:
    errors.UnassignRoleFromClientBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromClientForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromClientNotFound: If the response status code is 404. The role or client with the given ID or username was not found.
    errors.UnassignRoleFromClientInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromClientServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.unassign_role_from_client import sync as unassign_role_from_client_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_role_from_client_sync(**_kwargs)


    def delete_role(self, role_id: str, **kwargs: Any) -> None:
        """Delete role

 Deletes the role with the given ID.

Args:
    role_id (str):

Raises:
    errors.DeleteRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteRoleNotFound: If the response status code is 404. The role with the ID was not found.
    errors.DeleteRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteRoleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.delete_role import sync as delete_role_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return delete_role_sync(**_kwargs)


    def assign_role_to_user(self, role_id: str, username: str, **kwargs: Any) -> None:
        """Assign a role to a user

 Assigns the specified role to the user. The user will inherit the authorizations associated with
this role.

Args:
    role_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.AssignRoleToUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToUserNotFound: If the response status code is 404. The role or user with the given ID or username was not found.
    errors.AssignRoleToUserConflict: If the response status code is 409. The role is already assigned to the user with the given ID.
    errors.AssignRoleToUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.assign_role_to_user import sync as assign_role_to_user_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return assign_role_to_user_sync(**_kwargs)


    def unassign_role_from_group(self, role_id: str, group_id: str, **kwargs: Any) -> None:
        """Unassign a role from a group

 Unassigns the specified role from the group. All group members (user or client) no longer inherit
the authorizations associated with this role.

Args:
    role_id (str):
    group_id (str):

Raises:
    errors.UnassignRoleFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromGroupNotFound: If the response status code is 404. The role or group with the given ID was not found.
    errors.UnassignRoleFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.unassign_role_from_group import sync as unassign_role_from_group_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_role_from_group_sync(**_kwargs)


    def unassign_role_from_user(self, role_id: str, username: str, **kwargs: Any) -> None:
        """Unassign a role from a user

 Unassigns a role from a user. The user will no longer inherit the authorizations associated with
this role.

Args:
    role_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.UnassignRoleFromUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromUserNotFound: If the response status code is 404. The role or user with the given ID or username was not found.
    errors.UnassignRoleFromUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.unassign_role_from_user import sync as unassign_role_from_user_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return unassign_role_from_user_sync(**_kwargs)


    def get_license(self, **kwargs: Any) -> GetLicenseResponse200:
        """Get license status

 Obtains the status of the current Camunda license.

Raises:
    errors.GetLicenseInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetLicenseResponse200"""
        from .api.license_.get_license import sync as get_license_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return get_license_sync(**_kwargs)


    def broadcast_signal(self, *, data: BroadcastSignalData, **kwargs: Any) -> BroadcastSignalResponse200:
        """Broadcast signal

 Broadcasts a signal.

Args:
    body (BroadcastSignalData):

Raises:
    errors.BroadcastSignalBadRequest: If the response status code is 400. The provided data is not valid.
    errors.BroadcastSignalNotFound: If the response status code is 404. The signal is not found.
    errors.BroadcastSignalInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.BroadcastSignalServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    BroadcastSignalResponse200"""
        from .api.signal.broadcast_signal import sync as broadcast_signal_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return broadcast_signal_sync(**_kwargs)


    def evaluate_conditionals(self, *, data: EvaluateConditionalsData, **kwargs: Any) -> EvaluateConditionalsResponse200:
        """Evaluate root level conditional start events

 Evaluates root-level conditional start events for process definitions.
If the evaluation is successful, it will return the keys of all created process instances, along
with their associated process definition key.
Multiple root-level conditional start events of the same process definition can trigger if their
conditions evaluate to true.

Args:
    body (EvaluateConditionalsData):

Raises:
    errors.EvaluateConditionalsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.EvaluateConditionalsForbidden: If the response status code is 403. The client is not authorized to start process instances for the specified process definition. If a processDefinitionKey is not provided, this indicates that the client is not authorized to start process instances for at least one of the matched process definitions.
    errors.EvaluateConditionalsNotFound: If the response status code is 404. The process definition was not found for the given processDefinitionKey.
    errors.EvaluateConditionalsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.EvaluateConditionalsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    EvaluateConditionalsResponse200"""
        from .api.conditional.evaluate_conditionals import sync as evaluate_conditionals_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return evaluate_conditionals_sync(**_kwargs)



class CamundaAsyncClient:
    client: Client | AuthenticatedClient
    configuration: CamundaSdkConfiguration
    auth_provider: AuthProvider
    _workers: list[JobWorker]

    def __init__(self, configuration: CamundaSdkConfigPartial | None = None, auth_provider: AuthProvider | None = None, **kwargs: Any):
        resolved = ConfigurationResolver(
            environment=read_environment(),
            explicit_configuration=configuration,
        ).resolve()
        self.configuration = resolved.effective

        if "base_url" in kwargs:
            raise TypeError(
                "CamundaAsyncClient no longer accepts base_url; set CAMUNDA_REST_ADDRESS (or ZEEBE_REST_ADDRESS) via configuration/environment instead."
            )
        if "token" in kwargs:
            raise TypeError(
                "CamundaAsyncClient no longer accepts token; use configuration-based auth (CAMUNDA_AUTH_STRATEGY) instead."
            )

        if auth_provider is None:
            if self.configuration.CAMUNDA_AUTH_STRATEGY == "NONE":
                auth_provider = NullAuthProvider()
            elif self.configuration.CAMUNDA_AUTH_STRATEGY == "BASIC":
                auth_provider = BasicAuthProvider(
                    username=self.configuration.CAMUNDA_BASIC_AUTH_USERNAME or "",
                    password=self.configuration.CAMUNDA_BASIC_AUTH_PASSWORD or "",
                )
            elif self.configuration.CAMUNDA_AUTH_STRATEGY == "OAUTH":
                httpx_args: dict[str, Any] = kwargs.get("httpx_args") or {}
                transport: Any = httpx_args.get("transport")
                auth_provider = AsyncOAuthClientCredentialsAuthProvider(
                    oauth_url=self.configuration.CAMUNDA_OAUTH_URL,
                    client_id=self.configuration.CAMUNDA_CLIENT_ID or "",
                    client_secret=self.configuration.CAMUNDA_CLIENT_SECRET or "",
                    audience=self.configuration.CAMUNDA_TOKEN_AUDIENCE,
                    cache_dir=self.configuration.CAMUNDA_TOKEN_CACHE_DIR,
                    disk_cache_disable=self.configuration.CAMUNDA_TOKEN_DISK_CACHE_DISABLE,
                    transport=transport,
                )
            else:
                auth_provider = NullAuthProvider()

        self.auth_provider = auth_provider

        # Ensure every request gets auth headers via httpx event hooks.
        kwargs["httpx_args"] = inject_auth_event_hooks(
            kwargs.get("httpx_args"),
            auth_provider,
            async_client=True,
            log_level=self.configuration.CAMUNDA_SDK_LOG_LEVEL,
        )

        self.client = Client(base_url=self.configuration.CAMUNDA_REST_ADDRESS, **kwargs)
        self._workers = []

    async def __aenter__(self) -> "CamundaAsyncClient":
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        try:
            await self.client.__aexit__(*args, **kwargs)
        finally:
            aclose = getattr(self.auth_provider, "aclose", None)
            if callable(aclose):
                try:
                    await aclose()  # type: ignore[reportGeneralTypeIssues]
                except Exception:
                    pass
            else:
                close = getattr(self.auth_provider, "close", None)
                if callable(close):
                    try:
                        close()
                    except Exception:
                        pass

    async def aclose(self) -> None:
        """Close underlying HTTP clients.

        This closes both the API client's async httpx client and, when available,
        the auth provider's token client.
        """

        aclose = getattr(self.auth_provider, "aclose", None)
        if callable(aclose):
            try:
                await aclose()  # type: ignore[reportGeneralTypeIssues]
            except Exception:
                pass
        else:
            close = getattr(self.auth_provider, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass

        try:
            await self.client.get_async_httpx_client().aclose()
        except Exception:
            return

    def create_job_worker(self, config: WorkerConfig, callback: JobHandler, auto_start: bool = True) -> JobWorker:
        worker = JobWorker(self, callback, config)
        self._workers.append(worker)
        if auto_start:
            worker.start()
        return worker

    async def run_workers(self):
        stop_event = asyncio.Event()
        try:
            await stop_event.wait()
        except asyncio.CancelledError:
            pass
        finally:
            for worker in self._workers:
                worker.stop()

    async def deploy_resources_from_files(self, files: list[str | Path], tenant_id: str | None = None) -> ExtendedDeploymentResult:
        """Deploy BPMN/DMN/Form resources from local files.

        Async variant of :meth:`CamundaClient.deploy_resources_from_files`.

        This reads each file path in ``files`` as bytes, wraps them into
        :class:`camunda_orchestration_sdk.types.File`, calls :meth:`create_deployment`, and returns
        an :class:`ExtendedDeploymentResult`.

        Note: file reads are currently performed using blocking I/O (``open(...).read()``). If you
        need fully non-blocking file access, load the bytes yourself and call :meth:`create_deployment`.

        Args:
            files: File paths (``str`` or ``Path``) to deploy.
            tenant_id: Optional tenant identifier. If not provided, the default tenant is used.

        Returns:
            ExtendedDeploymentResult: The deployment result with extracted resource lists.

        Raises:
            FileNotFoundError: If any file path does not exist.
            PermissionError: If any file path cannot be read.
            IsADirectoryError: If any file path is a directory.
            OSError: For other I/O failures while reading files.
            Exception: Propagates any exception raised by :meth:`create_deployment` (including
                typed API errors in :mod:`camunda_orchestration_sdk.errors` and ``httpx.TimeoutException``).
        """
        from .models.create_deployment_data import CreateDeploymentData
        from .semantic_types import TenantId
        from .types import File, UNSET
        import io
        import os

        resources: list[File] = []
        for file_path in files:
            file_path = str(file_path)
            with open(file_path, "rb") as f:
                content = f.read()
            resources.append(File(payload=io.BytesIO(content), file_name=os.path.basename(file_path)))

        data = CreateDeploymentData(resources=resources, tenant_id=TenantId(tenant_id) if tenant_id is not None else UNSET)
        return ExtendedDeploymentResult(await self.create_deployment(data=data))


    async def get_audit_log(self, audit_log_key: str, **kwargs: Any) -> GetAuditLogResponse200:
        """Get audit log

 Get an audit log entry by auditLogKey.

Args:
    audit_log_key (str): System-generated key for an audit log entry. Example:
        22517998136843567.

Raises:
    errors.GetAuditLogUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetAuditLogForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetAuditLogNotFound: If the response status code is 404. The audit log with the given key was not found.
    errors.GetAuditLogInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetAuditLogResponse200"""
        from .api.audit_log.get_audit_log import asyncio as get_audit_log_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_audit_log_asyncio(**_kwargs)


    async def search_audit_logs(self, *, data: SearchAuditLogsData | Unset = UNSET, **kwargs: Any) -> SearchAuditLogsResponse200:
        """Search audit logs

 Search for audit logs based on given criteria.

Args:
    body (SearchAuditLogsData | Unset): Audit log search request.

Raises:
    errors.SearchAuditLogsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchAuditLogsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchAuditLogsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchAuditLogsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchAuditLogsResponse200"""
        from .api.audit_log.search_audit_logs import asyncio as search_audit_logs_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_audit_logs_asyncio(**_kwargs)


    async def cancel_batch_operation(self, batch_operation_key: str, *, data: Any | Unset = UNSET, **kwargs: Any) -> None:
        """Cancel Batch operation

 Cancels a running batch operation.
This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/{batchOperationKey}).

Args:
    batch_operation_key (str): System-generated key for an batch operation. Example:
        2251799813684321.
    body (Any | Unset):

Raises:
    errors.CancelBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CancelBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CancelBatchOperationNotFound: If the response status code is 404. Not found. The batch operation was not found.
    errors.CancelBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.batch_operation.cancel_batch_operation import asyncio as cancel_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await cancel_batch_operation_asyncio(**_kwargs)


    async def suspend_batch_operation(self, batch_operation_key: str, *, data: Any | Unset = UNSET, **kwargs: Any) -> None:
        """Suspend Batch operation

 Suspends a running batch operation.
This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/{batchOperationKey}).

Args:
    batch_operation_key (str): System-generated key for an batch operation. Example:
        2251799813684321.
    body (Any | Unset):

Raises:
    errors.SuspendBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SuspendBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SuspendBatchOperationNotFound: If the response status code is 404. Not found. The batch operation was not found.
    errors.SuspendBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.SuspendBatchOperationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.batch_operation.suspend_batch_operation import asyncio as suspend_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await suspend_batch_operation_asyncio(**_kwargs)


    async def search_batch_operations(self, *, data: SearchBatchOperationsData | Unset = UNSET, **kwargs: Any) -> SearchBatchOperationsResponse200:
        """Search batch operations

 Search for batch operations based on given criteria.

Args:
    body (SearchBatchOperationsData | Unset): Batch operation search request.

Raises:
    errors.SearchBatchOperationsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchBatchOperationsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchBatchOperationsResponse200"""
        from .api.batch_operation.search_batch_operations import asyncio as search_batch_operations_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_batch_operations_asyncio(**_kwargs)


    async def resume_batch_operation(self, batch_operation_key: str, *, data: Any | Unset = UNSET, **kwargs: Any) -> None:
        """Resume Batch operation

 Resumes a suspended batch operation.
This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/{batchOperationKey}).

Args:
    batch_operation_key (str): System-generated key for an batch operation. Example:
        2251799813684321.
    body (Any | Unset):

Raises:
    errors.ResumeBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ResumeBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.ResumeBatchOperationNotFound: If the response status code is 404. Not found. The batch operation was not found.
    errors.ResumeBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResumeBatchOperationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.batch_operation.resume_batch_operation import asyncio as resume_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await resume_batch_operation_asyncio(**_kwargs)


    async def get_batch_operation(self, batch_operation_key: str, **kwargs: Any) -> GetBatchOperationResponse200:
        """Get batch operation

 Get batch operation by key.

Args:
    batch_operation_key (str): System-generated key for an batch operation. Example:
        2251799813684321.

Raises:
    errors.GetBatchOperationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetBatchOperationNotFound: If the response status code is 404. The batch operation is not found.
    errors.GetBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetBatchOperationResponse200"""
        from .api.batch_operation.get_batch_operation import asyncio as get_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_batch_operation_asyncio(**_kwargs)


    async def search_batch_operation_items(self, *, data: SearchBatchOperationItemsData | Unset = UNSET, **kwargs: Any) -> SearchBatchOperationItemsResponse200:
        """Search batch operation items

 Search for batch operation items based on given criteria.

Args:
    body (SearchBatchOperationItemsData | Unset): Batch operation item search request.

Raises:
    errors.SearchBatchOperationItemsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchBatchOperationItemsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchBatchOperationItemsResponse200"""
        from .api.batch_operation.search_batch_operation_items import asyncio as search_batch_operation_items_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_batch_operation_items_asyncio(**_kwargs)


    async def get_start_process_form(self, process_definition_key: str, **kwargs: Any) -> GetStartProcessFormResponse200:
        """Get process start form

 Get the start form of a process.
Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

Args:
    process_definition_key (str): System-generated key for a deployed process definition.
        Example: 2251799813686749.

Raises:
    errors.GetStartProcessFormBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetStartProcessFormUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetStartProcessFormForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetStartProcessFormNotFound: If the response status code is 404. Not found
    errors.GetStartProcessFormInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetStartProcessFormResponse200"""
        from .api.process_definition.get_start_process_form import asyncio as get_start_process_form_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_start_process_form_asyncio(**_kwargs)


    async def search_process_definitions(self, *, data: SearchProcessDefinitionsData | Unset = UNSET, **kwargs: Any) -> SearchProcessDefinitionsResponse200:
        """Search process definitions

 Search for process definitions based on given criteria.

Args:
    body (SearchProcessDefinitionsData | Unset):

Raises:
    errors.SearchProcessDefinitionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchProcessDefinitionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchProcessDefinitionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchProcessDefinitionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchProcessDefinitionsResponse200"""
        from .api.process_definition.search_process_definitions import asyncio as search_process_definitions_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_process_definitions_asyncio(**_kwargs)


    async def get_process_definition_statistics(self, process_definition_key: str, *, data: GetProcessDefinitionStatisticsData | Unset = UNSET, **kwargs: Any) -> GetProcessDefinitionStatisticsResponse200:
        """Get process definition statistics

 Get statistics about elements in currently running process instances by process definition key and
search filter.

Args:
    process_definition_key (str): System-generated key for a deployed process definition.
        Example: 2251799813686749.
    body (GetProcessDefinitionStatisticsData | Unset): Process definition element statistics
        request.

Raises:
    errors.GetProcessDefinitionStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionStatisticsResponse200"""
        from .api.process_definition.get_process_definition_statistics import asyncio as get_process_definition_statistics_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_definition_statistics_asyncio(**_kwargs)


    async def get_process_definition_message_subscription_statistics(self, *, data: GetProcessDefinitionMessageSubscriptionStatisticsData | Unset = UNSET, **kwargs: Any) -> GetProcessDefinitionMessageSubscriptionStatisticsResponse200:
        """Get message subscription statistics

 Get message subscription statistics, grouped by process definition.

Args:
    body (GetProcessDefinitionMessageSubscriptionStatisticsData | Unset):

Raises:
    errors.GetProcessDefinitionMessageSubscriptionStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionMessageSubscriptionStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionMessageSubscriptionStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionMessageSubscriptionStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionMessageSubscriptionStatisticsResponse200"""
        from .api.process_definition.get_process_definition_message_subscription_statistics import asyncio as get_process_definition_message_subscription_statistics_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_definition_message_subscription_statistics_asyncio(**_kwargs)


    async def get_process_definition_instance_statistics(self, *, data: GetProcessDefinitionInstanceStatisticsData | Unset = UNSET, **kwargs: Any) -> GetProcessDefinitionInstanceStatisticsResponse200:
        """Get process instance statistics

 Get statistics about process instances, grouped by process definition and tenant.

Args:
    body (GetProcessDefinitionInstanceStatisticsData | Unset):

Raises:
    errors.GetProcessDefinitionInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionInstanceStatisticsResponse200"""
        from .api.process_definition.get_process_definition_instance_statistics import asyncio as get_process_definition_instance_statistics_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_definition_instance_statistics_asyncio(**_kwargs)


    async def get_process_definition(self, process_definition_key: str, **kwargs: Any) -> GetProcessDefinitionResponse200:
        """Get process definition

 Returns process definition as JSON.

Args:
    process_definition_key (str): System-generated key for a deployed process definition.
        Example: 2251799813686749.

Raises:
    errors.GetProcessDefinitionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionNotFound: If the response status code is 404. The process definition with the given key was not found. More details are provided in the response body.
    errors.GetProcessDefinitionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionResponse200"""
        from .api.process_definition.get_process_definition import asyncio as get_process_definition_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_definition_asyncio(**_kwargs)


    async def get_process_definition_instance_version_statistics(self, process_definition_id: str, *, data: GetProcessDefinitionInstanceVersionStatisticsData | Unset = UNSET, **kwargs: Any) -> GetProcessDefinitionInstanceVersionStatisticsResponse200:
        """Get process instance statistics by version

 Get statistics about process instances, grouped by version for a given process definition.

Args:
    process_definition_id (str): Id of a process definition, from the model. Only ids of
        process definitions that are deployed are useful. Example: new-account-onboarding-
        workflow.
    body (GetProcessDefinitionInstanceVersionStatisticsData | Unset):

Raises:
    errors.GetProcessDefinitionInstanceVersionStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessDefinitionInstanceVersionStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessDefinitionInstanceVersionStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessDefinitionInstanceVersionStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessDefinitionInstanceVersionStatisticsResponse200"""
        from .api.process_definition.get_process_definition_instance_version_statistics import asyncio as get_process_definition_instance_version_statistics_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_definition_instance_version_statistics_asyncio(**_kwargs)


    async def get_process_definition_xml(self, process_definition_key: str, **kwargs: Any) -> str:
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
        from .api.process_definition.get_process_definition_xml import asyncio as get_process_definition_xml_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_definition_xml_asyncio(**_kwargs)


    async def search_roles_for_group(self, group_id: str, *, data: SearchRolesForGroupData | Unset = UNSET, **kwargs: Any) -> SearchRolesForGroupResponse200:
        """Search group roles

 Search roles assigned to a group.

Args:
    group_id (str):
    body (SearchRolesForGroupData | Unset): Role search request.

Raises:
    errors.SearchRolesForGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchRolesForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchRolesForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchRolesForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.SearchRolesForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchRolesForGroupResponse200"""
        from .api.group.search_roles_for_group import asyncio as search_roles_for_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_roles_for_group_asyncio(**_kwargs)


    async def unassign_user_from_group(self, group_id: str, username: str, **kwargs: Any) -> None:
        """Unassign a user from a group

 Unassigns a user from a group.
The user is removed as a group member, with associated authorizations, roles, and tenant assignments
no longer applied.

Args:
    group_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.UnassignUserFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignUserFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignUserFromGroupNotFound: If the response status code is 404. The group or user with the given ID was not found, or the user is not assigned to this group.
    errors.UnassignUserFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignUserFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.unassign_user_from_group import asyncio as unassign_user_from_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_user_from_group_asyncio(**_kwargs)


    async def search_users_for_group(self, group_id: str, *, data: SearchUsersForGroupData | Unset = UNSET, **kwargs: Any) -> SearchUsersForGroupResponse200:
        """Search group users

 Search users assigned to a group.

Args:
    group_id (str):
    body (SearchUsersForGroupData | Unset):

Raises:
    errors.SearchUsersForGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUsersForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchUsersForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchUsersForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.SearchUsersForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUsersForGroupResponse200"""
        from .api.group.search_users_for_group import asyncio as search_users_for_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_users_for_group_asyncio(**_kwargs)


    async def unassign_client_from_group(self, group_id: str, client_id: str, **kwargs: Any) -> None:
        """Unassign a client from a group

 Unassigns a client from a group.
The client is removed as a group member, with associated authorizations, roles, and tenant
assignments no longer applied.

Args:
    group_id (str):
    client_id (str):

Raises:
    errors.UnassignClientFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignClientFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignClientFromGroupNotFound: If the response status code is 404. The group with the given ID was not found, or the client is not assigned to this group.
    errors.UnassignClientFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignClientFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.unassign_client_from_group import asyncio as unassign_client_from_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_client_from_group_asyncio(**_kwargs)


    async def assign_user_to_group(self, group_id: str, username: str, **kwargs: Any) -> None:
        """Assign a user to a group

 Assigns a user to a group, making the user a member of the group.
Group members inherit the group authorizations, roles, and tenant assignments.

Args:
    group_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.AssignUserToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignUserToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignUserToGroupNotFound: If the response status code is 404. The group or user with the given ID or username was not found.
    errors.AssignUserToGroupConflict: If the response status code is 409. The user with the given ID is already assigned to the group.
    errors.AssignUserToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignUserToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.assign_user_to_group import asyncio as assign_user_to_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_user_to_group_asyncio(**_kwargs)


    async def search_clients_for_group(self, group_id: str, *, data: SearchClientsForGroupData | Unset = UNSET, **kwargs: Any) -> SearchClientsForGroupResponse200:
        """Search group clients

 Search clients assigned to a group.

Args:
    group_id (str):
    body (SearchClientsForGroupData | Unset):

Raises:
    errors.SearchClientsForGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchClientsForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchClientsForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchClientsForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.SearchClientsForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClientsForGroupResponse200"""
        from .api.group.search_clients_for_group import asyncio as search_clients_for_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_clients_for_group_asyncio(**_kwargs)


    async def assign_mapping_rule_to_group(self, group_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Assign a mapping rule to a group

 Assigns a mapping rule to a group.

Args:
    group_id (str):
    mapping_rule_id (str):

Raises:
    errors.AssignMappingRuleToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignMappingRuleToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignMappingRuleToGroupNotFound: If the response status code is 404. The group or mapping rule with the given ID was not found.
    errors.AssignMappingRuleToGroupConflict: If the response status code is 409. The mapping rule with the given ID is already assigned to the group.
    errors.AssignMappingRuleToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignMappingRuleToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.assign_mapping_rule_to_group import asyncio as assign_mapping_rule_to_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_mapping_rule_to_group_asyncio(**_kwargs)


    async def search_mapping_rules_for_group(self, group_id: str, *, data: SearchMappingRulesForGroupData | Unset = UNSET, **kwargs: Any) -> SearchMappingRulesForGroupResponse200:
        """Search group mapping rules

 Search mapping rules assigned to a group.

Args:
    group_id (str):
    body (SearchMappingRulesForGroupData | Unset):

Raises:
    errors.SearchMappingRulesForGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMappingRulesForGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMappingRulesForGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMappingRulesForGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.SearchMappingRulesForGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMappingRulesForGroupResponse200"""
        from .api.group.search_mapping_rules_for_group import asyncio as search_mapping_rules_for_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_mapping_rules_for_group_asyncio(**_kwargs)


    async def search_groups(self, *, data: SearchGroupsData | Unset = UNSET, **kwargs: Any) -> SearchGroupsResponse200:
        """Search groups

 Search for groups based on given criteria.

Args:
    body (SearchGroupsData | Unset): Group search request.

Raises:
    errors.SearchGroupsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchGroupsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchGroupsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchGroupsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchGroupsResponse200"""
        from .api.group.search_groups import asyncio as search_groups_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_groups_asyncio(**_kwargs)


    async def get_group(self, group_id: str, **kwargs: Any) -> GetGroupResponse200:
        """Get group

 Get a group by its ID.

Args:
    group_id (str):

Raises:
    errors.GetGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.GetGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetGroupResponse200"""
        from .api.group.get_group import asyncio as get_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_group_asyncio(**_kwargs)


    async def delete_group(self, group_id: str, **kwargs: Any) -> None:
        """Delete group

 Deletes the group with the given ID.

Args:
    group_id (str):

Raises:
    errors.DeleteGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.DeleteGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.delete_group import asyncio as delete_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_group_asyncio(**_kwargs)


    async def assign_client_to_group(self, group_id: str, client_id: str, **kwargs: Any) -> None:
        """Assign a client to a group

 Assigns a client to a group, making it a member of the group.
Members of the group inherit the group authorizations, roles, and tenant assignments.

Args:
    group_id (str):
    client_id (str):

Raises:
    errors.AssignClientToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignClientToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignClientToGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.AssignClientToGroupConflict: If the response status code is 409. The client with the given ID is already assigned to the group.
    errors.AssignClientToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignClientToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.assign_client_to_group import asyncio as assign_client_to_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_client_to_group_asyncio(**_kwargs)


    async def update_group(self, group_id: str, *, data: UpdateGroupData, **kwargs: Any) -> UpdateGroupResponse200:
        """Update group

 Update a group with the given ID.

Args:
    group_id (str):
    body (UpdateGroupData):

Raises:
    errors.UpdateGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateGroupNotFound: If the response status code is 404. The group with the given ID was not found.
    errors.UpdateGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateGroupResponse200"""
        from .api.group.update_group import asyncio as update_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_group_asyncio(**_kwargs)


    async def unassign_mapping_rule_from_group(self, group_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Unassign a mapping rule from a group

 Unassigns a mapping rule from a group.

Args:
    group_id (str):
    mapping_rule_id (str):

Raises:
    errors.UnassignMappingRuleFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignMappingRuleFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignMappingRuleFromGroupNotFound: If the response status code is 404. The group or mapping rule with the given ID was not found, or the mapping rule is not assigned to this group.
    errors.UnassignMappingRuleFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignMappingRuleFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.group.unassign_mapping_rule_from_group import asyncio as unassign_mapping_rule_from_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_mapping_rule_from_group_asyncio(**_kwargs)


    async def create_group(self, *, data: CreateGroupData | Unset = UNSET, **kwargs: Any) -> CreateGroupResponse201:
        """Create group

 Create a new group.

Args:
    body (CreateGroupData | Unset):

Raises:
    errors.CreateGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateGroupUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateGroupResponse201"""
        from .api.group.create_group import asyncio as create_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_group_asyncio(**_kwargs)


    async def get_variable(self, variable_key: str, **kwargs: Any) -> GetVariableResponse200:
        """Get variable

 Get the variable by the variable key.

Args:
    variable_key (str): System-generated key for a variable. Example: 2251799813683287.

Raises:
    errors.GetVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetVariableNotFound: If the response status code is 404. Not found
    errors.GetVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetVariableResponse200"""
        from .api.variable.get_variable import asyncio as get_variable_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_variable_asyncio(**_kwargs)


    async def search_variables(self, *, data: SearchVariablesData | Unset = UNSET, truncate_values: bool | Unset = UNSET, **kwargs: Any) -> SearchVariablesResponse200:
        """Search variables

 Search for process and local variables based on given criteria. By default, long variable values in
the response are truncated.

Args:
    truncate_values (bool | Unset):
    body (SearchVariablesData | Unset): Variable search query request.

Raises:
    errors.SearchVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchVariablesResponse200"""
        from .api.variable.search_variables import asyncio as search_variables_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_variables_asyncio(**_kwargs)


    async def create_admin_user(self, *, data: CreateAdminUserData, **kwargs: Any) -> None:
        """Create admin user

 Creates a new user and assigns the admin role to it. This endpoint is only usable when users are
managed in the Orchestration Cluster and while no user is assigned to the admin role.

Args:
    body (CreateAdminUserData):

Raises:
    errors.CreateAdminUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateAdminUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateAdminUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateAdminUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.setup.create_admin_user import asyncio as create_admin_user_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_admin_user_asyncio(**_kwargs)


    async def delete_decision_instances_batch_operation(self, *, data: DeleteDecisionInstancesBatchOperationData, **kwargs: Any) -> DeleteDecisionInstancesBatchOperationResponse200:
        """Delete decision instances (batch)

 Delete multiple decision instances. This will delete the historic data from secondary storage.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (DeleteDecisionInstancesBatchOperationData): The decision instance filter that
        defines which decision instances should be deleted.

Raises:
    errors.DeleteDecisionInstancesBatchOperationBadRequest: If the response status code is 400. The decision instance batch operation failed. More details are provided in the response body.
    errors.DeleteDecisionInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteDecisionInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteDecisionInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteDecisionInstancesBatchOperationResponse200"""
        from .api.decision_instance.delete_decision_instances_batch_operation import asyncio as delete_decision_instances_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_decision_instances_batch_operation_asyncio(**_kwargs)


    async def delete_decision_instance(self, decision_instance_key: str, *, data: DeleteDecisionInstanceDataType0 | None | Unset = UNSET, **kwargs: Any) -> DeleteDecisionInstanceResponse200:
        """Delete decision instance

 Delete all associated decision evaluations based on provided key.

Args:
    decision_instance_key (str): System-generated key for a deployed decision instance.
        Example: 22517998136843567.
    body (DeleteDecisionInstanceDataType0 | None | Unset):

Raises:
    errors.DeleteDecisionInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteDecisionInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteDecisionInstanceNotFound: If the response status code is 404. The decision instance is not found.
    errors.DeleteDecisionInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteDecisionInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteDecisionInstanceResponse200"""
        from .api.decision_instance.delete_decision_instance import asyncio as delete_decision_instance_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_decision_instance_asyncio(**_kwargs)


    async def get_decision_instance(self, decision_evaluation_instance_key: str, **kwargs: Any) -> GetDecisionInstanceResponse200:
        """Get decision instance

 Returns a decision instance.

Args:
    decision_evaluation_instance_key (str): System-generated key for a deployed decision
        instance. Example: 22517998136843567.

Raises:
    errors.GetDecisionInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionInstanceNotFound: If the response status code is 404. The decision instance with the given key was not found. More details are provided in the response body.
    errors.GetDecisionInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetDecisionInstanceResponse200"""
        from .api.decision_instance.get_decision_instance import asyncio as get_decision_instance_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_decision_instance_asyncio(**_kwargs)


    async def search_decision_instances(self, *, data: SearchDecisionInstancesData | Unset = UNSET, **kwargs: Any) -> SearchDecisionInstancesResponse200:
        """Search decision instances

 Search for decision instances based on given criteria.

Args:
    body (SearchDecisionInstancesData | Unset):

Raises:
    errors.SearchDecisionInstancesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchDecisionInstancesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchDecisionInstancesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchDecisionInstancesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchDecisionInstancesResponse200"""
        from .api.decision_instance.search_decision_instances import asyncio as search_decision_instances_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_decision_instances_asyncio(**_kwargs)


    async def activate_jobs(self, *, data: ActivateJobsData, **kwargs: Any) -> ActivateJobsResponse200:
        """Activate jobs

 Iterate through all known partitions and activate jobs up to the requested maximum.

Args:
    body (ActivateJobsData):

Raises:
    errors.ActivateJobsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ActivateJobsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ActivateJobsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ActivateJobsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ActivateJobsResponse200"""
        from .api.job.activate_jobs import asyncio as activate_jobs_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await activate_jobs_asyncio(**_kwargs)


    async def complete_job(self, job_key: str, *, data: CompleteJobData | Unset = UNSET, **kwargs: Any) -> None:
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
        from .api.job.complete_job import asyncio as complete_job_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await complete_job_asyncio(**_kwargs)


    async def fail_job(self, job_key: str, *, data: FailJobData | Unset = UNSET, **kwargs: Any) -> None:
        """Fail job

 Mark the job as failed.

Args:
    job_key (str): System-generated key for a job. Example: 2251799813653498.
    body (FailJobData | Unset):

Raises:
    errors.FailJobBadRequest: If the response status code is 400. The provided data is not valid.
    errors.FailJobNotFound: If the response status code is 404. The job with the given jobKey is not found. It was completed by another worker, or the process instance itself was canceled.
    errors.FailJobConflict: If the response status code is 409. The job with the given key is in the wrong state (i.e: not ACTIVATED or ACTIVATABLE). The job was failed by another worker with retries = 0, and the process is now in an incident state.
    errors.FailJobInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.FailJobServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.job.fail_job import asyncio as fail_job_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await fail_job_asyncio(**_kwargs)


    async def throw_job_error(self, job_key: str, *, data: ThrowJobErrorData, **kwargs: Any) -> None:
        """Throw error for job

 Reports a business error (i.e. non-technical) that occurs while processing a job.

Args:
    job_key (str): System-generated key for a job. Example: 2251799813653498.
    body (ThrowJobErrorData):

Raises:
    errors.ThrowJobErrorBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ThrowJobErrorNotFound: If the response status code is 404. The job with the given key was not found or is not activated.
    errors.ThrowJobErrorConflict: If the response status code is 409. The job with the given key is in the wrong state currently. More details are provided in the response body.
    errors.ThrowJobErrorInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ThrowJobErrorServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.job.throw_job_error import asyncio as throw_job_error_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await throw_job_error_asyncio(**_kwargs)


    async def update_job(self, job_key: str, *, data: UpdateJobData, **kwargs: Any) -> None:
        """Update job

 Update a job with the given key.

Args:
    job_key (str): System-generated key for a job. Example: 2251799813653498.
    body (UpdateJobData):

Raises:
    errors.UpdateJobBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateJobNotFound: If the response status code is 404. The job with the jobKey is not found.
    errors.UpdateJobConflict: If the response status code is 409. The job with the given key is in the wrong state currently. More details are provided in the response body.
    errors.UpdateJobInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateJobServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.job.update_job import asyncio as update_job_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_job_asyncio(**_kwargs)


    async def search_jobs(self, *, data: SearchJobsData | Unset = UNSET, **kwargs: Any) -> SearchJobsResponse200:
        """Search jobs

 Search for jobs based on given criteria.

Args:
    body (SearchJobsData | Unset): Job search request.

Raises:
    errors.SearchJobsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchJobsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchJobsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchJobsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchJobsResponse200"""
        from .api.job.search_jobs import asyncio as search_jobs_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_jobs_asyncio(**_kwargs)


    async def get_global_job_statistics(self, *, from_: datetime.datetime, to: datetime.datetime, job_type: str | Unset = UNSET, **kwargs: Any) -> GetGlobalJobStatisticsResponse200:
        """Global job statistics

 Returns global aggregated counts for jobs. Optionally filter by the creation time window and/or
jobType.

Args:
    from_ (datetime.datetime):
    to (datetime.datetime):
    job_type (str | Unset):

Raises:
    errors.GetGlobalJobStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetGlobalJobStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetGlobalJobStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetGlobalJobStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetGlobalJobStatisticsResponse200"""
        from .api.job.get_global_job_statistics import asyncio as get_global_job_statistics_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_global_job_statistics_asyncio(**_kwargs)


    async def get_topology(self, **kwargs: Any) -> GetTopologyResponse200:
        """Get cluster topology

 Obtains the current topology of the cluster the gateway is part of.

Raises:
    errors.GetTopologyUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetTopologyInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetTopologyResponse200"""
        from .api.cluster.get_topology import asyncio as get_topology_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_topology_asyncio(**_kwargs)


    async def correlate_message(self, *, data: CorrelateMessageData, **kwargs: Any) -> CorrelateMessageResponse200:
        """Correlate message

 Publishes a message and correlates it to a subscription.
If correlation is successful it will return the first process instance key the message correlated
with.
The message is not buffered.
Use the publish message endpoint to send messages that can be buffered.

Args:
    body (CorrelateMessageData):

Raises:
    errors.CorrelateMessageBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CorrelateMessageForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CorrelateMessageNotFound: If the response status code is 404. Not found
    errors.CorrelateMessageInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CorrelateMessageServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CorrelateMessageResponse200"""
        from .api.message.correlate_message import asyncio as correlate_message_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await correlate_message_asyncio(**_kwargs)


    async def publish_message(self, *, data: PublishMessageData, **kwargs: Any) -> PublishMessageResponse200:
        """Publish message

 Publishes a single message.
Messages are published to specific partitions computed from their correlation keys.
Messages can be buffered.
The endpoint does not wait for a correlation result.
Use the message correlation endpoint for such use cases.

Args:
    body (PublishMessageData):

Raises:
    errors.PublishMessageBadRequest: If the response status code is 400. The provided data is not valid.
    errors.PublishMessageInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.PublishMessageServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    PublishMessageResponse200"""
        from .api.message.publish_message import asyncio as publish_message_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await publish_message_asyncio(**_kwargs)


    async def delete_process_instances_batch_operation(self, *, data: DeleteProcessInstancesBatchOperationData, **kwargs: Any) -> DeleteProcessInstancesBatchOperationResponse200:
        """Delete process instances (batch)

 Delete multiple process instances. This will delete the historic data from secondary storage.
Only process instances in a final state (COMPLETED or TERMINATED) can be deleted.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (DeleteProcessInstancesBatchOperationData): The process instance filter that defines
        which process instances should be deleted.

Raises:
    errors.DeleteProcessInstancesBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.DeleteProcessInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteProcessInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteProcessInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteProcessInstancesBatchOperationResponse200"""
        from .api.process_instance.delete_process_instances_batch_operation import asyncio as delete_process_instances_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_process_instances_batch_operation_asyncio(**_kwargs)


    async def migrate_process_instances_batch_operation(self, *, data: MigrateProcessInstancesBatchOperationData, **kwargs: Any) -> MigrateProcessInstancesBatchOperationResponse200:
        """Migrate process instances (batch)

 Migrate multiple process instances.
Since only process instances with ACTIVE state can be migrated, any given
filters for state are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (MigrateProcessInstancesBatchOperationData):

Raises:
    errors.MigrateProcessInstancesBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.MigrateProcessInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.MigrateProcessInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.MigrateProcessInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    MigrateProcessInstancesBatchOperationResponse200"""
        from .api.process_instance.migrate_process_instances_batch_operation import asyncio as migrate_process_instances_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await migrate_process_instances_batch_operation_asyncio(**_kwargs)


    async def modify_process_instances_batch_operation(self, *, data: ModifyProcessInstancesBatchOperationData, **kwargs: Any) -> ModifyProcessInstancesBatchOperationResponse200:
        """Modify process instances (batch)

 Modify multiple process instances.
Since only process instances with ACTIVE state can be modified, any given
filters for state are ignored and overridden during this batch operation.
In contrast to single modification operation, it is not possible to add variable instructions or
modify by element key.
It is only possible to use the element id of the source and target.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (ModifyProcessInstancesBatchOperationData): The process instance filter to define on
        which process instances tokens should be moved,
        and new element instances should be activated or terminated.

Raises:
    errors.ModifyProcessInstancesBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.ModifyProcessInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ModifyProcessInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.ModifyProcessInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ModifyProcessInstancesBatchOperationResponse200"""
        from .api.process_instance.modify_process_instances_batch_operation import asyncio as modify_process_instances_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await modify_process_instances_batch_operation_asyncio(**_kwargs)


    async def migrate_process_instance(self, process_instance_key: str, *, data: MigrateProcessInstanceData, **kwargs: Any) -> None:
        """Migrate process instance

 Migrates a process instance to a new process definition.
This request can contain multiple mapping instructions to define mapping between the active
process instance's elements and target process definition elements.

Use this to upgrade a process instance to a new version of a process or to
a different process definition, e.g. to keep your running instances up-to-date with the
latest process improvements.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (MigrateProcessInstanceData): The migration instructions describe how to migrate a
        process instance from one process definition to another.

Raises:
    errors.MigrateProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.MigrateProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
    errors.MigrateProcessInstanceConflict: If the response status code is 409. The process instance migration failed. More details are provided in the response body.
    errors.MigrateProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.MigrateProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.process_instance.migrate_process_instance import asyncio as migrate_process_instance_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await migrate_process_instance_asyncio(**_kwargs)


    async def resolve_process_instance_incidents(self, process_instance_key: str, **kwargs: Any) -> ResolveProcessInstanceIncidentsResponse200:
        """Resolve related incidents

 Creates a batch operation to resolve multiple incidents of a process instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.ResolveProcessInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ResolveProcessInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ResolveProcessInstanceIncidentsNotFound: If the response status code is 404. The process instance is not found.
    errors.ResolveProcessInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResolveProcessInstanceIncidentsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ResolveProcessInstanceIncidentsResponse200"""
        from .api.process_instance.resolve_process_instance_incidents import asyncio as resolve_process_instance_incidents_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await resolve_process_instance_incidents_asyncio(**_kwargs)


    async def resolve_incidents_batch_operation(self, *, data: ResolveIncidentsBatchOperationData | Unset = UNSET, **kwargs: Any) -> ResolveIncidentsBatchOperationResponse200:
        """Resolve related incidents (batch)

 Resolves multiple instances of process instances.
Since only process instances with ACTIVE state can have unresolved incidents, any given
filters for state are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (ResolveIncidentsBatchOperationData | Unset): The process instance filter that
        defines which process instances should have their incidents resolved.

Raises:
    errors.ResolveIncidentsBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.ResolveIncidentsBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ResolveIncidentsBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.ResolveIncidentsBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    ResolveIncidentsBatchOperationResponse200"""
        from .api.process_instance.resolve_incidents_batch_operation import asyncio as resolve_incidents_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await resolve_incidents_batch_operation_asyncio(**_kwargs)


    async def create_process_instance(self, *, data: Processcreationbyid | Processcreationbykey, **kwargs: Any) -> CreateProcessInstanceResponse200:
        """Create process instance

 Creates and starts an instance of the specified process.
The process definition to use to create the instance can be specified either using its unique key
(as returned by Deploy resources), or using the BPMN process id and a version.

Waits for the completion of the process instance before returning a result
when awaitCompletion is enabled.

Args:
    body (Processcreationbyid | Processcreationbykey): Instructions for creating a process
        instance. The process definition can be specified
        either by id or by key.

Raises:
    errors.CreateProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.CreateProcessInstanceGatewayTimeout: If the response status code is 504. The process instance creation request timed out in the gateway. This can happen if the `awaitCompletion` request parameter is set to `true` and the created process instance did not complete within the defined request timeout. This often happens when the created instance is not fully automated or contains wait states.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateProcessInstanceResponse200"""
        from .api.process_instance.create_process_instance import asyncio as create_process_instance_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_process_instance_asyncio(**_kwargs)


    async def cancel_process_instance(self, process_instance_key: str, *, data: CancelProcessInstanceDataType0 | None | Unset = UNSET, **kwargs: Any) -> None:
        """Cancel process instance

 Cancels a running process instance. As a cancellation includes more than just the removal of the
process instance resource, the cancellation resource must be posted.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (CancelProcessInstanceDataType0 | None | Unset):

Raises:
    errors.CancelProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CancelProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
    errors.CancelProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CancelProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.process_instance.cancel_process_instance import asyncio as cancel_process_instance_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await cancel_process_instance_asyncio(**_kwargs)


    async def get_process_instance_sequence_flows(self, process_instance_key: str, **kwargs: Any) -> GetProcessInstanceSequenceFlowsResponse200:
        """Get sequence flows

 Get sequence flows taken by the process instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceSequenceFlowsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceSequenceFlowsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceSequenceFlowsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceSequenceFlowsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceSequenceFlowsResponse200"""
        from .api.process_instance.get_process_instance_sequence_flows import asyncio as get_process_instance_sequence_flows_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_instance_sequence_flows_asyncio(**_kwargs)


    async def delete_process_instance(self, process_instance_key: str, *, data: DeleteProcessInstanceDataType0 | None | Unset = UNSET, **kwargs: Any) -> DeleteProcessInstanceResponse200:
        """Delete process instance

 Deletes a process instance. Only instances that are completed or terminated can be deleted.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (DeleteProcessInstanceDataType0 | None | Unset):

Raises:
    errors.DeleteProcessInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteProcessInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
    errors.DeleteProcessInstanceConflict: If the response status code is 409. The process instance is not in a completed or terminated state and cannot be deleted.
    errors.DeleteProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteProcessInstanceResponse200"""
        from .api.process_instance.delete_process_instance import asyncio as delete_process_instance_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_process_instance_asyncio(**_kwargs)


    async def search_process_instance_incidents(self, process_instance_key: str, *, data: SearchProcessInstanceIncidentsData | Unset = UNSET, **kwargs: Any) -> SearchProcessInstanceIncidentsResponse200:
        """Search related incidents

 Search for incidents caused by the process instance or any of its called process or decision
instances.

Although the `processInstanceKey` is provided as a path parameter to indicate the root process
instance,
you may also include a `processInstanceKey` within the filter object to narrow results to specific
child process instances. This is useful, for example, if you want to isolate incidents associated
with
subprocesses or called processes under the root instance while excluding incidents directly tied to
the root.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (SearchProcessInstanceIncidentsData | Unset):

Raises:
    errors.SearchProcessInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchProcessInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchProcessInstanceIncidentsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchProcessInstanceIncidentsNotFound: If the response status code is 404. The process instance with the given key was not found.
    errors.SearchProcessInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchProcessInstanceIncidentsResponse200"""
        from .api.process_instance.search_process_instance_incidents import asyncio as search_process_instance_incidents_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_process_instance_incidents_asyncio(**_kwargs)


    async def get_process_instance_statistics(self, process_instance_key: str, **kwargs: Any) -> GetProcessInstanceStatisticsResponse200:
        """Get element instance statistics

 Get statistics about elements by the process instance key.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceStatisticsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsResponse200"""
        from .api.process_instance.get_process_instance_statistics import asyncio as get_process_instance_statistics_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_instance_statistics_asyncio(**_kwargs)


    async def search_process_instances(self, *, data: SearchProcessInstancesData | Unset = UNSET, **kwargs: Any) -> SearchProcessInstancesResponse200:
        """Search process instances

 Search for process instances based on given criteria.

Args:
    body (SearchProcessInstancesData | Unset): Process instance search request.

Raises:
    errors.SearchProcessInstancesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchProcessInstancesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchProcessInstancesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchProcessInstancesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchProcessInstancesResponse200"""
        from .api.process_instance.search_process_instances import asyncio as search_process_instances_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_process_instances_asyncio(**_kwargs)


    async def cancel_process_instances_batch_operation(self, *, data: CancelProcessInstancesBatchOperationData, **kwargs: Any) -> CancelProcessInstancesBatchOperationResponse200:
        """Cancel process instances (batch)

 Cancels multiple running process instances.
Since only ACTIVE root instances can be cancelled, any given filters for state and
parentProcessInstanceKey are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/{batchOperationKey}).

Args:
    body (CancelProcessInstancesBatchOperationData): The process instance filter that defines
        which process instances should be canceled.

Raises:
    errors.CancelProcessInstancesBatchOperationBadRequest: If the response status code is 400. The process instance batch operation failed. More details are provided in the response body.
    errors.CancelProcessInstancesBatchOperationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CancelProcessInstancesBatchOperationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CancelProcessInstancesBatchOperationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CancelProcessInstancesBatchOperationResponse200"""
        from .api.process_instance.cancel_process_instances_batch_operation import asyncio as cancel_process_instances_batch_operation_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await cancel_process_instances_batch_operation_asyncio(**_kwargs)


    async def get_process_instance(self, process_instance_key: str, **kwargs: Any) -> GetProcessInstanceResponse200:
        """Get process instance

 Get the process instance by the process instance key.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceNotFound: If the response status code is 404. The process instance with the given key was not found.
    errors.GetProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceResponse200"""
        from .api.process_instance.get_process_instance import asyncio as get_process_instance_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_instance_asyncio(**_kwargs)


    async def get_process_instance_call_hierarchy(self, process_instance_key: str, **kwargs: Any) -> list[Any]:
        """Get call hierarchy

 Returns the call hierarchy for a given process instance, showing its ancestry up to the root
instance.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.

Raises:
    errors.GetProcessInstanceCallHierarchyBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceCallHierarchyUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceCallHierarchyForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceCallHierarchyNotFound: If the response status code is 404. The process instance is not found.
    errors.GetProcessInstanceCallHierarchyInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    list[Any]"""
        from .api.process_instance.get_process_instance_call_hierarchy import asyncio as get_process_instance_call_hierarchy_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_instance_call_hierarchy_asyncio(**_kwargs)


    async def modify_process_instance(self, process_instance_key: str, *, data: ModifyProcessInstanceData, **kwargs: Any) -> None:
        """Modify process instance

 Modifies a running process instance.
This request can contain multiple instructions to activate an element of the process or
to terminate an active instance of an element.

Use this to repair a process instance that is stuck on an element or took an unintended path.
For example, because an external system is not available or doesn't respond as expected.

Args:
    process_instance_key (str): System-generated key for a process instance. Example:
        2251799813690746.
    body (ModifyProcessInstanceData):

Raises:
    errors.ModifyProcessInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ModifyProcessInstanceNotFound: If the response status code is 404. The process instance is not found.
    errors.ModifyProcessInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ModifyProcessInstanceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.process_instance.modify_process_instance import asyncio as modify_process_instance_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await modify_process_instance_asyncio(**_kwargs)


    async def get_authentication(self, **kwargs: Any) -> GetAuthenticationResponse200:
        """Get current user

 Retrieves the current authenticated user.

Raises:
    errors.GetAuthenticationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetAuthenticationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetAuthenticationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetAuthenticationResponse200"""
        from .api.authentication.get_authentication import asyncio as get_authentication_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_authentication_asyncio(**_kwargs)


    async def assign_group_to_tenant(self, tenant_id: str, group_id: str, **kwargs: Any) -> None:
        """Assign a group to a tenant

 Assigns a group to a specified tenant.
Group members (users, clients) can then access tenant data and perform authorized actions.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    group_id (str):

Raises:
    errors.AssignGroupToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignGroupToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignGroupToTenantNotFound: If the response status code is 404. Not found. The tenant or group was not found.
    errors.AssignGroupToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignGroupToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_group_to_tenant import asyncio as assign_group_to_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_group_to_tenant_asyncio(**_kwargs)


    async def search_group_ids_for_tenant(self, tenant_id: str, *, data: SearchGroupIdsForTenantData | Unset = UNSET, **kwargs: Any) -> SearchGroupIdsForTenantResponse200:
        """Search groups for tenant

 Retrieves a filtered and sorted list of groups for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchGroupIdsForTenantData | Unset):

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchGroupIdsForTenantResponse200"""
        from .api.tenant.search_group_ids_for_tenant import asyncio as search_group_ids_for_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_group_ids_for_tenant_asyncio(**_kwargs)


    async def unassign_client_from_tenant(self, tenant_id: str, client_id: str, **kwargs: Any) -> None:
        """Unassign a client from a tenant

 Unassigns the client from the specified tenant.
The client can no longer access tenant data.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    client_id (str):

Raises:
    errors.UnassignClientFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignClientFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignClientFromTenantNotFound: If the response status code is 404. The tenant does not exist or the client was not assigned to it.
    errors.UnassignClientFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignClientFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_client_from_tenant import asyncio as unassign_client_from_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_client_from_tenant_asyncio(**_kwargs)


    async def get_tenant(self, tenant_id: str, **kwargs: Any) -> GetTenantResponse200:
        """Get tenant

 Retrieves a single tenant by tenant ID.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.

Raises:
    errors.GetTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetTenantUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetTenantNotFound: If the response status code is 404. Tenant not found.
    errors.GetTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetTenantResponse200"""
        from .api.tenant.get_tenant import asyncio as get_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_tenant_asyncio(**_kwargs)


    async def assign_mapping_rule_to_tenant(self, tenant_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Assign a mapping rule to a tenant

 Assign a single mapping rule to a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    mapping_rule_id (str):

Raises:
    errors.AssignMappingRuleToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignMappingRuleToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignMappingRuleToTenantNotFound: If the response status code is 404. Not found. The tenant or mapping rule was not found.
    errors.AssignMappingRuleToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignMappingRuleToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_mapping_rule_to_tenant import asyncio as assign_mapping_rule_to_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_mapping_rule_to_tenant_asyncio(**_kwargs)


    async def search_tenants(self, *, data: SearchTenantsData | Unset = UNSET, **kwargs: Any) -> SearchTenantsResponse200:
        """Search tenants

 Retrieves a filtered and sorted list of tenants.

Args:
    body (SearchTenantsData | Unset): Tenant search request

Raises:
    errors.SearchTenantsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchTenantsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchTenantsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchTenantsNotFound: If the response status code is 404. Not found
    errors.SearchTenantsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchTenantsResponse200"""
        from .api.tenant.search_tenants import asyncio as search_tenants_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_tenants_asyncio(**_kwargs)


    async def delete_tenant(self, tenant_id: str, **kwargs: Any) -> None:
        """Delete tenant

 Deletes an existing tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.

Raises:
    errors.DeleteTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteTenantNotFound: If the response status code is 404. Not found. The tenant was not found.
    errors.DeleteTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.delete_tenant import asyncio as delete_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_tenant_asyncio(**_kwargs)


    async def assign_client_to_tenant(self, tenant_id: str, client_id: str, **kwargs: Any) -> None:
        """Assign a client to a tenant

 Assign the client to the specified tenant.
The client can then access tenant data and perform authorized actions.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    client_id (str):

Raises:
    errors.AssignClientToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignClientToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignClientToTenantNotFound: If the response status code is 404. The tenant was not found.
    errors.AssignClientToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignClientToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_client_to_tenant import asyncio as assign_client_to_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_client_to_tenant_asyncio(**_kwargs)


    async def search_roles_for_tenant(self, tenant_id: str, *, data: SearchRolesForTenantData | Unset = UNSET, **kwargs: Any) -> SearchRolesForTenantResponse200:
        """Search roles for tenant

 Retrieves a filtered and sorted list of roles for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchRolesForTenantData | Unset): Role search request.

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchRolesForTenantResponse200"""
        from .api.tenant.search_roles_for_tenant import asyncio as search_roles_for_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_roles_for_tenant_asyncio(**_kwargs)


    async def unassign_role_from_tenant(self, tenant_id: str, role_id: str, **kwargs: Any) -> None:
        """Unassign a role from a tenant

 Unassigns a role from a specified tenant.
Users, Clients or Groups, that have the role assigned, will no longer have access to the
tenant's data - unless they are assigned directly to the tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    role_id (str):

Raises:
    errors.UnassignRoleFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromTenantNotFound: If the response status code is 404. Not found. The tenant or role was not found.
    errors.UnassignRoleFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_role_from_tenant import asyncio as unassign_role_from_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_role_from_tenant_asyncio(**_kwargs)


    async def unassign_mapping_rule_from_tenant(self, tenant_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Unassign a mapping rule from a tenant

 Unassigns a single mapping rule from a specified tenant without deleting the rule.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    mapping_rule_id (str):

Raises:
    errors.UnassignMappingRuleFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignMappingRuleFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignMappingRuleFromTenantNotFound: If the response status code is 404. Not found. The tenant or mapping rule was not found.
    errors.UnassignMappingRuleFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignMappingRuleFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_mapping_rule_from_tenant import asyncio as unassign_mapping_rule_from_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_mapping_rule_from_tenant_asyncio(**_kwargs)


    async def search_users_for_tenant(self, tenant_id: str, *, data: SearchUsersForTenantData | Unset = UNSET, **kwargs: Any) -> SearchUsersForTenantResponse200:
        """Search users for tenant

 Retrieves a filtered and sorted list of users for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchUsersForTenantData | Unset):

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUsersForTenantResponse200"""
        from .api.tenant.search_users_for_tenant import asyncio as search_users_for_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_users_for_tenant_asyncio(**_kwargs)


    async def assign_user_to_tenant(self, tenant_id: str, username: str, **kwargs: Any) -> None:
        """Assign a user to a tenant

 Assign a single user to a specified tenant. The user can then access tenant data and perform
authorized actions.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.AssignUserToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignUserToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignUserToTenantNotFound: If the response status code is 404. Not found. The tenant or user was not found.
    errors.AssignUserToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignUserToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_user_to_tenant import asyncio as assign_user_to_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_user_to_tenant_asyncio(**_kwargs)


    async def assign_role_to_tenant(self, tenant_id: str, role_id: str, **kwargs: Any) -> None:
        """Assign a role to a tenant

 Assigns a role to a specified tenant.
Users, Clients or Groups, that have the role assigned, will get access to the tenant's data and can
perform actions according to their authorizations.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    role_id (str):

Raises:
    errors.AssignRoleToTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToTenantNotFound: If the response status code is 404. Not found. The tenant or role was not found.
    errors.AssignRoleToTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.assign_role_to_tenant import asyncio as assign_role_to_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_role_to_tenant_asyncio(**_kwargs)


    async def create_tenant(self, *, data: CreateTenantData, **kwargs: Any) -> CreateTenantResponse201:
        """Create tenant

 Creates a new tenant.

Args:
    body (CreateTenantData):

Raises:
    errors.CreateTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateTenantNotFound: If the response status code is 404. Not found. The resource was not found.
    errors.CreateTenantConflict: If the response status code is 409. Tenant with this id already exists.
    errors.CreateTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateTenantResponse201"""
        from .api.tenant.create_tenant import asyncio as create_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_tenant_asyncio(**_kwargs)


    async def unassign_group_from_tenant(self, tenant_id: str, group_id: str, **kwargs: Any) -> None:
        """Unassign a group from a tenant

 Unassigns a group from a specified tenant.
Members of the group (users, clients) will no longer have access to the tenant's data - except they
are assigned directly to the tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    group_id (str):

Raises:
    errors.UnassignGroupFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignGroupFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignGroupFromTenantNotFound: If the response status code is 404. Not found. The tenant or group was not found.
    errors.UnassignGroupFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignGroupFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_group_from_tenant import asyncio as unassign_group_from_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_group_from_tenant_asyncio(**_kwargs)


    async def search_clients_for_tenant(self, tenant_id: str, *, data: SearchClientsForTenantData | Unset = UNSET, **kwargs: Any) -> SearchClientsForTenantResponse200:
        """Search clients for tenant

 Retrieves a filtered and sorted list of clients for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchClientsForTenantData | Unset):

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClientsForTenantResponse200"""
        from .api.tenant.search_clients_for_tenant import asyncio as search_clients_for_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_clients_for_tenant_asyncio(**_kwargs)


    async def unassign_user_from_tenant(self, tenant_id: str, username: str, **kwargs: Any) -> None:
        """Unassign a user from a tenant

 Unassigns the user from the specified tenant.
The user can no longer access tenant data.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.UnassignUserFromTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignUserFromTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignUserFromTenantNotFound: If the response status code is 404. Not found. The tenant or user was not found.
    errors.UnassignUserFromTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignUserFromTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.tenant.unassign_user_from_tenant import asyncio as unassign_user_from_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_user_from_tenant_asyncio(**_kwargs)


    async def update_tenant(self, tenant_id: str, *, data: UpdateTenantData, **kwargs: Any) -> UpdateTenantResponse200:
        """Update tenant

 Updates an existing tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (UpdateTenantData):

Raises:
    errors.UpdateTenantBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateTenantForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateTenantNotFound: If the response status code is 404. Not found. The tenant was not found.
    errors.UpdateTenantInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateTenantServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateTenantResponse200"""
        from .api.tenant.update_tenant import asyncio as update_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_tenant_asyncio(**_kwargs)


    async def search_mapping_rules_for_tenant(self, tenant_id: str, *, data: SearchMappingRulesForTenantData | Unset = UNSET, **kwargs: Any) -> SearchMappingRulesForTenantResponse200:
        """Search mapping rules for tenant

 Retrieves a filtered and sorted list of MappingRules for a specified tenant.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (SearchMappingRulesForTenantData | Unset):

Raises:
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMappingRulesForTenantResponse200"""
        from .api.tenant.search_mapping_rules_for_tenant import asyncio as search_mapping_rules_for_tenant_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_mapping_rules_for_tenant_asyncio(**_kwargs)


    async def update_global_cluster_variable(self, name: str, *, data: UpdateGlobalClusterVariableData, **kwargs: Any) -> UpdateGlobalClusterVariableResponse200:
        """Update a global-scoped cluster variable

 Updates the value of an existing global cluster variable.
The variable must exist, otherwise a 404 error is returned.

Args:
    name (str):
    body (UpdateGlobalClusterVariableData):

Raises:
    errors.UpdateGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.UpdateGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateGlobalClusterVariableResponse200"""
        from .api.cluster_variable.update_global_cluster_variable import asyncio as update_global_cluster_variable_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_global_cluster_variable_asyncio(**_kwargs)


    async def get_global_cluster_variable(self, name: str, **kwargs: Any) -> GetGlobalClusterVariableResponse200:
        """Get a global-scoped cluster variable

Args:
    name (str):

Raises:
    errors.GetGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.GetGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetGlobalClusterVariableResponse200"""
        from .api.cluster_variable.get_global_cluster_variable import asyncio as get_global_cluster_variable_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_global_cluster_variable_asyncio(**_kwargs)


    async def update_tenant_cluster_variable(self, tenant_id: str, name: str, *, data: UpdateTenantClusterVariableData, **kwargs: Any) -> UpdateTenantClusterVariableResponse200:
        """Update a tenant-scoped cluster variable

 Updates the value of an existing tenant-scoped cluster variable.
The variable must exist, otherwise a 404 error is returned.

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    name (str):
    body (UpdateTenantClusterVariableData):

Raises:
    errors.UpdateTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.UpdateTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateTenantClusterVariableResponse200"""
        from .api.cluster_variable.update_tenant_cluster_variable import asyncio as update_tenant_cluster_variable_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_tenant_cluster_variable_asyncio(**_kwargs)


    async def delete_global_cluster_variable(self, name: str, **kwargs: Any) -> None:
        """Delete a global-scoped cluster variable

Args:
    name (str):

Raises:
    errors.DeleteGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteGlobalClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.DeleteGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.cluster_variable.delete_global_cluster_variable import asyncio as delete_global_cluster_variable_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_global_cluster_variable_asyncio(**_kwargs)


    async def get_tenant_cluster_variable(self, tenant_id: str, name: str, **kwargs: Any) -> GetTenantClusterVariableResponse200:
        """Get a tenant-scoped cluster variable

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    name (str):

Raises:
    errors.GetTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.GetTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetTenantClusterVariableResponse200"""
        from .api.cluster_variable.get_tenant_cluster_variable import asyncio as get_tenant_cluster_variable_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_tenant_cluster_variable_asyncio(**_kwargs)


    async def create_tenant_cluster_variable(self, tenant_id: str, *, data: CreateTenantClusterVariableData, **kwargs: Any) -> CreateTenantClusterVariableResponse200:
        """Create a tenant-scoped cluster variable

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    body (CreateTenantClusterVariableData):

Raises:
    errors.CreateTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateTenantClusterVariableResponse200"""
        from .api.cluster_variable.create_tenant_cluster_variable import asyncio as create_tenant_cluster_variable_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_tenant_cluster_variable_asyncio(**_kwargs)


    async def delete_tenant_cluster_variable(self, tenant_id: str, name: str, **kwargs: Any) -> None:
        """Delete a tenant-scoped cluster variable

Args:
    tenant_id (str): The unique identifier of the tenant. Example: customer-service.
    name (str):

Raises:
    errors.DeleteTenantClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteTenantClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteTenantClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.DeleteTenantClusterVariableNotFound: If the response status code is 404. Cluster variable not found
    errors.DeleteTenantClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.cluster_variable.delete_tenant_cluster_variable import asyncio as delete_tenant_cluster_variable_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_tenant_cluster_variable_asyncio(**_kwargs)


    async def search_cluster_variables(self, *, data: SearchClusterVariablesData | Unset = UNSET, truncate_values: bool | Unset = UNSET, **kwargs: Any) -> SearchClusterVariablesResponse200:
        """Search for cluster variables based on given criteria. By default, long variable values in the
response are truncated.

Args:
    truncate_values (bool | Unset):
    body (SearchClusterVariablesData | Unset): Cluster variable search query request.

Raises:
    errors.SearchClusterVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchClusterVariablesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchClusterVariablesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchClusterVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClusterVariablesResponse200"""
        from .api.cluster_variable.search_cluster_variables import asyncio as search_cluster_variables_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_cluster_variables_asyncio(**_kwargs)


    async def create_global_cluster_variable(self, *, data: CreateGlobalClusterVariableData, **kwargs: Any) -> CreateGlobalClusterVariableResponse200:
        """Create a global-scoped cluster variable

Args:
    body (CreateGlobalClusterVariableData):

Raises:
    errors.CreateGlobalClusterVariableBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateGlobalClusterVariableUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateGlobalClusterVariableForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateGlobalClusterVariableInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateGlobalClusterVariableResponse200"""
        from .api.cluster_variable.create_global_cluster_variable import asyncio as create_global_cluster_variable_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_global_cluster_variable_asyncio(**_kwargs)


    async def get_document(self, document_id: str, *, store_id: str | Unset = UNSET, content_hash: str | Unset = UNSET, **kwargs: Any) -> File:
        """Download document

 Download a document from the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

Args:
    document_id (str): Document Id that uniquely identifies a document.
    store_id (str | Unset):
    content_hash (str | Unset):

Raises:
    errors.GetDocumentNotFound: If the response status code is 404. The document with the given ID was not found.
    errors.GetDocumentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    File"""
        from .api.document.get_document import asyncio as get_document_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_document_asyncio(**_kwargs)


    async def create_documents(self, *, data: CreateDocumentsData, store_id: str | Unset = UNSET, **kwargs: Any) -> CreateDocumentsResponse201:
        """Upload multiple documents

 Upload multiple documents to the Camunda 8 cluster.

The caller must provide a file name for each document, which will be used in case of a multi-status
response
to identify which documents failed to upload. The file name can be provided in the `Content-
Disposition` header
of the file part or in the `fileName` field of the metadata. You can add a parallel array of
metadata objects. These
are matched with the files based on index, and must have the same length as the files array.
To pass homogenous metadata for all files, spread the metadata over the metadata array.
A filename value provided explicitly via the metadata array in the request overrides the `Content-
Disposition` header
of the file part.

In case of a multi-status response, the response body will contain a list of
`DocumentBatchProblemDetail` objects,
each of which contains the file name of the document that failed to upload and the reason for the
failure.
The client can choose to retry the whole batch or individual documents based on the response.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

Args:
    store_id (str | Unset):
    body (CreateDocumentsData):

Raises:
    errors.CreateDocumentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateDocumentsUnsupportedMediaType: If the response status code is 415. The server cannot process the request because the media type (Content-Type) of the request payload is not supported by the server for the requested resource and method.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateDocumentsResponse201"""
        from .api.document.create_documents import asyncio as create_documents_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_documents_asyncio(**_kwargs)


    async def create_document_link(self, document_id: str, *, data: CreateDocumentLinkData | Unset = UNSET, store_id: str | Unset = UNSET, content_hash: str | Unset = UNSET, **kwargs: Any) -> CreateDocumentLinkResponse201:
        """Create document link

 Create a link to a document in the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP

Args:
    document_id (str): Document Id that uniquely identifies a document.
    store_id (str | Unset):
    content_hash (str | Unset):
    body (CreateDocumentLinkData | Unset):

Raises:
    errors.CreateDocumentLinkBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateDocumentLinkResponse201"""
        from .api.document.create_document_link import asyncio as create_document_link_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_document_link_asyncio(**_kwargs)


    async def create_document(self, *, data: CreateDocumentData, store_id: str | Unset = UNSET, document_id: str | Unset = UNSET, **kwargs: Any) -> CreateDocumentResponse201:
        """Upload document

 Upload a document to the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

Args:
    store_id (str | Unset):
    document_id (str | Unset): Document Id that uniquely identifies a document.
    body (CreateDocumentData):

Raises:
    errors.CreateDocumentBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateDocumentUnsupportedMediaType: If the response status code is 415. The server cannot process the request because the media type (Content-Type) of the request payload is not supported by the server for the requested resource and method.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateDocumentResponse201"""
        from .api.document.create_document import asyncio as create_document_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_document_asyncio(**_kwargs)


    async def delete_document(self, document_id: str, *, store_id: str | Unset = UNSET, **kwargs: Any) -> None:
        """Delete document

 Delete a document from the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

Args:
    document_id (str): Document Id that uniquely identifies a document.
    store_id (str | Unset):

Raises:
    errors.DeleteDocumentNotFound: If the response status code is 404. The document with the given ID was not found.
    errors.DeleteDocumentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.document.delete_document import asyncio as delete_document_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_document_asyncio(**_kwargs)


    async def delete_resource(self, resource_key: str, *, data: DeleteResourceDataType0 | None | Unset = UNSET, **kwargs: Any) -> DeleteResourceResponse200:
        """Delete resource

 Deletes a deployed resource. This can be a process definition, decision requirements
definition, or form definition deployed using the deploy resources endpoint. Specify the
resource you want to delete in the `resourceKey` parameter.

Once a resource has been deleted it cannot be recovered. If the resource needs to be
available again, a new deployment of the resource is required.

By default, only the resource itself is deleted from the runtime state. To also delete the
historic data associated with a resource, set the `deleteHistory` flag in the request body
to `true`. The historic data is deleted asynchronously via a batch operation. The details of
the created batch operation are included in the response. Note that history deletion is only
supported for process resources; for other resource types this flag is ignored and no history
will be deleted.

Args:
    resource_key (str): The system-assigned key for this resource.
    body (DeleteResourceDataType0 | None | Unset):

Raises:
    errors.DeleteResourceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteResourceNotFound: If the response status code is 404. The resource is not found.
    errors.DeleteResourceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteResourceServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    DeleteResourceResponse200"""
        from .api.resource.delete_resource import asyncio as delete_resource_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_resource_asyncio(**_kwargs)


    async def create_deployment(self, *, data: CreateDeploymentData, **kwargs: Any) -> CreateDeploymentResponse200:
        """Deploy resources

 Deploys one or more resources (e.g. processes, decision models, or forms).
This is an atomic call, i.e. either all resources are deployed or none of them are.

Args:
    body (CreateDeploymentData):

Raises:
    errors.CreateDeploymentBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateDeploymentServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateDeploymentResponse200"""
        from .api.resource.create_deployment import asyncio as create_deployment_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_deployment_asyncio(**_kwargs)


    async def get_resource(self, resource_key: str, **kwargs: Any) -> GetResourceResponse200:
        """Get resource

 Returns a deployed resource.
:::info
Currently, this endpoint only supports RPA resources.
:::

Args:
    resource_key (str): The system-assigned key for this resource.

Raises:
    errors.GetResourceNotFound: If the response status code is 404. A resource with the given key was not found.
    errors.GetResourceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetResourceResponse200"""
        from .api.resource.get_resource import asyncio as get_resource_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_resource_asyncio(**_kwargs)


    async def get_resource_content(self, resource_key: str, **kwargs: Any) -> File:
        """Get resource content

 Returns the content of a deployed resource.
:::info
Currently, this endpoint only supports RPA resources.
:::

Args:
    resource_key (str): The system-assigned key for this resource.

Raises:
    errors.GetResourceContentNotFound: If the response status code is 404. A resource with the given key was not found.
    errors.GetResourceContentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    File"""
        from .api.resource.get_resource_content import asyncio as get_resource_content_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_resource_content_asyncio(**_kwargs)


    async def pin_clock(self, *, data: PinClockData, **kwargs: Any) -> None:
        """Pin internal clock (alpha)

 Set a precise, static time for the Zeebe engine's internal clock.
When the clock is pinned, it remains at the specified time and does not advance.
To change the time, the clock must be pinned again with a new timestamp.

This endpoint is an alpha feature and may be subject to change
in future releases.

Args:
    body (PinClockData):

Raises:
    errors.PinClockBadRequest: If the response status code is 400. The provided data is not valid.
    errors.PinClockInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.PinClockServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.clock.pin_clock import asyncio as pin_clock_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await pin_clock_asyncio(**_kwargs)


    async def reset_clock(self, **kwargs: Any) -> None:
        """Reset internal clock (alpha)

 Resets the Zeebe engine's internal clock to the current system time, enabling it to tick in real-
time.
This operation is useful for returning the clock to
normal behavior after it has been pinned to a specific time.

This endpoint is an alpha feature and may be subject to change
in future releases.

Raises:
    errors.ResetClockInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResetClockServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.clock.reset_clock import asyncio as reset_clock_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await reset_clock_asyncio(**_kwargs)


    async def activate_ad_hoc_sub_process_activities(self, ad_hoc_sub_process_instance_key: str, *, data: ActivateAdHocSubProcessActivitiesData, **kwargs: Any) -> None:
        """Activate activities within an ad-hoc sub-process

 Activates selected activities within an ad-hoc sub-process identified by element ID.
The provided element IDs must exist within the ad-hoc sub-process instance identified by the
provided adHocSubProcessInstanceKey.

Args:
    ad_hoc_sub_process_instance_key (str): System-generated key for a element instance.
        Example: 2251799813686789.
    body (ActivateAdHocSubProcessActivitiesData):

Raises:
    errors.ActivateAdHocSubProcessActivitiesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ActivateAdHocSubProcessActivitiesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.ActivateAdHocSubProcessActivitiesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.ActivateAdHocSubProcessActivitiesNotFound: If the response status code is 404. The ad-hoc sub-process instance is not found or the provided key does not identify an ad-hoc sub-process.
    errors.ActivateAdHocSubProcessActivitiesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ActivateAdHocSubProcessActivitiesServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.ad_hoc_sub_process.activate_ad_hoc_sub_process_activities import asyncio as activate_ad_hoc_sub_process_activities_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await activate_ad_hoc_sub_process_activities_asyncio(**_kwargs)


    async def get_decision_requirements_xml(self, decision_requirements_key: str, **kwargs: Any) -> str:
        """Get decision requirements XML

 Returns decision requirements as XML.

Args:
    decision_requirements_key (str): System-generated key for a deployed decision requirements
        definition. Example: 2251799813683346.

Raises:
    errors.GetDecisionRequirementsXmlBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionRequirementsXmlUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionRequirementsXmlForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionRequirementsXmlNotFound: If the response status code is 404. The decision requirements with the given key was not found. More details are provided in the response body.
    errors.GetDecisionRequirementsXmlInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    str"""
        from .api.decision_requirements.get_decision_requirements_xml import asyncio as get_decision_requirements_xml_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_decision_requirements_xml_asyncio(**_kwargs)


    async def search_decision_requirements(self, *, data: SearchDecisionRequirementsData | Unset = UNSET, **kwargs: Any) -> SearchDecisionRequirementsResponse200:
        """Search decision requirements

 Search for decision requirements based on given criteria.

Args:
    body (SearchDecisionRequirementsData | Unset):

Raises:
    errors.SearchDecisionRequirementsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchDecisionRequirementsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchDecisionRequirementsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchDecisionRequirementsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchDecisionRequirementsResponse200"""
        from .api.decision_requirements.search_decision_requirements import asyncio as search_decision_requirements_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_decision_requirements_asyncio(**_kwargs)


    async def get_decision_requirements(self, decision_requirements_key: str, **kwargs: Any) -> GetDecisionRequirementsResponse200:
        """Get decision requirements

 Returns Decision Requirements as JSON.

Args:
    decision_requirements_key (str): System-generated key for a deployed decision requirements
        definition. Example: 2251799813683346.

Raises:
    errors.GetDecisionRequirementsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionRequirementsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionRequirementsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionRequirementsNotFound: If the response status code is 404. The decision requirements with the given key was not found. More details are provided in the response body.
    errors.GetDecisionRequirementsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetDecisionRequirementsResponse200"""
        from .api.decision_requirements.get_decision_requirements import asyncio as get_decision_requirements_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_decision_requirements_asyncio(**_kwargs)


    async def create_mapping_rule(self, *, data: CreateMappingRuleData | Unset = UNSET, **kwargs: Any) -> CreateMappingRuleResponse201:
        """Create mapping rule

 Create a new mapping rule

Args:
    body (CreateMappingRuleData | Unset):

Raises:
    errors.CreateMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateMappingRuleForbidden: If the response status code is 403. The request to create a mapping rule was denied. More details are provided in the response body.
    errors.CreateMappingRuleNotFound: If the response status code is 404. The request to create a mapping rule was denied.
    errors.CreateMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateMappingRuleResponse201"""
        from .api.mapping_rule.create_mapping_rule import asyncio as create_mapping_rule_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_mapping_rule_asyncio(**_kwargs)


    async def search_mapping_rule(self, *, data: SearchMappingRuleData | Unset = UNSET, **kwargs: Any) -> SearchMappingRuleResponse200:
        """Search mapping rules

 Search for mapping rules based on given criteria.

Args:
    body (SearchMappingRuleData | Unset):

Raises:
    errors.SearchMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMappingRuleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMappingRuleResponse200"""
        from .api.mapping_rule.search_mapping_rule import asyncio as search_mapping_rule_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_mapping_rule_asyncio(**_kwargs)


    async def delete_mapping_rule(self, mapping_rule_id: str, **kwargs: Any) -> None:
        """Delete a mapping rule

 Deletes the mapping rule with the given ID.

Args:
    mapping_rule_id (str):

Raises:
    errors.DeleteMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteMappingRuleNotFound: If the response status code is 404. The mapping rule with the mappingRuleId was not found.
    errors.DeleteMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.mapping_rule.delete_mapping_rule import asyncio as delete_mapping_rule_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_mapping_rule_asyncio(**_kwargs)


    async def get_mapping_rule(self, mapping_rule_id: str, **kwargs: Any) -> GetMappingRuleResponse200:
        """Get a mapping rule

 Gets the mapping rule with the given ID.

Args:
    mapping_rule_id (str):

Raises:
    errors.GetMappingRuleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetMappingRuleNotFound: If the response status code is 404. The mapping rule with the mappingRuleId was not found.
    errors.GetMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetMappingRuleResponse200"""
        from .api.mapping_rule.get_mapping_rule import asyncio as get_mapping_rule_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_mapping_rule_asyncio(**_kwargs)


    async def update_mapping_rule(self, mapping_rule_id: str, *, data: UpdateMappingRuleData | Unset = UNSET, **kwargs: Any) -> UpdateMappingRuleResponse200:
        """Update mapping rule

 Update a mapping rule.

Args:
    mapping_rule_id (str):
    body (UpdateMappingRuleData | Unset):

Raises:
    errors.UpdateMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateMappingRuleForbidden: If the response status code is 403. The request to update a mapping rule was denied. More details are provided in the response body.
    errors.UpdateMappingRuleNotFound: If the response status code is 404. The request to update a mapping rule was denied.
    errors.UpdateMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateMappingRuleResponse200"""
        from .api.mapping_rule.update_mapping_rule import asyncio as update_mapping_rule_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_mapping_rule_asyncio(**_kwargs)


    async def evaluate_expression(self, *, data: EvaluateExpressionData, **kwargs: Any) -> EvaluateExpressionResponse200:
        """Evaluate an expression

 Evaluates a FEEL expression and returns the result. Supports references to tenant scoped cluster
variables when a tenant ID is provided.

Args:
    body (EvaluateExpressionData):

Raises:
    errors.EvaluateExpressionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.EvaluateExpressionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.EvaluateExpressionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.EvaluateExpressionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    EvaluateExpressionResponse200"""
        from .api.expression.evaluate_expression import asyncio as evaluate_expression_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await evaluate_expression_asyncio(**_kwargs)


    async def get_element_instance(self, element_instance_key: str, **kwargs: Any) -> GetElementInstanceResponse200:
        """Get element instance

 Returns element instance as JSON.

Args:
    element_instance_key (str): System-generated key for a element instance. Example:
        2251799813686789.

Raises:
    errors.GetElementInstanceBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetElementInstanceUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetElementInstanceForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetElementInstanceNotFound: If the response status code is 404. The element instance with the given key was not found. More details are provided in the response body.
    errors.GetElementInstanceInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetElementInstanceResponse200"""
        from .api.element_instance.get_element_instance import asyncio as get_element_instance_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_element_instance_asyncio(**_kwargs)


    async def search_element_instances(self, *, data: SearchElementInstancesData | Unset = UNSET, **kwargs: Any) -> SearchElementInstancesResponse200:
        """Search element instances

 Search for element instances based on given criteria.

Args:
    body (SearchElementInstancesData | Unset): Element instance search request.

Raises:
    errors.SearchElementInstancesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchElementInstancesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchElementInstancesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchElementInstancesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchElementInstancesResponse200"""
        from .api.element_instance.search_element_instances import asyncio as search_element_instances_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_element_instances_asyncio(**_kwargs)


    async def create_element_instance_variables(self, element_instance_key: str, *, data: CreateElementInstanceVariablesData, **kwargs: Any) -> None:
        """Update element instance variables

 Updates all the variables of a particular scope (for example, process instance, element instance)
with the given variable data.
Specify the element instance in the `elementInstanceKey` parameter.

Args:
    element_instance_key (str): System-generated key for a element instance. Example:
        2251799813686789.
    body (CreateElementInstanceVariablesData):

Raises:
    errors.CreateElementInstanceVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateElementInstanceVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateElementInstanceVariablesServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.element_instance.create_element_instance_variables import asyncio as create_element_instance_variables_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_element_instance_variables_asyncio(**_kwargs)


    async def search_element_instance_incidents(self, element_instance_key: str, *, data: SearchElementInstanceIncidentsData, **kwargs: Any) -> SearchElementInstanceIncidentsResponse200:
        """Search for incidents of a specific element instance

 Search for incidents caused by the specified element instance, including incidents of any child
instances created from this element instance.

Although the `elementInstanceKey` is provided as a path parameter to indicate the root element
instance,
you may also include an `elementInstanceKey` within the filter object to narrow results to specific
child element instances. This is useful, for example, if you want to isolate incidents associated
with
nested or subordinate elements within the given element instance while excluding incidents directly
tied
to the root element itself.

Args:
    element_instance_key (str): System-generated key for a element instance. Example:
        2251799813686789.
    body (SearchElementInstanceIncidentsData):

Raises:
    errors.SearchElementInstanceIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchElementInstanceIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchElementInstanceIncidentsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchElementInstanceIncidentsNotFound: If the response status code is 404. The element instance with the given key was not found.
    errors.SearchElementInstanceIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchElementInstanceIncidentsResponse200"""
        from .api.element_instance.search_element_instance_incidents import asyncio as search_element_instance_incidents_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_element_instance_incidents_asyncio(**_kwargs)


    async def unassign_user_task(self, user_task_key: str, **kwargs: Any) -> None:
        """Unassign user task

 Removes the assignee of a task with the given key.

Args:
    user_task_key (str): System-generated key for a user task.

Raises:
    errors.UnassignUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.UnassignUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.UnassignUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user_task.unassign_user_task import asyncio as unassign_user_task_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_user_task_asyncio(**_kwargs)


    async def search_user_task_variables(self, user_task_key: str, *, data: SearchUserTaskVariablesData | Unset = UNSET, truncate_values: bool | Unset = UNSET, **kwargs: Any) -> SearchUserTaskVariablesResponse200:
        """Search user task variables

 Search for user task variables based on given criteria. By default, long variable values in the
response are truncated.

Args:
    user_task_key (str): System-generated key for a user task.
    truncate_values (bool | Unset):
    body (SearchUserTaskVariablesData | Unset): User task search query request.

Raises:
    errors.SearchUserTaskVariablesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUserTaskVariablesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUserTaskVariablesResponse200"""
        from .api.user_task.search_user_task_variables import asyncio as search_user_task_variables_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_user_task_variables_asyncio(**_kwargs)


    async def update_user_task(self, user_task_key: str, *, data: UpdateUserTaskData | Unset = UNSET, **kwargs: Any) -> None:
        """Update user task

 Update a user task with the given key.

Args:
    user_task_key (str): System-generated key for a user task.
    body (UpdateUserTaskData | Unset):

Raises:
    errors.UpdateUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.UpdateUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.UpdateUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user_task.update_user_task import asyncio as update_user_task_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_user_task_asyncio(**_kwargs)


    async def get_user_task_form(self, user_task_key: str, **kwargs: Any) -> GetUserTaskFormResponse200:
        """Get user task form

 Get the form of a user task.
Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

Args:
    user_task_key (str): System-generated key for a user task.

Raises:
    errors.GetUserTaskFormBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetUserTaskFormUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUserTaskFormForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUserTaskFormNotFound: If the response status code is 404. Not found
    errors.GetUserTaskFormInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUserTaskFormResponse200"""
        from .api.user_task.get_user_task_form import asyncio as get_user_task_form_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_user_task_form_asyncio(**_kwargs)


    async def get_user_task(self, user_task_key: str, **kwargs: Any) -> GetUserTaskResponse200:
        """Get user task

 Get the user task by the user task key.

Args:
    user_task_key (str): System-generated key for a user task.

Raises:
    errors.GetUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetUserTaskUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUserTaskForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.GetUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUserTaskResponse200"""
        from .api.user_task.get_user_task import asyncio as get_user_task_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_user_task_asyncio(**_kwargs)


    async def complete_user_task(self, user_task_key: str, *, data: CompleteUserTaskData | Unset = UNSET, **kwargs: Any) -> None:
        """Complete user task

 Completes a user task with the given key.

Args:
    user_task_key (str): System-generated key for a user task.
    body (CompleteUserTaskData | Unset):

Raises:
    errors.CompleteUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CompleteUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.CompleteUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.CompleteUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CompleteUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user_task.complete_user_task import asyncio as complete_user_task_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await complete_user_task_asyncio(**_kwargs)


    async def search_user_task_audit_logs(self, user_task_key: str, *, data: SearchUserTaskAuditLogsData | Unset = UNSET, **kwargs: Any) -> SearchUserTaskAuditLogsResponse200:
        """Search user task audit logs

 Search for user task audit logs based on given criteria.

Args:
    user_task_key (str): System-generated key for a user task.
    body (SearchUserTaskAuditLogsData | Unset): User task search query request.

Raises:
    errors.SearchUserTaskAuditLogsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUserTaskAuditLogsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUserTaskAuditLogsResponse200"""
        from .api.user_task.search_user_task_audit_logs import asyncio as search_user_task_audit_logs_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_user_task_audit_logs_asyncio(**_kwargs)


    async def search_user_tasks(self, *, data: SearchUserTasksData | Unset = UNSET, **kwargs: Any) -> SearchUserTasksResponse200:
        """Search user tasks

 Search for user tasks based on given criteria.

Args:
    body (SearchUserTasksData | Unset): User task search query request.

Raises:
    errors.SearchUserTasksBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUserTasksUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchUserTasksForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchUserTasksInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUserTasksResponse200"""
        from .api.user_task.search_user_tasks import asyncio as search_user_tasks_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_user_tasks_asyncio(**_kwargs)


    async def assign_user_task(self, user_task_key: str, *, data: AssignUserTaskData, **kwargs: Any) -> None:
        """Assign user task

 Assigns a user task with the given key to the given assignee.

Args:
    user_task_key (str): System-generated key for a user task.
    body (AssignUserTaskData):

Raises:
    errors.AssignUserTaskBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignUserTaskNotFound: If the response status code is 404. The user task with the given key was not found.
    errors.AssignUserTaskConflict: If the response status code is 409. The user task with the given key is in the wrong state currently. More details are provided in the response body.
    errors.AssignUserTaskInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignUserTaskServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user_task.assign_user_task import asyncio as assign_user_task_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_user_task_asyncio(**_kwargs)


    async def search_correlated_message_subscriptions(self, *, data: SearchCorrelatedMessageSubscriptionsData | Unset = UNSET, **kwargs: Any) -> SearchCorrelatedMessageSubscriptionsResponse200:
        """Search correlated message subscriptions

 Search correlated message subscriptions based on given criteria.

Args:
    body (SearchCorrelatedMessageSubscriptionsData | Unset):

Raises:
    errors.SearchCorrelatedMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchCorrelatedMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchCorrelatedMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchCorrelatedMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchCorrelatedMessageSubscriptionsResponse200"""
        from .api.message_subscription.search_correlated_message_subscriptions import asyncio as search_correlated_message_subscriptions_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_correlated_message_subscriptions_asyncio(**_kwargs)


    async def search_message_subscriptions(self, *, data: SearchMessageSubscriptionsData | Unset = UNSET, **kwargs: Any) -> SearchMessageSubscriptionsResponse200:
        """Search message subscriptions

 Search for message subscriptions based on given criteria.

Args:
    body (SearchMessageSubscriptionsData | Unset):

Raises:
    errors.SearchMessageSubscriptionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMessageSubscriptionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMessageSubscriptionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMessageSubscriptionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMessageSubscriptionsResponse200"""
        from .api.message_subscription.search_message_subscriptions import asyncio as search_message_subscriptions_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_message_subscriptions_asyncio(**_kwargs)


    async def get_decision_definition(self, decision_definition_key: str, **kwargs: Any) -> GetDecisionDefinitionResponse200:
        """Get decision definition

 Returns a decision definition by key.

Args:
    decision_definition_key (str): System-generated key for a decision definition. Example:
        2251799813326547.

Raises:
    errors.GetDecisionDefinitionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionDefinitionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionDefinitionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionDefinitionNotFound: If the response status code is 404. The decision definition with the given key was not found. More details are provided in the response body.
    errors.GetDecisionDefinitionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetDecisionDefinitionResponse200"""
        from .api.decision_definition.get_decision_definition import asyncio as get_decision_definition_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_decision_definition_asyncio(**_kwargs)


    async def evaluate_decision(self, *, data: DecisionevaluationbyID | Decisionevaluationbykey, **kwargs: Any) -> EvaluateDecisionResponse200:
        """Evaluate decision

 Evaluates a decision.
You specify the decision to evaluate either by using its unique key (as returned by
DeployResource), or using the decision ID. When using the decision ID, the latest deployed
version of the decision is used.

Args:
    body (DecisionevaluationbyID | Decisionevaluationbykey):

Raises:
    errors.EvaluateDecisionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.EvaluateDecisionNotFound: If the response status code is 404. The decision is not found.
    errors.EvaluateDecisionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.EvaluateDecisionServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    EvaluateDecisionResponse200"""
        from .api.decision_definition.evaluate_decision import asyncio as evaluate_decision_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await evaluate_decision_asyncio(**_kwargs)


    async def search_decision_definitions(self, *, data: SearchDecisionDefinitionsData | Unset = UNSET, **kwargs: Any) -> SearchDecisionDefinitionsResponse200:
        """Search decision definitions

 Search for decision definitions based on given criteria.

Args:
    body (SearchDecisionDefinitionsData | Unset):

Raises:
    errors.SearchDecisionDefinitionsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchDecisionDefinitionsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchDecisionDefinitionsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchDecisionDefinitionsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchDecisionDefinitionsResponse200"""
        from .api.decision_definition.search_decision_definitions import asyncio as search_decision_definitions_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_decision_definitions_asyncio(**_kwargs)


    async def get_decision_definition_xml(self, decision_definition_key: str, **kwargs: Any) -> str:
        """Get decision definition XML

 Returns decision definition as XML.

Args:
    decision_definition_key (str): System-generated key for a decision definition. Example:
        2251799813326547.

Raises:
    errors.GetDecisionDefinitionXmlBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetDecisionDefinitionXmlUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetDecisionDefinitionXmlForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetDecisionDefinitionXmlNotFound: If the response status code is 404. The decision definition with the given key was not found. More details are provided in the response body.
    errors.GetDecisionDefinitionXmlInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    str"""
        from .api.decision_definition.get_decision_definition_xml import asyncio as get_decision_definition_xml_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_decision_definition_xml_asyncio(**_kwargs)


    async def create_authorization(self, *, data: Object | Object1, **kwargs: Any) -> CreateAuthorizationResponse201:
        """Create authorization

 Create the authorization.

Args:
    body (Object | Object1): Defines an authorization request.
        Either an id-based or a property-based authorization can be provided.

Raises:
    errors.CreateAuthorizationBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateAuthorizationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateAuthorizationNotFound: If the response status code is 404. The owner was not found.
    errors.CreateAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateAuthorizationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateAuthorizationResponse201"""
        from .api.authorization.create_authorization import asyncio as create_authorization_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_authorization_asyncio(**_kwargs)


    async def get_authorization(self, authorization_key: str, **kwargs: Any) -> GetAuthorizationResponse200:
        """Get authorization

 Get authorization by the given key.

Args:
    authorization_key (str): System-generated key for an authorization. Example:
        2251799813684332.

Raises:
    errors.GetAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetAuthorizationForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetAuthorizationNotFound: If the response status code is 404. The authorization with the given key was not found.
    errors.GetAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetAuthorizationResponse200"""
        from .api.authorization.get_authorization import asyncio as get_authorization_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_authorization_asyncio(**_kwargs)


    async def update_authorization(self, authorization_key: str, *, data: Object | Object1, **kwargs: Any) -> None:
        """Update authorization

 Update the authorization with the given key.

Args:
    authorization_key (str): System-generated key for an authorization. Example:
        2251799813684332.
    body (Object | Object1): Defines an authorization request.
        Either an id-based or a property-based authorization can be provided.

Raises:
    errors.UpdateAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateAuthorizationNotFound: If the response status code is 404. The authorization with the authorizationKey was not found.
    errors.UpdateAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateAuthorizationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.authorization.update_authorization import asyncio as update_authorization_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_authorization_asyncio(**_kwargs)


    async def search_authorizations(self, *, data: SearchAuthorizationsData | Unset = UNSET, **kwargs: Any) -> SearchAuthorizationsResponse200:
        """Search authorizations

 Search for authorizations based on given criteria.

Args:
    body (SearchAuthorizationsData | Unset):

Raises:
    errors.SearchAuthorizationsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchAuthorizationsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchAuthorizationsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchAuthorizationsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchAuthorizationsResponse200"""
        from .api.authorization.search_authorizations import asyncio as search_authorizations_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_authorizations_asyncio(**_kwargs)


    async def delete_authorization(self, authorization_key: str, **kwargs: Any) -> None:
        """Delete authorization

 Deletes the authorization with the given key.

Args:
    authorization_key (str): System-generated key for an authorization. Example:
        2251799813684332.

Raises:
    errors.DeleteAuthorizationUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteAuthorizationNotFound: If the response status code is 404. The authorization with the authorizationKey was not found.
    errors.DeleteAuthorizationInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteAuthorizationServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.authorization.delete_authorization import asyncio as delete_authorization_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_authorization_asyncio(**_kwargs)


    async def search_incidents(self, *, data: SearchIncidentsData | Unset = UNSET, **kwargs: Any) -> SearchIncidentsResponse200:
        """Search incidents

 Search for incidents based on given criteria.

Args:
    body (SearchIncidentsData | Unset):

Raises:
    errors.SearchIncidentsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchIncidentsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchIncidentsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchIncidentsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchIncidentsResponse200"""
        from .api.incident.search_incidents import asyncio as search_incidents_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_incidents_asyncio(**_kwargs)


    async def get_process_instance_statistics_by_definition(self, *, data: GetProcessInstanceStatisticsByDefinitionData, **kwargs: Any) -> GetProcessInstanceStatisticsByDefinitionResponse200:
        """Get process instance statistics by definition

 Returns statistics for active process instances with incidents, grouped by process
definition. The result set is scoped to a specific incident error hash code, which must be
provided as a filter in the request body.

Args:
    body (GetProcessInstanceStatisticsByDefinitionData):

Raises:
    errors.GetProcessInstanceStatisticsByDefinitionBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsByDefinitionUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsByDefinitionForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsByDefinitionInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsByDefinitionResponse200"""
        from .api.incident.get_process_instance_statistics_by_definition import asyncio as get_process_instance_statistics_by_definition_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_instance_statistics_by_definition_asyncio(**_kwargs)


    async def get_incident(self, incident_key: str, **kwargs: Any) -> GetIncidentResponse200:
        """Get incident

 Returns incident as JSON.

Args:
    incident_key (str): System-generated key for a incident. Example: 2251799813689432.

Raises:
    errors.GetIncidentBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetIncidentUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetIncidentForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetIncidentNotFound: If the response status code is 404. The incident with the given key was not found.
    errors.GetIncidentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetIncidentResponse200"""
        from .api.incident.get_incident import asyncio as get_incident_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_incident_asyncio(**_kwargs)


    async def resolve_incident(self, incident_key: str, *, data: ResolveIncidentData | Unset = UNSET, **kwargs: Any) -> None:
        """Resolve incident

 Marks the incident as resolved; most likely a call to Update job will be necessary
to reset the job's retries, followed by this call.

Args:
    incident_key (str): System-generated key for a incident. Example: 2251799813689432.
    body (ResolveIncidentData | Unset):

Raises:
    errors.ResolveIncidentBadRequest: If the response status code is 400. The provided data is not valid.
    errors.ResolveIncidentNotFound: If the response status code is 404. The incident with the incidentKey is not found.
    errors.ResolveIncidentInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.ResolveIncidentServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.incident.resolve_incident import asyncio as resolve_incident_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await resolve_incident_asyncio(**_kwargs)


    async def get_process_instance_statistics_by_error(self, *, data: GetProcessInstanceStatisticsByErrorData | Unset = UNSET, **kwargs: Any) -> GetProcessInstanceStatisticsByErrorResponse200:
        """Get process instance statistics by error

 Returns statistics for active process instances that currently have active incidents,
grouped by incident error hash code.

Args:
    body (GetProcessInstanceStatisticsByErrorData | Unset):

Raises:
    errors.GetProcessInstanceStatisticsByErrorBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetProcessInstanceStatisticsByErrorUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetProcessInstanceStatisticsByErrorForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetProcessInstanceStatisticsByErrorInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetProcessInstanceStatisticsByErrorResponse200"""
        from .api.incident.get_process_instance_statistics_by_error import asyncio as get_process_instance_statistics_by_error_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_process_instance_statistics_by_error_asyncio(**_kwargs)


    async def get_user(self, username: str, **kwargs: Any) -> GetUserResponse200:
        """Get user

 Get a user by its username.

Args:
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.GetUserUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUserNotFound: If the response status code is 404. The user with the given username was not found.
    errors.GetUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUserResponse200"""
        from .api.user.get_user import asyncio as get_user_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_user_asyncio(**_kwargs)


    async def delete_user(self, username: str, **kwargs: Any) -> None:
        """Delete user

 Deletes a user.

Args:
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.DeleteUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.DeleteUserNotFound: If the response status code is 404. The user is not found.
    errors.DeleteUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.user.delete_user import asyncio as delete_user_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_user_asyncio(**_kwargs)


    async def create_user(self, *, data: CreateUserData, **kwargs: Any) -> CreateUserResponse201:
        """Create user

 Create a new user.

Args:
    body (CreateUserData):

Raises:
    errors.CreateUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateUserUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateUserConflict: If the response status code is 409. A user with this username already exists.
    errors.CreateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateUserResponse201"""
        from .api.user.create_user import asyncio as create_user_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_user_asyncio(**_kwargs)


    async def search_users(self, *, data: SearchUsersData | Unset = UNSET, **kwargs: Any) -> SearchUsersResponse200:
        """Search users

 Search for users based on given criteria.

Args:
    body (SearchUsersData | Unset):

Raises:
    errors.SearchUsersBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUsersUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchUsersForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchUsersInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUsersResponse200"""
        from .api.user.search_users import asyncio as search_users_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_users_asyncio(**_kwargs)


    async def update_user(self, username: str, *, data: UpdateUserData, **kwargs: Any) -> UpdateUserResponse200:
        """Update user

 Updates a user.

Args:
    username (str): The unique name of a user. Example: swillis.
    body (UpdateUserData):

Raises:
    errors.UpdateUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UpdateUserNotFound: If the response status code is 404. The user was not found.
    errors.UpdateUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateUserResponse200"""
        from .api.user.update_user import asyncio as update_user_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_user_asyncio(**_kwargs)


    async def get_usage_metrics(self, *, start_time: datetime.datetime, end_time: datetime.datetime, tenant_id: str | Unset = UNSET, with_tenants: bool | Unset = False, **kwargs: Any) -> GetUsageMetricsResponse200:
        """Get usage metrics

 Retrieve the usage metrics based on given criteria.

Args:
    start_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
    end_time (datetime.datetime):  Example: 2025-06-07T13:14:15Z.
    tenant_id (str | Unset): The unique identifier of the tenant. Example: customer-service.
    with_tenants (bool | Unset):  Default: False.

Raises:
    errors.GetUsageMetricsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.GetUsageMetricsUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetUsageMetricsForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetUsageMetricsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetUsageMetricsResponse200"""
        from .api.system.get_usage_metrics import asyncio as get_usage_metrics_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_usage_metrics_asyncio(**_kwargs)


    async def update_role(self, role_id: str, *, data: UpdateRoleData, **kwargs: Any) -> UpdateRoleResponse200:
        """Update role

 Update a role with the given ID.

Args:
    role_id (str):
    body (UpdateRoleData):

Raises:
    errors.UpdateRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UpdateRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.UpdateRoleNotFound: If the response status code is 404. The role with the ID is not found.
    errors.UpdateRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UpdateRoleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    UpdateRoleResponse200"""
        from .api.role.update_role import asyncio as update_role_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await update_role_asyncio(**_kwargs)


    async def assign_role_to_client(self, role_id: str, client_id: str, **kwargs: Any) -> None:
        """Assign a role to a client

 Assigns the specified role to the client. The client will inherit the authorizations associated with
this role.

Args:
    role_id (str):
    client_id (str):

Raises:
    errors.AssignRoleToClientBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToClientForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToClientNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.AssignRoleToClientConflict: If the response status code is 409. The role was already assigned to the client with the given ID.
    errors.AssignRoleToClientInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToClientServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.assign_role_to_client import asyncio as assign_role_to_client_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_role_to_client_asyncio(**_kwargs)


    async def get_role(self, role_id: str, **kwargs: Any) -> GetRoleResponse200:
        """Get role

 Get a role by its ID.

Args:
    role_id (str):

Raises:
    errors.GetRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.GetRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.GetRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.GetRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetRoleResponse200"""
        from .api.role.get_role import asyncio as get_role_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_role_asyncio(**_kwargs)


    async def unassign_role_from_mapping_rule(self, role_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Unassign a role from a mapping rule

 Unassigns a role from a mapping rule.

Args:
    role_id (str):
    mapping_rule_id (str):

Raises:
    errors.UnassignRoleFromMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromMappingRuleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromMappingRuleNotFound: If the response status code is 404. The role or mapping rule with the given ID was not found.
    errors.UnassignRoleFromMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.unassign_role_from_mapping_rule import asyncio as unassign_role_from_mapping_rule_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_role_from_mapping_rule_asyncio(**_kwargs)


    async def search_users_for_role(self, role_id: str, *, data: SearchUsersForRoleData | Unset = UNSET, **kwargs: Any) -> SearchUsersForRoleResponse200:
        """Search role users

 Search users with assigned role.

Args:
    role_id (str):
    body (SearchUsersForRoleData | Unset):

Raises:
    errors.SearchUsersForRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchUsersForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchUsersForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchUsersForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.SearchUsersForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchUsersForRoleResponse200"""
        from .api.role.search_users_for_role import asyncio as search_users_for_role_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_users_for_role_asyncio(**_kwargs)


    async def search_mapping_rules_for_role(self, role_id: str, *, data: SearchMappingRulesForRoleData | Unset = UNSET, **kwargs: Any) -> SearchMappingRulesForRoleResponse200:
        """Search role mapping rules

 Search mapping rules with assigned role.

Args:
    role_id (str):
    body (SearchMappingRulesForRoleData | Unset):

Raises:
    errors.SearchMappingRulesForRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchMappingRulesForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchMappingRulesForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchMappingRulesForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.SearchMappingRulesForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchMappingRulesForRoleResponse200"""
        from .api.role.search_mapping_rules_for_role import asyncio as search_mapping_rules_for_role_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_mapping_rules_for_role_asyncio(**_kwargs)


    async def search_groups_for_role(self, role_id: str, *, data: SearchGroupsForRoleData | Unset = UNSET, **kwargs: Any) -> SearchGroupsForRoleResponse200:
        """Search role groups

 Search groups with assigned role.

Args:
    role_id (str):
    body (SearchGroupsForRoleData | Unset):

Raises:
    errors.SearchGroupsForRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchGroupsForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchGroupsForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchGroupsForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.SearchGroupsForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchGroupsForRoleResponse200"""
        from .api.role.search_groups_for_role import asyncio as search_groups_for_role_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_groups_for_role_asyncio(**_kwargs)


    async def search_roles(self, *, data: SearchRolesData | Unset = UNSET, **kwargs: Any) -> SearchRolesResponse200:
        """Search roles

 Search for roles based on given criteria.

Args:
    body (SearchRolesData | Unset): Role search request.

Raises:
    errors.SearchRolesBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchRolesUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchRolesForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchRolesInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchRolesResponse200"""
        from .api.role.search_roles import asyncio as search_roles_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_roles_asyncio(**_kwargs)


    async def search_clients_for_role(self, role_id: str, *, data: SearchClientsForRoleData | Unset = UNSET, **kwargs: Any) -> SearchClientsForRoleResponse200:
        """Search role clients

 Search clients with assigned role.

Args:
    role_id (str):
    body (SearchClientsForRoleData | Unset):

Raises:
    errors.SearchClientsForRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.SearchClientsForRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.SearchClientsForRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.SearchClientsForRoleNotFound: If the response status code is 404. The role with the given ID was not found.
    errors.SearchClientsForRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    SearchClientsForRoleResponse200"""
        from .api.role.search_clients_for_role import asyncio as search_clients_for_role_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await search_clients_for_role_asyncio(**_kwargs)


    async def create_role(self, *, data: CreateRoleData | Unset = UNSET, **kwargs: Any) -> CreateRoleResponse201:
        """Create role

 Create a new role.

Args:
    body (CreateRoleData | Unset):

Raises:
    errors.CreateRoleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.CreateRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.CreateRoleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.CreateRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.CreateRoleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    CreateRoleResponse201"""
        from .api.role.create_role import asyncio as create_role_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await create_role_asyncio(**_kwargs)


    async def assign_role_to_group(self, role_id: str, group_id: str, **kwargs: Any) -> None:
        """Assign a role to a group

 Assigns the specified role to the group. Every member of the group (user or client) will inherit the
authorizations associated with this role.

Args:
    role_id (str):
    group_id (str):

Raises:
    errors.AssignRoleToGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToGroupNotFound: If the response status code is 404. The role or group with the given ID was not found.
    errors.AssignRoleToGroupConflict: If the response status code is 409. The role is already assigned to the group with the given ID.
    errors.AssignRoleToGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.assign_role_to_group import asyncio as assign_role_to_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_role_to_group_asyncio(**_kwargs)


    async def assign_role_to_mapping_rule(self, role_id: str, mapping_rule_id: str, **kwargs: Any) -> None:
        """Assign a role to a mapping rule

 Assigns a role to a mapping rule.

Args:
    role_id (str):
    mapping_rule_id (str):

Raises:
    errors.AssignRoleToMappingRuleBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToMappingRuleForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToMappingRuleNotFound: If the response status code is 404. The role or mapping rule with the given ID was not found.
    errors.AssignRoleToMappingRuleConflict: If the response status code is 409. The role is already assigned to the mapping rule with the given ID.
    errors.AssignRoleToMappingRuleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToMappingRuleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.assign_role_to_mapping_rule import asyncio as assign_role_to_mapping_rule_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_role_to_mapping_rule_asyncio(**_kwargs)


    async def unassign_role_from_client(self, role_id: str, client_id: str, **kwargs: Any) -> None:
        """Unassign a role from a client

 Unassigns the specified role from the client. The client will no longer inherit the authorizations
associated with this role.

Args:
    role_id (str):
    client_id (str):

Raises:
    errors.UnassignRoleFromClientBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromClientForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromClientNotFound: If the response status code is 404. The role or client with the given ID or username was not found.
    errors.UnassignRoleFromClientInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromClientServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.unassign_role_from_client import asyncio as unassign_role_from_client_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_role_from_client_asyncio(**_kwargs)


    async def delete_role(self, role_id: str, **kwargs: Any) -> None:
        """Delete role

 Deletes the role with the given ID.

Args:
    role_id (str):

Raises:
    errors.DeleteRoleUnauthorized: If the response status code is 401. The request lacks valid authentication credentials.
    errors.DeleteRoleNotFound: If the response status code is 404. The role with the ID was not found.
    errors.DeleteRoleInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.DeleteRoleServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.delete_role import asyncio as delete_role_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await delete_role_asyncio(**_kwargs)


    async def assign_role_to_user(self, role_id: str, username: str, **kwargs: Any) -> None:
        """Assign a role to a user

 Assigns the specified role to the user. The user will inherit the authorizations associated with
this role.

Args:
    role_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.AssignRoleToUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.AssignRoleToUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.AssignRoleToUserNotFound: If the response status code is 404. The role or user with the given ID or username was not found.
    errors.AssignRoleToUserConflict: If the response status code is 409. The role is already assigned to the user with the given ID.
    errors.AssignRoleToUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.AssignRoleToUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.assign_role_to_user import asyncio as assign_role_to_user_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await assign_role_to_user_asyncio(**_kwargs)


    async def unassign_role_from_group(self, role_id: str, group_id: str, **kwargs: Any) -> None:
        """Unassign a role from a group

 Unassigns the specified role from the group. All group members (user or client) no longer inherit
the authorizations associated with this role.

Args:
    role_id (str):
    group_id (str):

Raises:
    errors.UnassignRoleFromGroupBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromGroupForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromGroupNotFound: If the response status code is 404. The role or group with the given ID was not found.
    errors.UnassignRoleFromGroupInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromGroupServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.unassign_role_from_group import asyncio as unassign_role_from_group_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_role_from_group_asyncio(**_kwargs)


    async def unassign_role_from_user(self, role_id: str, username: str, **kwargs: Any) -> None:
        """Unassign a role from a user

 Unassigns a role from a user. The user will no longer inherit the authorizations associated with
this role.

Args:
    role_id (str):
    username (str): The unique name of a user. Example: swillis.

Raises:
    errors.UnassignRoleFromUserBadRequest: If the response status code is 400. The provided data is not valid.
    errors.UnassignRoleFromUserForbidden: If the response status code is 403. Forbidden. The request is not allowed.
    errors.UnassignRoleFromUserNotFound: If the response status code is 404. The role or user with the given ID or username was not found.
    errors.UnassignRoleFromUserInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnassignRoleFromUserServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    None"""
        from .api.role.unassign_role_from_user import asyncio as unassign_role_from_user_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await unassign_role_from_user_asyncio(**_kwargs)


    async def get_license(self, **kwargs: Any) -> GetLicenseResponse200:
        """Get license status

 Obtains the status of the current Camunda license.

Raises:
    errors.GetLicenseInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    GetLicenseResponse200"""
        from .api.license_.get_license import asyncio as get_license_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await get_license_asyncio(**_kwargs)


    async def broadcast_signal(self, *, data: BroadcastSignalData, **kwargs: Any) -> BroadcastSignalResponse200:
        """Broadcast signal

 Broadcasts a signal.

Args:
    body (BroadcastSignalData):

Raises:
    errors.BroadcastSignalBadRequest: If the response status code is 400. The provided data is not valid.
    errors.BroadcastSignalNotFound: If the response status code is 404. The signal is not found.
    errors.BroadcastSignalInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.BroadcastSignalServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    BroadcastSignalResponse200"""
        from .api.signal.broadcast_signal import asyncio as broadcast_signal_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await broadcast_signal_asyncio(**_kwargs)


    async def evaluate_conditionals(self, *, data: EvaluateConditionalsData, **kwargs: Any) -> EvaluateConditionalsResponse200:
        """Evaluate root level conditional start events

 Evaluates root-level conditional start events for process definitions.
If the evaluation is successful, it will return the keys of all created process instances, along
with their associated process definition key.
Multiple root-level conditional start events of the same process definition can trigger if their
conditions evaluate to true.

Args:
    body (EvaluateConditionalsData):

Raises:
    errors.EvaluateConditionalsBadRequest: If the response status code is 400. The provided data is not valid.
    errors.EvaluateConditionalsForbidden: If the response status code is 403. The client is not authorized to start process instances for the specified process definition. If a processDefinitionKey is not provided, this indicates that the client is not authorized to start process instances for at least one of the matched process definitions.
    errors.EvaluateConditionalsNotFound: If the response status code is 404. The process definition was not found for the given processDefinitionKey.
    errors.EvaluateConditionalsInternalServerError: If the response status code is 500. An internal error occurred while processing the request.
    errors.EvaluateConditionalsServiceUnavailable: If the response status code is 503. The service is currently unavailable. This may happen only on some requests where the system creates backpressure to prevent the server's compute resources from being exhausted, avoiding more severe failures. In this case, the title of the error object contains `RESOURCE_EXHAUSTED`. Clients are recommended to eventually retry those requests after a backoff period. You can learn more about the backpressure mechanism here: https://docs.camunda.io/docs/components/zeebe/technical-concepts/internal-processing/#handling-backpressure .
    errors.UnexpectedStatus: If the response status code is not documented.
    httpx.TimeoutException: If the request takes longer than Client.timeout.
Returns:
    EvaluateConditionalsResponse200"""
        from .api.conditional.evaluate_conditionals import asyncio as evaluate_conditionals_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await evaluate_conditionals_asyncio(**_kwargs)

