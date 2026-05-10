"""Post-generation hook: emit backward-compatible deprecated type aliases.

Adds deprecated aliases for model classes that were renamed between v9 and v10.
Users who import by the old name get a DeprecationWarning at import time,
but the import succeeds and the returned class is the same object as the new name.

Patches:
- models/__init__.py: adds __getattr__ for runtime deprecation warnings
- top-level __init__.py: adds __getattr__ for top-level imports
"""

from __future__ import annotations

import re
from pathlib import Path

from _api_compat_alias_map import RENAMES_V9_TO_V10


def _build_getattr_block(renames: dict[str, str], module_name: str) -> str:
    """Build a __getattr__ function that emits DeprecationWarning for old names."""
    lines: list[str] = []
    lines.append("")
    lines.append("")
    lines.append("# --- Deprecated type aliases (v9 → v10) ---")
    lines.append("# These names were used in v9 and have been renamed in v10.")
    lines.append("# They will be removed in the next major version (v11).")
    lines.append("import warnings as _warnings")
    lines.append("")
    lines.append("_DEPRECATED_ALIASES: dict[str, str] = {")
    for old, new in sorted(renames.items()):
        lines.append(f'    "{old}": "{new}",')
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def __getattr__(name: str) -> object:")
    lines.append("    if name in _DEPRECATED_ALIASES:")
    lines.append("        new_name = _DEPRECATED_ALIASES[name]")
    lines.append("        _warnings.warn(")
    lines.append('            f"{name} is deprecated, use {new_name} instead. "')
    lines.append('            "Will be removed in the next major version.",')
    lines.append("            DeprecationWarning,")
    lines.append("            stacklevel=2,")
    lines.append("        )")
    lines.append("        return globals()[new_name]")
    lines.append(
        f'    raise AttributeError(f"module {module_name!r} has no attribute {{name!r}}")'
    )
    lines.append("")
    return "\n".join(lines)


def _build_type_checking_block(renames: dict[str, str]) -> str:
    """Build a TYPE_CHECKING block so pyright sees the aliases statically."""
    lines: list[str] = []
    lines.append("")
    lines.append("")
    lines.append("from typing import TYPE_CHECKING as _TYPE_CHECKING")
    lines.append("")
    lines.append("if _TYPE_CHECKING:")
    lines.append("    # Static type aliases for backward compatibility (pyright/mypy)")
    for old, new in sorted(renames.items()):
        lines.append(f"    {old} = {new}")
    lines.append("")
    return "\n".join(lines)


def _patch_models_init(models_init: Path, renames: dict[str, str]) -> None:
    """Patch models/__init__.py with deprecated aliases."""
    text = models_init.read_text(encoding="utf-8")

    # Add old names to __all__ so star imports resolve them.
    # Star imports will trigger __getattr__ for each old name, emitting a DeprecationWarning.
    all_match = re.search(
        r"(__all__(?::\s*list\[str\])?\s*=\s*\[)(.*?)(\])",
        text,
        re.DOTALL,
    )
    if all_match:
        existing_block = all_match.group(2)
        existing_names: list[str] = re.findall(r'"([^"]+)"', existing_block)
        # Add old names
        all_names = sorted(set(existing_names) | set(renames.keys()))
        quoted = [f'    "{n}",' for n in all_names]
        new_all = "__all__: list[str] = [\n" + "\n".join(quoted) + "\n]"
        text = text[: all_match.start()] + new_all + text[all_match.end() :]

    # Append TYPE_CHECKING block and __getattr__
    text = text.rstrip("\n")
    text += _build_type_checking_block(renames)
    text += _build_getattr_block(renames, "camunda_orchestration_sdk.models")
    text += "\n"

    models_init.write_text(text, encoding="utf-8")


def _patch_top_level_init(init_file: Path, renames: dict[str, str]) -> None:
    """Patch top-level __init__.py with deprecated aliases.

    Relies on the new names being re-exported at top level via __all__.
    """
    text = init_file.read_text(encoding="utf-8")

    # Add old names to __all__
    all_match = re.search(
        r"(__all__(?::\s*list\[str\])?\s*=\s*\[)(.*?)(\])",
        text,
        re.DOTALL,
    )
    if all_match:
        existing_block = all_match.group(2)
        existing_names: list[str] = re.findall(r'"([^"]+)"', existing_block)
        all_names = sorted(set(existing_names) | set(renames.keys()))
        quoted = [f'    "{n}",' for n in all_names]
        new_all = "__all__: list[str] = [\n" + "\n".join(quoted) + "\n]"
        text = text[: all_match.start()] + new_all + text[all_match.end() :]

    # Append __getattr__ for top-level package
    text = text.rstrip("\n")
    text += _build_type_checking_block(renames)
    text += _build_getattr_block(renames, "camunda_orchestration_sdk")
    text += "\n"

    init_file.write_text(text, encoding="utf-8")


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    models_init = package_dir / "models" / "__init__.py"
    top_init = package_dir / "__init__.py"

    if not models_init.exists():
        print(f"Warning: {models_init} not found, skipping deprecated aliases")
        return
    if not top_init.exists():
        print(f"Warning: {top_init} not found, skipping deprecated aliases")
        return

    # Verify all new names exist in models before creating aliases.
    # Use word-boundary regex to avoid false positives from substring matches
    # (e.g. "UserResult" matching inside "UserUpdateResult").
    models_init_text = models_init.read_text(encoding="utf-8")
    missing: list[str] = []
    for old, new in RENAMES_V9_TO_V10.items():
        if not re.search(rf"\b{re.escape(new)}\b", models_init_text):
            missing.append(f"{old} -> {new}")

    if missing:
        print(
            f"Warning: {len(missing)} rename targets not found in models, "
            "skipping deprecated aliases for them:"
        )
        for m in missing:
            print(f"  {m}")

    # Only include renames where the target exists
    valid_renames = {
        old: new
        for old, new in RENAMES_V9_TO_V10.items()
        if re.search(rf"\b{re.escape(new)}\b", models_init_text)
    }

    if not valid_renames:
        print("No valid renames found, skipping deprecated aliases")
        return

    _patch_models_init(models_init, valid_renames)
    _patch_top_level_init(top_init, valid_renames)

    print(f"Emitted {len(valid_renames)} deprecated type aliases (v9 → v10)")
