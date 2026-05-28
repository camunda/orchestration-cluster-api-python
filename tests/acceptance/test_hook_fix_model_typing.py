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
        assert (
            result.count("terminate_instructions: list[dict[str, Any]]") == 1
        ), result
