"""Single source of truth for v9 → v10 model class renames.

Each key is the old (v9) class name; the value is the new (v10) class name.
Used by the deprecated-aliases hook and acceptance tests.
"""

RENAMES_V9_TO_V10: dict[str, str] = {
    "CreateMappingRuleResponse201": "MappingRuleCreateResult",
    "GetUserResponse200": "UserResult",
    "SearchClientsForGroupData": "GroupClientSearchQueryRequest",
    "SearchClientsForGroupResponse200": "GroupClientSearchResult",
    "SearchClientsForRoleData": "RoleClientSearchQueryRequest",
    "SearchClientsForRoleResponse200": "RoleClientSearchResult",
    "SearchClientsForTenantData": "TenantClientSearchQueryRequest",
    "SearchClientsForTenantResponse200": "TenantClientSearchResult",
    "SearchMappingRuleResponse200": "MappingRuleSearchQueryResult",
    "SearchMappingRulesForGroupResponse200": "GroupMappingRuleSearchResult",
    "SearchMappingRulesForRoleResponse200": "RoleMappingRuleSearchResult",
    "SearchMappingRulesForTenantResponse200": "TenantMappingRuleSearchResult",
    "SearchRolesForGroupResponse200": "GroupRoleSearchResult",
    "SearchRolesForTenantResponse200": "TenantRoleSearchResult",
    "SearchUserTaskEffectiveVariablesData": "UserTaskEffectiveVariableSearchQueryRequest",
    "SearchUserTaskVariablesData": "UserTaskVariableSearchQueryRequest",
    "SearchUsersForGroupData": "GroupUserSearchQueryRequest",
    "SearchUsersForGroupResponse200": "GroupUserSearchResult",
    "SearchUsersForRoleData": "RoleUserSearchQueryRequest",
    "SearchUsersForRoleResponse200": "RoleUserSearchResult",
    "SearchUsersForTenantData": "TenantUserSearchQueryRequest",
    "SearchUsersForTenantResponse200": "TenantUserSearchResult",
    "SearchUsersResponse200": "UserSearchResult",
    "SearchVariablesData": "VariableSearchQuery",
    "UpdateMappingRuleResponse200": "MappingRuleUpdateResult",
    "UpdateUserResponse200": "UserUpdateResult",
}
