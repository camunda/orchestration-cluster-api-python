"""Post-generation hook: drop discriminator-only ``oneOf`` union base models.

Upstream models a polymorphic ``oneOf`` union by giving each variant an
``allOf`` reference to a shared base that carries only the discriminator
property (e.g. ``BaseWaitStateDetails`` with just ``waitStateType``).
openapi-python-client flattens those fields into each variant, so the base
model is emitted and exported but referenced nowhere — dead public surface.

This hook detects such bases from the bundled spec and removes the generated
model module, its stub, and every re-export. A base is removed only when it is
*discriminator-only* and referenced nowhere except as the ``allOf`` base of the
union's variants, so genuinely-shared mixins (bases contributing real fields,
or referenced as a property/body/response type) are left untouched.

Mirrors the C# generator fix (camunda/orchestration-cluster-api-csharp#256).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, cast


def _get(obj: object, key: str) -> Any:
    """``obj.get(key)`` when ``obj`` is a mapping, else ``None`` (typed ``Any``)."""
    if isinstance(obj, dict):
        return cast("dict[str, Any]", obj).get(key)
    return None


def _items(obj: object) -> list[tuple[str, Any]]:
    """Items of a mapping with string keys, or empty when ``obj`` is not one."""
    if isinstance(obj, dict):
        return [(k, v) for k, v in cast("dict[str, Any]", obj).items() if isinstance(k, str)]
    return []


def _ref_name(node: object) -> str | None:
    """Return the schema name of a ``$ref`` node, or ``None``."""
    ref = _get(node, "$ref")
    if isinstance(ref, str) and "/" in ref:
        return ref.rsplit("/", 1)[-1]
    return None


def _load_spec(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        import yaml  # available in the generation environment

        return yaml.safe_load(text)


def _is_discriminator_only(schema: object, discriminator: str) -> bool:
    """True if ``schema``'s sole property is the union discriminator."""
    if not isinstance(schema, dict):
        return False
    if _get(schema, "allOf") or _get(schema, "oneOf") or _get(schema, "anyOf"):
        return False
    props = _get(schema, "properties")
    return isinstance(props, dict) and list(props.keys()) == [discriminator]


def _find_orphan_bases(spec: object) -> set[str]:
    schemas = _get(_get(spec, "components"), "schemas")
    if not isinstance(schemas, dict):
        return set()

    # Map each oneOf-union variant to its discriminator property.
    union_names: set[str] = set()
    variant_names: set[str] = set()
    variant_discriminator: dict[str, str] = {}
    for name, schema in _items(schemas):
        one_of = _get(schema, "oneOf")
        disc = _get(schema, "discriminator")
        if not (isinstance(one_of, list) and one_of and isinstance(disc, dict)):
            continue
        prop = _get(disc, "propertyName")
        if not isinstance(prop, str):
            continue
        variants = [r for r in (_ref_name(v) for v in one_of) if isinstance(r, str)]
        if len(variants) != len(one_of):
            continue  # some oneOf entry was not a plain $ref
        union_names.add(name)
        for variant in variants:
            variant_names.add(variant)
            variant_discriminator.setdefault(variant, prop)

    # Candidate bases: discriminator-only schemas pulled into a variant via allOf.
    candidates: set[str] = set()
    for variant, prop in variant_discriminator.items():
        all_of = _get(_get(schemas, variant), "allOf")
        if not isinstance(all_of, list):
            continue
        for entry in all_of:
            base = _ref_name(entry)
            if base and _is_discriminator_only(_get(schemas, base), prop):
                candidates.add(base)
    if not candidates:
        return set()

    # Collect every reference EXCEPT a variant's allOf ref to a candidate base;
    # any other reference is a genuine use that disqualifies suppression.
    referenced: set[str] = set()

    def collect(node: object) -> None:
        if isinstance(node, dict):
            ref = _ref_name(node)
            if ref is not None:
                referenced.add(ref)
                return
            for _key, value in _items(node):
                collect(value)
        elif isinstance(node, list):
            for item in node:
                collect(item)

    for name, schema in _items(schemas):
        is_variant = name in variant_names
        for key, value in _items(schema):
            if key == "allOf" and is_variant and isinstance(value, list):
                for entry in value:
                    base = _ref_name(entry)
                    if base and base in candidates:
                        continue  # the suppressible discriminator-base ref
                    collect(entry)
            else:
                collect(value)

    # Operation parameters, request bodies, and responses are real uses too.
    collect(_get(spec, "paths"))

    return {
        base
        for base in candidates
        if base not in referenced
        and base not in union_names
        and base not in variant_names
    }


def _class_to_module(models_init: Path) -> dict[str, str]:
    """Map exported class name -> model module, parsed from models/__init__.py."""
    mapping: dict[str, str] = {}
    for line in models_init.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\s*from \.(\w+) import (\w+)\s*$", line)
        if match:
            mapping[match.group(2)] = match.group(1)
    return mapping


def _strip_symbol(path: Path, class_name: str, module: str) -> None:
    """Remove the import and ``__all__`` entries for a symbol from an init file."""
    if not path.exists():
        return
    drop = {
        f'"{class_name}",',
        f'"{class_name}"',
        f"{class_name},",
        f"from .{module} import {class_name}",
    }
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = [line for line in lines if line.strip() not in drop]
    if len(kept) != len(lines):
        path.write_text("".join(kept), encoding="utf-8")


def run(context: dict[str, str]) -> None:
    bundled = context.get("bundled_spec_path")
    if not bundled or not Path(bundled).exists():
        print("drop-orphan-union-bases: no bundled spec, skipping")
        return

    out_dir = Path(context["out_dir"])
    package = out_dir / "camunda_orchestration_sdk"
    models_init = package / "models" / "__init__.py"
    if not models_init.exists():
        print("drop-orphan-union-bases: models/__init__.py not found, skipping")
        return

    orphans = _find_orphan_bases(_load_spec(Path(bundled)))
    if not orphans:
        print("drop-orphan-union-bases: no orphan union bases found")
        return

    class_to_module = _class_to_module(models_init)
    stubs_package = out_dir.parent / "stubs" / "camunda_orchestration_sdk"

    removed: list[str] = []
    for class_name in sorted(orphans):
        module = class_to_module.get(class_name)
        if module is None:
            # Cannot map the schema to a generated module; leave it untouched.
            continue
        for model_file in (
            package / "models" / f"{module}.py",
            stubs_package / "models" / f"{module}.pyi",
        ):
            if model_file.exists():
                model_file.unlink()
        for init_file in (
            package / "models" / "__init__.py",
            package / "__init__.py",
            stubs_package / "models" / "__init__.pyi",
            stubs_package / "__init__.pyi",
        ):
            _strip_symbol(init_file, class_name, module)
        removed.append(class_name)

    if removed:
        print(f"drop-orphan-union-bases: removed {', '.join(removed)}")
    else:
        print("drop-orphan-union-bases: no mappable orphan bases to remove")
