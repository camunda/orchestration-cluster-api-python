"""Runtime enforcement of the `x-present-when` lease coupling.

The generated table (`present_when_generated.py`) is the ground truth; these guards assert
the runtime still matches every marker the bundled spec declares, and that every declared
coupling has a runtime path enforcing it. Scoped to the class of defect, not the lease
instance, so a second `x-present-when` field added upstream cannot slip past unnoticed.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from camunda_orchestration_sdk.runtime.present_when import (
    ENFORCED_COUPLINGS,
    LeaseNotHonoredError,
    coupling_key,
    lease_request_flag,
    require_lease_presence,
)
from camunda_orchestration_sdk.runtime.present_when_generated import PRESENT_WHEN_COUPLINGS

_SPEC = Path(__file__).resolve().parents[2] / "external-spec" / "bundled" / "rest-api.bundle.json"


def _couplings_declared_by_spec() -> set[tuple[str, str, str]]:
    spec = json.loads(_SPEC.read_text(encoding="utf-8"))
    schemas = spec.get("components", {}).get("schemas", {})
    out: set[tuple[str, str, str]] = set()
    for schema_name, schema in schemas.items():
        props = schema.get("properties") if isinstance(schema, dict) else None
        if not isinstance(props, dict):
            continue
        for field_name, field in props.items():
            if not isinstance(field, dict) or "x-present-when" not in field:
                continue
            marker = field["x-present-when"]
            out.add((schema_name, field_name, marker["request"]))
    return out


def test_generated_table_matches_the_spec() -> None:
    if not _SPEC.exists():
        pytest.skip("bundled spec not present")
    declared = _couplings_declared_by_spec()
    assert declared, "spec declares no x-present-when markers; this guard must not pass vacuously"
    generated = {
        (c.response_schema, c.response_field, c.request_flag) for c in PRESENT_WHEN_COUPLINGS
    }
    assert generated == declared


def test_every_declared_coupling_is_enforced() -> None:
    for c in PRESENT_WHEN_COUPLINGS:
        assert coupling_key(c) in ENFORCED_COUPLINGS, (
            f"spec declares dependent presence for {coupling_key(c)} (when {c.request_flag!r} is "
            "set) but no runtime path enforces it"
        )


def test_every_enforced_coupling_is_declared() -> None:
    declared = {coupling_key(c) for c in PRESENT_WHEN_COUPLINGS}
    for key in ENFORCED_COUPLINGS:
        assert key in declared, f"runtime enforces {key} but the spec no longer declares it"


def test_lease_flag_is_read_from_the_table() -> None:
    assert lease_request_flag() == "withLease"


def test_require_lease_presence_covers_every_case() -> None:
    # requested and honoured
    require_lease_presence(True, "1", "tok")
    # not requested, none returned
    require_lease_presence(False, "1", None)
    # not requested, one returned anyway
    require_lease_presence(False, "1", "tok")
    # requested but empty token is as good as none
    with pytest.raises(LeaseNotHonoredError):
        require_lease_presence(True, "1", "")
    # requested but not honoured — carries the offending job key and the flag
    with pytest.raises(LeaseNotHonoredError) as exc:
        require_lease_presence(True, "job-9", None)
    assert exc.value.job_key == "job-9"
    assert exc.value.request_flag == "withLease"


def _wire_job(**overrides: object) -> dict[str, object]:
    """A realistic activate-jobs job object, as a server actually sends it."""
    job: dict[str, object] = {
        "type": "greet",
        "processDefinitionId": "p",
        "processDefinitionVersion": 1,
        "elementId": "e",
        "customHeaders": {},
        "worker": "w",
        "retries": 3,
        "deadline": 1_700_000_000_000,
        "variables": {},
        "tenantId": "<default>",
        "jobKey": "1",
        "processInstanceKey": "2",
        "processDefinitionKey": "3",
        "elementInstanceKey": "4",
        "kind": "BPMN_ELEMENT",
        "listenerEventType": "UNSPECIFIED",
        "userTask": None,
        "tags": [],
        "rootProcessInstanceKey": None,
        "businessId": None,
        "priority": 0,
        "physicalTenantId": "pt",
    }
    job.update(overrides)
    return job


def test_marker_declared_fields_tolerate_an_absent_key() -> None:
    """`x-present-when` means the key is *absent*, not null, when the flag was not set.

    Scoped to the class of defect: every marker-declared field must survive omission, not
    just the lease token. A bare `d.pop("field")` raises KeyError and fails the whole
    activation before any runtime guard can see it — which would break unleased (default)
    workers too, not only leased ones.
    """
    from camunda_orchestration_sdk import models as _models

    for c in PRESENT_WHEN_COUPLINGS:
        model = getattr(_models, c.response_schema)
        assert hasattr(model, "from_dict"), f"{c.response_schema} has no from_dict"
        if c.response_schema != "ActivatedJobResult":
            # Only ActivatedJobResult has a wire fixture here; other schemas would need
            # their own. Assert the parser source is tolerant instead.
            import inspect

            src = inspect.getsource(model.from_dict)
            assert f'"{c.response_field}")' not in src, (
                f"{c.response_schema}.from_dict pops {c.response_field} without a default"
            )
            continue

        # Absent — the shape the marker describes for an unleased activation.
        parsed = model.from_dict(_wire_job())
        assert getattr(parsed, "job_lease_token", "sentinel") is None
        # Explicitly null, and present — both must still work.
        assert model.from_dict(_wire_job(jobLeaseToken=None)).job_lease_token is None
        assert model.from_dict(_wire_job(jobLeaseToken="tok")).job_lease_token == "tok"
