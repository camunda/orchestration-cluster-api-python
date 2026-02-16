"""Post-gen hook: Fix attrs typing issues for pyright strict mode.

``attrs.field(factory=dict)`` causes pyright to infer the field as
``dict[Unknown, Unknown]`` because ``dict()`` has unresolved type parameters
in strict mode.

The fix is to replace ``factory=dict`` with typed factory functions defined in
``types.py``:
- ``str_any_dict_factory() -> dict[str, Any]``
- ``str_str_dict_factory() -> dict[str, str]``

For ``client.py``, which also uses ``field(factory=dict)``, we apply the same
replacement for the ``_cookies``, ``_headers``, and ``_httpx_args`` fields.
"""

from __future__ import annotations

import re
from pathlib import Path


_TYPES_PY_FACTORIES = '''

def str_any_dict_factory() -> "dict[str, Any]":
    """Typed factory for ``dict[str, Any]`` attrs fields."""
    return {}


def str_str_dict_factory() -> dict[str, str]:
    """Typed factory for ``dict[str, str]`` attrs fields."""
    return {}
'''


def _patch_types_py(types_path: Path) -> None:
    """Add typed dict factory functions to types.py."""
    content = types_path.read_text(encoding="utf-8")
    if "str_any_dict_factory" in content:
        return  # Already patched

    # Ensure 'Any' is in the typing imports (needed for factory return type).
    # The file already has: from typing import IO, BinaryIO, Generic, Literal, TypeVar
    typing_import_pattern = re.compile(r"(from typing import )(.+)")
    match = typing_import_pattern.search(content)
    if match and "Any" not in match.group(2):
        content = content.replace(
            match.group(0), f"{match.group(1)}Any, {match.group(2)}", 1
        )

    # Add factory functions
    content += _TYPES_PY_FACTORIES
    # Add factories to __all__ if it exists
    content = content.replace(
        '__all__ = ["UNSET", "File", "FileTypes", "RequestFiles", "Response", "Unset"]',
        '__all__ = ["UNSET", "File", "FileTypes", "RequestFiles", "Response", "Unset", "str_any_dict_factory", "str_str_dict_factory"]',
    )
    types_path.write_text(content, encoding="utf-8")
    print("Added typed factory functions to types.py")


def _patch_model_file(file_path: Path) -> None:
    """Replace ``factory=dict`` with ``factory=str_any_dict_factory`` in model files."""
    content = file_path.read_text(encoding="utf-8")
    if "factory=dict" not in content:
        return

    original = content

    # Replace factory=dict for additional_properties (dict[str, Any])
    content = content.replace(
        "_attrs_field(init=False, factory=dict)",
        "_attrs_field(init=False, factory=str_any_dict_factory)",
    )

    if content != original:
        # Ensure str_any_dict_factory is imported
        before_class = content.split("class ")[0] if "class " in content else content
        if "str_any_dict_factory" not in before_class:
            # Try to augment an existing ..types import
            types_import_match = re.search(r"(from \.\.(\.?)types import .+)", content)
            if types_import_match:
                content = content.replace(
                    types_import_match.group(0),
                    types_import_match.group(0) + ", str_any_dict_factory",
                    1,
                )
            else:
                # No existing ..types import — add one after the attrs imports
                attrs_import_match = re.search(r"(from attrs import .+\n)", content)
                if attrs_import_match:
                    insert_pos = attrs_import_match.end()
                    content = (
                        content[:insert_pos]
                        + "\nfrom ..types import str_any_dict_factory\n"
                        + content[insert_pos:]
                    )
        file_path.write_text(content, encoding="utf-8")
        print(f"Patched factory=dict in {file_path.name}")


def _patch_client_file(client_path: Path) -> None:
    """Replace ``factory=dict`` with typed factories in client.py."""
    content = client_path.read_text(encoding="utf-8")
    if "factory=dict" not in content:
        return

    original = content

    # _cookies and _headers are dict[str, str]
    content = re.sub(
        r"(_(cookies|headers)\s*:\s*dict\[str,\s*str\]\s*=\s*field\(factory=)dict",
        r"\1str_str_dict_factory",
        content,
    )

    # _httpx_args is dict[str, Any]
    content = re.sub(
        r"(_httpx_args\s*:\s*dict\[str,\s*Any\]\s*=\s*field\(factory=)dict",
        r"\1str_any_dict_factory",
        content,
    )

    if content != original:
        # Add import for the factory functions
        # The client.py imports from .types already
        if "str_any_dict_factory" not in content.split("class ")[0]:
            content = re.sub(
                r"(from \.types import .+)",
                r"\1, str_any_dict_factory, str_str_dict_factory",
                content,
                count=1,
            )
        client_path.write_text(content, encoding="utf-8")
        print("Patched factory=dict in client.py")


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    models_dir = package_dir / "models"
    types_path = package_dir / "types.py"
    client_path = package_dir / "client.py"

    # Step 1: Add factory functions to types.py
    if types_path.exists():
        _patch_types_py(types_path)

    # Step 2: Patch model files
    if models_dir.exists():
        for model_file in sorted(models_dir.glob("*.py")):
            if model_file.name == "__init__.py":
                continue
            _patch_model_file(model_file)

    # Step 3: Patch client.py
    if client_path.exists():
        _patch_client_file(client_path)
