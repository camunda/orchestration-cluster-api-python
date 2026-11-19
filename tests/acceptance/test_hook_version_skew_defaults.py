"""Tests for hooks/post_gen/0460_version_skew_defaults.py.

A spec-required field that older servers omit must decode with its default,
and every declared entry must still match the generated code.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from camunda_orchestration_sdk.errors import MissingRequiredFieldError

_root = Path(__file__).resolve().parents[2]
_hook_path = _root / "hooks" / "post_gen" / "0460_version_skew_defaults.py"
_spec = importlib.util.spec_from_file_location("_version_skew_hook", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)

_MODELS = _root / "generated" / "camunda_orchestration_sdk" / "models"


@pytest.mark.parametrize(
    ("module", "wire_name", "default"),
    [(m, w, d) for m, w, d, _ in _hook.VERSION_SKEW_DEFAULTS],
)
def test_every_declared_field_is_defaulted_in_the_generated_model(
    module: str, wire_name: str, default: str
) -> None:
    source = (_MODELS / f"{module}.py").read_text(encoding="utf-8")
    assert f'd.pop("{wire_name}", {default})' in source
    assert f'd.pop_required("{wire_name}")' not in source


def test_apply_is_idempotent() -> None:
    once = _hook.apply('x = d.pop("flag")\n', "flag", "False")
    assert once == 'x = d.pop("flag", False)\n'
    assert _hook.apply(once, "flag", "False") == once


def test_apply_rejects_a_field_that_no_longer_matches() -> None:
    with pytest.raises(SystemExit, match=r'd\.pop\("flag"\), found 0'):
        _hook.apply('x = d.pop("renamed")\n', "flag", "False")


def test_authenticated_user_from_a_server_predating_is_anonymous_decodes() -> None:
    from camunda_orchestration_sdk.models.camunda_user_result import CamundaUserResult

    older_server_response = {
        "username": "demo",
        "displayName": "Demo User",
        "email": "demo@example.com",
        "authorizedComponents": ["*"],
        "tenants": [],
        "groups": [],
        "roles": [],
        "salesPlanType": None,
        "c8Links": {},
        "canLogout": True,
    }
    user = CamundaUserResult.from_dict(older_server_response)
    assert user.is_anonymous is False
    assert user.username == "demo"


def test_deployment_configuration_from_a_server_predating_wait_states_decodes() -> None:
    from camunda_orchestration_sdk.models.deployment_configuration_response import (
        DeploymentConfigurationResponse,
    )

    config = DeploymentConfigurationResponse.from_dict(
        {
            "isMultiTenancyEnabled": False,
            "isTenantsApiEnabled": True,
            "maxRequestSize": 4194304,
        }
    )
    assert config.is_wait_states_enabled is False
    assert config.max_request_size == 4194304


def test_other_required_fields_are_still_enforced() -> None:
    from camunda_orchestration_sdk.models.camunda_user_result import CamundaUserResult

    with pytest.raises(MissingRequiredFieldError):
        CamundaUserResult.from_dict({"isAnonymous": False})
