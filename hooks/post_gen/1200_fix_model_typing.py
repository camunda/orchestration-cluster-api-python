"""Post-gen hook: Fix typing issues in generated model and API files for pyright strict.

Addresses several patterns:

1. ``_parse_*`` helper functions use ``isinstance(data, dict)`` guards.
   After narrowing through ``isinstance``, pyright infers
   ``dict[Unknown, Unknown]`` which is incompatible with
   ``Mapping[str, Any]`` expected by ``from_dict``.
   Fix: insert ``data = cast(dict[str, Any], data)`` after the isinstance
   guard so pyright sees the correct type.

2. Empty list accumulators in ``from_dict`` methods (e.g. ``elements = []``)
   are inferred as ``list[Unknown]`` in strict mode.  Fix: annotate with the
   concrete model type derived from the class attribute declaration.

3. Empty list accumulators in ``to_dict`` methods (e.g. ``elements = []``
   followed by ``for elements_item_data in self.elements:``) are inferred as
   ``list[Unknown]``.  Fix: annotate with ``list[dict[str, Any]]`` when items
   come from ``.to_dict()`` or ``list[Any]`` otherwise.

4. Empty list accumulators in API ``_parse_response`` functions (e.g.
   ``response_200 = []`` with ``.from_dict()`` appends).  Fix: annotate with
   ``list[ModelName]`` derived from the ``.from_dict()`` call.

5. Single-variant isinstance guards in ``to_dict`` that produce
   ``reportUnnecessaryIsInstance`` and ``reportPossiblyUnboundVariable``.
   Fix: replace the guard with a direct ``.to_dict()`` call.
"""

from __future__ import annotations

import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Pattern 1: cast data after isinstance(data, dict) guard
# ---------------------------------------------------------------------------

_ISINSTANCE_GUARD_RE = re.compile(
    r"((\s+)if not isinstance\(data, dict\):\n\s+raise TypeError\(\))\n",
)


def _fix_parse_isinstance_guard(content: str) -> str:
    """Insert ``data = cast(dict[str, Any], data)`` after isinstance guards."""
    if "raise TypeError()" not in content:
        return content
    if 'data = cast(dict[str, Any], data)' in content:
        return content

    def _insert_cast(match: re.Match[str]) -> str:
        full = match.group(1)
        indent = match.group(2)
        return f"{full}\n{indent}data = cast(dict[str, Any], data)\n"

    return _ISINSTANCE_GUARD_RE.sub(_insert_cast, content)


# ---------------------------------------------------------------------------
# Pattern 2: untyped list accumulator in from_dict  →  typed list annotation
# ---------------------------------------------------------------------------

_UNTYPED_LIST_INIT_RE = re.compile(
    r"^([ \t]+)(\w+) = \[\](?=\n\1_\2 = d\.pop\()",
    re.MULTILINE,
)

_CLASS_LIST_ATTR_RE = re.compile(
    r"^\s+(\w+):\s*list\[([^\]]+)\]",
    re.MULTILINE,
)


def _fix_list_accumulators(content: str) -> str:
    """Add type annotations to empty list accumulators in from_dict methods."""
    list_attrs: dict[str, str] = {}
    for m in _CLASS_LIST_ATTR_RE.finditer(content):
        list_attrs[m.group(1)] = m.group(2)

    if not list_attrs:
        return content

    def _annotate(match: re.Match[str]) -> str:
        indent, var = match.group(1), match.group(2)
        if var in list_attrs:
            return f"{indent}{var}: list[{list_attrs[var]}] = []"
        return match.group(0)

    return _UNTYPED_LIST_INIT_RE.sub(_annotate, content)


# ---------------------------------------------------------------------------
# Pattern 3: untyped list accumulator in to_dict  →  typed list annotation
# ---------------------------------------------------------------------------

# Matches:
#   var = []
#   for var_item_data in self.var:
#       var_item = var_item_data.METHOD()
_TODICT_LIST_RE = re.compile(
    r"^([ \t]+)(\w+) = \[\]\n"
    r"\1for \2_item_data in self\.\2:\n"
    r"\1    \2_item = \2_item_data\.(\w+)\(\)",
    re.MULTILINE,
)

# Matches enum value access variant:
#   var = []
#   for var_item_data in self.var:
#       var_item = var_item_data.value
_TODICT_LIST_VALUE_RE = re.compile(
    r"^([ \t]+)(\w+) = \[\]\n"
    r"\1for \2_item_data in self\.\2:\n"
    r"\1    \2_item = \2_item_data\.(value)\n",
    re.MULTILINE,
)


def _fix_todict_list_accumulators(content: str) -> str:
    """Add type annotations to empty list accumulators in to_dict methods."""
    if "def to_dict(self)" not in content:
        return content

    # Find where to_dict method starts so we can distinguish class attrs
    # from local variable declarations inside to_dict
    todict_pos = content.index("def to_dict(self)")

    def _annotate(match: re.Match[str]) -> str:
        indent = match.group(1)
        var = match.group(2)
        method = match.group(3)
        # Only skip if this variable was already declared with a type annotation
        # INSIDE the to_dict method (after to_dict_pos), not as a class attribute
        after_todict = content[todict_pos:match.start()]
        if re.search(rf"\b{re.escape(var)}: list\[", after_todict):
            return match.group(0)
        if method == "to_dict":
            ann = "list[dict[str, Any]]"
        else:
            ann = "list[Any]"
        return (
            f"{indent}{var}: {ann} = []\n"
            f"{indent}for {var}_item_data in self.{var}:\n"
            f"{indent}    {var}_item = {var}_item_data.{method}()"
        )

    content = _TODICT_LIST_RE.sub(_annotate, content)

    # Handle .value pattern (enum access — no parens)
    def _annotate_value(match: re.Match[str]) -> str:
        indent = match.group(1)
        var = match.group(2)
        after_todict = content[todict_pos:match.start()]
        if re.search(rf"\b{re.escape(var)}: list\[", after_todict):
            return match.group(0)
        return (
            f"{indent}{var}: list[Any] = []\n"
            f"{indent}for {var}_item_data in self.{var}:\n"
            f"{indent}    {var}_item = {var}_item_data.value\n"
        )

    content = _TODICT_LIST_VALUE_RE.sub(_annotate_value, content)

    return content


# ---------------------------------------------------------------------------
# Pattern 4: untyped list in API _parse_response  →  list[ModelName]
# ---------------------------------------------------------------------------

# Matches in _parse_response:
#   response_NNN = []
#   ... (some lines)
#   response_NNN_item = ModelName.from_dict(...)
_API_LIST_RE = re.compile(
    r"^([ \t]+)(response_\d+) = \[\]",
    re.MULTILINE,
)

_API_FROM_DICT_RE = re.compile(
    r"(\w+)_item = (\w+)\.from_dict\(",
)


def _fix_api_parse_response_lists(content: str) -> str:
    """Add type annotations to list accumulators in API _parse_response."""
    if "_parse_response" not in content:
        return content

    # Find model names used in from_dict calls after list init
    for m in _API_LIST_RE.finditer(content):
        var = m.group(2)  # e.g., "response_200"
        indent = m.group(1)
        # Look for the from_dict call that uses this var's items
        after = content[m.end():]
        from_dict_m = re.search(
            rf"{var}_item = (\w+)\.from_dict\(", after
        )
        if from_dict_m:
            model_name = from_dict_m.group(1)
            old = f"{indent}{var} = []"
            new = f"{indent}{var}: list[{model_name}] = []"
            content = content.replace(old, new, 1)

    return content


# ---------------------------------------------------------------------------
# Pattern 5: single-variant isinstance in to_dict → direct .to_dict()
# ---------------------------------------------------------------------------

# Matches the pattern where an isinstance check guards a single type,
# causing reportUnnecessaryIsInstance and reportPossiblyUnboundVariable:
#   runtime_instructions_item: dict[str, Any]
#   if isinstance(
#       runtime_instructions_item_data,
#       SomeType,
#   ):
#       runtime_instructions_item = runtime_instructions_item_data.to_dict()
#
#   runtime_instructions.append(runtime_instructions_item)

_SINGLE_VARIANT_ISINSTANCE_RE = re.compile(
    r"^([ \t]+)(\w+): dict\[str, Any\]\n"
    r"\1if isinstance\(\n"
    r"\1    (\w+),\n"
    r"\1    (\w+),\n"
    r"\1\):\n"
    r"\1    \2 = \3\.to_dict\(\)\n"
    r"\n"
    r"\1(\w+)\.append\(\2\)",
    re.MULTILINE,
)


def _fix_single_variant_isinstance(content: str) -> str:
    """Replace single-variant isinstance guards with direct .to_dict() calls.
    
    Also removes the now-unused import of the Type0 class.
    """
    removed_types: set[str] = set()

    def _simplify(match: re.Match[str]) -> str:
        indent = match.group(1)
        var = match.group(2)          # e.g., runtime_instructions_item
        data_var = match.group(3)     # e.g., runtime_instructions_item_data
        type_name = match.group(4)    # e.g., ProcesscreationbyidRuntimeInstructionsItemType0
        list_var = match.group(5)     # e.g., runtime_instructions
        removed_types.add(type_name)
        return (
            f"{indent}{var} = {data_var}.to_dict()\n"
            f"\n"
            f"{indent}{list_var}.append({var})"
        )

    content = _SINGLE_VARIANT_ISINSTANCE_RE.sub(_simplify, content)

    # Remove now-unused imports of removed types — only if the type is no
    # longer referenced anywhere else in the file after import removal.
    for type_name in removed_types:
        # Match multi-line import blocks: from ..module import (\n    TypeName,\n)
        import_pattern = re.compile(
            rf"^[ \t]+from [^\n]+ import \(\n\s+{re.escape(type_name)},?\n\s+\)\n",
            re.MULTILINE,
        )
        # Find all such import blocks
        import_blocks = list(import_pattern.finditer(content))
        if not import_blocks:
            continue

        # For each import block, check if removing it leaves zero references.
        # Process in reverse order so positions stay valid.
        for match in reversed(import_blocks):
            # Strip JUST this one import block and count remaining references
            stripped = content[:match.start()] + content[match.end():]
            remaining_refs = len(re.findall(rf"\b{re.escape(type_name)}\b", stripped))
            if remaining_refs == 0:
                # No more references at all — safe to remove
                content = stripped
            else:
                # Check if this specific import block is inside a function
                # where the type is no longer used (e.g. to_dict after
                # isinstance removal).  Find the enclosing def.
                before = content[:match.start()]
                last_def = before.rfind("\n    def ")
                if last_def == -1:
                    continue
                # Find the end of this function (next def at same indent or EOF)
                next_def = content.find("\n    def ", match.end())
                func_end = next_def if next_def != -1 else len(content)
                func_body = content[match.end():func_end]
                # If the type name doesn't appear in the rest of this function,
                # the import is unused locally — remove it.
                if not re.search(rf"\b{re.escape(type_name)}\b", func_body):
                    content = content[:match.start()] + content[match.end():]

    return content


# ---------------------------------------------------------------------------
# Pattern 6: tag_set.py — use Tag semantic type instead of raw str
# ---------------------------------------------------------------------------

_UNTYPED_LIST_VALIDATOR_RE = re.compile(
    r"from typing import List\n",
)

_UNTYPED_LIST_PARAM_RE = re.compile(
    r"def _validate_array\(cls, v: List\)",
)

_TAG_ROOT_MODEL_RE = re.compile(
    r"RootModel\[list\[str\]\]",
)


def _fix_tag_set_typing(content: str) -> str:
    """Rewrite TagSet to use the ``Tag`` semantic type instead of raw ``str``."""
    # Remove unused `from typing import List`
    content = _UNTYPED_LIST_VALIDATOR_RE.sub("", content)
    # Fix validator signature
    content = _UNTYPED_LIST_PARAM_RE.sub(
        "def _validate_array(cls, v: list[Tag]) -> list[Tag]", content
    )
    # RootModel[list[str]] → RootModel[list[Tag]]
    content = _TAG_ROOT_MODEL_RE.sub("RootModel[list[Tag]]", content)
    # Add Tag import after the pydantic import
    if "from ..semantic_types import Tag" not in content:
        content = content.replace(
            "from pydantic import RootModel, field_validator",
            "from pydantic import RootModel, field_validator\n\nfrom ..semantic_types import Tag",
        )
    return content


# ---------------------------------------------------------------------------
# Ensure typing imports
# ---------------------------------------------------------------------------

def _ensure_typing_imports(content: str, needs_cast: bool) -> str:
    """Ensure needed typing imports are present.

    Always ensures ``Any`` is imported.  Adds ``cast`` only when *needs_cast* is
    ``True`` (files that received the isinstance-guard fix).  Also **removes**
    ``cast`` when the file does not use it — the generator sometimes emits an
    unused ``cast`` import.
    """
    if "from typing import" not in content:
        return content
    typing_match = re.search(r"from typing import (.+)", content)
    if not typing_match:
        return content
    imports = typing_match.group(1)

    import_names = [n.strip() for n in imports.split(",")]

    if "Any" not in import_names:
        import_names.append("Any")

    if needs_cast and "cast" not in import_names:
        import_names.append("cast")
    elif not needs_cast and "cast" in import_names and "cast(" not in content:
        import_names.remove("cast")

    new_import_line = f"from typing import {', '.join(import_names)}"
    if new_import_line != typing_match.group(0):
        content = content.replace(typing_match.group(0), new_import_line, 1)
    return content


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"])
    models_dir = out_dir / "camunda_orchestration_sdk" / "models"
    api_dir = out_dir / "camunda_orchestration_sdk" / "api"

    if not models_dir.exists():
        return

    patched_cast = 0
    patched_list = 0
    patched_todict = 0
    patched_isinstance = 0

    for model_file in sorted(models_dir.glob("*.py")):
        if model_file.name == "__init__.py":
            continue

        content = model_file.read_text(encoding="utf-8")
        original = content

        added_isinstance_cast = "raise TypeError()" in content and "cast(dict[str, Any], data)" not in content
        content = _fix_parse_isinstance_guard(content)
        content = _fix_list_accumulators(content)
        content = _fix_todict_list_accumulators(content)
        content = _fix_single_variant_isinstance(content)
        if model_file.name == "tag_set.py":
            content = _fix_tag_set_typing(content)
        needs_cast = added_isinstance_cast and "cast(dict[str, Any], data)" in content
        content = _ensure_typing_imports(content, needs_cast=needs_cast)

        if content != original:
            model_file.write_text(content, encoding="utf-8")

            if "cast(dict[str, Any], data)" in content:
                patched_cast += 1
            if ": list[" in content and ": list[" not in original:
                patched_list += 1
            if "list[dict[str, Any]]" in content and "list[dict[str, Any]]" not in original:
                patched_todict += 1
            if original != content and _SINGLE_VARIANT_ISINSTANCE_RE.search(original):
                patched_isinstance += 1

    print(f"Fixed isinstance→cast in {patched_cast} files, from_dict list typing in {patched_list} files, "
          f"to_dict list typing in {patched_todict} files, single-variant isinstance in {patched_isinstance} files")

    # Also fix API files (Pattern 4)
    if api_dir.exists():
        patched_api = 0
        for api_file in sorted(api_dir.rglob("*.py")):
            if api_file.name == "__init__.py":
                continue
            content = api_file.read_text(encoding="utf-8")
            original = content
            content = _fix_api_parse_response_lists(content)
            if content != original:
                api_file.write_text(content, encoding="utf-8")
                patched_api += 1
        if patched_api:
            print(f"Fixed API _parse_response list typing in {patched_api} files")

    # Fix __all__ tuple type in models/__init__.py
    # pyright can't infer the type of very large tuples (1500+ elements);
    # convert to list[str] which is correctly typed.
    init_file = models_dir / "__init__.py"
    if init_file.exists():
        init_content = init_file.read_text(encoding="utf-8")
        if "__all__ = (" in init_content:
            # Find position of __all__ = (
            all_pos = init_content.index("__all__ = (")
            before = init_content[:all_pos]
            after = init_content[all_pos:]
            # Replace __all__ = ( with __all__: list[str] = [
            after = after.replace("__all__ = (", "__all__: list[str] = [", 1)
            # Find the closing ) that ends the __all__ block (last ) in the section)
            # The __all__ block is at the end of the file; find the final standalone )
            after = re.sub(r"\)\s*$", "]", after)
            init_content = before + after
            init_file.write_text(init_content, encoding="utf-8")
            print("Fixed __all__ tuple → list[str] in models/__init__.py")
