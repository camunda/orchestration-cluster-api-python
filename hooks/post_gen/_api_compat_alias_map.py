"""Single source of truth for deprecated model class renames.

Each key is the old class name; the value is the current class name it now
resolves to. Used by the deprecated-aliases hook and acceptance tests.

Two maps are kept, keyed by the release boundary at which the rename happened,
so the deprecation vintage of each alias stays legible:

- ``RENAMES_V9_TO_V10`` — names renamed between the v9 and v10 majors.
- ``RENAMES_V10_0_TO_V10_1`` — names removed/renamed by an upstream spec
  backport within the 10.x line (e.g. the ``stable/8.10`` backport that folded
  the shared process-creation fields into ``ProcessInstanceCreationInstructionBase``).

``ALL_RENAMES`` is the merged view the hook actually emits.
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

# Renames introduced within the 10.x line by an upstream spec backport.
#
# camunda/camunda stable/8.10 backported the refactor that folds the shared
# process-creation fields into ProcessInstanceCreationInstructionBase. As a
# result the generator stopped emitting the per-reference *Variables classes and
# now emits a single ProcessInstanceCreationInstructionBaseVariables. v10.0.0
# exported the old names publicly, so they are kept as deprecated aliases for the
# 10.x line rather than removed in a minor release.
RENAMES_V10_0_TO_V10_1: dict[str, str] = {
    "ProcessInstanceCreationInstructionByKeyVariables": "ProcessInstanceCreationInstructionBaseVariables",
    "ProcessInstanceCreationInstructionByIdVariables": "ProcessInstanceCreationInstructionBaseVariables",
}

# Merged view consumed by the deprecated-aliases hook.
ALL_RENAMES: dict[str, str] = {**RENAMES_V9_TO_V10, **RENAMES_V10_0_TO_V10_1}
