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


_BUNDLED_SCHEMAS = _hook._load_schemas(
    _root / "external-spec" / "bundled" / "rest-api.bundle.json"
)


@pytest.mark.parametrize(
    ("schema", "module", "wire_name", "default"),
    [(s, m, w, d) for s, m, w, d, _ in _hook.VERSION_SKEW_DEFAULTS],
)
def test_every_declared_field_is_defaulted_in_the_generated_model(
    schema: str, module: str, wire_name: str, default: str
) -> None:
    assert wire_name in _hook._required(_BUNDLED_SCHEMAS, schema), (
        f"the committed bundle no longer requires {schema}.{wire_name}; drop the entry"
    )
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


def test_run_skips_an_entry_the_spec_does_not_require(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = tmp_path / "spec.json"
    spec.write_text('{"components": {"schemas": {"Model": {"required": ["other"]}}}}')
    models = tmp_path / "camunda_orchestration_sdk" / "models"
    models.mkdir(parents=True)
    monkeypatch.setattr(
        _hook, "VERSION_SKEW_DEFAULTS", [("Model", "model", "flag", "False", "test")]
    )

    _hook.run({"out_dir": str(tmp_path), "bundled_spec_path": str(spec)})

    assert not (models / "model.py").exists()


def test_run_rejects_a_required_entry_with_no_matching_pop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = tmp_path / "spec.json"
    spec.write_text('{"components": {"schemas": {"Model": {"required": ["flag"]}}}}')
    models = tmp_path / "camunda_orchestration_sdk" / "models"
    models.mkdir(parents=True)
    (models / "model.py").write_text('x = d.pop("renamed")\n')
    monkeypatch.setattr(
        _hook, "VERSION_SKEW_DEFAULTS", [("Model", "model", "flag", "False", "test")]
    )

    with pytest.raises(SystemExit, match="found 0"):
        _hook.run({"out_dir": str(tmp_path), "bundled_spec_path": str(spec)})


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
