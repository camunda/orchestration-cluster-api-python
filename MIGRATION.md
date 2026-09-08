# Migration guide: v9 → v10 (Camunda 8.9 → 8.10)

`camunda-orchestration-sdk` v10 targets Camunda 8.10. This guide covers **only the
changes that require you to edit code**. The 8.10 API is overwhelmingly additive —
62 new client methods and nothing removed — so most upgrades touch a handful of call
sites.

```bash
uv add "camunda-orchestration-sdk>=10,<11"
# or: pip install "camunda-orchestration-sdk>=10,<11"
```

## At a glance

| # | Change | Action required |
|---|--------|-----------------|
| 1 | [Identifier arguments are now semantic types](#1-identifier-arguments-are-now-semantic-types) | **Yes** — wrap identifiers at the boundary |
| 2 | [`get_resource_content` returns an object, and there is a new binary endpoint](#2-get_resource_content-returns-an-object-and-there-is-a-new-binary-endpoint) | **Yes**, if you call it |
| 3 | [26 model classes renamed](#3-model-class-renames-deprecated-not-removed) | No — old names still work, with a warning |

No client method was removed or renamed, and no module disappeared. See
[What does not change](#what-does-not-change).

---

## 1. Identifier arguments are now semantic types

Four identifier types moved from plain `str` to semantic types. The brand
constructors are `str` subclasses, so wrapped values stay valid anywhere a `str` is
expected — f-strings, logging, JSON serialisation. Only the **input** side changes.

Wrap once at your application boundary. The constructor validates the upstream
pattern and length constraints and raises `ValueError` on a malformed identifier, so
a bad value fails fast locally instead of coming back as an HTTP 400.

```python
from camunda_orchestration_sdk import CamundaClient, GroupId, RoleId

with CamundaClient() as client:
    # v9 — plain strings were accepted
    client.assign_role_to_group(role_id="developer", group_id="engineering")

    # v10 — wrap with the semantic type at the boundary
    client.assign_role_to_group(
        role_id=RoleId("developer"),
        group_id=GroupId("engineering"),
    )
```

### Affected methods

| Semantic type | Methods |
|---|---|
| `GroupId` (17) | `assign_client_to_group`, `assign_group_to_tenant`, `assign_mapping_rule_to_group`, `assign_role_to_group`, `assign_user_to_group`, `delete_group`, `get_group`, `search_clients_for_group`, `search_mapping_rules_for_group`, `search_roles_for_group`, `search_users_for_group`, `unassign_client_from_group`, `unassign_group_from_tenant`, `unassign_mapping_rule_from_group`, `unassign_role_from_group`, `unassign_user_from_group`, `update_group` |
| `RoleId` (17) | `assign_role_to_client`, `assign_role_to_group`, `assign_role_to_mapping_rule`, `assign_role_to_tenant`, `assign_role_to_user`, `delete_role`, `get_role`, `search_clients_for_role`, `search_groups_for_role`, `search_mapping_rules_for_role`, `search_users_for_role`, `unassign_role_from_client`, `unassign_role_from_group`, `unassign_role_from_mapping_rule`, `unassign_role_from_tenant`, `unassign_role_from_user`, `update_role` |
| `MappingRuleId` (9) | `assign_mapping_rule_to_group`, `assign_mapping_rule_to_tenant`, `assign_role_to_mapping_rule`, `delete_mapping_rule`, `get_mapping_rule`, `unassign_mapping_rule_from_group`, `unassign_mapping_rule_from_tenant`, `unassign_role_from_mapping_rule`, `update_mapping_rule` |
| `ClientId` (6) | `assign_client_to_group`, `assign_client_to_tenant`, `assign_role_to_client`, `unassign_client_from_group`, `unassign_client_from_tenant`, `unassign_role_from_client` |

Reading values back needs no change — they are still strings.

All semantic types are importable from `camunda_orchestration_sdk` or
`camunda_orchestration_sdk.semantic_types`.

## 2. `get_resource_content` returns an object, and there is a new binary endpoint

```python
# v9
def get_resource_content(...) -> str: ...

# v10
def get_resource_content(...) -> GetResourceContentResponse200: ...
def get_resource_content_binary(...) -> File: ...   # new in v10
```

Two things changed. `GET /resources/{resourceKey}/content` has always been declared
`application/json` upstream — the v9 `str` return was the generator flattening that
JSON response, not the resource bytes. v10 types it honestly as an object. Separately,
8.10 adds `GET /resources/{resourceKey}/content/binary`, which serves
`application/octet-stream`.

**If you wanted the raw resource** — BPMN XML, a DMN file, a form — use the new binary
endpoint:

```python
from pathlib import Path

# v10 — raw bytes from the new binary endpoint
resource = client.get_resource_content_binary(resource_key=key)
Path("process.bpmn").write_bytes(resource.payload.read())
```

**If you wanted the JSON metadata**, keep `get_resource_content` and read the parsed
object. It behaves like a mapping:

```python
import json
from pathlib import Path

content = client.get_resource_content(resource_key=key)
print(content["resourceName"])                      # subscript access
Path("resource.json").write_text(json.dumps(content.to_dict()))
```

`get_resource_content` is the only client method whose return type changed.

## 3. Model class renames (deprecated, not removed)

26 model classes were renamed to match upstream conventions. **No action is required
to upgrade.** The old names still resolve, emitting a `DeprecationWarning`, and will
be removed in v11. Updating imports is recommended.

```python
>>> import camunda_orchestration_sdk.models as m
>>> m.CreateMappingRuleResponse201
DeprecationWarning: CreateMappingRuleResponse201 is deprecated,
use MappingRuleCreateResult instead. Will be removed in the next major version.
<class '...MappingRuleCreateResult'>
```

| Old name (deprecated) | New name |
|---|---|
| `CreateMappingRuleResponse201` | `MappingRuleCreateResult` |
| `GetUserResponse200` | `UserResult` |
| `SearchClientsForGroupData` | `GroupClientSearchQueryRequest` |
| `SearchClientsForGroupResponse200` | `GroupClientSearchResult` |
| `SearchClientsForRoleData` | `RoleClientSearchQueryRequest` |
| `SearchClientsForRoleResponse200` | `RoleClientSearchResult` |
| `SearchClientsForTenantData` | `TenantClientSearchQueryRequest` |
| `SearchClientsForTenantResponse200` | `TenantClientSearchResult` |
| `SearchMappingRuleResponse200` | `MappingRuleSearchQueryResult` |
| `SearchMappingRulesForGroupResponse200` | `GroupMappingRuleSearchResult` |
| `SearchMappingRulesForRoleResponse200` | `RoleMappingRuleSearchResult` |
| `SearchMappingRulesForTenantResponse200` | `TenantMappingRuleSearchResult` |
| `SearchRolesForGroupResponse200` | `GroupRoleSearchResult` |
| `SearchRolesForTenantResponse200` | `TenantRoleSearchResult` |
| `SearchUserTaskEffectiveVariablesData` | `UserTaskEffectiveVariableSearchQueryRequest` |
| `SearchUserTaskVariablesData` | `UserTaskVariableSearchQueryRequest` |
| `SearchUsersForGroupData` | `GroupUserSearchQueryRequest` |
| `SearchUsersForGroupResponse200` | `GroupUserSearchResult` |
| `SearchUsersForRoleData` | `RoleUserSearchQueryRequest` |
| `SearchUsersForRoleResponse200` | `RoleUserSearchResult` |
| `SearchUsersForTenantData` | `TenantUserSearchQueryRequest` |
| `SearchUsersForTenantResponse200` | `TenantUserSearchResult` |
| `SearchUsersResponse200` | `UserSearchResult` |
| `SearchVariablesData` | `VariableSearchQuery` |
| `UpdateMappingRuleResponse200` | `MappingRuleUpdateResult` |
| `UpdateUserResponse200` | `UserUpdateResult` |

To find affected imports, run your test suite with warnings visible:

```bash
uv run python -W error::DeprecationWarning -m pytest
```

---

## What does not change

Verified by diffing the generated surface of `stable/9` against `main`:

- **No client method was removed or renamed.** The count went from 200 to 262 —
  every change is additive. Method names and arity are unchanged.
- **No module was removed.** Stub modules went from 819 to 1,136.
- **No model class was removed.** The 26 renames are aliased, not deleted.
- **The wire format is unchanged.** Semantic types serialise as the strings they
  already were.
- **Existing valid v9 identifiers still satisfy the new constraints** — the
  patterns are permissive supersets of typical identifiers.
- **62 new client methods** are available. They are additive and need no migration.

## How this guide was produced

Derived by comparing the `stable/9` and `main` generated surfaces directly, using
the checked-in `stubs/` tree as the API surface:

```bash
git archive origin/stable/9 stubs | tar -x -C /tmp/py-v9
# then diff /tmp/py-v9/stubs/.../client.pyi against stubs/.../client.pyi
```

The underlying OpenAPI specs were also compared (`stable/8.9` vs `stable/8.10`):
183 → 243 operations, 547 → 753 schemas, with no operation, schema, property or
enum value removed.

Two traps worth recording for whoever writes the next one of these:

- 8.10 refactored the search filters into `allOf: [XFilterFields, {$or}]`. A naive
  schema diff reports every filter field as *removed*, because the fields now sit one
  level down in the composition. They are not removed — `GroupFilterFields.properties`
  is identical to v9's `GroupFilter.properties`. Flatten `allOf` before comparing.
- A previous draft of this guide listed `CancelProcessInstanceData`,
  `DeleteDecisionInstanceData` and `DeleteProcessInstanceData` as removed request-body
  classes and "a hard break". Those names have never existed in the Python SDK — they
  are TypeScript-generator naming that was transcribed across. Verify class names
  against this repo's own output before documenting them.
