"""Default newly required response fields that older servers omit.

The bundled spec marks some response fields required that servers released
before the field existed do not send. The generated ``d.pop("field")`` (made
``pop_required`` by hook 1260) then rejects an otherwise valid response from
those servers. For each listed field this hook pops with a default instead.

Runs before 1260, which only rewrites bare single-argument pops. An entry the
bundled spec does not declare as required (an older SPEC_REF) is skipped; one it
does declare must match, so a renamed model or field fails generation instead of
silently restoring the strict check.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

# (schema, model module, wire name, Python default literal, reason)
VERSION_SKEW_DEFAULTS: list[tuple[str, str, str, str, str]] = [
    (
        "CamundaUserResult",
        "camunda_user_result",
        "isAnonymous",
        "False",
        "added in 8.10.10; older servers never answer an anonymous caller",
    ),
    (
        "AuthenticatedCamundaUserResult",
        "authenticated_camunda_user_result",
        "isAnonymous",
        "False",
        "added in 8.10.10; older servers never answer an anonymous caller",
    ),
]


def apply(source: str, wire_name: str, default: str) -> str:
    """Return ``source`` with the bare pop of ``wire_name`` given ``default``."""
    patched = f'd.pop("{wire_name}", {default})'
    if patched in source:
        return source
    bare = re.compile(r'\bd\.pop\("' + re.escape(wire_name) + r'"\)')
    updated, count = bare.subn(patched, source)
    if count != 1:
        raise SystemExit(
            f'hook 0460: expected exactly one d.pop("{wire_name}"), found {count}; '
            "update VERSION_SKEW_DEFAULTS"
        )
    return updated


def _required(schemas: dict, name: str, seen: set[str] | None = None) -> set[str]:
    """Required wire fields of ``name``, including those inherited through allOf."""
    seen = seen or {name}
    schema = schemas.get(name)
    if not isinstance(schema, dict):
        return set()
    out = {f for f in schema.get("required") or [] if isinstance(f, str)}
    for part in schema.get("allOf") or []:
        if not isinstance(part, dict):
            continue
        ref = part.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
            parent = ref.rsplit("/", 1)[-1]
            if parent not in seen:
                seen.add(parent)
                out |= _required(schemas, parent, seen)
        else:
            out |= _required({"_": part}, "_", seen)
    return out


def _load_schemas(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        spec = json.load(f) if path.suffix == ".json" else yaml.safe_load(f)
    components = spec.get("components") if isinstance(spec, dict) else None
    schemas = components.get("schemas") if isinstance(components, dict) else None
    return schemas if isinstance(schemas, dict) else {}


def run(context: dict[str, str]) -> None:
    bundled = context.get("bundled_spec_path") or context.get("spec_path")
    if not bundled:
        raise SystemExit("hook 0460: no spec path in context")
    schemas = _load_schemas(Path(bundled).resolve())
    models = Path(context["out_dir"]).resolve() / "camunda_orchestration_sdk" / "models"
    applied, skipped = [], []
    for schema, module, wire_name, default, _reason in VERSION_SKEW_DEFAULTS:
        if wire_name not in _required(schemas, schema):
            skipped.append(f"{schema}.{wire_name}")
            continue
        target = models / f"{module}.py"
        if not target.exists():
            raise SystemExit(
                f"hook 0460: {target.name} not found for {schema}.{wire_name}; update "
                "VERSION_SKEW_DEFAULTS"
            )
        source = target.read_text(encoding="utf-8")
        updated = apply(source, wire_name, default)
        if updated != source:
            target.write_text(updated, encoding="utf-8")
        applied.append(f"{module}.{wire_name}")
    print(
        f"hook 0460: defaulted {len(applied)} version-skew field(s) {applied}; "
        f"not in this spec: {skipped}"
    )
