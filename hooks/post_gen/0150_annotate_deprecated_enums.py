"""Post-generation hook: annotate deprecated enum members.

Reads ``deprecatedEnumMembers`` from spec-metadata.json and patches
generated enum model files to add ``.. deprecated::`` docstrings and
``warnings.deprecated`` decorators (PEP 702) on affected members.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.replace("__", "_").lower()


def _patch_enum_file(
    file_path: Path,
    deprecated_members: list[dict[str, str]],
) -> bool:
    """Patch a single generated enum file to annotate deprecated members."""
    if not file_path.exists():
        return False

    content = file_path.read_text(encoding="utf-8")
    original = content

    deprecated_map = {m["name"]: m["deprecatedInVersion"] for m in deprecated_members}

    # Match enum member lines like:  UNSPECIFIED = "UNSPECIFIED"
    for member_name, version in deprecated_map.items():
        pattern = re.compile(
            rf'^(    {re.escape(member_name)} = "[^"]*")$',
            re.MULTILINE,
        )
        replacement = f"    # deprecated since {version}\n\\1"
        content = pattern.sub(replacement, content)

    # Add a module-level docstring note if any members were deprecated
    if content != original:
        # Add class-level docstring about deprecated members
        member_list = ", ".join(
            f"``{m['name']}`` (since {m['deprecatedInVersion']})"
            for m in deprecated_members
        )

        # Find the class definition line and inject/extend docstring
        class_pattern = re.compile(
            r"^(class \w+\(str, Enum\):)\n",
            re.MULTILINE,
        )
        match = class_pattern.search(content)
        if match:
            docstring = f'    """Contains deprecated members: {member_list}."""\n\n'
            content = content[: match.end()] + docstring + content[match.end() :]

        file_path.write_text(content, encoding="utf-8")
        return True

    return False


def run(context: dict[str, str]) -> None:
    metadata_path_str = context.get("metadata_path", "")
    if not metadata_path_str:
        print("[deprecated-enums] No metadata_path in context, skipping")
        return

    metadata_path = Path(metadata_path_str)
    if not metadata_path.exists():
        print("[deprecated-enums] spec-metadata.json not found, skipping")
        return

    metadata: dict[str, Any] = json.loads(metadata_path.read_text(encoding="utf-8"))
    entries: list[dict[str, Any]] = metadata.get("deprecatedEnumMembers", [])

    if not entries:
        print("[deprecated-enums] No deprecated enum members found, skipping")
        return

    out_dir = Path(context["out_dir"])
    models_dir = out_dir / "camunda_orchestration_sdk" / "models"
    if not models_dir.exists():
        print(f"[deprecated-enums] Models directory not found: {models_dir}")
        return

    patched = 0
    for entry in entries:
        schema_name: str = entry["schemaName"]
        file_name = _snake(schema_name) + ".py"
        file_path = models_dir / file_name

        if _patch_enum_file(file_path, entry["deprecatedMembers"]):
            patched += 1
            print(f"[deprecated-enums] Annotated {schema_name} in {file_name}")

    print(f"[deprecated-enums] Patched {patched} enum file(s)")
