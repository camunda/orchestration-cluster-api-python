"""Tests for hooks/post_gen/0350_generate_present_when.py.

Class-scoped guards on the `x-present-when` derivation: the runtime table only compares the
committed output with the spec, so without these a regression in multi-marker emission,
malformed/null-marker rejection, escaping, or idempotency would pass until regeneration
drift is noticed.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import pytest

_hook_path = (
    Path(__file__).resolve().parents[2] / "hooks" / "post_gen" / "0350_generate_present_when.py"
)
_spec = importlib.util.spec_from_file_location("_present_when_hook", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)

derive_couplings = _hook.derive_couplings
render = _hook.render


def _schema_with_marker(marker: Any) -> dict[str, Any]:
    return {"Resp": {"properties": {"tok": {"type": "string", "x-present-when": marker}}}}


def test_derives_multiple_markers_sorted() -> None:
    schemas = {
        "Beta": {"properties": {"b": {"x-present-when": {"request": "flagB", "equals": True}}}},
        "Alpha": {
            "properties": {
                "z": {"x-present-when": {"request": "flagZ", "equals": True}},
                "a": {"x-present-when": {"request": "flagA", "equals": True}},
            }
        },
    }
    # Sorted by schema then field, so the emitted table is stable across regenerations.
    assert derive_couplings(schemas) == [
        ("Alpha", "a", "flagA"),
        ("Alpha", "z", "flagZ"),
        ("Beta", "b", "flagB"),
    ]


def test_ignores_fields_without_a_marker() -> None:
    schemas = {
        "Resp": {
            "properties": {
                "plain": {"type": "string"},
                "tok": {"x-present-when": {"request": "withLease", "equals": True}},
            }
        }
    }
    assert derive_couplings(schemas) == [("Resp", "tok", "withLease")]


@pytest.mark.parametrize(
    "marker",
    [
        None,  # explicit null
        "withLease",  # not an object
        {"equals": True},  # missing request
        {"request": "", "equals": True},  # empty request
        {"request": 1, "equals": True},  # non-string request
        {"request": "withLease", "equals": False},  # equals not true
        {"request": "withLease"},  # equals missing
    ],
)
def test_rejects_every_malformed_marker_shape(marker: Any) -> None:
    # Each is a distinct way the marker can be wrong; all must fail loudly rather than be
    # silently dropped (which would retire the runtime guard for that field).
    with pytest.raises(SystemExit):
        derive_couplings(_schema_with_marker(marker))


def test_empty_result_is_an_error() -> None:
    with pytest.raises(SystemExit):
        derive_couplings({"Resp": {"properties": {"x": {"type": "string"}}}})


def test_render_escapes_quotes_and_backslashes() -> None:
    out = render([("Sch", 'fie"ld', "fl\\ag")])
    # repr() escaping keeps the emitted module valid Python.
    assert "'fie\"ld'" in out or '"fie\\"ld"' in out
    assert "'fl\\\\ag'" in out


def test_render_is_valid_python_and_stable() -> None:
    couplings = [("ActivatedJobResult", "jobLeaseToken", "withLease")]
    first = render(couplings)
    second = render(couplings)
    assert first == second
    ns: dict[str, Any] = {}
    exec(compile(first, "<generated>", "exec"), ns)
    table = ns["PRESENT_WHEN_COUPLINGS"]
    assert len(table) == 1
    assert table[0].response_schema == "ActivatedJobResult"
    assert table[0].request_flag == "withLease"


tolerate_absent_field = _hook.tolerate_absent_field


def test_tolerate_absent_field_defaults_the_pop() -> None:
    src = '_raw = _parse(d.pop("jobLeaseToken"))'
    assert tolerate_absent_field(src, "jobLeaseToken") == '_raw = _parse(d.pop("jobLeaseToken", None))'


def test_tolerate_absent_field_is_idempotent() -> None:
    once = tolerate_absent_field('d.pop("jobLeaseToken")', "jobLeaseToken")
    assert tolerate_absent_field(once, "jobLeaseToken") == once


def test_tolerate_absent_field_leaves_other_fields_alone() -> None:
    src = 'a = d.pop("other")\nb = d.pop("jobLeaseToken")'
    out = tolerate_absent_field(src, "jobLeaseToken")
    assert 'd.pop("other")' in out
    assert 'd.pop("jobLeaseToken", None)' in out


def test_tolerate_absent_field_does_not_match_a_prefix() -> None:
    # "job" must not rewrite "jobLeaseToken"; the pattern is anchored to the whole key.
    src = 'd.pop("jobLeaseToken")'
    assert tolerate_absent_field(src, "job") == src
