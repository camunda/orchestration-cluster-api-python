"""
Behavioral regression tests for semantic types.

These tests document the contract that users depend on when constructing,
serialising, deserialising, and comparing semantic-typed values.  They must
pass identically regardless of the underlying implementation strategy.

The tests are grouped into classes that each target a specific concern:
    - Construction & validation
    - str-subtype contract (isinstance, str operations)
    - JSON serialisation round-trip
    - Equality and hashing
    - Disjointness between semantic key types
    - Model from_dict / to_dict round-trip
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
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
    UserTaskKey,
    VariableKey,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Representative sample of (constructor, valid_value) pairs covering
# every constraint category: pattern+minLen+maxLen, pattern-only, enum, unconstrained.
STR_KEY_SAMPLES: list[tuple[type, str]] = [
    (ProcessDefinitionKey, "12345"),
    (ProcessInstanceKey, "67890"),
    (DecisionDefinitionKey, "111"),
    (ElementInstanceKey, "222"),
    (JobKey, "333"),
    (UserTaskKey, "444"),
    (VariableKey, "555"),
]

# All key types that share the numeric-string pattern ^-?[0-9]+$
NUMERIC_KEY_TYPES: list[type] = [
    ProcessDefinitionKey,
    ProcessInstanceKey,
    DecisionDefinitionKey,
    ElementInstanceKey,
    JobKey,
    UserTaskKey,
    VariableKey,
]


# ===================================================================
# 1 · Construction & validation
# ===================================================================


class TestConstruction:
    """Constructors accept valid input and reject invalid input."""

    @pytest.mark.parametrize(
        "_type,value",
        STR_KEY_SAMPLES,
        ids=lambda x: x.__name__ if callable(x) else str(x),  # type: ignore[union-attr]
    )
    def test_constructor_returns_value_for_valid_input(
        self, _type: Callable[..., Any], value: str
    ) -> None:
        result = _type(value)
        assert result == value

    @pytest.mark.parametrize(
        "_type", NUMERIC_KEY_TYPES, ids=lambda t: t.__name__
    )
    def test_constructor_rejects_non_numeric_string(self, _type: type) -> None:
        with pytest.raises(ValueError, match="does not match pattern"):
            _type("not-a-number")

    @pytest.mark.parametrize(
        "_type", NUMERIC_KEY_TYPES, ids=lambda t: t.__name__
    )
    def test_constructor_rejects_non_str_type(self, _type: type) -> None:
        with pytest.raises(TypeError, match="must be str"):
            _type(12345)

    @pytest.mark.parametrize(
        "_type", NUMERIC_KEY_TYPES, ids=lambda t: t.__name__
    )
    def test_constructor_rejects_empty_string(self, _type: type) -> None:
        with pytest.raises(ValueError):
            _type("")

    def test_constructor_rejects_string_exceeding_max_length(self) -> None:
        with pytest.raises(ValueError, match="longer than maxLength"):
            ProcessDefinitionKey("1" * 26)

    def test_constructor_accepts_negative_numeric_key(self) -> None:
        result = ProcessDefinitionKey("-42")
        assert result == "-42"

    def test_process_definition_id_pattern_validation(self) -> None:
        val = ProcessDefinitionId("my_process_v1")
        assert val == "my_process_v1"

    def test_process_definition_id_rejects_leading_special_char(self) -> None:
        with pytest.raises(ValueError, match="does not match pattern"):
            ProcessDefinitionId("!invalid")

    def test_tenant_id_accepts_default(self) -> None:
        val = TenantId("<default>")
        assert val == "<default>"

    def test_tenant_id_accepts_alphanumeric(self) -> None:
        val = TenantId("my_tenant-1")
        assert val == "my_tenant-1"


# ===================================================================
# 2 · str-subtype contract
# ===================================================================


class TestStrSubtype:
    """Semantic types must behave as str at runtime for user code that
    passes them to standard library functions, HTTP clients, etc."""

    @pytest.mark.parametrize(
        "_type,value",
        STR_KEY_SAMPLES,
        ids=lambda x: x.__name__ if callable(x) else str(x),  # type: ignore[union-attr]
    )
    def test_isinstance_str(
        self, _type: Callable[..., Any], value: str
    ) -> None:
        result = _type(value)
        assert isinstance(result, str)

    def test_str_builtin_returns_same_value(self) -> None:
        key = ProcessDefinitionKey("12345")
        assert str(key) == "12345"

    def test_string_concatenation(self) -> None:
        key = ProcessDefinitionKey("100")
        assert "key=" + key == "key=100"

    def test_string_slicing(self) -> None:
        key = ProcessDefinitionKey("12345")
        assert key[:3] == "123"

    def test_string_format(self) -> None:
        key = ProcessDefinitionKey("42")
        assert f"Process {key}" == "Process 42"

    def test_len(self) -> None:
        key = ProcessDefinitionKey("12345")
        assert len(key) == 5

    def test_in_operator(self) -> None:
        key = ProcessDefinitionKey("12345")
        assert "234" in key


# ===================================================================
# 3 · JSON serialisation round-trip
# ===================================================================


class TestJsonSerialisation:
    """Semantic values must survive json.dumps -> json.loads without
    data loss, since they flow through REST API request/response bodies."""

    def test_json_dumps_produces_plain_string(self) -> None:
        key = ProcessDefinitionKey("12345")
        assert json.dumps(key) == '"12345"'

    def test_json_dumps_in_dict(self) -> None:
        key = ProcessDefinitionKey("12345")
        payload: dict[str, Any] = {"processDefinitionKey": key, "count": 1}
        result: dict[str, Any] = json.loads(json.dumps(payload))
        assert result == {"processDefinitionKey": "12345", "count": 1}

    def test_json_dumps_in_list(self) -> None:
        keys = [ProcessDefinitionKey("1"), ProcessDefinitionKey("2")]
        result: list[str] = json.loads(json.dumps(keys))
        assert result == ["1", "2"]

    def test_json_round_trip_preserves_value(self) -> None:
        original = ProcessDefinitionKey("9876543210")
        serialised = json.dumps({"key": original})
        deserialised: dict[str, Any] = json.loads(serialised)
        reconstructed = ProcessDefinitionKey(deserialised["key"])
        assert reconstructed == original


# ===================================================================
# 4 · Equality and hashing
# ===================================================================


class TestEqualityAndHashing:
    """Users rely on equality comparisons and using semantic values as
    dict keys / set members."""

    def test_equal_to_plain_str(self) -> None:
        key = ProcessDefinitionKey("100")
        assert key == "100"
        assert "100" == key

    def test_equal_to_same_semantic_type(self) -> None:
        a = ProcessDefinitionKey("100")
        b = ProcessDefinitionKey("100")
        assert a == b

    def test_not_equal_to_different_value(self) -> None:
        a = ProcessDefinitionKey("100")
        b = ProcessDefinitionKey("200")
        assert a != b

    def test_hash_consistent_with_str(self) -> None:
        key = ProcessDefinitionKey("100")
        assert hash(key) == hash("100")

    def test_usable_as_dict_key(self) -> None:
        key = ProcessDefinitionKey("100")
        d: dict[str, str] = {key: "found"}
        assert d["100"] == "found"
        assert d[key] == "found"

    def test_usable_in_set(self) -> None:
        a = ProcessDefinitionKey("100")
        b = ProcessDefinitionKey("100")
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

    With class-based types (each inheriting from ``str``) the runtime
    ``type()`` returns the semantic class rather than plain ``str``, and
    ``isinstance`` checks against the class work correctly.  Because the
    classes inherit ``str.__eq__`` and ``str.__hash__`` without override,
    two different semantic types wrapping the same string value are still
    equal and share a hash at runtime.
    """

    def test_different_key_types_same_value_are_equal_at_runtime(self) -> None:
        """Class-based types inherit str.__eq__, so two different semantic
        keys wrapping the same value still compare equal at runtime."""
        pdk = ProcessDefinitionKey("100")
        pik = ProcessInstanceKey("100")
        assert pdk == pik  # both compare as "100" via str.__eq__

    def test_runtime_type_is_semantic_class(self) -> None:
        """With class-based types, type() returns the semantic class, not plain str."""
        pdk = ProcessDefinitionKey("100")
        assert type(pdk) is ProcessDefinitionKey
        assert isinstance(pdk, str)  # still a str subclass

    @pytest.mark.parametrize(
        "_type,value",
        STR_KEY_SAMPLES,
        ids=lambda x: x.__name__ if callable(x) else str(x),  # type: ignore[union-attr]
    )
    def test_every_constructed_value_runtime_type_is_semantic_class(
        self, _type: Callable[..., Any], value: str
    ) -> None:
        result = _type(value)
        assert type(result) is _type
        assert isinstance(result, str)  # still a str subclass

    def test_can_isinstance_distinguish_key_types(self) -> None:
        """With class-based types, isinstance checks against the semantic
        class work correctly -- each type is a real class, not a NewType alias.
        """
        pdk = ProcessDefinitionKey("100")
        assert isinstance(pdk, ProcessDefinitionKey)
        pik = ProcessInstanceKey("100")
        assert not isinstance(pik, ProcessDefinitionKey)

    def test_different_key_types_share_hash(self) -> None:
        """Because they are all plain str, different semantic types with
        the same value have the same hash and are fungible as dict keys."""
        pdk = ProcessDefinitionKey("100")
        pik = ProcessInstanceKey("100")
        assert hash(pdk) == hash(pik)
        d: dict[str, str] = {pdk: "from-pdk"}
        assert d[pik] == "from-pdk"  # same bucket

    def test_set_collapses_different_key_types_same_value(self) -> None:
        """A set containing the same string from two different semantic
        types collapses to a single element."""
        pdk = ProcessDefinitionKey("100")
        pik = ProcessInstanceKey("100")
        s = {pdk, pik}
        assert len(s) == 1


# ===================================================================
# 6 · Model from_dict / to_dict round-trip
# ===================================================================


class TestModelRoundTrip:
    """Models that use semantic types must correctly construct values in
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
        """from_dict constructs semantic types, which validate -- bad input must raise."""
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
# 7 · Copy / pickle safety
# ===================================================================


class TestCopyAndPickle:
    """Users may copy or pickle semantic values, e.g. when passing them
    between threads or caching them."""

    def test_copy(self) -> None:
        key = ProcessDefinitionKey("100")
        copied = copy.copy(key)
        assert copied == key
        assert copied == "100"

    def test_deepcopy(self) -> None:
        key = ProcessDefinitionKey("100")
        copied = copy.deepcopy(key)
        assert copied == key

    def test_pickle_round_trip(self) -> None:
        key = ProcessDefinitionKey("100")
        pickled = pickle.dumps(key)
        unpickled: str = pickle.loads(pickled)  # noqa: S301
        assert unpickled == key
        assert unpickled == "100"
