"""
Behavioral regression tests for semantic types.

These tests document the contract that users depend on when constructing,
serialising, deserialising, and comparing semantic-typed values.  They must
pass identically regardless of the underlying implementation strategy
(NewType, class-based, or any future approach).

The tests are grouped into classes that each target a specific concern:
    - Construction & validation (lifter + direct constructor)
    - str-subtype contract (isinstance, str operations)
    - JSON serialisation round-trip
    - Equality and hashing
    - Disjointness between semantic key types
    - Model from_dict / to_dict round-trip
    - try_lift variants
    - Copy / pickle safety
"""

from __future__ import annotations

import copy
import json
import pickle
from typing import Any, Callable

import pytest

from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionKey,
    ElementInstanceKey,
    JobKey,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    UserTaskKey,
    VariableKey,
    lift_decision_definition_key,
    lift_element_instance_key,
    lift_job_key,
    lift_process_definition_id,
    lift_process_definition_key,
    lift_process_instance_key,
    lift_tenant_id,
    lift_user_task_key,
    lift_variable_key,
    try_lift_process_definition_key,
    try_lift_process_instance_key,
)

# Type alias for a lifter function: takes Any, returns str
Lifter = Callable[[Any], str]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Representative sample of (lifter, newtype_alias, valid_value) triples covering
# every constraint category: pattern+minLen+maxLen, pattern-only, enum, unconstrained.
STR_KEY_SAMPLES: list[tuple[Lifter, Callable[..., Any], str]] = [
    (lift_process_definition_key, ProcessDefinitionKey, "12345"),
    (lift_process_instance_key, ProcessInstanceKey, "67890"),
    (lift_decision_definition_key, DecisionDefinitionKey, "111"),
    (lift_element_instance_key, ElementInstanceKey, "222"),
    (lift_job_key, JobKey, "333"),
    (lift_user_task_key, UserTaskKey, "444"),
    (lift_variable_key, VariableKey, "555"),
]

# All key-type lifters that share the numeric-string pattern ^-?[0-9]+$
NUMERIC_KEY_LIFTERS: list[Lifter] = [
    lift_process_definition_key,
    lift_process_instance_key,
    lift_decision_definition_key,
    lift_element_instance_key,
    lift_job_key,
    lift_user_task_key,
    lift_variable_key,
]


# ===================================================================
# 1 · Construction & validation
# ===================================================================


class TestConstruction:
    """Lifters accept valid input and reject invalid input."""

    @pytest.mark.parametrize(
        "lifter,_type,value",
        STR_KEY_SAMPLES,
        ids=lambda x: x.__name__ if callable(x) else str(x),  # type: ignore[union-attr]
    )
    def test_lifter_returns_value_for_valid_input(
        self, lifter: Lifter, _type: Callable[..., Any], value: str
    ) -> None:
        result = lifter(value)
        assert result == value

    @pytest.mark.parametrize(
        "lifter", NUMERIC_KEY_LIFTERS, ids=lambda fn: fn.__name__
    )
    def test_lifter_rejects_non_numeric_string(self, lifter: Lifter) -> None:
        with pytest.raises(ValueError, match="does not match pattern"):
            lifter("not-a-number")

    @pytest.mark.parametrize(
        "lifter", NUMERIC_KEY_LIFTERS, ids=lambda fn: fn.__name__
    )
    def test_lifter_rejects_non_str_type(self, lifter: Lifter) -> None:
        with pytest.raises(TypeError, match="must be str"):
            lifter(12345)

    @pytest.mark.parametrize(
        "lifter", NUMERIC_KEY_LIFTERS, ids=lambda fn: fn.__name__
    )
    def test_lifter_rejects_empty_string(self, lifter: Lifter) -> None:
        with pytest.raises(ValueError):
            lifter("")

    def test_lifter_rejects_string_exceeding_max_length(self) -> None:
        with pytest.raises(ValueError, match="longer than maxLength"):
            lift_process_definition_key("1" * 26)

    def test_lifter_accepts_negative_numeric_key(self) -> None:
        result = lift_process_definition_key("-42")
        assert result == "-42"

    def test_process_definition_id_pattern_validation(self) -> None:
        val = lift_process_definition_id("my_process_v1")
        assert val == "my_process_v1"

    def test_process_definition_id_rejects_leading_special_char(self) -> None:
        with pytest.raises(ValueError, match="does not match pattern"):
            lift_process_definition_id("!invalid")

    def test_tenant_id_accepts_default(self) -> None:
        val = lift_tenant_id("<default>")
        assert val == "<default>"

    def test_tenant_id_accepts_alphanumeric(self) -> None:
        val = lift_tenant_id("my_tenant-1")
        assert val == "my_tenant-1"


# ===================================================================
# 2 · str-subtype contract
# ===================================================================


class TestStrSubtype:
    """Semantic types must behave as str at runtime for user code that
    passes them to standard library functions, HTTP clients, etc."""

    @pytest.mark.parametrize(
        "lifter,_type,value",
        STR_KEY_SAMPLES,
        ids=lambda x: x.__name__ if callable(x) else str(x),  # type: ignore[union-attr]
    )
    def test_isinstance_str(
        self, lifter: Lifter, _type: Callable[..., Any], value: str
    ) -> None:
        result = lifter(value)
        assert isinstance(result, str)

    def test_str_builtin_returns_same_value(self) -> None:
        key = lift_process_definition_key("12345")
        assert str(key) == "12345"

    def test_string_concatenation(self) -> None:
        key = lift_process_definition_key("100")
        assert "key=" + key == "key=100"

    def test_string_slicing(self) -> None:
        key = lift_process_definition_key("12345")
        assert key[:3] == "123"

    def test_string_format(self) -> None:
        key = lift_process_definition_key("42")
        assert f"Process {key}" == "Process 42"

    def test_len(self) -> None:
        key = lift_process_definition_key("12345")
        assert len(key) == 5

    def test_in_operator(self) -> None:
        key = lift_process_definition_key("12345")
        assert "234" in key


# ===================================================================
# 3 · JSON serialisation round-trip
# ===================================================================


class TestJsonSerialisation:
    """Semantic values must survive json.dumps -> json.loads without
    data loss, since they flow through REST API request/response bodies."""

    def test_json_dumps_produces_plain_string(self) -> None:
        key = lift_process_definition_key("12345")
        assert json.dumps(key) == '"12345"'

    def test_json_dumps_in_dict(self) -> None:
        key = lift_process_definition_key("12345")
        payload: dict[str, Any] = {"processDefinitionKey": key, "count": 1}
        result: dict[str, Any] = json.loads(json.dumps(payload))
        assert result == {"processDefinitionKey": "12345", "count": 1}

    def test_json_dumps_in_list(self) -> None:
        keys = [lift_process_definition_key("1"), lift_process_definition_key("2")]
        result: list[str] = json.loads(json.dumps(keys))
        assert result == ["1", "2"]

    def test_json_round_trip_preserves_value(self) -> None:
        original = lift_process_definition_key("9876543210")
        serialised = json.dumps({"key": original})
        deserialised: dict[str, Any] = json.loads(serialised)
        reconstructed = lift_process_definition_key(deserialised["key"])
        assert reconstructed == original


# ===================================================================
# 4 · Equality and hashing
# ===================================================================


class TestEqualityAndHashing:
    """Users rely on equality comparisons and using semantic values as
    dict keys / set members."""

    def test_equal_to_plain_str(self) -> None:
        key = lift_process_definition_key("100")
        assert key == "100"
        assert "100" == key

    def test_equal_to_same_semantic_type(self) -> None:
        a = lift_process_definition_key("100")
        b = lift_process_definition_key("100")
        assert a == b

    def test_not_equal_to_different_value(self) -> None:
        a = lift_process_definition_key("100")
        b = lift_process_definition_key("200")
        assert a != b

    def test_hash_consistent_with_str(self) -> None:
        key = lift_process_definition_key("100")
        assert hash(key) == hash("100")

    def test_usable_as_dict_key(self) -> None:
        key = lift_process_definition_key("100")
        d: dict[str, str] = {key: "found"}
        assert d["100"] == "found"
        assert d[key] == "found"

    def test_usable_in_set(self) -> None:
        a = lift_process_definition_key("100")
        b = lift_process_definition_key("100")
        s = {a, b}
        assert len(s) == 1
        assert "100" in s


# ===================================================================
# 5 · Disjointness between semantic key types
# ===================================================================


class TestDisjointness:
    """Semantic key types with the same underlying value should be
    distinguishable at the *type-checking* level.  This class documents
    the actual runtime behaviour -- whether or not the runtime can
    distinguish between, say, a ProcessDefinitionKey("100") and a
    ProcessInstanceKey("100").

    With NewType the runtime type is plain ``str`` for all, so they are
    indistinguishable at runtime.  If the implementation changes to
    class-based types, some of these assertions will flip -- that is the
    intended regression signal.
    """

    def test_different_key_types_same_value_are_equal_at_runtime(self) -> None:
        """NewType does not create distinct runtime types, so two
        different semantic keys wrapping the same value compare equal."""
        pdk = lift_process_definition_key("100")
        pik = lift_process_instance_key("100")
        assert pdk == pik  # both are just "100"

    def test_runtime_type_is_str(self) -> None:
        """With NewType, type() returns str -- not the semantic type."""
        pdk = lift_process_definition_key("100")
        assert type(pdk) is str

    @pytest.mark.parametrize(
        "lifter,_type,value",
        STR_KEY_SAMPLES,
        ids=lambda x: x.__name__ if callable(x) else str(x),  # type: ignore[union-attr]
    )
    def test_every_lifted_value_runtime_type_is_str(
        self, lifter: Lifter, _type: Callable[..., Any], value: str
    ) -> None:
        result = lifter(value)
        assert type(result) is str

    def test_cannot_isinstance_distinguish_key_types(self) -> None:
        """With NewType there is no class to use with isinstance -- the
        NewType alias is erased at runtime.  Attempting to use it with
        isinstance raises TypeError because NewType aliases are not
        classes.

        If the implementation switches to class-based types, isinstance
        WILL work and this test must be updated to reflect the new
        contract.
        """
        pdk = lift_process_definition_key("100")
        # NewType aliases are callables, not classes; isinstance raises TypeError
        with pytest.raises(TypeError):
            isinstance(pdk, ProcessDefinitionKey)  # type: ignore[arg-type]

    def test_different_key_types_share_hash(self) -> None:
        """Because they are all plain str, different semantic types with
        the same value have the same hash and are fungible as dict keys."""
        pdk = lift_process_definition_key("100")
        pik = lift_process_instance_key("100")
        assert hash(pdk) == hash(pik)
        d: dict[str, str] = {pdk: "from-pdk"}
        assert d[pik] == "from-pdk"  # same bucket

    def test_set_collapses_different_key_types_same_value(self) -> None:
        """A set containing the same string from two different semantic
        types collapses to a single element."""
        pdk = lift_process_definition_key("100")
        pik = lift_process_instance_key("100")
        s = {pdk, pik}
        assert len(s) == 1


# ===================================================================
# 6 · Model from_dict / to_dict round-trip
# ===================================================================


class TestModelRoundTrip:
    """Models that use semantic types must correctly lift values in
    from_dict and emit plain strings in to_dict, enabling a full
    JSON <-> model round-trip."""

    def _sample_dict(self) -> dict[str, Any]:
        return {
            "processInstanceKey": "2251799813690746",
            "processDefinitionKey": "2251799813686749",
            "processDefinitionName": "order-process",
        }

    def test_from_dict_produces_semantic_typed_fields(self) -> None:
        from camunda_orchestration_sdk.models.process_instance_call_hierarchy_entry import (
            ProcessInstanceCallHierarchyEntry,
        )

        obj = ProcessInstanceCallHierarchyEntry.from_dict(self._sample_dict())
        # Values are correct
        assert obj.process_instance_key == "2251799813690746"
        assert obj.process_definition_key == "2251799813686749"
        assert obj.process_definition_name == "order-process"
        # They are str (semantic or not)
        assert isinstance(obj.process_instance_key, str)
        assert isinstance(obj.process_definition_key, str)

    def test_to_dict_emits_plain_json_compatible_values(self) -> None:
        from camunda_orchestration_sdk.models.process_instance_call_hierarchy_entry import (
            ProcessInstanceCallHierarchyEntry,
        )

        obj = ProcessInstanceCallHierarchyEntry.from_dict(self._sample_dict())
        result = obj.to_dict()
        assert result == self._sample_dict()
        # Verify it is JSON-serialisable
        json_str = json.dumps(result)
        assert json.loads(json_str) == self._sample_dict()

    def test_full_round_trip_dict_to_model_to_dict(self) -> None:
        from camunda_orchestration_sdk.models.process_instance_call_hierarchy_entry import (
            ProcessInstanceCallHierarchyEntry,
        )

        original = self._sample_dict()
        obj = ProcessInstanceCallHierarchyEntry.from_dict(original)
        reconstructed = obj.to_dict()
        assert reconstructed == original

    def test_from_dict_validates_semantic_fields(self) -> None:
        """from_dict calls lifters which validate -- bad input must raise."""
        from camunda_orchestration_sdk.models.process_instance_call_hierarchy_entry import (
            ProcessInstanceCallHierarchyEntry,
        )

        bad = self._sample_dict()
        bad["processInstanceKey"] = "not-a-number"
        with pytest.raises(ValueError, match="does not match pattern"):
            ProcessInstanceCallHierarchyEntry.from_dict(bad)

    def test_additional_properties_preserved_through_round_trip(self) -> None:
        from camunda_orchestration_sdk.models.process_instance_call_hierarchy_entry import (
            ProcessInstanceCallHierarchyEntry,
        )

        data = self._sample_dict()
        data["extraField"] = "extra-value"
        obj = ProcessInstanceCallHierarchyEntry.from_dict(data)
        result = obj.to_dict()
        assert result["extraField"] == "extra-value"


# ===================================================================
# 7 · try_lift variants
# ===================================================================


class TestTryLift:
    """try_lift_* returns (True, value) on success and (False, exception)
    on failure, allowing callers to handle errors without try/except."""

    def test_try_lift_success(self) -> None:
        ok, val = try_lift_process_definition_key("12345")
        assert ok is True
        assert val == "12345"

    def test_try_lift_failure_returns_false_and_exception(self) -> None:
        ok, err = try_lift_process_definition_key("not-a-number")
        assert ok is False
        assert isinstance(err, ValueError)

    def test_try_lift_type_error(self) -> None:
        ok, err = try_lift_process_definition_key(999)
        assert ok is False
        assert isinstance(err, TypeError)

    def test_try_lift_process_instance_key_success(self) -> None:
        ok, val = try_lift_process_instance_key("42")
        assert ok is True
        assert val == "42"


# ===================================================================
# 8 · Copy / pickle safety
# ===================================================================


class TestCopyAndPickle:
    """Users may copy or pickle semantic values, e.g. when passing them
    between threads or caching them."""

    def test_copy(self) -> None:
        key = lift_process_definition_key("100")
        copied = copy.copy(key)
        assert copied == key
        assert copied == "100"

    def test_deepcopy(self) -> None:
        key = lift_process_definition_key("100")
        copied = copy.deepcopy(key)
        assert copied == key

    def test_pickle_round_trip(self) -> None:
        key = lift_process_definition_key("100")
        pickled = pickle.dumps(key)
        unpickled: str = pickle.loads(pickled)  # noqa: S301
        assert unpickled == key
        assert unpickled == "100"
