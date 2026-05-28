"""Tests for hooks/post_gen/1200_fix_model_typing.py.

Regression guards for the typing-annotation transformations applied to
generated model files. The transformations are tested directly on synthetic
snippets so that the guards remain meaningful even when no schema in the
current upstream spec triggers a given codegen shape.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

# Import the numbered hook module via importlib (filename starts with a digit).
_hook_path = (
    Path(__file__).resolve().parents[2]
    / "hooks"
    / "post_gen"
    / "1200_fix_model_typing.py"
)
_spec = importlib.util.spec_from_file_location("_fix_model_typing", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)

_fix_todict_list_accumulators = _hook._fix_todict_list_accumulators
_fix_parse_helper_lists = _hook._fix_parse_helper_lists


class TestToDictUnionVariantListAnnotation:
    """Pattern: required, non-nullable array of a polymorphic ``oneOf`` schema.

    The generator emits a ``to_dict`` body where the per-item value is
    pre-declared with ``var_item: dict[str, Any]`` and then assigned inside an
    ``if isinstance(...) / else`` block. The outer accumulator ``var = []`` is
    bare (no surrounding ``if not isinstance(self.var, Unset)`` wrapper because
    the field is required), so pyright infers it as ``list[Unknown]``.

    Hook 1200 must annotate the accumulator as ``list[dict[str, Any]]``.
    """

    def test_required_polymorphic_list_to_dict_gets_annotated(self) -> None:
        content = (
            "    def to_dict(self) -> dict[str, Any]:\n"
            "        items = []\n"
            "        for items_item_data in self.items:\n"
            "            items_item: dict[str, Any]\n"
            "            if isinstance(items_item_data, JobResult):\n"
            "                items_item = items_item_data.to_dict()\n"
            "            else:\n"
            "                items_item = items_item_data.to_dict()\n"
            "\n"
            "            items.append(items_item)\n"
        )

        result = _fix_todict_list_accumulators(content)

        assert "items: list[dict[str, Any]] = []" in result, (
            "Expected required, non-nullable polymorphic-list accumulator "
            "to be annotated as list[dict[str, Any]]. Got:\n" + result
        )

    def test_multi_field_required_polymorphic_lists_all_annotated(self) -> None:
        """Class-of-defect scope: any field of this shape must be annotated,
        not just one called ``items``.
        """
        content = (
            "    def to_dict(self) -> dict[str, Any]:\n"
            "        entries = []\n"
            "        for entries_item_data in self.entries:\n"
            "            entries_item: dict[str, Any]\n"
            "            if isinstance(entries_item_data, VariantA):\n"
            "                entries_item = entries_item_data.to_dict()\n"
            "            else:\n"
            "                entries_item = entries_item_data.to_dict()\n"
            "\n"
            "            entries.append(entries_item)\n"
            "\n"
            "        records = []\n"
            "        for records_item_data in self.records:\n"
            "            records_item: dict[str, Any]\n"
            "            if isinstance(records_item_data, VariantX):\n"
            "                records_item = records_item_data.to_dict()\n"
            "            else:\n"
            "                records_item = records_item_data.to_dict()\n"
            "\n"
            "            records.append(records_item)\n"
        )

        result = _fix_todict_list_accumulators(content)

        assert "entries: list[dict[str, Any]] = []" in result
        assert "records: list[dict[str, Any]] = []" in result

    def test_optional_wrapped_variant_is_not_re_annotated(self) -> None:
        """Optional polymorphic-list fields already declare an outer typed
        accumulator inside the ``if not isinstance(..., Unset)`` block, so the
        existing skip-if-already-annotated guard must keep working.
        """
        content = (
            "    def to_dict(self) -> dict[str, Any]:\n"
            "        terminate_instructions: list[dict[str, Any]] | Unset = UNSET\n"
            "        if not isinstance(self.terminate_instructions, Unset):\n"
            "            terminate_instructions = []\n"
            "            for terminate_instructions_item_data in self.terminate_instructions:\n"
            "                terminate_instructions_item: dict[str, Any]\n"
            "                if isinstance(terminate_instructions_item_data, A):\n"
            "                    terminate_instructions_item = terminate_instructions_item_data.to_dict()\n"
            "                else:\n"
            "                    terminate_instructions_item = terminate_instructions_item_data.to_dict()\n"
            "\n"
            "                terminate_instructions.append(terminate_instructions_item)\n"
        )

        result = _fix_todict_list_accumulators(content)

        # The existing outer declaration must not be duplicated, and the inner
        # ``terminate_instructions = []`` must not gain its own annotation
        # (it would shadow the outer typed declaration).
        assert result.count("terminate_instructions: list[dict[str, Any]]") == 1, result


class TestParseHelperListAnnotation:
    """Pattern: 3-variant ``list[T] | None | Unset`` _parse_* helper.

    Emitted by openapi-python-client for optional + nullable array fields.
    The helper narrows ``data: object`` via ``isinstance(data, list)`` and
    aliases it as ``_var = data``; without annotations the entire chain
    (alias, iteration variable, ``from_dict`` argument, ``append``, return
    value) is ``Unknown``.

    Hook 1200 must annotate both the accumulator (``list[Model]``) and the
    narrowed-data alias (``list[Any]``).
    """

    def test_three_variant_parse_helper_gets_annotated(self) -> None:
        content = (
            "        def _parse_tools(data: object) -> list[AgentTool] | None | Unset:\n"
            "            if data is None:\n"
            "                return data\n"
            "            if isinstance(data, Unset):\n"
            "                return data\n"
            "            try:\n"
            "                if not isinstance(data, list):\n"
            "                    raise TypeError()\n"
            "                tools_type_0 = []\n"
            "                _tools_type_0 = data\n"
            "                for tools_type_0_item_data in _tools_type_0:\n"
            "                    tools_type_0_item = AgentTool.from_dict(tools_type_0_item_data)\n"
            "\n"
            "                    tools_type_0.append(tools_type_0_item)\n"
            "\n"
            "                return tools_type_0\n"
            "            except (TypeError, ValueError, AttributeError, KeyError):\n"
            "                pass\n"
            "            return cast(list[AgentTool] | None | Unset, data)\n"
        )

        result = _fix_parse_helper_lists(content)

        assert "tools_type_0: list[AgentTool] = []" in result, result
        assert "_tools_type_0 = cast(list[Any], data)" in result, result

    def test_multiple_parse_helpers_in_same_file_all_annotated(self) -> None:
        """Class-of-defect scope: any ``_parse_*`` helper with this shape
        must be annotated, regardless of field name or model.
        """
        content = (
            "        def _parse_first(data: object) -> list[ModelA] | None | Unset:\n"
            "            try:\n"
            "                if not isinstance(data, list):\n"
            "                    raise TypeError()\n"
            "                first_type_0 = []\n"
            "                _first_type_0 = data\n"
            "                for first_type_0_item_data in _first_type_0:\n"
            "                    first_type_0_item = ModelA.from_dict(first_type_0_item_data)\n"
            "                    first_type_0.append(first_type_0_item)\n"
            "                return first_type_0\n"
            "            except (TypeError,):\n"
            "                pass\n"
            "            return cast(list[ModelA] | None | Unset, data)\n"
            "\n"
            "        def _parse_second(data: object) -> list[ModelB] | None | Unset:\n"
            "            try:\n"
            "                if not isinstance(data, list):\n"
            "                    raise TypeError()\n"
            "                second_type_0 = []\n"
            "                _second_type_0 = data\n"
            "                for second_type_0_item_data in _second_type_0:\n"
            "                    second_type_0_item = ModelB.from_dict(second_type_0_item_data)\n"
            "                    second_type_0.append(second_type_0_item)\n"
            "                return second_type_0\n"
            "            except (TypeError,):\n"
            "                pass\n"
            "            return cast(list[ModelB] | None | Unset, data)\n"
        )

        result = _fix_parse_helper_lists(content)

        assert "first_type_0: list[ModelA] = []" in result
        assert "_first_type_0 = cast(list[Any], data)" in result
        assert "second_type_0: list[ModelB] = []" in result
        assert "_second_type_0 = cast(list[Any], data)" in result

    def test_already_annotated_is_idempotent(self) -> None:
        """Re-running the hook on already-annotated output must not
        double-annotate (the codegen never includes the annotation; this
        guards against accidental match-on-output if the regex is
        broadened later).
        """
        content = (
            "                tools_type_0: list[AgentTool] = []\n"
            "                _tools_type_0 = cast(list[Any], data)\n"
            "                for tools_type_0_item_data in _tools_type_0:\n"
            "                    tools_type_0_item = AgentTool.from_dict(tools_type_0_item_data)\n"
        )

        result = _fix_parse_helper_lists(content)

        assert result.count("tools_type_0: list[AgentTool] = []") == 1
