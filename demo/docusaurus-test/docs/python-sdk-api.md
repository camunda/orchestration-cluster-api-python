# API Reference

A client library for accessing Orchestration Cluster API

### *class* camunda_orchestration_sdk.AuthenticatedClient(base_url: str, token: str, prefix: str = 'Bearer', auth_header_name: str = 'Authorization', , raise_on_unexpected_status: bool = False, cookies: dict[str, str] = NOTHING, headers: dict[str, str] = NOTHING, timeout: Timeout | None = None, verify_ssl: str | bool | SSLContext = True, follow_redirects: bool = False, httpx_args: dict[str, Any] = NOTHING)

Bases: `object`

A Client which has been authenticated for use on secured endpoints

The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

> `base_url`: The base URL for the API, all requests are made to a relative path to this URL

> `cookies`: A dictionary of cookies to be sent with every request

> `headers`: A dictionary of headers to be sent with every request

> `timeout`: The maximum amount of a time a request can take. API functions will raise
> httpx.TimeoutException if this is exceeded.

> `verify_ssl`: Whether or not to verify the SSL certificate of the API server. This should be True in production,
> but can be set to False for testing purposes.

> `follow_redirects`: Whether or not to follow redirects. Default value is False.

> `httpx_args`: A dictionary of additional arguments to be passed to the `httpx.Client` and `httpx.AsyncClient` constructor.

#### raise_on_unexpected_status

Whether or not to raise an errors.UnexpectedStatus if the API returns a
status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
argument to the constructor.

* **Type:**
  bool

#### token

The token to use for authentication

* **Type:**
  str

#### prefix

The prefix to use for the Authorization header

* **Type:**
  str

#### auth_header_name

The name of the Authorization header

* **Type:**
  str

#### auth_header_name *: str*

#### get_async_httpx_client() → AsyncClient

Get the underlying httpx.AsyncClient, constructing a new one if not previously set

#### get_httpx_client() → Client

Get the underlying httpx.Client, constructing a new one if not previously set

#### prefix *: str*

#### raise_on_unexpected_status *: bool*

#### set_async_httpx_client(async_client: AsyncClient) → [AuthenticatedClient](#camunda_orchestration_sdk.AuthenticatedClient)

Manually set the underlying httpx.AsyncClient

**NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.

#### set_httpx_client(client: Client) → [AuthenticatedClient](#camunda_orchestration_sdk.AuthenticatedClient)

Manually set the underlying httpx.Client

**NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.

#### token *: str*

#### with_cookies(cookies: dict[str, str]) → [AuthenticatedClient](#camunda_orchestration_sdk.AuthenticatedClient)

Get a new client matching this one with additional cookies

#### with_headers(headers: dict[str, str]) → [AuthenticatedClient](#camunda_orchestration_sdk.AuthenticatedClient)

Get a new client matching this one with additional headers

#### with_timeout(timeout: Timeout) → [AuthenticatedClient](#camunda_orchestration_sdk.AuthenticatedClient)

Get a new client matching this one with a new timeout configuration

### *class* camunda_orchestration_sdk.CamundaClient(base_url: str = 'http://localhost:8080/v2', token: str | None = None, \*\*kwargs)

Bases: `object`

#### activate_ad_hoc_sub_process_activities(ad_hoc_sub_process_instance_key: str, , data: ActivateAdHocSubProcessActivitiesData, \*\*kwargs: Any) → ActivateAdHocSubProcessActivitiesResponse400

Activate activities within an ad-hoc sub-process

> Activates selected activities within an ad-hoc sub-process identified by element ID.

The provided element IDs must exist within the ad-hoc sub-process instance identified by the
provided adHocSubProcessInstanceKey.

* **Parameters:**
  * **ad_hoc_sub_process_instance_key** (*str*) – System-generated key for a element instance.
    Example: 2251799813686789.
  * **body** (*ActivateAdHocSubProcessActivitiesData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ActivateAdHocSubProcessActivitiesResponse400 | ActivateAdHocSubProcessActivitiesResponse401 | ActivateAdHocSubProcessActivitiesResponse403 | ActivateAdHocSubProcessActivitiesResponse404 | ActivateAdHocSubProcessActivitiesResponse500 | ActivateAdHocSubProcessActivitiesResponse503 | Any]

#### *async* activate_ad_hoc_sub_process_activities_async(ad_hoc_sub_process_instance_key: str, , data: ActivateAdHocSubProcessActivitiesData, \*\*kwargs: Any) → ActivateAdHocSubProcessActivitiesResponse400

Activate activities within an ad-hoc sub-process

> Activates selected activities within an ad-hoc sub-process identified by element ID.

The provided element IDs must exist within the ad-hoc sub-process instance identified by the
provided adHocSubProcessInstanceKey.

* **Parameters:**
  * **ad_hoc_sub_process_instance_key** (*str*) – System-generated key for a element instance.
    Example: 2251799813686789.
  * **body** (*ActivateAdHocSubProcessActivitiesData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ActivateAdHocSubProcessActivitiesResponse400 | ActivateAdHocSubProcessActivitiesResponse401 | ActivateAdHocSubProcessActivitiesResponse403 | ActivateAdHocSubProcessActivitiesResponse404 | ActivateAdHocSubProcessActivitiesResponse500 | ActivateAdHocSubProcessActivitiesResponse503 | Any]

#### activate_jobs(, data: ActivateJobsData, \*\*kwargs: Any) → ActivateJobsResponse200

Activate jobs

> Iterate through all known partitions and activate jobs up to the requested maximum.
* **Parameters:**
  **body** (*ActivateJobsData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ActivateJobsResponse200 | ActivateJobsResponse400 | ActivateJobsResponse401 | ActivateJobsResponse500 | ActivateJobsResponse503]

#### *async* activate_jobs_async(, data: ActivateJobsData, \*\*kwargs: Any) → ActivateJobsResponse200

Activate jobs

> Iterate through all known partitions and activate jobs up to the requested maximum.
* **Parameters:**
  **body** (*ActivateJobsData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ActivateJobsResponse200 | ActivateJobsResponse400 | ActivateJobsResponse401 | ActivateJobsResponse500 | ActivateJobsResponse503]

#### assign_client_to_group(group_id: str, client_id: str, \*\*kwargs: Any) → Any

Assign a client to a group

> Assigns a client to a group, making it a member of the group.

Members of the group inherit the group authorizations, roles, and tenant assignments.

* **Parameters:**
  * **group_id** (*str*)
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignClientToGroupResponse400 | AssignClientToGroupResponse403 | AssignClientToGroupResponse404 | AssignClientToGroupResponse409 | AssignClientToGroupResponse500 | AssignClientToGroupResponse503]

#### *async* assign_client_to_group_async(group_id: str, client_id: str, \*\*kwargs: Any) → Any

Assign a client to a group

> Assigns a client to a group, making it a member of the group.

Members of the group inherit the group authorizations, roles, and tenant assignments.

* **Parameters:**
  * **group_id** (*str*)
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignClientToGroupResponse400 | AssignClientToGroupResponse403 | AssignClientToGroupResponse404 | AssignClientToGroupResponse409 | AssignClientToGroupResponse500 | AssignClientToGroupResponse503]

#### assign_client_to_tenant(tenant_id: str, client_id: str, \*\*kwargs: Any) → Any

Assign a client to a tenant

> Assign the client to the specified tenant.

The client can then access tenant data and perform authorized actions.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignClientToTenantResponse400 | AssignClientToTenantResponse403 | AssignClientToTenantResponse404 | AssignClientToTenantResponse500 | AssignClientToTenantResponse503]

#### *async* assign_client_to_tenant_async(tenant_id: str, client_id: str, \*\*kwargs: Any) → Any

Assign a client to a tenant

> Assign the client to the specified tenant.

The client can then access tenant data and perform authorized actions.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignClientToTenantResponse400 | AssignClientToTenantResponse403 | AssignClientToTenantResponse404 | AssignClientToTenantResponse500 | AssignClientToTenantResponse503]

#### assign_group_to_tenant(tenant_id: str, group_id: str, \*\*kwargs: Any) → Any

Assign a group to a tenant

> Assigns a group to a specified tenant.

Group members (users, clients) can then access tenant data and perform authorized actions.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignGroupToTenantResponse400 | AssignGroupToTenantResponse403 | AssignGroupToTenantResponse404 | AssignGroupToTenantResponse500 | AssignGroupToTenantResponse503]

#### *async* assign_group_to_tenant_async(tenant_id: str, group_id: str, \*\*kwargs: Any) → Any

Assign a group to a tenant

> Assigns a group to a specified tenant.

Group members (users, clients) can then access tenant data and perform authorized actions.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignGroupToTenantResponse400 | AssignGroupToTenantResponse403 | AssignGroupToTenantResponse404 | AssignGroupToTenantResponse500 | AssignGroupToTenantResponse503]

#### assign_mapping_rule_to_group(group_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Assign a mapping rule to a group

> Assigns a mapping rule to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignMappingRuleToGroupResponse400 | AssignMappingRuleToGroupResponse403 | AssignMappingRuleToGroupResponse404 | AssignMappingRuleToGroupResponse409 | AssignMappingRuleToGroupResponse500 | AssignMappingRuleToGroupResponse503]

#### *async* assign_mapping_rule_to_group_async(group_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Assign a mapping rule to a group

> Assigns a mapping rule to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignMappingRuleToGroupResponse400 | AssignMappingRuleToGroupResponse403 | AssignMappingRuleToGroupResponse404 | AssignMappingRuleToGroupResponse409 | AssignMappingRuleToGroupResponse500 | AssignMappingRuleToGroupResponse503]

#### assign_mapping_rule_to_tenant(tenant_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Assign a mapping rule to a tenant

> Assign a single mapping rule to a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignMappingRuleToTenantResponse400 | AssignMappingRuleToTenantResponse403 | AssignMappingRuleToTenantResponse404 | AssignMappingRuleToTenantResponse500 | AssignMappingRuleToTenantResponse503]

#### *async* assign_mapping_rule_to_tenant_async(tenant_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Assign a mapping rule to a tenant

> Assign a single mapping rule to a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignMappingRuleToTenantResponse400 | AssignMappingRuleToTenantResponse403 | AssignMappingRuleToTenantResponse404 | AssignMappingRuleToTenantResponse500 | AssignMappingRuleToTenantResponse503]

#### assign_role_to_client(role_id: str, client_id: str, \*\*kwargs: Any) → Any

Assign a role to a client

> Assigns the specified role to the client. The client will inherit the authorizations associated with

this role.

* **Parameters:**
  * **role_id** (*str*)
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToClientResponse400 | AssignRoleToClientResponse403 | AssignRoleToClientResponse404 | AssignRoleToClientResponse409 | AssignRoleToClientResponse500 | AssignRoleToClientResponse503]

#### *async* assign_role_to_client_async(role_id: str, client_id: str, \*\*kwargs: Any) → Any

Assign a role to a client

> Assigns the specified role to the client. The client will inherit the authorizations associated with

this role.

* **Parameters:**
  * **role_id** (*str*)
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToClientResponse400 | AssignRoleToClientResponse403 | AssignRoleToClientResponse404 | AssignRoleToClientResponse409 | AssignRoleToClientResponse500 | AssignRoleToClientResponse503]

#### assign_role_to_group(role_id: str, group_id: str, \*\*kwargs: Any) → Any

Assign a role to a group

> Assigns the specified role to the group. Every member of the group (user or client) will inherit the

authorizations associated with this role.

* **Parameters:**
  * **role_id** (*str*)
  * **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToGroupResponse400 | AssignRoleToGroupResponse403 | AssignRoleToGroupResponse404 | AssignRoleToGroupResponse409 | AssignRoleToGroupResponse500 | AssignRoleToGroupResponse503]

#### *async* assign_role_to_group_async(role_id: str, group_id: str, \*\*kwargs: Any) → Any

Assign a role to a group

> Assigns the specified role to the group. Every member of the group (user or client) will inherit the

authorizations associated with this role.

* **Parameters:**
  * **role_id** (*str*)
  * **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToGroupResponse400 | AssignRoleToGroupResponse403 | AssignRoleToGroupResponse404 | AssignRoleToGroupResponse409 | AssignRoleToGroupResponse500 | AssignRoleToGroupResponse503]

#### assign_role_to_mapping_rule(role_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Assign a role to a mapping rule

> Assigns a role to a mapping rule.
* **Parameters:**
  * **role_id** (*str*)
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToMappingRuleResponse400 | AssignRoleToMappingRuleResponse403 | AssignRoleToMappingRuleResponse404 | AssignRoleToMappingRuleResponse409 | AssignRoleToMappingRuleResponse500 | AssignRoleToMappingRuleResponse503]

#### *async* assign_role_to_mapping_rule_async(role_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Assign a role to a mapping rule

> Assigns a role to a mapping rule.
* **Parameters:**
  * **role_id** (*str*)
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToMappingRuleResponse400 | AssignRoleToMappingRuleResponse403 | AssignRoleToMappingRuleResponse404 | AssignRoleToMappingRuleResponse409 | AssignRoleToMappingRuleResponse500 | AssignRoleToMappingRuleResponse503]

#### assign_role_to_tenant(tenant_id: str, role_id: str, \*\*kwargs: Any) → Any

Assign a role to a tenant

> Assigns a role to a specified tenant.

Users, Clients or Groups, that have the role assigned, will get access to the tenant’s data and can
perform actions according to their authorizations.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **role_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToTenantResponse400 | AssignRoleToTenantResponse403 | AssignRoleToTenantResponse404 | AssignRoleToTenantResponse500 | AssignRoleToTenantResponse503]

#### *async* assign_role_to_tenant_async(tenant_id: str, role_id: str, \*\*kwargs: Any) → Any

Assign a role to a tenant

> Assigns a role to a specified tenant.

Users, Clients or Groups, that have the role assigned, will get access to the tenant’s data and can
perform actions according to their authorizations.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **role_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToTenantResponse400 | AssignRoleToTenantResponse403 | AssignRoleToTenantResponse404 | AssignRoleToTenantResponse500 | AssignRoleToTenantResponse503]

#### assign_role_to_user(role_id: str, username: str, \*\*kwargs: Any) → Any

Assign a role to a user

> Assigns the specified role to the user. The user will inherit the authorizations associated with

this role.

* **Parameters:**
  * **role_id** (*str*)
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToUserResponse400 | AssignRoleToUserResponse403 | AssignRoleToUserResponse404 | AssignRoleToUserResponse409 | AssignRoleToUserResponse500 | AssignRoleToUserResponse503]

#### *async* assign_role_to_user_async(role_id: str, username: str, \*\*kwargs: Any) → Any

Assign a role to a user

> Assigns the specified role to the user. The user will inherit the authorizations associated with

this role.

* **Parameters:**
  * **role_id** (*str*)
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignRoleToUserResponse400 | AssignRoleToUserResponse403 | AssignRoleToUserResponse404 | AssignRoleToUserResponse409 | AssignRoleToUserResponse500 | AssignRoleToUserResponse503]

#### assign_user_task(user_task_key: str, , data: AssignUserTaskData, \*\*kwargs: Any) → Any

Assign user task

> Assigns a user task with the given key to the given assignee.
* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **body** (*AssignUserTaskData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignUserTaskResponse400 | AssignUserTaskResponse404 | AssignUserTaskResponse409 | AssignUserTaskResponse500 | AssignUserTaskResponse503]

#### *async* assign_user_task_async(user_task_key: str, , data: AssignUserTaskData, \*\*kwargs: Any) → Any

Assign user task

> Assigns a user task with the given key to the given assignee.
* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **body** (*AssignUserTaskData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignUserTaskResponse400 | AssignUserTaskResponse404 | AssignUserTaskResponse409 | AssignUserTaskResponse500 | AssignUserTaskResponse503]

#### assign_user_to_group(group_id: str, username: str, \*\*kwargs: Any) → Any

Assign a user to a group

> Assigns a user to a group, making the user a member of the group.

Group members inherit the group authorizations, roles, and tenant assignments.

* **Parameters:**
  * **group_id** (*str*)
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignUserToGroupResponse400 | AssignUserToGroupResponse403 | AssignUserToGroupResponse404 | AssignUserToGroupResponse409 | AssignUserToGroupResponse500 | AssignUserToGroupResponse503]

#### *async* assign_user_to_group_async(group_id: str, username: str, \*\*kwargs: Any) → Any

Assign a user to a group

> Assigns a user to a group, making the user a member of the group.

Group members inherit the group authorizations, roles, and tenant assignments.

* **Parameters:**
  * **group_id** (*str*)
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignUserToGroupResponse400 | AssignUserToGroupResponse403 | AssignUserToGroupResponse404 | AssignUserToGroupResponse409 | AssignUserToGroupResponse500 | AssignUserToGroupResponse503]

#### assign_user_to_tenant(tenant_id: str, username: str, \*\*kwargs: Any) → Any

Assign a user to a tenant

> Assign a single user to a specified tenant. The user can then access tenant data and perform

authorized actions.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignUserToTenantResponse400 | AssignUserToTenantResponse403 | AssignUserToTenantResponse404 | AssignUserToTenantResponse500 | AssignUserToTenantResponse503]

#### *async* assign_user_to_tenant_async(tenant_id: str, username: str, \*\*kwargs: Any) → Any

Assign a user to a tenant

> Assign a single user to a specified tenant. The user can then access tenant data and perform

authorized actions.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | AssignUserToTenantResponse400 | AssignUserToTenantResponse403 | AssignUserToTenantResponse404 | AssignUserToTenantResponse500 | AssignUserToTenantResponse503]

#### broadcast_signal(, data: BroadcastSignalData, \*\*kwargs: Any) → BroadcastSignalResponse200

Broadcast signal

> Broadcasts a signal.
* **Parameters:**
  **body** (*BroadcastSignalData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[BroadcastSignalResponse200 | BroadcastSignalResponse400 | BroadcastSignalResponse404 | BroadcastSignalResponse500 | BroadcastSignalResponse503]

#### *async* broadcast_signal_async(, data: BroadcastSignalData, \*\*kwargs: Any) → BroadcastSignalResponse200

Broadcast signal

> Broadcasts a signal.
* **Parameters:**
  **body** (*BroadcastSignalData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[BroadcastSignalResponse200 | BroadcastSignalResponse400 | BroadcastSignalResponse404 | BroadcastSignalResponse500 | BroadcastSignalResponse503]

#### cancel_batch_operation(batch_operation_key: str, \*, data: ~typing.Any | ~camunda_orchestration_sdk.types.Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: ~typing.Any) → Any

Cancel Batch operation

> Cancels a running batch operation.

This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  * **batch_operation_key** (*str*) – System-generated key for an batch operation. Example:
    2251799813684321.
  * **body** (*Any* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CancelBatchOperationResponse400 | CancelBatchOperationResponse403 | CancelBatchOperationResponse404 | CancelBatchOperationResponse500]

#### *async* cancel_batch_operation_async(batch_operation_key: str, \*, data: ~typing.Any | ~camunda_orchestration_sdk.types.Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: ~typing.Any) → Any

Cancel Batch operation

> Cancels a running batch operation.

This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  * **batch_operation_key** (*str*) – System-generated key for an batch operation. Example:
    2251799813684321.
  * **body** (*Any* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CancelBatchOperationResponse400 | CancelBatchOperationResponse403 | CancelBatchOperationResponse404 | CancelBatchOperationResponse500]

#### cancel_process_instance(process_instance_key: str, \*, data: CancelProcessInstanceDataType0 | None | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Cancel process instance

> Cancels a running process instance. As a cancellation includes more than just the removal of the

process instance resource, the cancellation resource must be posted.

* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*CancelProcessInstanceDataType0* *|* *None* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CancelProcessInstanceResponse400 | CancelProcessInstanceResponse404 | CancelProcessInstanceResponse500 | CancelProcessInstanceResponse503]

#### *async* cancel_process_instance_async(process_instance_key: str, \*, data: CancelProcessInstanceDataType0 | None | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Cancel process instance

> Cancels a running process instance. As a cancellation includes more than just the removal of the

process instance resource, the cancellation resource must be posted.

* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*CancelProcessInstanceDataType0* *|* *None* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CancelProcessInstanceResponse400 | CancelProcessInstanceResponse404 | CancelProcessInstanceResponse500 | CancelProcessInstanceResponse503]

#### cancel_process_instances_batch_operation(, data: CancelProcessInstancesBatchOperationData, \*\*kwargs: Any) → CancelProcessInstancesBatchOperationResponse200

Cancel process instances (batch)

> Cancels multiple running process instances.

Since only ACTIVE root instances can be cancelled, any given filters for state and
parentProcessInstanceKey are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*CancelProcessInstancesBatchOperationData*) – The process instance filter that defines
  which process instances should be canceled.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CancelProcessInstancesBatchOperationResponse200 | CancelProcessInstancesBatchOperationResponse400 | CancelProcessInstancesBatchOperationResponse401 | CancelProcessInstancesBatchOperationResponse403 | CancelProcessInstancesBatchOperationResponse500]

#### *async* cancel_process_instances_batch_operation_async(, data: CancelProcessInstancesBatchOperationData, \*\*kwargs: Any) → CancelProcessInstancesBatchOperationResponse200

Cancel process instances (batch)

> Cancels multiple running process instances.

Since only ACTIVE root instances can be cancelled, any given filters for state and
parentProcessInstanceKey are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*CancelProcessInstancesBatchOperationData*) – The process instance filter that defines
  which process instances should be canceled.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CancelProcessInstancesBatchOperationResponse200 | CancelProcessInstancesBatchOperationResponse400 | CancelProcessInstancesBatchOperationResponse401 | CancelProcessInstancesBatchOperationResponse403 | CancelProcessInstancesBatchOperationResponse500]

#### client *: [Client](#camunda_orchestration_sdk.Client) | [AuthenticatedClient](#camunda_orchestration_sdk.AuthenticatedClient)*

#### complete_job(job_key: str, \*, data: CompleteJobData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Complete job

> Complete a job with the given payload, which allows completing the associated service task.
* **Parameters:**
  * **job_key** (*str*) – System-generated key for a job. Example: 2251799813653498.
  * **body** (*CompleteJobData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CompleteJobResponse400 | CompleteJobResponse404 | CompleteJobResponse409 | CompleteJobResponse500 | CompleteJobResponse503]

#### *async* complete_job_async(job_key: str, \*, data: CompleteJobData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Complete job

> Complete a job with the given payload, which allows completing the associated service task.
* **Parameters:**
  * **job_key** (*str*) – System-generated key for a job. Example: 2251799813653498.
  * **body** (*CompleteJobData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CompleteJobResponse400 | CompleteJobResponse404 | CompleteJobResponse409 | CompleteJobResponse500 | CompleteJobResponse503]

#### complete_user_task(user_task_key: str, \*, data: CompleteUserTaskData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Complete user task

> Completes a user task with the given key.
* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **body** (*CompleteUserTaskData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CompleteUserTaskResponse400 | CompleteUserTaskResponse404 | CompleteUserTaskResponse409 | CompleteUserTaskResponse500 | CompleteUserTaskResponse503]

#### *async* complete_user_task_async(user_task_key: str, \*, data: CompleteUserTaskData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Complete user task

> Completes a user task with the given key.
* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **body** (*CompleteUserTaskData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CompleteUserTaskResponse400 | CompleteUserTaskResponse404 | CompleteUserTaskResponse409 | CompleteUserTaskResponse500 | CompleteUserTaskResponse503]

#### correlate_message(, data: CorrelateMessageData, \*\*kwargs: Any) → CorrelateMessageResponse200

Correlate message

> Publishes a message and correlates it to a subscription.

If correlation is successful it will return the first process instance key the message correlated
with.
The message is not buffered.
Use the publish message endpoint to send messages that can be buffered.

* **Parameters:**
  **body** (*CorrelateMessageData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CorrelateMessageResponse200 | CorrelateMessageResponse400 | CorrelateMessageResponse403 | CorrelateMessageResponse404 | CorrelateMessageResponse500 | CorrelateMessageResponse503]

#### *async* correlate_message_async(, data: CorrelateMessageData, \*\*kwargs: Any) → CorrelateMessageResponse200

Correlate message

> Publishes a message and correlates it to a subscription.

If correlation is successful it will return the first process instance key the message correlated
with.
The message is not buffered.
Use the publish message endpoint to send messages that can be buffered.

* **Parameters:**
  **body** (*CorrelateMessageData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CorrelateMessageResponse200 | CorrelateMessageResponse400 | CorrelateMessageResponse403 | CorrelateMessageResponse404 | CorrelateMessageResponse500 | CorrelateMessageResponse503]

#### create_admin_user(, data: CreateAdminUserData, \*\*kwargs: Any) → Any

Create admin user

> Creates a new user and assigns the admin role to it. This endpoint is only usable when users are

managed in the Orchestration Cluster and while no user is assigned to the admin role.

* **Parameters:**
  **body** (*CreateAdminUserData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CreateAdminUserResponse400 | CreateAdminUserResponse403 | CreateAdminUserResponse500 | CreateAdminUserResponse503]

#### *async* create_admin_user_async(, data: CreateAdminUserData, \*\*kwargs: Any) → Any

Create admin user

> Creates a new user and assigns the admin role to it. This endpoint is only usable when users are

managed in the Orchestration Cluster and while no user is assigned to the admin role.

* **Parameters:**
  **body** (*CreateAdminUserData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CreateAdminUserResponse400 | CreateAdminUserResponse403 | CreateAdminUserResponse500 | CreateAdminUserResponse503]

#### create_authorization(, data: Object | Object1, \*\*kwargs: Any) → CreateAuthorizationResponse201

Create authorization

> Create the authorization.
* **Parameters:**
  **body** (*Object* *|* *Object1*) – Defines an authorization request.
  Either an id-based or a property-based authorization can be provided.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateAuthorizationResponse201 | CreateAuthorizationResponse400 | CreateAuthorizationResponse401 | CreateAuthorizationResponse403 | CreateAuthorizationResponse404 | CreateAuthorizationResponse500 | CreateAuthorizationResponse503]

#### *async* create_authorization_async(, data: Object | Object1, \*\*kwargs: Any) → CreateAuthorizationResponse201

Create authorization

> Create the authorization.
* **Parameters:**
  **body** (*Object* *|* *Object1*) – Defines an authorization request.
  Either an id-based or a property-based authorization can be provided.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateAuthorizationResponse201 | CreateAuthorizationResponse400 | CreateAuthorizationResponse401 | CreateAuthorizationResponse403 | CreateAuthorizationResponse404 | CreateAuthorizationResponse500 | CreateAuthorizationResponse503]

#### create_deployment(, data: CreateDeploymentData, \*\*kwargs: Any) → CreateDeploymentResponse200

Deploy resources

> Deploys one or more resources (e.g. processes, decision models, or forms).

This is an atomic call, i.e. either all resources are deployed or none of them are.

* **Parameters:**
  **body** (*CreateDeploymentData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateDeploymentResponse200 | CreateDeploymentResponse400 | CreateDeploymentResponse503]

#### *async* create_deployment_async(, data: CreateDeploymentData, \*\*kwargs: Any) → CreateDeploymentResponse200

Deploy resources

> Deploys one or more resources (e.g. processes, decision models, or forms).

This is an atomic call, i.e. either all resources are deployed or none of them are.

* **Parameters:**
  **body** (*CreateDeploymentData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateDeploymentResponse200 | CreateDeploymentResponse400 | CreateDeploymentResponse503]

#### create_document(\*, data: CreateDocumentData, store_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, document_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateDocumentResponse201

Upload document

> Upload a document to the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

* **Parameters:**
  * **store_id** (*str* *|* *Unset*)
  * **document_id** (*str* *|* *Unset*) – Document Id that uniquely identifies a document.
  * **body** (*CreateDocumentData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateDocumentResponse201 | CreateDocumentResponse400 | CreateDocumentResponse415]

#### *async* create_document_async(\*, data: CreateDocumentData, store_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, document_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateDocumentResponse201

Upload document

> Upload a document to the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

* **Parameters:**
  * **store_id** (*str* *|* *Unset*)
  * **document_id** (*str* *|* *Unset*) – Document Id that uniquely identifies a document.
  * **body** (*CreateDocumentData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateDocumentResponse201 | CreateDocumentResponse400 | CreateDocumentResponse415]

#### create_document_link(document_id: str, \*, data: CreateDocumentLinkData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, store_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, content_hash: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateDocumentLinkResponse201

Create document link

> Create a link to a document in the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP

* **Parameters:**
  * **document_id** (*str*) – Document Id that uniquely identifies a document.
  * **store_id** (*str* *|* *Unset*)
  * **content_hash** (*str* *|* *Unset*)
  * **body** (*CreateDocumentLinkData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateDocumentLinkResponse201 | CreateDocumentLinkResponse400]

#### *async* create_document_link_async(document_id: str, \*, data: CreateDocumentLinkData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, store_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, content_hash: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateDocumentLinkResponse201

Create document link

> Create a link to a document in the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP

* **Parameters:**
  * **document_id** (*str*) – Document Id that uniquely identifies a document.
  * **store_id** (*str* *|* *Unset*)
  * **content_hash** (*str* *|* *Unset*)
  * **body** (*CreateDocumentLinkData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateDocumentLinkResponse201 | CreateDocumentLinkResponse400]

#### create_documents(\*, data: CreateDocumentsData, store_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateDocumentsResponse201

Upload multiple documents

> Upload multiple documents to the Camunda 8 cluster.

The caller must provide a file name for each document, which will be used in case of a multi-status
response
to identify which documents failed to upload. The file name can be provided in the Content-
Disposition header
of the file part or in the fileName field of the metadata. You can add a parallel array of
metadata objects. These
are matched with the files based on index, and must have the same length as the files array.
To pass homogenous metadata for all files, spread the metadata over the metadata array.
A filename value provided explicitly via the metadata array in the request overrides the Content-
Disposition header
of the file part.

In case of a multi-status response, the response body will contain a list of
DocumentBatchProblemDetail objects,
each of which contains the file name of the document that failed to upload and the reason for the
failure.
The client can choose to retry the whole batch or individual documents based on the response.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

* **Parameters:**
  * **store_id** (*str* *|* *Unset*)
  * **body** (*CreateDocumentsData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateDocumentsResponse201 | CreateDocumentsResponse207 | CreateDocumentsResponse400 | CreateDocumentsResponse415]

#### *async* create_documents_async(\*, data: CreateDocumentsData, store_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateDocumentsResponse201

Upload multiple documents

> Upload multiple documents to the Camunda 8 cluster.

The caller must provide a file name for each document, which will be used in case of a multi-status
response
to identify which documents failed to upload. The file name can be provided in the Content-
Disposition header
of the file part or in the fileName field of the metadata. You can add a parallel array of
metadata objects. These
are matched with the files based on index, and must have the same length as the files array.
To pass homogenous metadata for all files, spread the metadata over the metadata array.
A filename value provided explicitly via the metadata array in the request overrides the Content-
Disposition header
of the file part.

In case of a multi-status response, the response body will contain a list of
DocumentBatchProblemDetail objects,
each of which contains the file name of the document that failed to upload and the reason for the
failure.
The client can choose to retry the whole batch or individual documents based on the response.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

* **Parameters:**
  * **store_id** (*str* *|* *Unset*)
  * **body** (*CreateDocumentsData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateDocumentsResponse201 | CreateDocumentsResponse207 | CreateDocumentsResponse400 | CreateDocumentsResponse415]

#### create_element_instance_variables(element_instance_key: str, , data: CreateElementInstanceVariablesData, \*\*kwargs: Any) → Any

Update element instance variables

> Updates all the variables of a particular scope (for example, process instance, element instance)

with the given variable data.
Specify the element instance in the elementInstanceKey parameter.

* **Parameters:**
  * **element_instance_key** (*str*) – System-generated key for a element instance. Example:
    2251799813686789.
  * **body** (*CreateElementInstanceVariablesData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CreateElementInstanceVariablesResponse400 | CreateElementInstanceVariablesResponse500 | CreateElementInstanceVariablesResponse503]

#### *async* create_element_instance_variables_async(element_instance_key: str, , data: CreateElementInstanceVariablesData, \*\*kwargs: Any) → Any

Update element instance variables

> Updates all the variables of a particular scope (for example, process instance, element instance)

with the given variable data.
Specify the element instance in the elementInstanceKey parameter.

* **Parameters:**
  * **element_instance_key** (*str*) – System-generated key for a element instance. Example:
    2251799813686789.
  * **body** (*CreateElementInstanceVariablesData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CreateElementInstanceVariablesResponse400 | CreateElementInstanceVariablesResponse500 | CreateElementInstanceVariablesResponse503]

#### create_global_cluster_variable(, data: CreateGlobalClusterVariableData, \*\*kwargs: Any) → CreateGlobalClusterVariableResponse200

Create a global-scoped cluster variable

* **Parameters:**
  **body** (*CreateGlobalClusterVariableData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateGlobalClusterVariableResponse200 | CreateGlobalClusterVariableResponse400 | CreateGlobalClusterVariableResponse401 | CreateGlobalClusterVariableResponse403 | CreateGlobalClusterVariableResponse500]

#### *async* create_global_cluster_variable_async(, data: CreateGlobalClusterVariableData, \*\*kwargs: Any) → CreateGlobalClusterVariableResponse200

Create a global-scoped cluster variable

* **Parameters:**
  **body** (*CreateGlobalClusterVariableData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateGlobalClusterVariableResponse200 | CreateGlobalClusterVariableResponse400 | CreateGlobalClusterVariableResponse401 | CreateGlobalClusterVariableResponse403 | CreateGlobalClusterVariableResponse500]

#### create_group(\*, data: CreateGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateGroupResponse201

Create group

> Create a new group.
* **Parameters:**
  **body** (*CreateGroupData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateGroupResponse201 | CreateGroupResponse400 | CreateGroupResponse401 | CreateGroupResponse403 | CreateGroupResponse500 | CreateGroupResponse503]

#### *async* create_group_async(\*, data: CreateGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateGroupResponse201

Create group

> Create a new group.
* **Parameters:**
  **body** (*CreateGroupData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateGroupResponse201 | CreateGroupResponse400 | CreateGroupResponse401 | CreateGroupResponse403 | CreateGroupResponse500 | CreateGroupResponse503]

#### create_job_worker(config: [WorkerConfig](#camunda_orchestration_sdk.WorkerConfig), callback: JobHandler, auto_start: bool = True) → JobWorker

#### create_mapping_rule(\*, data: CreateMappingRuleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateMappingRuleResponse201

Create mapping rule

> Create a new mapping rule
* **Parameters:**
  **body** (*CreateMappingRuleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateMappingRuleResponse201 | CreateMappingRuleResponse400 | CreateMappingRuleResponse403 | CreateMappingRuleResponse404 | CreateMappingRuleResponse500]

#### *async* create_mapping_rule_async(\*, data: CreateMappingRuleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateMappingRuleResponse201

Create mapping rule

> Create a new mapping rule
* **Parameters:**
  **body** (*CreateMappingRuleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateMappingRuleResponse201 | CreateMappingRuleResponse400 | CreateMappingRuleResponse403 | CreateMappingRuleResponse404 | CreateMappingRuleResponse500]

#### create_process_instance(, data: Processcreationbyid | Processcreationbykey, \*\*kwargs: Any) → CreateProcessInstanceResponse200

Create process instance

> Creates and starts an instance of the specified process.

The process definition to use to create the instance can be specified either using its unique key
(as returned by Deploy resources), or using the BPMN process id and a version.

Waits for the completion of the process instance before returning a result
when awaitCompletion is enabled.

* **Parameters:**
  **body** (*Processcreationbyid* *|* *Processcreationbykey*) – Instructions for creating a process
  instance. The process definition can be specified
  either by id or by key.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateProcessInstanceResponse200 | CreateProcessInstanceResponse400 | CreateProcessInstanceResponse500 | CreateProcessInstanceResponse503 | CreateProcessInstanceResponse504]

#### *async* create_process_instance_async(, data: Processcreationbyid | Processcreationbykey, \*\*kwargs: Any) → CreateProcessInstanceResponse200

Create process instance

> Creates and starts an instance of the specified process.

The process definition to use to create the instance can be specified either using its unique key
(as returned by Deploy resources), or using the BPMN process id and a version.

Waits for the completion of the process instance before returning a result
when awaitCompletion is enabled.

* **Parameters:**
  **body** (*Processcreationbyid* *|* *Processcreationbykey*) – Instructions for creating a process
  instance. The process definition can be specified
  either by id or by key.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateProcessInstanceResponse200 | CreateProcessInstanceResponse400 | CreateProcessInstanceResponse500 | CreateProcessInstanceResponse503 | CreateProcessInstanceResponse504]

#### create_role(\*, data: CreateRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateRoleResponse201

Create role

> Create a new role.
* **Parameters:**
  **body** (*CreateRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateRoleResponse201 | CreateRoleResponse400 | CreateRoleResponse401 | CreateRoleResponse403 | CreateRoleResponse500 | CreateRoleResponse503]

#### *async* create_role_async(\*, data: CreateRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → CreateRoleResponse201

Create role

> Create a new role.
* **Parameters:**
  **body** (*CreateRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateRoleResponse201 | CreateRoleResponse400 | CreateRoleResponse401 | CreateRoleResponse403 | CreateRoleResponse500 | CreateRoleResponse503]

#### create_tenant(, data: CreateTenantData, \*\*kwargs: Any) → Any

Create tenant

> Creates a new tenant.
* **Parameters:**
  **body** (*CreateTenantData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CreateTenantResponse201 | CreateTenantResponse400 | CreateTenantResponse403 | CreateTenantResponse404 | CreateTenantResponse500 | CreateTenantResponse503]

#### *async* create_tenant_async(, data: CreateTenantData, \*\*kwargs: Any) → Any

Create tenant

> Creates a new tenant.
* **Parameters:**
  **body** (*CreateTenantData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | CreateTenantResponse201 | CreateTenantResponse400 | CreateTenantResponse403 | CreateTenantResponse404 | CreateTenantResponse500 | CreateTenantResponse503]

#### create_tenant_cluster_variable(tenant_id: str, , data: CreateTenantClusterVariableData, \*\*kwargs: Any) → CreateTenantClusterVariableResponse200

Create a tenant-scoped cluster variable

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*CreateTenantClusterVariableData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateTenantClusterVariableResponse200 | CreateTenantClusterVariableResponse400 | CreateTenantClusterVariableResponse401 | CreateTenantClusterVariableResponse403 | CreateTenantClusterVariableResponse500]

#### *async* create_tenant_cluster_variable_async(tenant_id: str, , data: CreateTenantClusterVariableData, \*\*kwargs: Any) → CreateTenantClusterVariableResponse200

Create a tenant-scoped cluster variable

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*CreateTenantClusterVariableData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateTenantClusterVariableResponse200 | CreateTenantClusterVariableResponse400 | CreateTenantClusterVariableResponse401 | CreateTenantClusterVariableResponse403 | CreateTenantClusterVariableResponse500]

#### create_user(, data: CreateUserData, \*\*kwargs: Any) → CreateUserResponse201

Create user

> Create a new user.
* **Parameters:**
  **body** (*CreateUserData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateUserResponse201 | CreateUserResponse400 | CreateUserResponse401 | CreateUserResponse403 | CreateUserResponse409 | CreateUserResponse500 | CreateUserResponse503]

#### *async* create_user_async(, data: CreateUserData, \*\*kwargs: Any) → CreateUserResponse201

Create user

> Create a new user.
* **Parameters:**
  **body** (*CreateUserData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[CreateUserResponse201 | CreateUserResponse400 | CreateUserResponse401 | CreateUserResponse403 | CreateUserResponse409 | CreateUserResponse500 | CreateUserResponse503]

#### delete_authorization(authorization_key: str, \*\*kwargs: Any) → Any

Delete authorization

> Deletes the authorization with the given key.
* **Parameters:**
  **authorization_key** (*str*) – System-generated key for an authorization. Example:
  2251799813684332.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteAuthorizationResponse401 | DeleteAuthorizationResponse404 | DeleteAuthorizationResponse500 | DeleteAuthorizationResponse503]

#### *async* delete_authorization_async(authorization_key: str, \*\*kwargs: Any) → Any

Delete authorization

> Deletes the authorization with the given key.
* **Parameters:**
  **authorization_key** (*str*) – System-generated key for an authorization. Example:
  2251799813684332.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteAuthorizationResponse401 | DeleteAuthorizationResponse404 | DeleteAuthorizationResponse500 | DeleteAuthorizationResponse503]

#### delete_document(document_id: str, \*, store_id: str | ~camunda_orchestration_sdk.types.Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: ~typing.Any) → Any

Delete document

> Delete a document from the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

* **Parameters:**
  * **document_id** (*str*) – Document Id that uniquely identifies a document.
  * **store_id** (*str* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteDocumentResponse404 | DeleteDocumentResponse500]

#### *async* delete_document_async(document_id: str, \*, store_id: str | ~camunda_orchestration_sdk.types.Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: ~typing.Any) → Any

Delete document

> Delete a document from the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

* **Parameters:**
  * **document_id** (*str*) – Document Id that uniquely identifies a document.
  * **store_id** (*str* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteDocumentResponse404 | DeleteDocumentResponse500]

#### delete_global_cluster_variable(name: str, \*\*kwargs: Any) → Any

Delete a global-scoped cluster variable

* **Parameters:**
  **name** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteGlobalClusterVariableResponse400 | DeleteGlobalClusterVariableResponse401 | DeleteGlobalClusterVariableResponse403 | DeleteGlobalClusterVariableResponse404 | DeleteGlobalClusterVariableResponse500]

#### *async* delete_global_cluster_variable_async(name: str, \*\*kwargs: Any) → Any

Delete a global-scoped cluster variable

* **Parameters:**
  **name** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteGlobalClusterVariableResponse400 | DeleteGlobalClusterVariableResponse401 | DeleteGlobalClusterVariableResponse403 | DeleteGlobalClusterVariableResponse404 | DeleteGlobalClusterVariableResponse500]

#### delete_group(group_id: str, \*\*kwargs: Any) → Any

Delete group

> Deletes the group with the given ID.
* **Parameters:**
  **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteGroupResponse401 | DeleteGroupResponse404 | DeleteGroupResponse500 | DeleteGroupResponse503]

#### *async* delete_group_async(group_id: str, \*\*kwargs: Any) → Any

Delete group

> Deletes the group with the given ID.
* **Parameters:**
  **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteGroupResponse401 | DeleteGroupResponse404 | DeleteGroupResponse500 | DeleteGroupResponse503]

#### delete_mapping_rule(mapping_rule_id: str, \*\*kwargs: Any) → Any

Delete a mapping rule

> Deletes the mapping rule with the given ID.
* **Parameters:**
  **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteMappingRuleResponse401 | DeleteMappingRuleResponse404 | DeleteMappingRuleResponse500 | DeleteMappingRuleResponse503]

#### *async* delete_mapping_rule_async(mapping_rule_id: str, \*\*kwargs: Any) → Any

Delete a mapping rule

> Deletes the mapping rule with the given ID.
* **Parameters:**
  **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteMappingRuleResponse401 | DeleteMappingRuleResponse404 | DeleteMappingRuleResponse500 | DeleteMappingRuleResponse503]

#### delete_process_instance(process_instance_key: str, \*, data: DeleteProcessInstanceDataType0 | None | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → DeleteProcessInstanceResponse200

Delete process instance

> Deletes a process instance. Only instances that are completed or terminated can be deleted.
* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*DeleteProcessInstanceDataType0* *|* *None* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[DeleteProcessInstanceResponse200 | DeleteProcessInstanceResponse401 | DeleteProcessInstanceResponse403 | DeleteProcessInstanceResponse404 | DeleteProcessInstanceResponse409 | DeleteProcessInstanceResponse500 | DeleteProcessInstanceResponse503]

#### *async* delete_process_instance_async(process_instance_key: str, \*, data: DeleteProcessInstanceDataType0 | None | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → DeleteProcessInstanceResponse200

Delete process instance

> Deletes a process instance. Only instances that are completed or terminated can be deleted.
* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*DeleteProcessInstanceDataType0* *|* *None* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[DeleteProcessInstanceResponse200 | DeleteProcessInstanceResponse401 | DeleteProcessInstanceResponse403 | DeleteProcessInstanceResponse404 | DeleteProcessInstanceResponse409 | DeleteProcessInstanceResponse500 | DeleteProcessInstanceResponse503]

#### delete_process_instances_batch_operation(, data: DeleteProcessInstancesBatchOperationData, \*\*kwargs: Any) → DeleteProcessInstancesBatchOperationResponse200

Delete process instances (batch)

> Delete multiple process instances. This will delete the historic data from secondary storage.

Only process instances in a final state (COMPLETED or TERMINATED) can be deleted.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*DeleteProcessInstancesBatchOperationData*) – The process instance filter that defines
  which process instances should be deleted.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[DeleteProcessInstancesBatchOperationResponse200 | DeleteProcessInstancesBatchOperationResponse400 | DeleteProcessInstancesBatchOperationResponse401 | DeleteProcessInstancesBatchOperationResponse403 | DeleteProcessInstancesBatchOperationResponse500]

#### *async* delete_process_instances_batch_operation_async(, data: DeleteProcessInstancesBatchOperationData, \*\*kwargs: Any) → DeleteProcessInstancesBatchOperationResponse200

Delete process instances (batch)

> Delete multiple process instances. This will delete the historic data from secondary storage.

Only process instances in a final state (COMPLETED or TERMINATED) can be deleted.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*DeleteProcessInstancesBatchOperationData*) – The process instance filter that defines
  which process instances should be deleted.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[DeleteProcessInstancesBatchOperationResponse200 | DeleteProcessInstancesBatchOperationResponse400 | DeleteProcessInstancesBatchOperationResponse401 | DeleteProcessInstancesBatchOperationResponse403 | DeleteProcessInstancesBatchOperationResponse500]

#### delete_resource(resource_key: str, \*, data: DeleteResourceDataType0 | None | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Delete resource

> Deletes a deployed resource.

This can be a process definition, decision requirements definition, or form definition
deployed using the deploy resources endpoint. Specify the resource you want to delete in the
resourceKey parameter.

* **Parameters:**
  * **resource_key** (*str*) – The system-assigned key for this resource.
  * **body** (*DeleteResourceDataType0* *|* *None* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteResourceResponse400 | DeleteResourceResponse404 | DeleteResourceResponse500 | DeleteResourceResponse503]

#### *async* delete_resource_async(resource_key: str, \*, data: DeleteResourceDataType0 | None | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Delete resource

> Deletes a deployed resource.

This can be a process definition, decision requirements definition, or form definition
deployed using the deploy resources endpoint. Specify the resource you want to delete in the
resourceKey parameter.

* **Parameters:**
  * **resource_key** (*str*) – The system-assigned key for this resource.
  * **body** (*DeleteResourceDataType0* *|* *None* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteResourceResponse400 | DeleteResourceResponse404 | DeleteResourceResponse500 | DeleteResourceResponse503]

#### delete_role(role_id: str, \*\*kwargs: Any) → Any

Delete role

> Deletes the role with the given ID.
* **Parameters:**
  **role_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteRoleResponse401 | DeleteRoleResponse404 | DeleteRoleResponse500 | DeleteRoleResponse503]

#### *async* delete_role_async(role_id: str, \*\*kwargs: Any) → Any

Delete role

> Deletes the role with the given ID.
* **Parameters:**
  **role_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteRoleResponse401 | DeleteRoleResponse404 | DeleteRoleResponse500 | DeleteRoleResponse503]

#### delete_tenant(tenant_id: str, \*\*kwargs: Any) → Any

Delete tenant

> Deletes an existing tenant.
* **Parameters:**
  **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteTenantResponse400 | DeleteTenantResponse403 | DeleteTenantResponse404 | DeleteTenantResponse500 | DeleteTenantResponse503]

#### *async* delete_tenant_async(tenant_id: str, \*\*kwargs: Any) → Any

Delete tenant

> Deletes an existing tenant.
* **Parameters:**
  **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteTenantResponse400 | DeleteTenantResponse403 | DeleteTenantResponse404 | DeleteTenantResponse500 | DeleteTenantResponse503]

#### delete_tenant_cluster_variable(tenant_id: str, name: str, \*\*kwargs: Any) → Any

Delete a tenant-scoped cluster variable

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **name** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteTenantClusterVariableResponse400 | DeleteTenantClusterVariableResponse401 | DeleteTenantClusterVariableResponse403 | DeleteTenantClusterVariableResponse404 | DeleteTenantClusterVariableResponse500]

#### *async* delete_tenant_cluster_variable_async(tenant_id: str, name: str, \*\*kwargs: Any) → Any

Delete a tenant-scoped cluster variable

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **name** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteTenantClusterVariableResponse400 | DeleteTenantClusterVariableResponse401 | DeleteTenantClusterVariableResponse403 | DeleteTenantClusterVariableResponse404 | DeleteTenantClusterVariableResponse500]

#### delete_user(username: str, \*\*kwargs: Any) → Any

Delete user

> Deletes a user.
* **Parameters:**
  **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteUserResponse400 | DeleteUserResponse404 | DeleteUserResponse500 | DeleteUserResponse503]

#### *async* delete_user_async(username: str, \*\*kwargs: Any) → Any

Delete user

> Deletes a user.
* **Parameters:**
  **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | DeleteUserResponse400 | DeleteUserResponse404 | DeleteUserResponse500 | DeleteUserResponse503]

#### deploy_resources_from_files(files: list[str | Path], tenant_id: str | None = None) → ExtendedDeploymentResult

#### *async* deploy_resources_from_files_async(files: list[str | Path], tenant_id: str | None = None) → ExtendedDeploymentResult

#### evaluate_conditionals(, data: EvaluateConditionalsData, \*\*kwargs: Any) → EvaluateConditionalsResponse200

Evaluate root level conditional start events

> Evaluates root-level conditional start events for process definitions.

If the evaluation is successful, it will return the keys of all created process instances, along
with their associated process definition key.
Multiple root-level conditional start events of the same process definition can trigger if their
conditions evaluate to true.

* **Parameters:**
  **body** (*EvaluateConditionalsData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[EvaluateConditionalsResponse200 | EvaluateConditionalsResponse400 | EvaluateConditionalsResponse403 | EvaluateConditionalsResponse404 | EvaluateConditionalsResponse500 | EvaluateConditionalsResponse503]

#### *async* evaluate_conditionals_async(, data: EvaluateConditionalsData, \*\*kwargs: Any) → EvaluateConditionalsResponse200

Evaluate root level conditional start events

> Evaluates root-level conditional start events for process definitions.

If the evaluation is successful, it will return the keys of all created process instances, along
with their associated process definition key.
Multiple root-level conditional start events of the same process definition can trigger if their
conditions evaluate to true.

* **Parameters:**
  **body** (*EvaluateConditionalsData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[EvaluateConditionalsResponse200 | EvaluateConditionalsResponse400 | EvaluateConditionalsResponse403 | EvaluateConditionalsResponse404 | EvaluateConditionalsResponse500 | EvaluateConditionalsResponse503]

#### evaluate_decision(, data: DecisionevaluationbyID | Decisionevaluationbykey, \*\*kwargs: Any) → Any

Evaluate decision

> Evaluates a decision.

You specify the decision to evaluate either by using its unique key (as returned by
DeployResource), or using the decision ID. When using the decision ID, the latest deployed
version of the decision is used.

* **Parameters:**
  **body** (*DecisionevaluationbyID* *|* *Decisionevaluationbykey*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | EvaluateDecisionResponse200 | EvaluateDecisionResponse400 | EvaluateDecisionResponse500 | EvaluateDecisionResponse503]

#### *async* evaluate_decision_async(, data: DecisionevaluationbyID | Decisionevaluationbykey, \*\*kwargs: Any) → Any

Evaluate decision

> Evaluates a decision.

You specify the decision to evaluate either by using its unique key (as returned by
DeployResource), or using the decision ID. When using the decision ID, the latest deployed
version of the decision is used.

* **Parameters:**
  **body** (*DecisionevaluationbyID* *|* *Decisionevaluationbykey*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | EvaluateDecisionResponse200 | EvaluateDecisionResponse400 | EvaluateDecisionResponse500 | EvaluateDecisionResponse503]

#### evaluate_expression(, data: EvaluateExpressionData, \*\*kwargs: Any) → EvaluateExpressionResponse200

Evaluate an expression

> Evaluates a FEEL expression and returns the result. Supports references to tenant scoped cluster

variables when a tenant ID is provided.

* **Parameters:**
  **body** (*EvaluateExpressionData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[EvaluateExpressionResponse200 | EvaluateExpressionResponse400 | EvaluateExpressionResponse401 | EvaluateExpressionResponse403 | EvaluateExpressionResponse500]

#### *async* evaluate_expression_async(, data: EvaluateExpressionData, \*\*kwargs: Any) → EvaluateExpressionResponse200

Evaluate an expression

> Evaluates a FEEL expression and returns the result. Supports references to tenant scoped cluster

variables when a tenant ID is provided.

* **Parameters:**
  **body** (*EvaluateExpressionData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[EvaluateExpressionResponse200 | EvaluateExpressionResponse400 | EvaluateExpressionResponse401 | EvaluateExpressionResponse403 | EvaluateExpressionResponse500]

#### fail_job(job_key: str, \*, data: FailJobData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Fail job

> Mark the job as failed.
* **Parameters:**
  * **job_key** (*str*) – System-generated key for a job. Example: 2251799813653498.
  * **body** (*FailJobData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | FailJobResponse400 | FailJobResponse404 | FailJobResponse409 | FailJobResponse500 | FailJobResponse503]

#### *async* fail_job_async(job_key: str, \*, data: FailJobData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Fail job

> Mark the job as failed.
* **Parameters:**
  * **job_key** (*str*) – System-generated key for a job. Example: 2251799813653498.
  * **body** (*FailJobData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | FailJobResponse400 | FailJobResponse404 | FailJobResponse409 | FailJobResponse500 | FailJobResponse503]

#### get_audit_log(audit_log_key: str, \*\*kwargs: Any) → GetAuditLogResponse200

Get audit log

> Get an audit log entry by auditLogKey.
* **Parameters:**
  **audit_log_key** (*str*) – System-generated key for an audit log entry. Example:
  22517998136843567.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetAuditLogResponse200 | GetAuditLogResponse401 | GetAuditLogResponse403 | GetAuditLogResponse404 | GetAuditLogResponse500]

#### *async* get_audit_log_async(audit_log_key: str, \*\*kwargs: Any) → GetAuditLogResponse200

Get audit log

> Get an audit log entry by auditLogKey.
* **Parameters:**
  **audit_log_key** (*str*) – System-generated key for an audit log entry. Example:
  22517998136843567.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetAuditLogResponse200 | GetAuditLogResponse401 | GetAuditLogResponse403 | GetAuditLogResponse404 | GetAuditLogResponse500]

#### get_authentication(\*\*kwargs: Any) → GetAuthenticationResponse200

Get current user

> Retrieves the current authenticated user.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetAuthenticationResponse200 | GetAuthenticationResponse401 | GetAuthenticationResponse403 | GetAuthenticationResponse500]

#### *async* get_authentication_async(\*\*kwargs: Any) → GetAuthenticationResponse200

Get current user

> Retrieves the current authenticated user.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetAuthenticationResponse200 | GetAuthenticationResponse401 | GetAuthenticationResponse403 | GetAuthenticationResponse500]

#### get_authorization(authorization_key: str, \*\*kwargs: Any) → GetAuthorizationResponse200

Get authorization

> Get authorization by the given key.
* **Parameters:**
  **authorization_key** (*str*) – System-generated key for an authorization. Example:
  2251799813684332.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetAuthorizationResponse200 | GetAuthorizationResponse401 | GetAuthorizationResponse403 | GetAuthorizationResponse404 | GetAuthorizationResponse500]

#### *async* get_authorization_async(authorization_key: str, \*\*kwargs: Any) → GetAuthorizationResponse200

Get authorization

> Get authorization by the given key.
* **Parameters:**
  **authorization_key** (*str*) – System-generated key for an authorization. Example:
  2251799813684332.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetAuthorizationResponse200 | GetAuthorizationResponse401 | GetAuthorizationResponse403 | GetAuthorizationResponse404 | GetAuthorizationResponse500]

#### get_batch_operation(batch_operation_key: str, \*\*kwargs: Any) → GetBatchOperationResponse200

Get batch operation

> Get batch operation by key.
* **Parameters:**
  **batch_operation_key** (*str*) – System-generated key for an batch operation. Example:
  2251799813684321.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetBatchOperationResponse200 | GetBatchOperationResponse400 | GetBatchOperationResponse404 | GetBatchOperationResponse500]

#### *async* get_batch_operation_async(batch_operation_key: str, \*\*kwargs: Any) → GetBatchOperationResponse200

Get batch operation

> Get batch operation by key.
* **Parameters:**
  **batch_operation_key** (*str*) – System-generated key for an batch operation. Example:
  2251799813684321.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetBatchOperationResponse200 | GetBatchOperationResponse400 | GetBatchOperationResponse404 | GetBatchOperationResponse500]

#### get_decision_definition(decision_definition_key: str, \*\*kwargs: Any) → GetDecisionDefinitionResponse200

Get decision definition

> Returns a decision definition by key.
* **Parameters:**
  **decision_definition_key** (*str*) – System-generated key for a decision definition. Example:
  2251799813326547.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionDefinitionResponse200 | GetDecisionDefinitionResponse400 | GetDecisionDefinitionResponse401 | GetDecisionDefinitionResponse403 | GetDecisionDefinitionResponse404 | GetDecisionDefinitionResponse500]

#### *async* get_decision_definition_async(decision_definition_key: str, \*\*kwargs: Any) → GetDecisionDefinitionResponse200

Get decision definition

> Returns a decision definition by key.
* **Parameters:**
  **decision_definition_key** (*str*) – System-generated key for a decision definition. Example:
  2251799813326547.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionDefinitionResponse200 | GetDecisionDefinitionResponse400 | GetDecisionDefinitionResponse401 | GetDecisionDefinitionResponse403 | GetDecisionDefinitionResponse404 | GetDecisionDefinitionResponse500]

#### get_decision_definition_xml(decision_definition_key: str, \*\*kwargs: Any) → GetDecisionDefinitionXMLResponse400

Get decision definition XML

> Returns decision definition as XML.
* **Parameters:**
  **decision_definition_key** (*str*) – System-generated key for a decision definition. Example:
  2251799813326547.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionDefinitionXMLResponse400 | GetDecisionDefinitionXMLResponse401 | GetDecisionDefinitionXMLResponse403 | GetDecisionDefinitionXMLResponse404 | GetDecisionDefinitionXMLResponse500 | str]

#### *async* get_decision_definition_xml_async(decision_definition_key: str, \*\*kwargs: Any) → GetDecisionDefinitionXMLResponse400

Get decision definition XML

> Returns decision definition as XML.
* **Parameters:**
  **decision_definition_key** (*str*) – System-generated key for a decision definition. Example:
  2251799813326547.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionDefinitionXMLResponse400 | GetDecisionDefinitionXMLResponse401 | GetDecisionDefinitionXMLResponse403 | GetDecisionDefinitionXMLResponse404 | GetDecisionDefinitionXMLResponse500 | str]

#### get_decision_instance(decision_evaluation_instance_key: str, \*\*kwargs: Any) → GetDecisionInstanceResponse200

Get decision instance

> Returns a decision instance.
* **Parameters:**
  **decision_evaluation_instance_key** (*str*) – System-generated key for a deployed decision
  instance. Example: 22517998136843567.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionInstanceResponse200 | GetDecisionInstanceResponse400 | GetDecisionInstanceResponse401 | GetDecisionInstanceResponse403 | GetDecisionInstanceResponse404 | GetDecisionInstanceResponse500]

#### *async* get_decision_instance_async(decision_evaluation_instance_key: str, \*\*kwargs: Any) → GetDecisionInstanceResponse200

Get decision instance

> Returns a decision instance.
* **Parameters:**
  **decision_evaluation_instance_key** (*str*) – System-generated key for a deployed decision
  instance. Example: 22517998136843567.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionInstanceResponse200 | GetDecisionInstanceResponse400 | GetDecisionInstanceResponse401 | GetDecisionInstanceResponse403 | GetDecisionInstanceResponse404 | GetDecisionInstanceResponse500]

#### get_decision_requirements(decision_requirements_key: str, \*\*kwargs: Any) → GetDecisionRequirementsResponse200

Get decision requirements

> Returns Decision Requirements as JSON.
* **Parameters:**
  **decision_requirements_key** (*str*) – System-generated key for a deployed decision requirements
  definition. Example: 2251799813683346.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionRequirementsResponse200 | GetDecisionRequirementsResponse400 | GetDecisionRequirementsResponse401 | GetDecisionRequirementsResponse403 | GetDecisionRequirementsResponse404 | GetDecisionRequirementsResponse500]

#### *async* get_decision_requirements_async(decision_requirements_key: str, \*\*kwargs: Any) → GetDecisionRequirementsResponse200

Get decision requirements

> Returns Decision Requirements as JSON.
* **Parameters:**
  **decision_requirements_key** (*str*) – System-generated key for a deployed decision requirements
  definition. Example: 2251799813683346.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionRequirementsResponse200 | GetDecisionRequirementsResponse400 | GetDecisionRequirementsResponse401 | GetDecisionRequirementsResponse403 | GetDecisionRequirementsResponse404 | GetDecisionRequirementsResponse500]

#### get_decision_requirements_xml(decision_requirements_key: str, \*\*kwargs: Any) → GetDecisionRequirementsXMLResponse400

Get decision requirements XML

> Returns decision requirements as XML.
* **Parameters:**
  **decision_requirements_key** (*str*) – System-generated key for a deployed decision requirements
  definition. Example: 2251799813683346.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionRequirementsXMLResponse400 | GetDecisionRequirementsXMLResponse401 | GetDecisionRequirementsXMLResponse403 | GetDecisionRequirementsXMLResponse404 | GetDecisionRequirementsXMLResponse500 | str]

#### *async* get_decision_requirements_xml_async(decision_requirements_key: str, \*\*kwargs: Any) → GetDecisionRequirementsXMLResponse400

Get decision requirements XML

> Returns decision requirements as XML.
* **Parameters:**
  **decision_requirements_key** (*str*) – System-generated key for a deployed decision requirements
  definition. Example: 2251799813683346.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetDecisionRequirementsXMLResponse400 | GetDecisionRequirementsXMLResponse401 | GetDecisionRequirementsXMLResponse403 | GetDecisionRequirementsXMLResponse404 | GetDecisionRequirementsXMLResponse500 | str]

#### get_document(document_id: str, \*, store_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, content_hash: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → File

Download document

> Download a document from the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

* **Parameters:**
  * **document_id** (*str*) – Document Id that uniquely identifies a document.
  * **store_id** (*str* *|* *Unset*)
  * **content_hash** (*str* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[File | GetDocumentResponse404 | GetDocumentResponse500]

#### *async* get_document_async(document_id: str, \*, store_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, content_hash: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → File

Download document

> Download a document from the Camunda 8 cluster.

Note that this is currently supported for document stores of type: AWS, GCP, in-memory (non-
production), local (non-production)

* **Parameters:**
  * **document_id** (*str*) – Document Id that uniquely identifies a document.
  * **store_id** (*str* *|* *Unset*)
  * **content_hash** (*str* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[File | GetDocumentResponse404 | GetDocumentResponse500]

#### get_element_instance(element_instance_key: str, \*\*kwargs: Any) → GetElementInstanceResponse200

Get element instance

> Returns element instance as JSON.
* **Parameters:**
  **element_instance_key** (*str*) – System-generated key for a element instance. Example:
  2251799813686789.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetElementInstanceResponse200 | GetElementInstanceResponse400 | GetElementInstanceResponse401 | GetElementInstanceResponse403 | GetElementInstanceResponse404 | GetElementInstanceResponse500]

#### *async* get_element_instance_async(element_instance_key: str, \*\*kwargs: Any) → GetElementInstanceResponse200

Get element instance

> Returns element instance as JSON.
* **Parameters:**
  **element_instance_key** (*str*) – System-generated key for a element instance. Example:
  2251799813686789.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetElementInstanceResponse200 | GetElementInstanceResponse400 | GetElementInstanceResponse401 | GetElementInstanceResponse403 | GetElementInstanceResponse404 | GetElementInstanceResponse500]

#### get_global_cluster_variable(name: str, \*\*kwargs: Any) → GetGlobalClusterVariableResponse200

Get a global-scoped cluster variable

* **Parameters:**
  **name** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetGlobalClusterVariableResponse200 | GetGlobalClusterVariableResponse400 | GetGlobalClusterVariableResponse401 | GetGlobalClusterVariableResponse403 | GetGlobalClusterVariableResponse404 | GetGlobalClusterVariableResponse500]

#### *async* get_global_cluster_variable_async(name: str, \*\*kwargs: Any) → GetGlobalClusterVariableResponse200

Get a global-scoped cluster variable

* **Parameters:**
  **name** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetGlobalClusterVariableResponse200 | GetGlobalClusterVariableResponse400 | GetGlobalClusterVariableResponse401 | GetGlobalClusterVariableResponse403 | GetGlobalClusterVariableResponse404 | GetGlobalClusterVariableResponse500]

#### get_group(group_id: str, \*\*kwargs: Any) → GetGroupResponse200

Get group

> Get a group by its ID.
* **Parameters:**
  **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetGroupResponse200 | GetGroupResponse401 | GetGroupResponse403 | GetGroupResponse404 | GetGroupResponse500]

#### *async* get_group_async(group_id: str, \*\*kwargs: Any) → GetGroupResponse200

Get group

> Get a group by its ID.
* **Parameters:**
  **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetGroupResponse200 | GetGroupResponse401 | GetGroupResponse403 | GetGroupResponse404 | GetGroupResponse500]

#### get_incident(incident_key: str, \*\*kwargs: Any) → GetIncidentResponse200

Get incident

> Returns incident as JSON.
* **Parameters:**
  **incident_key** (*str*) – System-generated key for a incident. Example: 2251799813689432.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetIncidentResponse200 | GetIncidentResponse400 | GetIncidentResponse401 | GetIncidentResponse403 | GetIncidentResponse404 | GetIncidentResponse500]

#### *async* get_incident_async(incident_key: str, \*\*kwargs: Any) → GetIncidentResponse200

Get incident

> Returns incident as JSON.
* **Parameters:**
  **incident_key** (*str*) – System-generated key for a incident. Example: 2251799813689432.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetIncidentResponse200 | GetIncidentResponse400 | GetIncidentResponse401 | GetIncidentResponse403 | GetIncidentResponse404 | GetIncidentResponse500]

#### get_license(\*\*kwargs: Any) → GetLicenseResponse200

Get license status

> Obtains the status of the current Camunda license.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetLicenseResponse200 | GetLicenseResponse500]

#### *async* get_license_async(\*\*kwargs: Any) → GetLicenseResponse200

Get license status

> Obtains the status of the current Camunda license.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetLicenseResponse200 | GetLicenseResponse500]

#### get_mapping_rule(mapping_rule_id: str, \*\*kwargs: Any) → GetMappingRuleResponse200

Get a mapping rule

> Gets the mapping rule with the given ID.
* **Parameters:**
  **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetMappingRuleResponse200 | GetMappingRuleResponse401 | GetMappingRuleResponse404 | GetMappingRuleResponse500]

#### *async* get_mapping_rule_async(mapping_rule_id: str, \*\*kwargs: Any) → GetMappingRuleResponse200

Get a mapping rule

> Gets the mapping rule with the given ID.
* **Parameters:**
  **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetMappingRuleResponse200 | GetMappingRuleResponse401 | GetMappingRuleResponse404 | GetMappingRuleResponse500]

#### get_process_definition(process_definition_key: str, \*\*kwargs: Any) → GetProcessDefinitionResponse200

Get process definition

> Returns process definition as JSON.
* **Parameters:**
  **process_definition_key** (*str*) – System-generated key for a deployed process definition.
  Example: 2251799813686749.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionResponse200 | GetProcessDefinitionResponse400 | GetProcessDefinitionResponse401 | GetProcessDefinitionResponse403 | GetProcessDefinitionResponse404 | GetProcessDefinitionResponse500]

#### *async* get_process_definition_async(process_definition_key: str, \*\*kwargs: Any) → GetProcessDefinitionResponse200

Get process definition

> Returns process definition as JSON.
* **Parameters:**
  **process_definition_key** (*str*) – System-generated key for a deployed process definition.
  Example: 2251799813686749.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionResponse200 | GetProcessDefinitionResponse400 | GetProcessDefinitionResponse401 | GetProcessDefinitionResponse403 | GetProcessDefinitionResponse404 | GetProcessDefinitionResponse500]

#### get_process_definition_instance_statistics(\*, data: GetProcessDefinitionInstanceStatisticsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessDefinitionInstanceStatisticsResponse200

Get process instance statistics

> Get statistics about process instances, grouped by process definition and tenant.
* **Parameters:**
  **body** (*GetProcessDefinitionInstanceStatisticsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionInstanceStatisticsResponse200 | GetProcessDefinitionInstanceStatisticsResponse400 | GetProcessDefinitionInstanceStatisticsResponse401 | GetProcessDefinitionInstanceStatisticsResponse403 | GetProcessDefinitionInstanceStatisticsResponse500]

#### *async* get_process_definition_instance_statistics_async(\*, data: GetProcessDefinitionInstanceStatisticsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessDefinitionInstanceStatisticsResponse200

Get process instance statistics

> Get statistics about process instances, grouped by process definition and tenant.
* **Parameters:**
  **body** (*GetProcessDefinitionInstanceStatisticsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionInstanceStatisticsResponse200 | GetProcessDefinitionInstanceStatisticsResponse400 | GetProcessDefinitionInstanceStatisticsResponse401 | GetProcessDefinitionInstanceStatisticsResponse403 | GetProcessDefinitionInstanceStatisticsResponse500]

#### get_process_definition_instance_version_statistics(process_definition_id: str, \*, data: GetProcessDefinitionInstanceVersionStatisticsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessDefinitionInstanceVersionStatisticsResponse200

Get process instance statistics by version

> Get statistics about process instances, grouped by version for a given process definition.
* **Parameters:**
  * **process_definition_id** (*str*) – Id of a process definition, from the model. Only ids of
    process definitions that are deployed are useful. Example: new-account-onboarding-
    workflow.
  * **body** (*GetProcessDefinitionInstanceVersionStatisticsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionInstanceVersionStatisticsResponse200 | GetProcessDefinitionInstanceVersionStatisticsResponse400 | GetProcessDefinitionInstanceVersionStatisticsResponse401 | GetProcessDefinitionInstanceVersionStatisticsResponse403 | GetProcessDefinitionInstanceVersionStatisticsResponse500]

#### *async* get_process_definition_instance_version_statistics_async(process_definition_id: str, \*, data: GetProcessDefinitionInstanceVersionStatisticsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessDefinitionInstanceVersionStatisticsResponse200

Get process instance statistics by version

> Get statistics about process instances, grouped by version for a given process definition.
* **Parameters:**
  * **process_definition_id** (*str*) – Id of a process definition, from the model. Only ids of
    process definitions that are deployed are useful. Example: new-account-onboarding-
    workflow.
  * **body** (*GetProcessDefinitionInstanceVersionStatisticsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionInstanceVersionStatisticsResponse200 | GetProcessDefinitionInstanceVersionStatisticsResponse400 | GetProcessDefinitionInstanceVersionStatisticsResponse401 | GetProcessDefinitionInstanceVersionStatisticsResponse403 | GetProcessDefinitionInstanceVersionStatisticsResponse500]

#### get_process_definition_message_subscription_statistics(\*, data: GetProcessDefinitionMessageSubscriptionStatisticsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessDefinitionMessageSubscriptionStatisticsResponse200

Get message subscription statistics

> Get message subscription statistics, grouped by process definition.
* **Parameters:**
  **body** (*GetProcessDefinitionMessageSubscriptionStatisticsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionMessageSubscriptionStatisticsResponse200 | GetProcessDefinitionMessageSubscriptionStatisticsResponse400 | GetProcessDefinitionMessageSubscriptionStatisticsResponse401 | GetProcessDefinitionMessageSubscriptionStatisticsResponse403 | GetProcessDefinitionMessageSubscriptionStatisticsResponse500]

#### *async* get_process_definition_message_subscription_statistics_async(\*, data: GetProcessDefinitionMessageSubscriptionStatisticsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessDefinitionMessageSubscriptionStatisticsResponse200

Get message subscription statistics

> Get message subscription statistics, grouped by process definition.
* **Parameters:**
  **body** (*GetProcessDefinitionMessageSubscriptionStatisticsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionMessageSubscriptionStatisticsResponse200 | GetProcessDefinitionMessageSubscriptionStatisticsResponse400 | GetProcessDefinitionMessageSubscriptionStatisticsResponse401 | GetProcessDefinitionMessageSubscriptionStatisticsResponse403 | GetProcessDefinitionMessageSubscriptionStatisticsResponse500]

#### get_process_definition_statistics(process_definition_key: str, \*, data: GetProcessDefinitionStatisticsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessDefinitionStatisticsResponse200

Get process definition statistics

> Get statistics about elements in currently running process instances by process definition key and

search filter.

* **Parameters:**
  * **process_definition_key** (*str*) – System-generated key for a deployed process definition.
    Example: 2251799813686749.
  * **body** (*GetProcessDefinitionStatisticsData* *|* *Unset*) – Process definition element statistics
    request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionStatisticsResponse200 | GetProcessDefinitionStatisticsResponse400 | GetProcessDefinitionStatisticsResponse401 | GetProcessDefinitionStatisticsResponse403 | GetProcessDefinitionStatisticsResponse500]

#### *async* get_process_definition_statistics_async(process_definition_key: str, \*, data: GetProcessDefinitionStatisticsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessDefinitionStatisticsResponse200

Get process definition statistics

> Get statistics about elements in currently running process instances by process definition key and

search filter.

* **Parameters:**
  * **process_definition_key** (*str*) – System-generated key for a deployed process definition.
    Example: 2251799813686749.
  * **body** (*GetProcessDefinitionStatisticsData* *|* *Unset*) – Process definition element statistics
    request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionStatisticsResponse200 | GetProcessDefinitionStatisticsResponse400 | GetProcessDefinitionStatisticsResponse401 | GetProcessDefinitionStatisticsResponse403 | GetProcessDefinitionStatisticsResponse500]

#### get_process_definition_xml(process_definition_key: str, \*\*kwargs: Any) → GetProcessDefinitionXMLResponse400

Get process definition XML

> Returns process definition as XML.
* **Parameters:**
  **process_definition_key** (*str*) – System-generated key for a deployed process definition.
  Example: 2251799813686749.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionXMLResponse400 | GetProcessDefinitionXMLResponse401 | GetProcessDefinitionXMLResponse403 | GetProcessDefinitionXMLResponse404 | GetProcessDefinitionXMLResponse500 | str]

#### *async* get_process_definition_xml_async(process_definition_key: str, \*\*kwargs: Any) → GetProcessDefinitionXMLResponse400

Get process definition XML

> Returns process definition as XML.
* **Parameters:**
  **process_definition_key** (*str*) – System-generated key for a deployed process definition.
  Example: 2251799813686749.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessDefinitionXMLResponse400 | GetProcessDefinitionXMLResponse401 | GetProcessDefinitionXMLResponse403 | GetProcessDefinitionXMLResponse404 | GetProcessDefinitionXMLResponse500 | str]

#### get_process_instance(process_instance_key: str, \*\*kwargs: Any) → GetProcessInstanceResponse200

Get process instance

> Get the process instance by the process instance key.
* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceResponse200 | GetProcessInstanceResponse400 | GetProcessInstanceResponse401 | GetProcessInstanceResponse403 | GetProcessInstanceResponse404 | GetProcessInstanceResponse500]

#### *async* get_process_instance_async(process_instance_key: str, \*\*kwargs: Any) → GetProcessInstanceResponse200

Get process instance

> Get the process instance by the process instance key.
* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceResponse200 | GetProcessInstanceResponse400 | GetProcessInstanceResponse401 | GetProcessInstanceResponse403 | GetProcessInstanceResponse404 | GetProcessInstanceResponse500]

#### get_process_instance_call_hierarchy(process_instance_key: str, \*\*kwargs: Any) → GetProcessInstanceCallHierarchyResponse400

Get call hierarchy

> Returns the call hierarchy for a given process instance, showing its ancestry up to the root

instance.

* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceCallHierarchyResponse400 | GetProcessInstanceCallHierarchyResponse401 | GetProcessInstanceCallHierarchyResponse403 | GetProcessInstanceCallHierarchyResponse404 | GetProcessInstanceCallHierarchyResponse500 | list[GetProcessInstanceCallHierarchyResponse200Item]]

#### *async* get_process_instance_call_hierarchy_async(process_instance_key: str, \*\*kwargs: Any) → GetProcessInstanceCallHierarchyResponse400

Get call hierarchy

> Returns the call hierarchy for a given process instance, showing its ancestry up to the root

instance.

* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceCallHierarchyResponse400 | GetProcessInstanceCallHierarchyResponse401 | GetProcessInstanceCallHierarchyResponse403 | GetProcessInstanceCallHierarchyResponse404 | GetProcessInstanceCallHierarchyResponse500 | list[GetProcessInstanceCallHierarchyResponse200Item]]

#### get_process_instance_sequence_flows(process_instance_key: str, \*\*kwargs: Any) → GetProcessInstanceSequenceFlowsResponse200

Get sequence flows

> Get sequence flows taken by the process instance.
* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceSequenceFlowsResponse200 | GetProcessInstanceSequenceFlowsResponse400 | GetProcessInstanceSequenceFlowsResponse401 | GetProcessInstanceSequenceFlowsResponse403 | GetProcessInstanceSequenceFlowsResponse500]

#### *async* get_process_instance_sequence_flows_async(process_instance_key: str, \*\*kwargs: Any) → GetProcessInstanceSequenceFlowsResponse200

Get sequence flows

> Get sequence flows taken by the process instance.
* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceSequenceFlowsResponse200 | GetProcessInstanceSequenceFlowsResponse400 | GetProcessInstanceSequenceFlowsResponse401 | GetProcessInstanceSequenceFlowsResponse403 | GetProcessInstanceSequenceFlowsResponse500]

#### get_process_instance_statistics(process_instance_key: str, \*\*kwargs: Any) → GetProcessInstanceStatisticsResponse200

Get element instance statistics

> Get statistics about elements by the process instance key.
* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceStatisticsResponse200 | GetProcessInstanceStatisticsResponse400 | GetProcessInstanceStatisticsResponse401 | GetProcessInstanceStatisticsResponse403 | GetProcessInstanceStatisticsResponse500]

#### *async* get_process_instance_statistics_async(process_instance_key: str, \*\*kwargs: Any) → GetProcessInstanceStatisticsResponse200

Get element instance statistics

> Get statistics about elements by the process instance key.
* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceStatisticsResponse200 | GetProcessInstanceStatisticsResponse400 | GetProcessInstanceStatisticsResponse401 | GetProcessInstanceStatisticsResponse403 | GetProcessInstanceStatisticsResponse500]

#### get_process_instance_statistics_by_definition(, data: GetProcessInstanceStatisticsByDefinitionData, \*\*kwargs: Any) → GetProcessInstanceStatisticsByDefinitionResponse200

Get process instance statistics by definition

> Returns statistics for active process instances with incidents, grouped by process

definition. The result set is scoped to a specific incident error hash code, which must be
provided as a filter in the request body.

* **Parameters:**
  **body** (*GetProcessInstanceStatisticsByDefinitionData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceStatisticsByDefinitionResponse200 | GetProcessInstanceStatisticsByDefinitionResponse400 | GetProcessInstanceStatisticsByDefinitionResponse401 | GetProcessInstanceStatisticsByDefinitionResponse403 | GetProcessInstanceStatisticsByDefinitionResponse500]

#### *async* get_process_instance_statistics_by_definition_async(, data: GetProcessInstanceStatisticsByDefinitionData, \*\*kwargs: Any) → GetProcessInstanceStatisticsByDefinitionResponse200

Get process instance statistics by definition

> Returns statistics for active process instances with incidents, grouped by process

definition. The result set is scoped to a specific incident error hash code, which must be
provided as a filter in the request body.

* **Parameters:**
  **body** (*GetProcessInstanceStatisticsByDefinitionData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceStatisticsByDefinitionResponse200 | GetProcessInstanceStatisticsByDefinitionResponse400 | GetProcessInstanceStatisticsByDefinitionResponse401 | GetProcessInstanceStatisticsByDefinitionResponse403 | GetProcessInstanceStatisticsByDefinitionResponse500]

#### get_process_instance_statistics_by_error(\*, data: GetProcessInstanceStatisticsByErrorData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessInstanceStatisticsByErrorResponse200

Get process instance statistics by error

> Returns statistics for active process instances that currently have active incidents,

grouped by incident error hash code.

* **Parameters:**
  **body** (*GetProcessInstanceStatisticsByErrorData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceStatisticsByErrorResponse200 | GetProcessInstanceStatisticsByErrorResponse400 | GetProcessInstanceStatisticsByErrorResponse401 | GetProcessInstanceStatisticsByErrorResponse403 | GetProcessInstanceStatisticsByErrorResponse500]

#### *async* get_process_instance_statistics_by_error_async(\*, data: GetProcessInstanceStatisticsByErrorData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → GetProcessInstanceStatisticsByErrorResponse200

Get process instance statistics by error

> Returns statistics for active process instances that currently have active incidents,

grouped by incident error hash code.

* **Parameters:**
  **body** (*GetProcessInstanceStatisticsByErrorData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetProcessInstanceStatisticsByErrorResponse200 | GetProcessInstanceStatisticsByErrorResponse400 | GetProcessInstanceStatisticsByErrorResponse401 | GetProcessInstanceStatisticsByErrorResponse403 | GetProcessInstanceStatisticsByErrorResponse500]

#### get_resource(resource_key: str, \*\*kwargs: Any) → GetResourceResponse200

Get resource

> Returns a deployed resource.

:::info
Currently, this endpoint only supports RPA resources.
:::
* **resource_key**: The system-assigned key for this resource.

* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetResourceResponse200 | GetResourceResponse404 | GetResourceResponse500]

#### *async* get_resource_async(resource_key: str, \*\*kwargs: Any) → GetResourceResponse200

Get resource

> Returns a deployed resource.

:::info
Currently, this endpoint only supports RPA resources.
:::
* **resource_key**: The system-assigned key for this resource.

* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetResourceResponse200 | GetResourceResponse404 | GetResourceResponse500]

#### get_resource_content(resource_key: str, \*\*kwargs: Any) → File

Get resource content

> Returns the content of a deployed resource.

:::info
Currently, this endpoint only supports RPA resources.
:::
* **resource_key**: The system-assigned key for this resource.

* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[File | GetResourceContentResponse404 | GetResourceContentResponse500]

#### *async* get_resource_content_async(resource_key: str, \*\*kwargs: Any) → File

Get resource content

> Returns the content of a deployed resource.

:::info
Currently, this endpoint only supports RPA resources.
:::
* **resource_key**: The system-assigned key for this resource.

* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[File | GetResourceContentResponse404 | GetResourceContentResponse500]

#### get_role(role_id: str, \*\*kwargs: Any) → GetRoleResponse200

Get role

> Get a role by its ID.
* **Parameters:**
  **role_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetRoleResponse200 | GetRoleResponse401 | GetRoleResponse403 | GetRoleResponse404 | GetRoleResponse500]

#### *async* get_role_async(role_id: str, \*\*kwargs: Any) → GetRoleResponse200

Get role

> Get a role by its ID.
* **Parameters:**
  **role_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetRoleResponse200 | GetRoleResponse401 | GetRoleResponse403 | GetRoleResponse404 | GetRoleResponse500]

#### get_start_process_form(process_definition_key: str, \*\*kwargs: Any) → Any

Get process start form

> Get the start form of a process.

Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

* **Parameters:**
  **process_definition_key** (*str*) – System-generated key for a deployed process definition.
  Example: 2251799813686749.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | GetStartProcessFormResponse200 | GetStartProcessFormResponse400 | GetStartProcessFormResponse401 | GetStartProcessFormResponse403 | GetStartProcessFormResponse404 | GetStartProcessFormResponse500]

#### *async* get_start_process_form_async(process_definition_key: str, \*\*kwargs: Any) → Any

Get process start form

> Get the start form of a process.

Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

* **Parameters:**
  **process_definition_key** (*str*) – System-generated key for a deployed process definition.
  Example: 2251799813686749.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | GetStartProcessFormResponse200 | GetStartProcessFormResponse400 | GetStartProcessFormResponse401 | GetStartProcessFormResponse403 | GetStartProcessFormResponse404 | GetStartProcessFormResponse500]

#### get_tenant(tenant_id: str, \*\*kwargs: Any) → GetTenantResponse200

Get tenant

> Retrieves a single tenant by tenant ID.
* **Parameters:**
  **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetTenantResponse200 | GetTenantResponse400 | GetTenantResponse401 | GetTenantResponse403 | GetTenantResponse404 | GetTenantResponse500]

#### *async* get_tenant_async(tenant_id: str, \*\*kwargs: Any) → GetTenantResponse200

Get tenant

> Retrieves a single tenant by tenant ID.
* **Parameters:**
  **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetTenantResponse200 | GetTenantResponse400 | GetTenantResponse401 | GetTenantResponse403 | GetTenantResponse404 | GetTenantResponse500]

#### get_tenant_cluster_variable(tenant_id: str, name: str, \*\*kwargs: Any) → GetTenantClusterVariableResponse200

Get a tenant-scoped cluster variable

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **name** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetTenantClusterVariableResponse200 | GetTenantClusterVariableResponse400 | GetTenantClusterVariableResponse401 | GetTenantClusterVariableResponse403 | GetTenantClusterVariableResponse404 | GetTenantClusterVariableResponse500]

#### *async* get_tenant_cluster_variable_async(tenant_id: str, name: str, \*\*kwargs: Any) → GetTenantClusterVariableResponse200

Get a tenant-scoped cluster variable

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **name** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetTenantClusterVariableResponse200 | GetTenantClusterVariableResponse400 | GetTenantClusterVariableResponse401 | GetTenantClusterVariableResponse403 | GetTenantClusterVariableResponse404 | GetTenantClusterVariableResponse500]

#### get_topology(\*\*kwargs: Any) → GetTopologyResponse200

Get cluster topology

> Obtains the current topology of the cluster the gateway is part of.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetTopologyResponse200 | GetTopologyResponse401 | GetTopologyResponse500]

#### *async* get_topology_async(\*\*kwargs: Any) → GetTopologyResponse200

Get cluster topology

> Obtains the current topology of the cluster the gateway is part of.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetTopologyResponse200 | GetTopologyResponse401 | GetTopologyResponse500]

#### get_usage_metrics(\*, start_time: datetime.datetime, end_time: datetime.datetime, tenant_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, with_tenants: bool | Unset = False, \*\*kwargs: Any) → GetUsageMetricsResponse200

Get usage metrics

> Retrieve the usage metrics based on given criteria.
* **Parameters:**
  * **start_time** (*datetime.datetime*) – Example: 2025-06-07T13:14:15Z.
  * **end_time** (*datetime.datetime*) – Example: 2025-06-07T13:14:15Z.
  * **tenant_id** (*str* *|* *Unset*) – The unique identifier of the tenant. Example: customer-service.
  * **with_tenants** (*bool* *|* *Unset*) – Default: False.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetUsageMetricsResponse200 | GetUsageMetricsResponse400 | GetUsageMetricsResponse401 | GetUsageMetricsResponse403 | GetUsageMetricsResponse500]

#### *async* get_usage_metrics_async(\*, start_time: datetime.datetime, end_time: datetime.datetime, tenant_id: str | Unset = `<camunda_orchestration_sdk.types.Unset object>`, with_tenants: bool | Unset = False, \*\*kwargs: Any) → GetUsageMetricsResponse200

Get usage metrics

> Retrieve the usage metrics based on given criteria.
* **Parameters:**
  * **start_time** (*datetime.datetime*) – Example: 2025-06-07T13:14:15Z.
  * **end_time** (*datetime.datetime*) – Example: 2025-06-07T13:14:15Z.
  * **tenant_id** (*str* *|* *Unset*) – The unique identifier of the tenant. Example: customer-service.
  * **with_tenants** (*bool* *|* *Unset*) – Default: False.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetUsageMetricsResponse200 | GetUsageMetricsResponse400 | GetUsageMetricsResponse401 | GetUsageMetricsResponse403 | GetUsageMetricsResponse500]

#### get_user(username: str, \*\*kwargs: Any) → GetUserResponse200

Get user

> Get a user by its username.
* **Parameters:**
  **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetUserResponse200 | GetUserResponse401 | GetUserResponse403 | GetUserResponse404 | GetUserResponse500]

#### *async* get_user_async(username: str, \*\*kwargs: Any) → GetUserResponse200

Get user

> Get a user by its username.
* **Parameters:**
  **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetUserResponse200 | GetUserResponse401 | GetUserResponse403 | GetUserResponse404 | GetUserResponse500]

#### get_user_task(user_task_key: str, \*\*kwargs: Any) → GetUserTaskResponse200

Get user task

> Get the user task by the user task key.
* **Parameters:**
  **user_task_key** (*str*) – System-generated key for a user task.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetUserTaskResponse200 | GetUserTaskResponse400 | GetUserTaskResponse401 | GetUserTaskResponse403 | GetUserTaskResponse404 | GetUserTaskResponse500]

#### *async* get_user_task_async(user_task_key: str, \*\*kwargs: Any) → GetUserTaskResponse200

Get user task

> Get the user task by the user task key.
* **Parameters:**
  **user_task_key** (*str*) – System-generated key for a user task.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetUserTaskResponse200 | GetUserTaskResponse400 | GetUserTaskResponse401 | GetUserTaskResponse403 | GetUserTaskResponse404 | GetUserTaskResponse500]

#### get_user_task_form(user_task_key: str, \*\*kwargs: Any) → Any

Get user task form

> Get the form of a user task.

Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

* **Parameters:**
  **user_task_key** (*str*) – System-generated key for a user task.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | GetUserTaskFormResponse200 | GetUserTaskFormResponse400 | GetUserTaskFormResponse401 | GetUserTaskFormResponse403 | GetUserTaskFormResponse404 | GetUserTaskFormResponse500]

#### *async* get_user_task_form_async(user_task_key: str, \*\*kwargs: Any) → Any

Get user task form

> Get the form of a user task.

Note that this endpoint will only return linked forms. This endpoint does not support embedded
forms.

* **Parameters:**
  **user_task_key** (*str*) – System-generated key for a user task.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | GetUserTaskFormResponse200 | GetUserTaskFormResponse400 | GetUserTaskFormResponse401 | GetUserTaskFormResponse403 | GetUserTaskFormResponse404 | GetUserTaskFormResponse500]

#### get_variable(variable_key: str, \*\*kwargs: Any) → GetVariableResponse200

Get variable

> Get the variable by the variable key.
* **Parameters:**
  **variable_key** (*str*) – System-generated key for a variable. Example: 2251799813683287.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetVariableResponse200 | GetVariableResponse400 | GetVariableResponse401 | GetVariableResponse403 | GetVariableResponse404 | GetVariableResponse500]

#### *async* get_variable_async(variable_key: str, \*\*kwargs: Any) → GetVariableResponse200

Get variable

> Get the variable by the variable key.
* **Parameters:**
  **variable_key** (*str*) – System-generated key for a variable. Example: 2251799813683287.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[GetVariableResponse200 | GetVariableResponse400 | GetVariableResponse401 | GetVariableResponse403 | GetVariableResponse404 | GetVariableResponse500]

#### migrate_process_instance(process_instance_key: str, , data: MigrateProcessInstanceData, \*\*kwargs: Any) → Any

Migrate process instance

> Migrates a process instance to a new process definition.

This request can contain multiple mapping instructions to define mapping between the active
process instance’s elements and target process definition elements.

Use this to upgrade a process instance to a new version of a process or to
a different process definition, e.g. to keep your running instances up-to-date with the
latest process improvements.

* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*MigrateProcessInstanceData*) – The migration instructions describe how to migrate a
    process instance from one process definition to another.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | MigrateProcessInstanceResponse400 | MigrateProcessInstanceResponse404 | MigrateProcessInstanceResponse409 | MigrateProcessInstanceResponse500 | MigrateProcessInstanceResponse503]

#### *async* migrate_process_instance_async(process_instance_key: str, , data: MigrateProcessInstanceData, \*\*kwargs: Any) → Any

Migrate process instance

> Migrates a process instance to a new process definition.

This request can contain multiple mapping instructions to define mapping between the active
process instance’s elements and target process definition elements.

Use this to upgrade a process instance to a new version of a process or to
a different process definition, e.g. to keep your running instances up-to-date with the
latest process improvements.

* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*MigrateProcessInstanceData*) – The migration instructions describe how to migrate a
    process instance from one process definition to another.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | MigrateProcessInstanceResponse400 | MigrateProcessInstanceResponse404 | MigrateProcessInstanceResponse409 | MigrateProcessInstanceResponse500 | MigrateProcessInstanceResponse503]

#### migrate_process_instances_batch_operation(, data: MigrateProcessInstancesBatchOperationData, \*\*kwargs: Any) → MigrateProcessInstancesBatchOperationResponse200

Migrate process instances (batch)

> Migrate multiple process instances.

Since only process instances with ACTIVE state can be migrated, any given
filters for state are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*MigrateProcessInstancesBatchOperationData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[MigrateProcessInstancesBatchOperationResponse200 | MigrateProcessInstancesBatchOperationResponse400 | MigrateProcessInstancesBatchOperationResponse401 | MigrateProcessInstancesBatchOperationResponse403 | MigrateProcessInstancesBatchOperationResponse500]

#### *async* migrate_process_instances_batch_operation_async(, data: MigrateProcessInstancesBatchOperationData, \*\*kwargs: Any) → MigrateProcessInstancesBatchOperationResponse200

Migrate process instances (batch)

> Migrate multiple process instances.

Since only process instances with ACTIVE state can be migrated, any given
filters for state are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*MigrateProcessInstancesBatchOperationData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[MigrateProcessInstancesBatchOperationResponse200 | MigrateProcessInstancesBatchOperationResponse400 | MigrateProcessInstancesBatchOperationResponse401 | MigrateProcessInstancesBatchOperationResponse403 | MigrateProcessInstancesBatchOperationResponse500]

#### modify_process_instance(process_instance_key: str, , data: ModifyProcessInstanceData, \*\*kwargs: Any) → Any

Modify process instance

> Modifies a running process instance.

This request can contain multiple instructions to activate an element of the process or
to terminate an active instance of an element.

Use this to repair a process instance that is stuck on an element or took an unintended path.
For example, because an external system is not available or doesn’t respond as expected.

* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*ModifyProcessInstanceData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ModifyProcessInstanceResponse400 | ModifyProcessInstanceResponse404 | ModifyProcessInstanceResponse500 | ModifyProcessInstanceResponse503]

#### *async* modify_process_instance_async(process_instance_key: str, , data: ModifyProcessInstanceData, \*\*kwargs: Any) → Any

Modify process instance

> Modifies a running process instance.

This request can contain multiple instructions to activate an element of the process or
to terminate an active instance of an element.

Use this to repair a process instance that is stuck on an element or took an unintended path.
For example, because an external system is not available or doesn’t respond as expected.

* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*ModifyProcessInstanceData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ModifyProcessInstanceResponse400 | ModifyProcessInstanceResponse404 | ModifyProcessInstanceResponse500 | ModifyProcessInstanceResponse503]

#### modify_process_instances_batch_operation(, data: ModifyProcessInstancesBatchOperationData, \*\*kwargs: Any) → ModifyProcessInstancesBatchOperationResponse200

Modify process instances (batch)

> Modify multiple process instances.

Since only process instances with ACTIVE state can be modified, any given
filters for state are ignored and overridden during this batch operation.
In contrast to single modification operation, it is not possible to add variable instructions or
modify by element key.
It is only possible to use the element id of the source and target.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*ModifyProcessInstancesBatchOperationData*) – The process instance filter to define on
  which process instances tokens should be moved,
  and new element instances should be activated or terminated.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ModifyProcessInstancesBatchOperationResponse200 | ModifyProcessInstancesBatchOperationResponse400 | ModifyProcessInstancesBatchOperationResponse401 | ModifyProcessInstancesBatchOperationResponse403 | ModifyProcessInstancesBatchOperationResponse500]

#### *async* modify_process_instances_batch_operation_async(, data: ModifyProcessInstancesBatchOperationData, \*\*kwargs: Any) → ModifyProcessInstancesBatchOperationResponse200

Modify process instances (batch)

> Modify multiple process instances.

Since only process instances with ACTIVE state can be modified, any given
filters for state are ignored and overridden during this batch operation.
In contrast to single modification operation, it is not possible to add variable instructions or
modify by element key.
It is only possible to use the element id of the source and target.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*ModifyProcessInstancesBatchOperationData*) – The process instance filter to define on
  which process instances tokens should be moved,
  and new element instances should be activated or terminated.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ModifyProcessInstancesBatchOperationResponse200 | ModifyProcessInstancesBatchOperationResponse400 | ModifyProcessInstancesBatchOperationResponse401 | ModifyProcessInstancesBatchOperationResponse403 | ModifyProcessInstancesBatchOperationResponse500]

#### pin_clock(, data: PinClockData, \*\*kwargs: Any) → Any

Pin internal clock (alpha)

> Set a precise, static time for the Zeebe engine’s internal clock.

When the clock is pinned, it remains at the specified time and does not advance.
To change the time, the clock must be pinned again with a new timestamp.

This endpoint is an alpha feature and may be subject to change
in future releases.

* **Parameters:**
  **body** (*PinClockData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | PinClockResponse400 | PinClockResponse500 | PinClockResponse503]

#### *async* pin_clock_async(, data: PinClockData, \*\*kwargs: Any) → Any

Pin internal clock (alpha)

> Set a precise, static time for the Zeebe engine’s internal clock.

When the clock is pinned, it remains at the specified time and does not advance.
To change the time, the clock must be pinned again with a new timestamp.

This endpoint is an alpha feature and may be subject to change
in future releases.

* **Parameters:**
  **body** (*PinClockData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | PinClockResponse400 | PinClockResponse500 | PinClockResponse503]

#### publish_message(, data: PublishMessageData, \*\*kwargs: Any) → PublishMessageResponse200

Publish message

> Publishes a single message.

Messages are published to specific partitions computed from their correlation keys.
Messages can be buffered.
The endpoint does not wait for a correlation result.
Use the message correlation endpoint for such use cases.

* **Parameters:**
  **body** (*PublishMessageData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[PublishMessageResponse200 | PublishMessageResponse400 | PublishMessageResponse500 | PublishMessageResponse503]

#### *async* publish_message_async(, data: PublishMessageData, \*\*kwargs: Any) → PublishMessageResponse200

Publish message

> Publishes a single message.

Messages are published to specific partitions computed from their correlation keys.
Messages can be buffered.
The endpoint does not wait for a correlation result.
Use the message correlation endpoint for such use cases.

* **Parameters:**
  **body** (*PublishMessageData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[PublishMessageResponse200 | PublishMessageResponse400 | PublishMessageResponse500 | PublishMessageResponse503]

#### reset_clock(\*\*kwargs: Any) → Any

Reset internal clock (alpha)

> Resets the Zeebe engine’s internal clock to the current system time, enabling it to tick in real-

time.
This operation is useful for returning the clock to
normal behavior after it has been pinned to a specific time.

This endpoint is an alpha feature and may be subject to change
in future releases.

* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ResetClockResponse500 | ResetClockResponse503]

#### *async* reset_clock_async(\*\*kwargs: Any) → Any

Reset internal clock (alpha)

> Resets the Zeebe engine’s internal clock to the current system time, enabling it to tick in real-

time.
This operation is useful for returning the clock to
normal behavior after it has been pinned to a specific time.

This endpoint is an alpha feature and may be subject to change
in future releases.

* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ResetClockResponse500 | ResetClockResponse503]

#### resolve_incident(incident_key: str, \*, data: ResolveIncidentData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Resolve incident

> Marks the incident as resolved; most likely a call to Update job will be necessary

to reset the job’s retries, followed by this call.

* **Parameters:**
  * **incident_key** (*str*) – System-generated key for a incident. Example: 2251799813689432.
  * **body** (*ResolveIncidentData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ResolveIncidentResponse400 | ResolveIncidentResponse404 | ResolveIncidentResponse500 | ResolveIncidentResponse503]

#### *async* resolve_incident_async(incident_key: str, \*, data: ResolveIncidentData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Resolve incident

> Marks the incident as resolved; most likely a call to Update job will be necessary

to reset the job’s retries, followed by this call.

* **Parameters:**
  * **incident_key** (*str*) – System-generated key for a incident. Example: 2251799813689432.
  * **body** (*ResolveIncidentData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ResolveIncidentResponse400 | ResolveIncidentResponse404 | ResolveIncidentResponse500 | ResolveIncidentResponse503]

#### resolve_incidents_batch_operation(\*, data: ResolveIncidentsBatchOperationData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → ResolveIncidentsBatchOperationResponse200

Resolve related incidents (batch)

> Resolves multiple instances of process instances.

Since only process instances with ACTIVE state can have unresolved incidents, any given
filters for state are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*ResolveIncidentsBatchOperationData* *|* *Unset*) – The process instance filter that
  defines which process instances should have their incidents resolved.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ResolveIncidentsBatchOperationResponse200 | ResolveIncidentsBatchOperationResponse400 | ResolveIncidentsBatchOperationResponse401 | ResolveIncidentsBatchOperationResponse403 | ResolveIncidentsBatchOperationResponse500]

#### *async* resolve_incidents_batch_operation_async(\*, data: ResolveIncidentsBatchOperationData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → ResolveIncidentsBatchOperationResponse200

Resolve related incidents (batch)

> Resolves multiple instances of process instances.

Since only process instances with ACTIVE state can have unresolved incidents, any given
filters for state are ignored and overridden during this batch operation.
This is done asynchronously, the progress can be tracked using the batchOperationKey from the
response and the batch operation status endpoint (/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  **body** (*ResolveIncidentsBatchOperationData* *|* *Unset*) – The process instance filter that
  defines which process instances should have their incidents resolved.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ResolveIncidentsBatchOperationResponse200 | ResolveIncidentsBatchOperationResponse400 | ResolveIncidentsBatchOperationResponse401 | ResolveIncidentsBatchOperationResponse403 | ResolveIncidentsBatchOperationResponse500]

#### resolve_process_instance_incidents(process_instance_key: str, \*\*kwargs: Any) → ResolveProcessInstanceIncidentsResponse200

Resolve related incidents

> Creates a batch operation to resolve multiple incidents of a process instance.
* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ResolveProcessInstanceIncidentsResponse200 | ResolveProcessInstanceIncidentsResponse400 | ResolveProcessInstanceIncidentsResponse401 | ResolveProcessInstanceIncidentsResponse404 | ResolveProcessInstanceIncidentsResponse500 | ResolveProcessInstanceIncidentsResponse503]

#### *async* resolve_process_instance_incidents_async(process_instance_key: str, \*\*kwargs: Any) → ResolveProcessInstanceIncidentsResponse200

Resolve related incidents

> Creates a batch operation to resolve multiple incidents of a process instance.
* **Parameters:**
  **process_instance_key** (*str*) – System-generated key for a process instance. Example:
  2251799813690746.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[ResolveProcessInstanceIncidentsResponse200 | ResolveProcessInstanceIncidentsResponse400 | ResolveProcessInstanceIncidentsResponse401 | ResolveProcessInstanceIncidentsResponse404 | ResolveProcessInstanceIncidentsResponse500 | ResolveProcessInstanceIncidentsResponse503]

#### resume_batch_operation(batch_operation_key: str, \*, data: ~typing.Any | ~camunda_orchestration_sdk.types.Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: ~typing.Any) → Any

Resume Batch operation

> Resumes a suspended batch operation.

This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  * **batch_operation_key** (*str*) – System-generated key for an batch operation. Example:
    2251799813684321.
  * **body** (*Any* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ResumeBatchOperationResponse400 | ResumeBatchOperationResponse403 | ResumeBatchOperationResponse404 | ResumeBatchOperationResponse500 | ResumeBatchOperationResponse503]

#### *async* resume_batch_operation_async(batch_operation_key: str, \*, data: ~typing.Any | ~camunda_orchestration_sdk.types.Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: ~typing.Any) → Any

Resume Batch operation

> Resumes a suspended batch operation.

This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  * **batch_operation_key** (*str*) – System-generated key for an batch operation. Example:
    2251799813684321.
  * **body** (*Any* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ResumeBatchOperationResponse400 | ResumeBatchOperationResponse403 | ResumeBatchOperationResponse404 | ResumeBatchOperationResponse500 | ResumeBatchOperationResponse503]

#### *async* run_workers()

#### search_audit_logs(\*, data: SearchAuditLogsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Search audit logs

> Search for audit logs based on given criteria.
* **Parameters:**
  **body** (*SearchAuditLogsData* *|* *Unset*) – Audit log search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SearchAuditLogsResponse200 | SearchAuditLogsResponse400 | SearchAuditLogsResponse401 | SearchAuditLogsResponse403]

#### *async* search_audit_logs_async(\*, data: SearchAuditLogsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Search audit logs

> Search for audit logs based on given criteria.
* **Parameters:**
  **body** (*SearchAuditLogsData* *|* *Unset*) – Audit log search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SearchAuditLogsResponse200 | SearchAuditLogsResponse400 | SearchAuditLogsResponse401 | SearchAuditLogsResponse403]

#### search_authorizations(\*, data: SearchAuthorizationsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchAuthorizationsResponse200

Search authorizations

> Search for authorizations based on given criteria.
* **Parameters:**
  **body** (*SearchAuthorizationsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchAuthorizationsResponse200 | SearchAuthorizationsResponse400 | SearchAuthorizationsResponse401 | SearchAuthorizationsResponse403 | SearchAuthorizationsResponse500]

#### *async* search_authorizations_async(\*, data: SearchAuthorizationsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchAuthorizationsResponse200

Search authorizations

> Search for authorizations based on given criteria.
* **Parameters:**
  **body** (*SearchAuthorizationsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchAuthorizationsResponse200 | SearchAuthorizationsResponse400 | SearchAuthorizationsResponse401 | SearchAuthorizationsResponse403 | SearchAuthorizationsResponse500]

#### search_batch_operation_items(\*, data: SearchBatchOperationItemsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchBatchOperationItemsResponse200

Search batch operation items

> Search for batch operation items based on given criteria.
* **Parameters:**
  **body** (*SearchBatchOperationItemsData* *|* *Unset*) – Batch operation item search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchBatchOperationItemsResponse200 | SearchBatchOperationItemsResponse400 | SearchBatchOperationItemsResponse500]

#### *async* search_batch_operation_items_async(\*, data: SearchBatchOperationItemsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchBatchOperationItemsResponse200

Search batch operation items

> Search for batch operation items based on given criteria.
* **Parameters:**
  **body** (*SearchBatchOperationItemsData* *|* *Unset*) – Batch operation item search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchBatchOperationItemsResponse200 | SearchBatchOperationItemsResponse400 | SearchBatchOperationItemsResponse500]

#### search_batch_operations(\*, data: SearchBatchOperationsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchBatchOperationsResponse200

Search batch operations

> Search for batch operations based on given criteria.
* **Parameters:**
  **body** (*SearchBatchOperationsData* *|* *Unset*) – Batch operation search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchBatchOperationsResponse200 | SearchBatchOperationsResponse400 | SearchBatchOperationsResponse500]

#### *async* search_batch_operations_async(\*, data: SearchBatchOperationsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchBatchOperationsResponse200

Search batch operations

> Search for batch operations based on given criteria.
* **Parameters:**
  **body** (*SearchBatchOperationsData* *|* *Unset*) – Batch operation search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchBatchOperationsResponse200 | SearchBatchOperationsResponse400 | SearchBatchOperationsResponse500]

#### search_clients_for_group(group_id: str, \*, data: SearchClientsForGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchClientsForGroupResponse200

Search group clients

> Search clients assigned to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*SearchClientsForGroupData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchClientsForGroupResponse200 | SearchClientsForGroupResponse400 | SearchClientsForGroupResponse401 | SearchClientsForGroupResponse403 | SearchClientsForGroupResponse404 | SearchClientsForGroupResponse500]

#### *async* search_clients_for_group_async(group_id: str, \*, data: SearchClientsForGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchClientsForGroupResponse200

Search group clients

> Search clients assigned to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*SearchClientsForGroupData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchClientsForGroupResponse200 | SearchClientsForGroupResponse400 | SearchClientsForGroupResponse401 | SearchClientsForGroupResponse403 | SearchClientsForGroupResponse404 | SearchClientsForGroupResponse500]

#### search_clients_for_role(role_id: str, \*, data: SearchClientsForRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchClientsForRoleResponse200

Search role clients

> Search clients with assigned role.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*SearchClientsForRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchClientsForRoleResponse200 | SearchClientsForRoleResponse400 | SearchClientsForRoleResponse401 | SearchClientsForRoleResponse403 | SearchClientsForRoleResponse404 | SearchClientsForRoleResponse500]

#### *async* search_clients_for_role_async(role_id: str, \*, data: SearchClientsForRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchClientsForRoleResponse200

Search role clients

> Search clients with assigned role.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*SearchClientsForRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchClientsForRoleResponse200 | SearchClientsForRoleResponse400 | SearchClientsForRoleResponse401 | SearchClientsForRoleResponse403 | SearchClientsForRoleResponse404 | SearchClientsForRoleResponse500]

#### search_clients_for_tenant(tenant_id: str, \*, data: SearchClientsForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchClientsForTenantResponse200

Search clients for tenant

> Retrieves a filtered and sorted list of clients for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchClientsForTenantData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchClientsForTenantResponse200]

#### *async* search_clients_for_tenant_async(tenant_id: str, \*, data: SearchClientsForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchClientsForTenantResponse200

Search clients for tenant

> Retrieves a filtered and sorted list of clients for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchClientsForTenantData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchClientsForTenantResponse200]

#### search_cluster_variables(\*, data: SearchClusterVariablesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, truncate_values: bool | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchClusterVariablesResponse200

Search for cluster variables based on given criteria. By default, long variable values in the
response are truncated.

* **Parameters:**
  * **truncate_values** (*bool* *|* *Unset*)
  * **body** (*SearchClusterVariablesData* *|* *Unset*) – Cluster variable search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchClusterVariablesResponse200 | SearchClusterVariablesResponse400 | SearchClusterVariablesResponse401 | SearchClusterVariablesResponse403 | SearchClusterVariablesResponse500]

#### *async* search_cluster_variables_async(\*, data: SearchClusterVariablesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, truncate_values: bool | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchClusterVariablesResponse200

Search for cluster variables based on given criteria. By default, long variable values in the
response are truncated.

* **Parameters:**
  * **truncate_values** (*bool* *|* *Unset*)
  * **body** (*SearchClusterVariablesData* *|* *Unset*) – Cluster variable search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchClusterVariablesResponse200 | SearchClusterVariablesResponse400 | SearchClusterVariablesResponse401 | SearchClusterVariablesResponse403 | SearchClusterVariablesResponse500]

#### search_correlated_message_subscriptions(\*, data: SearchCorrelatedMessageSubscriptionsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchCorrelatedMessageSubscriptionsResponse200

Search correlated message subscriptions

> Search correlated message subscriptions based on given criteria.
* **Parameters:**
  **body** (*SearchCorrelatedMessageSubscriptionsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchCorrelatedMessageSubscriptionsResponse200 | SearchCorrelatedMessageSubscriptionsResponse400 | SearchCorrelatedMessageSubscriptionsResponse401 | SearchCorrelatedMessageSubscriptionsResponse403 | SearchCorrelatedMessageSubscriptionsResponse500]

#### *async* search_correlated_message_subscriptions_async(\*, data: SearchCorrelatedMessageSubscriptionsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchCorrelatedMessageSubscriptionsResponse200

Search correlated message subscriptions

> Search correlated message subscriptions based on given criteria.
* **Parameters:**
  **body** (*SearchCorrelatedMessageSubscriptionsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchCorrelatedMessageSubscriptionsResponse200 | SearchCorrelatedMessageSubscriptionsResponse400 | SearchCorrelatedMessageSubscriptionsResponse401 | SearchCorrelatedMessageSubscriptionsResponse403 | SearchCorrelatedMessageSubscriptionsResponse500]

#### search_decision_definitions(\*, data: SearchDecisionDefinitionsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchDecisionDefinitionsResponse200

Search decision definitions

> Search for decision definitions based on given criteria.
* **Parameters:**
  **body** (*SearchDecisionDefinitionsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchDecisionDefinitionsResponse200 | SearchDecisionDefinitionsResponse400 | SearchDecisionDefinitionsResponse401 | SearchDecisionDefinitionsResponse403 | SearchDecisionDefinitionsResponse500]

#### *async* search_decision_definitions_async(\*, data: SearchDecisionDefinitionsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchDecisionDefinitionsResponse200

Search decision definitions

> Search for decision definitions based on given criteria.
* **Parameters:**
  **body** (*SearchDecisionDefinitionsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchDecisionDefinitionsResponse200 | SearchDecisionDefinitionsResponse400 | SearchDecisionDefinitionsResponse401 | SearchDecisionDefinitionsResponse403 | SearchDecisionDefinitionsResponse500]

#### search_decision_instances(\*, data: SearchDecisionInstancesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchDecisionInstancesResponse200

Search decision instances

> Search for decision instances based on given criteria.
* **Parameters:**
  **body** (*SearchDecisionInstancesData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchDecisionInstancesResponse200 | SearchDecisionInstancesResponse400 | SearchDecisionInstancesResponse401 | SearchDecisionInstancesResponse403 | SearchDecisionInstancesResponse500]

#### *async* search_decision_instances_async(\*, data: SearchDecisionInstancesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchDecisionInstancesResponse200

Search decision instances

> Search for decision instances based on given criteria.
* **Parameters:**
  **body** (*SearchDecisionInstancesData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchDecisionInstancesResponse200 | SearchDecisionInstancesResponse400 | SearchDecisionInstancesResponse401 | SearchDecisionInstancesResponse403 | SearchDecisionInstancesResponse500]

#### search_decision_requirements(\*, data: SearchDecisionRequirementsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchDecisionRequirementsResponse200

Search decision requirements

> Search for decision requirements based on given criteria.
* **Parameters:**
  **body** (*SearchDecisionRequirementsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchDecisionRequirementsResponse200 | SearchDecisionRequirementsResponse400 | SearchDecisionRequirementsResponse401 | SearchDecisionRequirementsResponse403 | SearchDecisionRequirementsResponse500]

#### *async* search_decision_requirements_async(\*, data: SearchDecisionRequirementsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchDecisionRequirementsResponse200

Search decision requirements

> Search for decision requirements based on given criteria.
* **Parameters:**
  **body** (*SearchDecisionRequirementsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchDecisionRequirementsResponse200 | SearchDecisionRequirementsResponse400 | SearchDecisionRequirementsResponse401 | SearchDecisionRequirementsResponse403 | SearchDecisionRequirementsResponse500]

#### search_element_instance_incidents(element_instance_key: str, , data: SearchElementInstanceIncidentsData, \*\*kwargs: Any) → SearchElementInstanceIncidentsResponse200

Search for incidents of a specific element instance

> Search for incidents caused by the specified element instance, including incidents of any child

instances created from this element instance.

Although the elementInstanceKey is provided as a path parameter to indicate the root element
instance,
you may also include an elementInstanceKey within the filter object to narrow results to specific
child element instances. This is useful, for example, if you want to isolate incidents associated
with
nested or subordinate elements within the given element instance while excluding incidents directly
tied
to the root element itself.

* **Parameters:**
  * **element_instance_key** (*str*) – System-generated key for a element instance. Example:
    2251799813686789.
  * **body** (*SearchElementInstanceIncidentsData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchElementInstanceIncidentsResponse200 | SearchElementInstanceIncidentsResponse400 | SearchElementInstanceIncidentsResponse401 | SearchElementInstanceIncidentsResponse403 | SearchElementInstanceIncidentsResponse404 | SearchElementInstanceIncidentsResponse500]

#### *async* search_element_instance_incidents_async(element_instance_key: str, , data: SearchElementInstanceIncidentsData, \*\*kwargs: Any) → SearchElementInstanceIncidentsResponse200

Search for incidents of a specific element instance

> Search for incidents caused by the specified element instance, including incidents of any child

instances created from this element instance.

Although the elementInstanceKey is provided as a path parameter to indicate the root element
instance,
you may also include an elementInstanceKey within the filter object to narrow results to specific
child element instances. This is useful, for example, if you want to isolate incidents associated
with
nested or subordinate elements within the given element instance while excluding incidents directly
tied
to the root element itself.

* **Parameters:**
  * **element_instance_key** (*str*) – System-generated key for a element instance. Example:
    2251799813686789.
  * **body** (*SearchElementInstanceIncidentsData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchElementInstanceIncidentsResponse200 | SearchElementInstanceIncidentsResponse400 | SearchElementInstanceIncidentsResponse401 | SearchElementInstanceIncidentsResponse403 | SearchElementInstanceIncidentsResponse404 | SearchElementInstanceIncidentsResponse500]

#### search_element_instances(\*, data: SearchElementInstancesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchElementInstancesResponse200

Search element instances

> Search for element instances based on given criteria.
* **Parameters:**
  **body** (*SearchElementInstancesData* *|* *Unset*) – Element instance search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchElementInstancesResponse200 | SearchElementInstancesResponse400 | SearchElementInstancesResponse401 | SearchElementInstancesResponse403 | SearchElementInstancesResponse500]

#### *async* search_element_instances_async(\*, data: SearchElementInstancesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchElementInstancesResponse200

Search element instances

> Search for element instances based on given criteria.
* **Parameters:**
  **body** (*SearchElementInstancesData* *|* *Unset*) – Element instance search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchElementInstancesResponse200 | SearchElementInstancesResponse400 | SearchElementInstancesResponse401 | SearchElementInstancesResponse403 | SearchElementInstancesResponse500]

#### search_group_ids_for_tenant(tenant_id: str, \*, data: SearchGroupIdsForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchGroupIdsForTenantResponse200

Search groups for tenant

> Retrieves a filtered and sorted list of groups for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchGroupIdsForTenantData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchGroupIdsForTenantResponse200]

#### *async* search_group_ids_for_tenant_async(tenant_id: str, \*, data: SearchGroupIdsForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchGroupIdsForTenantResponse200

Search groups for tenant

> Retrieves a filtered and sorted list of groups for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchGroupIdsForTenantData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchGroupIdsForTenantResponse200]

#### search_groups(\*, data: SearchGroupsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Search groups

> Search for groups based on given criteria.
* **Parameters:**
  **body** (*SearchGroupsData* *|* *Unset*) – Group search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SearchGroupsResponse200 | SearchGroupsResponse400 | SearchGroupsResponse401 | SearchGroupsResponse403]

#### *async* search_groups_async(\*, data: SearchGroupsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Search groups

> Search for groups based on given criteria.
* **Parameters:**
  **body** (*SearchGroupsData* *|* *Unset*) – Group search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SearchGroupsResponse200 | SearchGroupsResponse400 | SearchGroupsResponse401 | SearchGroupsResponse403]

#### search_groups_for_role(role_id: str, \*, data: SearchGroupsForRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchGroupsForRoleResponse200

Search role groups

> Search groups with assigned role.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*SearchGroupsForRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchGroupsForRoleResponse200 | SearchGroupsForRoleResponse400 | SearchGroupsForRoleResponse401 | SearchGroupsForRoleResponse403 | SearchGroupsForRoleResponse404 | SearchGroupsForRoleResponse500]

#### *async* search_groups_for_role_async(role_id: str, \*, data: SearchGroupsForRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchGroupsForRoleResponse200

Search role groups

> Search groups with assigned role.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*SearchGroupsForRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchGroupsForRoleResponse200 | SearchGroupsForRoleResponse400 | SearchGroupsForRoleResponse401 | SearchGroupsForRoleResponse403 | SearchGroupsForRoleResponse404 | SearchGroupsForRoleResponse500]

#### search_incidents(\*, data: SearchIncidentsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchIncidentsResponse200

Search incidents

> Search for incidents based on given criteria.
* **Parameters:**
  **body** (*SearchIncidentsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchIncidentsResponse200 | SearchIncidentsResponse400 | SearchIncidentsResponse401 | SearchIncidentsResponse403 | SearchIncidentsResponse500]

#### *async* search_incidents_async(\*, data: SearchIncidentsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchIncidentsResponse200

Search incidents

> Search for incidents based on given criteria.
* **Parameters:**
  **body** (*SearchIncidentsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchIncidentsResponse200 | SearchIncidentsResponse400 | SearchIncidentsResponse401 | SearchIncidentsResponse403 | SearchIncidentsResponse500]

#### search_jobs(\*, data: SearchJobsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchJobsResponse200

Search jobs

> Search for jobs based on given criteria.
* **Parameters:**
  **body** (*SearchJobsData* *|* *Unset*) – Job search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchJobsResponse200 | SearchJobsResponse400 | SearchJobsResponse401 | SearchJobsResponse403 | SearchJobsResponse500]

#### *async* search_jobs_async(\*, data: SearchJobsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchJobsResponse200

Search jobs

> Search for jobs based on given criteria.
* **Parameters:**
  **body** (*SearchJobsData* *|* *Unset*) – Job search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchJobsResponse200 | SearchJobsResponse400 | SearchJobsResponse401 | SearchJobsResponse403 | SearchJobsResponse500]

#### search_mapping_rule(\*, data: SearchMappingRuleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMappingRuleResponse200

Search mapping rules

> Search for mapping rules based on given criteria.
* **Parameters:**
  **body** (*SearchMappingRuleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMappingRuleResponse200 | SearchMappingRuleResponse400 | SearchMappingRuleResponse401 | SearchMappingRuleResponse403 | SearchMappingRuleResponse500]

#### *async* search_mapping_rule_async(\*, data: SearchMappingRuleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMappingRuleResponse200

Search mapping rules

> Search for mapping rules based on given criteria.
* **Parameters:**
  **body** (*SearchMappingRuleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMappingRuleResponse200 | SearchMappingRuleResponse400 | SearchMappingRuleResponse401 | SearchMappingRuleResponse403 | SearchMappingRuleResponse500]

#### search_mapping_rules_for_group(group_id: str, \*, data: SearchMappingRulesForGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMappingRulesForGroupResponse200

Search group mapping rules

> Search mapping rules assigned to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*SearchMappingRulesForGroupData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMappingRulesForGroupResponse200 | SearchMappingRulesForGroupResponse400 | SearchMappingRulesForGroupResponse401 | SearchMappingRulesForGroupResponse403 | SearchMappingRulesForGroupResponse404 | SearchMappingRulesForGroupResponse500]

#### *async* search_mapping_rules_for_group_async(group_id: str, \*, data: SearchMappingRulesForGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMappingRulesForGroupResponse200

Search group mapping rules

> Search mapping rules assigned to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*SearchMappingRulesForGroupData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMappingRulesForGroupResponse200 | SearchMappingRulesForGroupResponse400 | SearchMappingRulesForGroupResponse401 | SearchMappingRulesForGroupResponse403 | SearchMappingRulesForGroupResponse404 | SearchMappingRulesForGroupResponse500]

#### search_mapping_rules_for_role(role_id: str, \*, data: SearchMappingRulesForRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMappingRulesForRoleResponse200

Search role mapping rules

> Search mapping rules with assigned role.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*SearchMappingRulesForRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMappingRulesForRoleResponse200 | SearchMappingRulesForRoleResponse400 | SearchMappingRulesForRoleResponse401 | SearchMappingRulesForRoleResponse403 | SearchMappingRulesForRoleResponse404 | SearchMappingRulesForRoleResponse500]

#### *async* search_mapping_rules_for_role_async(role_id: str, \*, data: SearchMappingRulesForRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMappingRulesForRoleResponse200

Search role mapping rules

> Search mapping rules with assigned role.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*SearchMappingRulesForRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMappingRulesForRoleResponse200 | SearchMappingRulesForRoleResponse400 | SearchMappingRulesForRoleResponse401 | SearchMappingRulesForRoleResponse403 | SearchMappingRulesForRoleResponse404 | SearchMappingRulesForRoleResponse500]

#### search_mapping_rules_for_tenant(tenant_id: str, \*, data: SearchMappingRulesForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMappingRulesForTenantResponse200

Search mapping rules for tenant

> Retrieves a filtered and sorted list of MappingRules for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchMappingRulesForTenantData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMappingRulesForTenantResponse200]

#### *async* search_mapping_rules_for_tenant_async(tenant_id: str, \*, data: SearchMappingRulesForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMappingRulesForTenantResponse200

Search mapping rules for tenant

> Retrieves a filtered and sorted list of MappingRules for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchMappingRulesForTenantData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMappingRulesForTenantResponse200]

#### search_message_subscriptions(\*, data: SearchMessageSubscriptionsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMessageSubscriptionsResponse200

Search message subscriptions

> Search for message subscriptions based on given criteria.
* **Parameters:**
  **body** (*SearchMessageSubscriptionsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMessageSubscriptionsResponse200 | SearchMessageSubscriptionsResponse400 | SearchMessageSubscriptionsResponse401 | SearchMessageSubscriptionsResponse403 | SearchMessageSubscriptionsResponse500]

#### *async* search_message_subscriptions_async(\*, data: SearchMessageSubscriptionsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchMessageSubscriptionsResponse200

Search message subscriptions

> Search for message subscriptions based on given criteria.
* **Parameters:**
  **body** (*SearchMessageSubscriptionsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchMessageSubscriptionsResponse200 | SearchMessageSubscriptionsResponse400 | SearchMessageSubscriptionsResponse401 | SearchMessageSubscriptionsResponse403 | SearchMessageSubscriptionsResponse500]

#### search_process_definitions(\*, data: SearchProcessDefinitionsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchProcessDefinitionsResponse200

Search process definitions

> Search for process definitions based on given criteria.
* **Parameters:**
  **body** (*SearchProcessDefinitionsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchProcessDefinitionsResponse200 | SearchProcessDefinitionsResponse400 | SearchProcessDefinitionsResponse401 | SearchProcessDefinitionsResponse403 | SearchProcessDefinitionsResponse500]

#### *async* search_process_definitions_async(\*, data: SearchProcessDefinitionsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchProcessDefinitionsResponse200

Search process definitions

> Search for process definitions based on given criteria.
* **Parameters:**
  **body** (*SearchProcessDefinitionsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchProcessDefinitionsResponse200 | SearchProcessDefinitionsResponse400 | SearchProcessDefinitionsResponse401 | SearchProcessDefinitionsResponse403 | SearchProcessDefinitionsResponse500]

#### search_process_instance_incidents(process_instance_key: str, \*, data: SearchProcessInstanceIncidentsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchProcessInstanceIncidentsResponse200

Search related incidents

> Search for incidents caused by the process instance or any of its called process or decision

instances.

Although the processInstanceKey is provided as a path parameter to indicate the root process
instance,
you may also include a processInstanceKey within the filter object to narrow results to specific
child process instances. This is useful, for example, if you want to isolate incidents associated
with
subprocesses or called processes under the root instance while excluding incidents directly tied to
the root.

* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*SearchProcessInstanceIncidentsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchProcessInstanceIncidentsResponse200 | SearchProcessInstanceIncidentsResponse400 | SearchProcessInstanceIncidentsResponse401 | SearchProcessInstanceIncidentsResponse403 | SearchProcessInstanceIncidentsResponse404 | SearchProcessInstanceIncidentsResponse500]

#### *async* search_process_instance_incidents_async(process_instance_key: str, \*, data: SearchProcessInstanceIncidentsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchProcessInstanceIncidentsResponse200

Search related incidents

> Search for incidents caused by the process instance or any of its called process or decision

instances.

Although the processInstanceKey is provided as a path parameter to indicate the root process
instance,
you may also include a processInstanceKey within the filter object to narrow results to specific
child process instances. This is useful, for example, if you want to isolate incidents associated
with
subprocesses or called processes under the root instance while excluding incidents directly tied to
the root.

* **Parameters:**
  * **process_instance_key** (*str*) – System-generated key for a process instance. Example:
    2251799813690746.
  * **body** (*SearchProcessInstanceIncidentsData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchProcessInstanceIncidentsResponse200 | SearchProcessInstanceIncidentsResponse400 | SearchProcessInstanceIncidentsResponse401 | SearchProcessInstanceIncidentsResponse403 | SearchProcessInstanceIncidentsResponse404 | SearchProcessInstanceIncidentsResponse500]

#### search_process_instances(\*, data: SearchProcessInstancesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchProcessInstancesResponse200

Search process instances

> Search for process instances based on given criteria.
* **Parameters:**
  **body** (*SearchProcessInstancesData* *|* *Unset*) – Process instance search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchProcessInstancesResponse200 | SearchProcessInstancesResponse400 | SearchProcessInstancesResponse401 | SearchProcessInstancesResponse403 | SearchProcessInstancesResponse500]

#### *async* search_process_instances_async(\*, data: SearchProcessInstancesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchProcessInstancesResponse200

Search process instances

> Search for process instances based on given criteria.
* **Parameters:**
  **body** (*SearchProcessInstancesData* *|* *Unset*) – Process instance search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchProcessInstancesResponse200 | SearchProcessInstancesResponse400 | SearchProcessInstancesResponse401 | SearchProcessInstancesResponse403 | SearchProcessInstancesResponse500]

#### search_roles(\*, data: SearchRolesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Search roles

> Search for roles based on given criteria.
* **Parameters:**
  **body** (*SearchRolesData* *|* *Unset*) – Role search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SearchRolesResponse200 | SearchRolesResponse400 | SearchRolesResponse401 | SearchRolesResponse403]

#### *async* search_roles_async(\*, data: SearchRolesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Search roles

> Search for roles based on given criteria.
* **Parameters:**
  **body** (*SearchRolesData* *|* *Unset*) – Role search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SearchRolesResponse200 | SearchRolesResponse400 | SearchRolesResponse401 | SearchRolesResponse403]

#### search_roles_for_group(group_id: str, \*, data: SearchRolesForGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchRolesForGroupResponse200

Search group roles

> Search roles assigned to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*SearchRolesForGroupData* *|* *Unset*) – Role search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchRolesForGroupResponse200 | SearchRolesForGroupResponse400 | SearchRolesForGroupResponse401 | SearchRolesForGroupResponse403 | SearchRolesForGroupResponse404 | SearchRolesForGroupResponse500]

#### *async* search_roles_for_group_async(group_id: str, \*, data: SearchRolesForGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchRolesForGroupResponse200

Search group roles

> Search roles assigned to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*SearchRolesForGroupData* *|* *Unset*) – Role search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchRolesForGroupResponse200 | SearchRolesForGroupResponse400 | SearchRolesForGroupResponse401 | SearchRolesForGroupResponse403 | SearchRolesForGroupResponse404 | SearchRolesForGroupResponse500]

#### search_roles_for_tenant(tenant_id: str, \*, data: SearchRolesForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchRolesForTenantResponse200

Search roles for tenant

> Retrieves a filtered and sorted list of roles for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchRolesForTenantData* *|* *Unset*) – Role search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchRolesForTenantResponse200]

#### *async* search_roles_for_tenant_async(tenant_id: str, \*, data: SearchRolesForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchRolesForTenantResponse200

Search roles for tenant

> Retrieves a filtered and sorted list of roles for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchRolesForTenantData* *|* *Unset*) – Role search request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchRolesForTenantResponse200]

#### search_tenants(\*, data: SearchTenantsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Search tenants

> Retrieves a filtered and sorted list of tenants.
* **Parameters:**
  **body** (*SearchTenantsData* *|* *Unset*) – Tenant search request
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SearchTenantsResponse200 | SearchTenantsResponse400 | SearchTenantsResponse401 | SearchTenantsResponse403 | SearchTenantsResponse500]

#### *async* search_tenants_async(\*, data: SearchTenantsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Search tenants

> Retrieves a filtered and sorted list of tenants.
* **Parameters:**
  **body** (*SearchTenantsData* *|* *Unset*) – Tenant search request
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SearchTenantsResponse200 | SearchTenantsResponse400 | SearchTenantsResponse401 | SearchTenantsResponse403 | SearchTenantsResponse500]

#### search_user_task_audit_logs(user_task_key: str, \*, data: SearchUserTaskAuditLogsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUserTaskAuditLogsResponse200

Search user task audit logs

> Search for user task audit logs based on given criteria.
* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **body** (*SearchUserTaskAuditLogsData* *|* *Unset*) – User task search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUserTaskAuditLogsResponse200 | SearchUserTaskAuditLogsResponse400 | SearchUserTaskAuditLogsResponse500]

#### *async* search_user_task_audit_logs_async(user_task_key: str, \*, data: SearchUserTaskAuditLogsData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUserTaskAuditLogsResponse200

Search user task audit logs

> Search for user task audit logs based on given criteria.
* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **body** (*SearchUserTaskAuditLogsData* *|* *Unset*) – User task search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUserTaskAuditLogsResponse200 | SearchUserTaskAuditLogsResponse400 | SearchUserTaskAuditLogsResponse500]

#### search_user_task_variables(user_task_key: str, \*, data: SearchUserTaskVariablesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, truncate_values: bool | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUserTaskVariablesResponse200

Search user task variables

> Search for user task variables based on given criteria. By default, long variable values in the

response are truncated.

* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **truncate_values** (*bool* *|* *Unset*)
  * **body** (*SearchUserTaskVariablesData* *|* *Unset*) – User task search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUserTaskVariablesResponse200 | SearchUserTaskVariablesResponse400 | SearchUserTaskVariablesResponse500]

#### *async* search_user_task_variables_async(user_task_key: str, \*, data: SearchUserTaskVariablesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, truncate_values: bool | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUserTaskVariablesResponse200

Search user task variables

> Search for user task variables based on given criteria. By default, long variable values in the

response are truncated.

* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **truncate_values** (*bool* *|* *Unset*)
  * **body** (*SearchUserTaskVariablesData* *|* *Unset*) – User task search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUserTaskVariablesResponse200 | SearchUserTaskVariablesResponse400 | SearchUserTaskVariablesResponse500]

#### search_user_tasks(\*, data: SearchUserTasksData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUserTasksResponse200

Search user tasks

> Search for user tasks based on given criteria.
* **Parameters:**
  **body** (*SearchUserTasksData* *|* *Unset*) – User task search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUserTasksResponse200 | SearchUserTasksResponse400 | SearchUserTasksResponse401 | SearchUserTasksResponse403 | SearchUserTasksResponse500]

#### *async* search_user_tasks_async(\*, data: SearchUserTasksData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUserTasksResponse200

Search user tasks

> Search for user tasks based on given criteria.
* **Parameters:**
  **body** (*SearchUserTasksData* *|* *Unset*) – User task search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUserTasksResponse200 | SearchUserTasksResponse400 | SearchUserTasksResponse401 | SearchUserTasksResponse403 | SearchUserTasksResponse500]

#### search_users(\*, data: SearchUsersData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUsersResponse200

Search users

> Search for users based on given criteria.
* **Parameters:**
  **body** (*SearchUsersData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUsersResponse200 | SearchUsersResponse400 | SearchUsersResponse401 | SearchUsersResponse403 | SearchUsersResponse500]

#### *async* search_users_async(\*, data: SearchUsersData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUsersResponse200

Search users

> Search for users based on given criteria.
* **Parameters:**
  **body** (*SearchUsersData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUsersResponse200 | SearchUsersResponse400 | SearchUsersResponse401 | SearchUsersResponse403 | SearchUsersResponse500]

#### search_users_for_group(group_id: str, \*, data: SearchUsersForGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUsersForGroupResponse200

Search group users

> Search users assigned to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*SearchUsersForGroupData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUsersForGroupResponse200 | SearchUsersForGroupResponse400 | SearchUsersForGroupResponse401 | SearchUsersForGroupResponse403 | SearchUsersForGroupResponse404 | SearchUsersForGroupResponse500]

#### *async* search_users_for_group_async(group_id: str, \*, data: SearchUsersForGroupData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUsersForGroupResponse200

Search group users

> Search users assigned to a group.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*SearchUsersForGroupData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUsersForGroupResponse200 | SearchUsersForGroupResponse400 | SearchUsersForGroupResponse401 | SearchUsersForGroupResponse403 | SearchUsersForGroupResponse404 | SearchUsersForGroupResponse500]

#### search_users_for_role(role_id: str, \*, data: SearchUsersForRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUsersForRoleResponse200

Search role users

> Search users with assigned role.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*SearchUsersForRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUsersForRoleResponse200 | SearchUsersForRoleResponse400 | SearchUsersForRoleResponse401 | SearchUsersForRoleResponse403 | SearchUsersForRoleResponse404 | SearchUsersForRoleResponse500]

#### *async* search_users_for_role_async(role_id: str, \*, data: SearchUsersForRoleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUsersForRoleResponse200

Search role users

> Search users with assigned role.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*SearchUsersForRoleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUsersForRoleResponse200 | SearchUsersForRoleResponse400 | SearchUsersForRoleResponse401 | SearchUsersForRoleResponse403 | SearchUsersForRoleResponse404 | SearchUsersForRoleResponse500]

#### search_users_for_tenant(tenant_id: str, \*, data: SearchUsersForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUsersForTenantResponse200

Search users for tenant

> Retrieves a filtered and sorted list of users for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchUsersForTenantData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUsersForTenantResponse200]

#### *async* search_users_for_tenant_async(tenant_id: str, \*, data: SearchUsersForTenantData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchUsersForTenantResponse200

Search users for tenant

> Retrieves a filtered and sorted list of users for a specified tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*SearchUsersForTenantData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchUsersForTenantResponse200]

#### search_variables(\*, data: SearchVariablesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, truncate_values: bool | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchVariablesResponse200

Search variables

> Search for process and local variables based on given criteria. By default, long variable values in

the response are truncated.

* **Parameters:**
  * **truncate_values** (*bool* *|* *Unset*)
  * **body** (*SearchVariablesData* *|* *Unset*) – Variable search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchVariablesResponse200 | SearchVariablesResponse400 | SearchVariablesResponse401 | SearchVariablesResponse403 | SearchVariablesResponse500]

#### *async* search_variables_async(\*, data: SearchVariablesData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, truncate_values: bool | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → SearchVariablesResponse200

Search variables

> Search for process and local variables based on given criteria. By default, long variable values in

the response are truncated.

* **Parameters:**
  * **truncate_values** (*bool* *|* *Unset*)
  * **body** (*SearchVariablesData* *|* *Unset*) – Variable search query request.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[SearchVariablesResponse200 | SearchVariablesResponse400 | SearchVariablesResponse401 | SearchVariablesResponse403 | SearchVariablesResponse500]

#### suspend_batch_operation(batch_operation_key: str, \*, data: ~typing.Any | ~camunda_orchestration_sdk.types.Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: ~typing.Any) → Any

Suspend Batch operation

> Suspends a running batch operation.

This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  * **batch_operation_key** (*str*) – System-generated key for an batch operation. Example:
    2251799813684321.
  * **body** (*Any* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SuspendBatchOperationResponse400 | SuspendBatchOperationResponse403 | SuspendBatchOperationResponse404 | SuspendBatchOperationResponse500 | SuspendBatchOperationResponse503]

#### *async* suspend_batch_operation_async(batch_operation_key: str, \*, data: ~typing.Any | ~camunda_orchestration_sdk.types.Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: ~typing.Any) → Any

Suspend Batch operation

> Suspends a running batch operation.

This is done asynchronously, the progress can be tracked using the batch operation status endpoint
(/batch-operations/`{batchOperationKey}`).

* **Parameters:**
  * **batch_operation_key** (*str*) – System-generated key for an batch operation. Example:
    2251799813684321.
  * **body** (*Any* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | SuspendBatchOperationResponse400 | SuspendBatchOperationResponse403 | SuspendBatchOperationResponse404 | SuspendBatchOperationResponse500 | SuspendBatchOperationResponse503]

#### throw_job_error(job_key: str, , data: ThrowJobErrorData, \*\*kwargs: Any) → Any

Throw error for job

> Reports a business error (i.e. non-technical) that occurs while processing a job.
* **Parameters:**
  * **job_key** (*str*) – System-generated key for a job. Example: 2251799813653498.
  * **body** (*ThrowJobErrorData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ThrowJobErrorResponse400 | ThrowJobErrorResponse404 | ThrowJobErrorResponse409 | ThrowJobErrorResponse500 | ThrowJobErrorResponse503]

#### *async* throw_job_error_async(job_key: str, , data: ThrowJobErrorData, \*\*kwargs: Any) → Any

Throw error for job

> Reports a business error (i.e. non-technical) that occurs while processing a job.
* **Parameters:**
  * **job_key** (*str*) – System-generated key for a job. Example: 2251799813653498.
  * **body** (*ThrowJobErrorData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | ThrowJobErrorResponse400 | ThrowJobErrorResponse404 | ThrowJobErrorResponse409 | ThrowJobErrorResponse500 | ThrowJobErrorResponse503]

#### unassign_client_from_group(group_id: str, client_id: str, \*\*kwargs: Any) → Any

Unassign a client from a group

> Unassigns a client from a group.

The client is removed as a group member, with associated authorizations, roles, and tenant
assignments no longer applied.

* **Parameters:**
  * **group_id** (*str*)
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignClientFromGroupResponse400 | UnassignClientFromGroupResponse403 | UnassignClientFromGroupResponse404 | UnassignClientFromGroupResponse500 | UnassignClientFromGroupResponse503]

#### *async* unassign_client_from_group_async(group_id: str, client_id: str, \*\*kwargs: Any) → Any

Unassign a client from a group

> Unassigns a client from a group.

The client is removed as a group member, with associated authorizations, roles, and tenant
assignments no longer applied.

* **Parameters:**
  * **group_id** (*str*)
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignClientFromGroupResponse400 | UnassignClientFromGroupResponse403 | UnassignClientFromGroupResponse404 | UnassignClientFromGroupResponse500 | UnassignClientFromGroupResponse503]

#### unassign_client_from_tenant(tenant_id: str, client_id: str, \*\*kwargs: Any) → Any

Unassign a client from a tenant

> Unassigns the client from the specified tenant.

The client can no longer access tenant data.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignClientFromTenantResponse400 | UnassignClientFromTenantResponse403 | UnassignClientFromTenantResponse404 | UnassignClientFromTenantResponse500 | UnassignClientFromTenantResponse503]

#### *async* unassign_client_from_tenant_async(tenant_id: str, client_id: str, \*\*kwargs: Any) → Any

Unassign a client from a tenant

> Unassigns the client from the specified tenant.

The client can no longer access tenant data.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignClientFromTenantResponse400 | UnassignClientFromTenantResponse403 | UnassignClientFromTenantResponse404 | UnassignClientFromTenantResponse500 | UnassignClientFromTenantResponse503]

#### unassign_group_from_tenant(tenant_id: str, group_id: str, \*\*kwargs: Any) → Any

Unassign a group from a tenant

> Unassigns a group from a specified tenant.

Members of the group (users, clients) will no longer have access to the tenant’s data - except they
are assigned directly to the tenant.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignGroupFromTenantResponse400 | UnassignGroupFromTenantResponse403 | UnassignGroupFromTenantResponse404 | UnassignGroupFromTenantResponse500 | UnassignGroupFromTenantResponse503]

#### *async* unassign_group_from_tenant_async(tenant_id: str, group_id: str, \*\*kwargs: Any) → Any

Unassign a group from a tenant

> Unassigns a group from a specified tenant.

Members of the group (users, clients) will no longer have access to the tenant’s data - except they
are assigned directly to the tenant.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignGroupFromTenantResponse400 | UnassignGroupFromTenantResponse403 | UnassignGroupFromTenantResponse404 | UnassignGroupFromTenantResponse500 | UnassignGroupFromTenantResponse503]

#### unassign_mapping_rule_from_group(group_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Unassign a mapping rule from a group

> Unassigns a mapping rule from a group.
* **Parameters:**
  * **group_id** (*str*)
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignMappingRuleFromGroupResponse400 | UnassignMappingRuleFromGroupResponse403 | UnassignMappingRuleFromGroupResponse404 | UnassignMappingRuleFromGroupResponse500 | UnassignMappingRuleFromGroupResponse503]

#### *async* unassign_mapping_rule_from_group_async(group_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Unassign a mapping rule from a group

> Unassigns a mapping rule from a group.
* **Parameters:**
  * **group_id** (*str*)
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignMappingRuleFromGroupResponse400 | UnassignMappingRuleFromGroupResponse403 | UnassignMappingRuleFromGroupResponse404 | UnassignMappingRuleFromGroupResponse500 | UnassignMappingRuleFromGroupResponse503]

#### unassign_mapping_rule_from_tenant(tenant_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Unassign a mapping rule from a tenant

> Unassigns a single mapping rule from a specified tenant without deleting the rule.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignMappingRuleFromTenantResponse400 | UnassignMappingRuleFromTenantResponse403 | UnassignMappingRuleFromTenantResponse404 | UnassignMappingRuleFromTenantResponse500 | UnassignMappingRuleFromTenantResponse503]

#### *async* unassign_mapping_rule_from_tenant_async(tenant_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Unassign a mapping rule from a tenant

> Unassigns a single mapping rule from a specified tenant without deleting the rule.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignMappingRuleFromTenantResponse400 | UnassignMappingRuleFromTenantResponse403 | UnassignMappingRuleFromTenantResponse404 | UnassignMappingRuleFromTenantResponse500 | UnassignMappingRuleFromTenantResponse503]

#### unassign_role_from_client(role_id: str, client_id: str, \*\*kwargs: Any) → Any

Unassign a role from a client

> Unassigns the specified role from the client. The client will no longer inherit the authorizations

associated with this role.

* **Parameters:**
  * **role_id** (*str*)
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromClientResponse400 | UnassignRoleFromClientResponse403 | UnassignRoleFromClientResponse404 | UnassignRoleFromClientResponse500 | UnassignRoleFromClientResponse503]

#### *async* unassign_role_from_client_async(role_id: str, client_id: str, \*\*kwargs: Any) → Any

Unassign a role from a client

> Unassigns the specified role from the client. The client will no longer inherit the authorizations

associated with this role.

* **Parameters:**
  * **role_id** (*str*)
  * **client_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromClientResponse400 | UnassignRoleFromClientResponse403 | UnassignRoleFromClientResponse404 | UnassignRoleFromClientResponse500 | UnassignRoleFromClientResponse503]

#### unassign_role_from_group(role_id: str, group_id: str, \*\*kwargs: Any) → Any

Unassign a role from a group

> Unassigns the specified role from the group. All group members (user or client) no longer inherit

the authorizations associated with this role.

* **Parameters:**
  * **role_id** (*str*)
  * **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromGroupResponse400 | UnassignRoleFromGroupResponse403 | UnassignRoleFromGroupResponse404 | UnassignRoleFromGroupResponse500 | UnassignRoleFromGroupResponse503]

#### *async* unassign_role_from_group_async(role_id: str, group_id: str, \*\*kwargs: Any) → Any

Unassign a role from a group

> Unassigns the specified role from the group. All group members (user or client) no longer inherit

the authorizations associated with this role.

* **Parameters:**
  * **role_id** (*str*)
  * **group_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromGroupResponse400 | UnassignRoleFromGroupResponse403 | UnassignRoleFromGroupResponse404 | UnassignRoleFromGroupResponse500 | UnassignRoleFromGroupResponse503]

#### unassign_role_from_mapping_rule(role_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Unassign a role from a mapping rule

> Unassigns a role from a mapping rule.
* **Parameters:**
  * **role_id** (*str*)
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromMappingRuleResponse400 | UnassignRoleFromMappingRuleResponse403 | UnassignRoleFromMappingRuleResponse404 | UnassignRoleFromMappingRuleResponse500 | UnassignRoleFromMappingRuleResponse503]

#### *async* unassign_role_from_mapping_rule_async(role_id: str, mapping_rule_id: str, \*\*kwargs: Any) → Any

Unassign a role from a mapping rule

> Unassigns a role from a mapping rule.
* **Parameters:**
  * **role_id** (*str*)
  * **mapping_rule_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromMappingRuleResponse400 | UnassignRoleFromMappingRuleResponse403 | UnassignRoleFromMappingRuleResponse404 | UnassignRoleFromMappingRuleResponse500 | UnassignRoleFromMappingRuleResponse503]

#### unassign_role_from_tenant(tenant_id: str, role_id: str, \*\*kwargs: Any) → Any

Unassign a role from a tenant

> Unassigns a role from a specified tenant.

Users, Clients or Groups, that have the role assigned, will no longer have access to the
tenant’s data - unless they are assigned directly to the tenant.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **role_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromTenantResponse400 | UnassignRoleFromTenantResponse403 | UnassignRoleFromTenantResponse404 | UnassignRoleFromTenantResponse500 | UnassignRoleFromTenantResponse503]

#### *async* unassign_role_from_tenant_async(tenant_id: str, role_id: str, \*\*kwargs: Any) → Any

Unassign a role from a tenant

> Unassigns a role from a specified tenant.

Users, Clients or Groups, that have the role assigned, will no longer have access to the
tenant’s data - unless they are assigned directly to the tenant.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **role_id** (*str*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromTenantResponse400 | UnassignRoleFromTenantResponse403 | UnassignRoleFromTenantResponse404 | UnassignRoleFromTenantResponse500 | UnassignRoleFromTenantResponse503]

#### unassign_role_from_user(role_id: str, username: str, \*\*kwargs: Any) → Any

Unassign a role from a user

> Unassigns a role from a user. The user will no longer inherit the authorizations associated with

this role.

* **Parameters:**
  * **role_id** (*str*)
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromUserResponse400 | UnassignRoleFromUserResponse403 | UnassignRoleFromUserResponse404 | UnassignRoleFromUserResponse500 | UnassignRoleFromUserResponse503]

#### *async* unassign_role_from_user_async(role_id: str, username: str, \*\*kwargs: Any) → Any

Unassign a role from a user

> Unassigns a role from a user. The user will no longer inherit the authorizations associated with

this role.

* **Parameters:**
  * **role_id** (*str*)
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignRoleFromUserResponse400 | UnassignRoleFromUserResponse403 | UnassignRoleFromUserResponse404 | UnassignRoleFromUserResponse500 | UnassignRoleFromUserResponse503]

#### unassign_user_from_group(group_id: str, username: str, \*\*kwargs: Any) → Any

Unassign a user from a group

> Unassigns a user from a group.

The user is removed as a group member, with associated authorizations, roles, and tenant assignments
no longer applied.

* **Parameters:**
  * **group_id** (*str*)
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignUserFromGroupResponse400 | UnassignUserFromGroupResponse403 | UnassignUserFromGroupResponse404 | UnassignUserFromGroupResponse500 | UnassignUserFromGroupResponse503]

#### *async* unassign_user_from_group_async(group_id: str, username: str, \*\*kwargs: Any) → Any

Unassign a user from a group

> Unassigns a user from a group.

The user is removed as a group member, with associated authorizations, roles, and tenant assignments
no longer applied.

* **Parameters:**
  * **group_id** (*str*)
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignUserFromGroupResponse400 | UnassignUserFromGroupResponse403 | UnassignUserFromGroupResponse404 | UnassignUserFromGroupResponse500 | UnassignUserFromGroupResponse503]

#### unassign_user_from_tenant(tenant_id: str, username: str, \*\*kwargs: Any) → Any

Unassign a user from a tenant

> Unassigns the user from the specified tenant.

The user can no longer access tenant data.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignUserFromTenantResponse400 | UnassignUserFromTenantResponse403 | UnassignUserFromTenantResponse404 | UnassignUserFromTenantResponse500 | UnassignUserFromTenantResponse503]

#### *async* unassign_user_from_tenant_async(tenant_id: str, username: str, \*\*kwargs: Any) → Any

Unassign a user from a tenant

> Unassigns the user from the specified tenant.

The user can no longer access tenant data.

* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **username** (*str*) – The unique name of a user. Example: swillis.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignUserFromTenantResponse400 | UnassignUserFromTenantResponse403 | UnassignUserFromTenantResponse404 | UnassignUserFromTenantResponse500 | UnassignUserFromTenantResponse503]

#### unassign_user_task(user_task_key: str, \*\*kwargs: Any) → Any

Unassign user task

> Removes the assignee of a task with the given key.
* **Parameters:**
  **user_task_key** (*str*) – System-generated key for a user task.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignUserTaskResponse400 | UnassignUserTaskResponse404 | UnassignUserTaskResponse409 | UnassignUserTaskResponse500 | UnassignUserTaskResponse503]

#### *async* unassign_user_task_async(user_task_key: str, \*\*kwargs: Any) → Any

Unassign user task

> Removes the assignee of a task with the given key.
* **Parameters:**
  **user_task_key** (*str*) – System-generated key for a user task.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UnassignUserTaskResponse400 | UnassignUserTaskResponse404 | UnassignUserTaskResponse409 | UnassignUserTaskResponse500 | UnassignUserTaskResponse503]

#### update_authorization(authorization_key: str, , data: Object | Object1, \*\*kwargs: Any) → Any

Update authorization

> Update the authorization with the given key.
* **Parameters:**
  * **authorization_key** (*str*) – System-generated key for an authorization. Example:
    2251799813684332.
  * **body** (*Object* *|* *Object1*) – Defines an authorization request.
    Either an id-based or a property-based authorization can be provided.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UpdateAuthorizationResponse401 | UpdateAuthorizationResponse404 | UpdateAuthorizationResponse500 | UpdateAuthorizationResponse503]

#### *async* update_authorization_async(authorization_key: str, , data: Object | Object1, \*\*kwargs: Any) → Any

Update authorization

> Update the authorization with the given key.
* **Parameters:**
  * **authorization_key** (*str*) – System-generated key for an authorization. Example:
    2251799813684332.
  * **body** (*Object* *|* *Object1*) – Defines an authorization request.
    Either an id-based or a property-based authorization can be provided.
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UpdateAuthorizationResponse401 | UpdateAuthorizationResponse404 | UpdateAuthorizationResponse500 | UpdateAuthorizationResponse503]

#### update_group(group_id: str, , data: UpdateGroupData, \*\*kwargs: Any) → UpdateGroupResponse200

Update group

> Update a group with the given ID.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*UpdateGroupData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateGroupResponse200 | UpdateGroupResponse400 | UpdateGroupResponse401 | UpdateGroupResponse404 | UpdateGroupResponse500 | UpdateGroupResponse503]

#### *async* update_group_async(group_id: str, , data: UpdateGroupData, \*\*kwargs: Any) → UpdateGroupResponse200

Update group

> Update a group with the given ID.
* **Parameters:**
  * **group_id** (*str*)
  * **body** (*UpdateGroupData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateGroupResponse200 | UpdateGroupResponse400 | UpdateGroupResponse401 | UpdateGroupResponse404 | UpdateGroupResponse500 | UpdateGroupResponse503]

#### update_job(job_key: str, , data: UpdateJobData, \*\*kwargs: Any) → Any

Update job

> Update a job with the given key.
* **Parameters:**
  * **job_key** (*str*) – System-generated key for a job. Example: 2251799813653498.
  * **body** (*UpdateJobData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UpdateJobResponse400 | UpdateJobResponse404 | UpdateJobResponse409 | UpdateJobResponse500 | UpdateJobResponse503]

#### *async* update_job_async(job_key: str, , data: UpdateJobData, \*\*kwargs: Any) → Any

Update job

> Update a job with the given key.
* **Parameters:**
  * **job_key** (*str*) – System-generated key for a job. Example: 2251799813653498.
  * **body** (*UpdateJobData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UpdateJobResponse400 | UpdateJobResponse404 | UpdateJobResponse409 | UpdateJobResponse500 | UpdateJobResponse503]

#### update_mapping_rule(mapping_rule_id: str, \*, data: UpdateMappingRuleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → UpdateMappingRuleResponse200

Update mapping rule

> Update a mapping rule.
* **Parameters:**
  * **mapping_rule_id** (*str*)
  * **body** (*UpdateMappingRuleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateMappingRuleResponse200 | UpdateMappingRuleResponse400 | UpdateMappingRuleResponse403 | UpdateMappingRuleResponse404 | UpdateMappingRuleResponse500 | UpdateMappingRuleResponse503]

#### *async* update_mapping_rule_async(mapping_rule_id: str, \*, data: UpdateMappingRuleData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → UpdateMappingRuleResponse200

Update mapping rule

> Update a mapping rule.
* **Parameters:**
  * **mapping_rule_id** (*str*)
  * **body** (*UpdateMappingRuleData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateMappingRuleResponse200 | UpdateMappingRuleResponse400 | UpdateMappingRuleResponse403 | UpdateMappingRuleResponse404 | UpdateMappingRuleResponse500 | UpdateMappingRuleResponse503]

#### update_role(role_id: str, , data: UpdateRoleData, \*\*kwargs: Any) → UpdateRoleResponse200

Update role

> Update a role with the given ID.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*UpdateRoleData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateRoleResponse200 | UpdateRoleResponse400 | UpdateRoleResponse401 | UpdateRoleResponse404 | UpdateRoleResponse500 | UpdateRoleResponse503]

#### *async* update_role_async(role_id: str, , data: UpdateRoleData, \*\*kwargs: Any) → UpdateRoleResponse200

Update role

> Update a role with the given ID.
* **Parameters:**
  * **role_id** (*str*)
  * **body** (*UpdateRoleData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateRoleResponse200 | UpdateRoleResponse400 | UpdateRoleResponse401 | UpdateRoleResponse404 | UpdateRoleResponse500 | UpdateRoleResponse503]

#### update_tenant(tenant_id: str, , data: UpdateTenantData, \*\*kwargs: Any) → UpdateTenantResponse200

Update tenant

> Updates an existing tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*UpdateTenantData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateTenantResponse200 | UpdateTenantResponse400 | UpdateTenantResponse403 | UpdateTenantResponse404 | UpdateTenantResponse500 | UpdateTenantResponse503]

#### *async* update_tenant_async(tenant_id: str, , data: UpdateTenantData, \*\*kwargs: Any) → UpdateTenantResponse200

Update tenant

> Updates an existing tenant.
* **Parameters:**
  * **tenant_id** (*str*) – The unique identifier of the tenant. Example: customer-service.
  * **body** (*UpdateTenantData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateTenantResponse200 | UpdateTenantResponse400 | UpdateTenantResponse403 | UpdateTenantResponse404 | UpdateTenantResponse500 | UpdateTenantResponse503]

#### update_user(username: str, , data: UpdateUserData, \*\*kwargs: Any) → UpdateUserResponse200

Update user

> Updates a user.
* **Parameters:**
  * **username** (*str*) – The unique name of a user. Example: swillis.
  * **body** (*UpdateUserData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateUserResponse200 | UpdateUserResponse400 | UpdateUserResponse403 | UpdateUserResponse404 | UpdateUserResponse500 | UpdateUserResponse503]

#### *async* update_user_async(username: str, , data: UpdateUserData, \*\*kwargs: Any) → UpdateUserResponse200

Update user

> Updates a user.
* **Parameters:**
  * **username** (*str*) – The unique name of a user. Example: swillis.
  * **body** (*UpdateUserData*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[UpdateUserResponse200 | UpdateUserResponse400 | UpdateUserResponse403 | UpdateUserResponse404 | UpdateUserResponse500 | UpdateUserResponse503]

#### update_user_task(user_task_key: str, \*, data: UpdateUserTaskData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Update user task

> Update a user task with the given key.
* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **body** (*UpdateUserTaskData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UpdateUserTaskResponse400 | UpdateUserTaskResponse404 | UpdateUserTaskResponse409 | UpdateUserTaskResponse500 | UpdateUserTaskResponse503]

#### *async* update_user_task_async(user_task_key: str, \*, data: UpdateUserTaskData | Unset = `<camunda_orchestration_sdk.types.Unset object>`, \*\*kwargs: Any) → Any

Update user task

> Update a user task with the given key.
* **Parameters:**
  * **user_task_key** (*str*) – System-generated key for a user task.
  * **body** (*UpdateUserTaskData* *|* *Unset*)
* **Raises:**
  * **errors.UnexpectedStatus** – If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
  * **httpx.TimeoutException** – If the request takes longer than Client.timeout.
* **Returns:**
  Response[Any | UpdateUserTaskResponse400 | UpdateUserTaskResponse404 | UpdateUserTaskResponse409 | UpdateUserTaskResponse500 | UpdateUserTaskResponse503]

### *class* camunda_orchestration_sdk.Client(base_url: str, , raise_on_unexpected_status: bool = False, cookies: dict[str, str] = NOTHING, headers: dict[str, str] = NOTHING, timeout: Timeout | None = None, verify_ssl: str | bool | SSLContext = True, follow_redirects: bool = False, httpx_args: dict[str, Any] = NOTHING)

Bases: `object`

A class for keeping track of data related to the API

The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

> `base_url`: The base URL for the API, all requests are made to a relative path to this URL

> `cookies`: A dictionary of cookies to be sent with every request

> `headers`: A dictionary of headers to be sent with every request

> `timeout`: The maximum amount of a time a request can take. API functions will raise
> httpx.TimeoutException if this is exceeded.

> `verify_ssl`: Whether or not to verify the SSL certificate of the API server. This should be True in production,
> but can be set to False for testing purposes.

> `follow_redirects`: Whether or not to follow redirects. Default value is False.

> `httpx_args`: A dictionary of additional arguments to be passed to the `httpx.Client` and `httpx.AsyncClient` constructor.

#### raise_on_unexpected_status

Whether or not to raise an errors.UnexpectedStatus if the API returns a
status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
argument to the constructor.

* **Type:**
  bool

#### get_async_httpx_client() → AsyncClient

Get the underlying httpx.AsyncClient, constructing a new one if not previously set

#### get_httpx_client() → Client

Get the underlying httpx.Client, constructing a new one if not previously set

#### raise_on_unexpected_status *: bool*

#### set_async_httpx_client(async_client: AsyncClient) → [Client](#camunda_orchestration_sdk.Client)

Manually set the underlying httpx.AsyncClient

**NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.

#### set_httpx_client(client: Client) → [Client](#camunda_orchestration_sdk.Client)

Manually set the underlying httpx.Client

**NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.

#### with_cookies(cookies: dict[str, str]) → [Client](#camunda_orchestration_sdk.Client)

Get a new client matching this one with additional cookies

#### with_headers(headers: dict[str, str]) → [Client](#camunda_orchestration_sdk.Client)

Get a new client matching this one with additional headers

#### with_timeout(timeout: Timeout) → [Client](#camunda_orchestration_sdk.Client)

Get a new client matching this one with a new timeout configuration

### *class* camunda_orchestration_sdk.WorkerConfig(job_type: str, job_timeout_milliseconds: int, request_timeout_milliseconds: int = 0, max_concurrent_jobs: int = 10, execution_strategy: Literal['thread', 'process', 'async', 'auto'] = 'auto', fetch_variables: list[str] | None = None, worker_name: str = 'camunda-python-sdk-worker')

Bases: `object`

User-facing configuration

#### execution_strategy *: Literal['thread', 'process', 'async', 'auto']* *= 'auto'*

#### fetch_variables *: list[str] | None* *= None*

#### job_timeout_milliseconds *: int*

Long-poll request timeout in milliseconds. Defaults to 0, which allows the server to set the request timeout

#### job_type *: str*

How long the job is reserved for this worker only

#### max_concurrent_jobs *: int* *= 10*

#### request_timeout_milliseconds *: int* *= 0*

#### worker_name *: str* *= 'camunda-python-sdk-worker'*
