"""Default newly required response fields that older servers omit.

The bundled spec marks some response fields required that servers released
before the field existed do not send. The generated ``d.pop("field")`` (made
``pop_required`` by hook 1260) then rejects an otherwise valid response from
those servers. For each listed field this hook pops with a default instead.

Runs before 1260, which only rewrites bare single-argument pops. Every entry
must match, so a renamed model or field fails generation instead of silently
restoring the strict check.
"""

from __future__ import annotations

import re
from pathlib import Path

# (model module, wire name, Python default literal, reason)
VERSION_SKEW_DEFAULTS: list[tuple[str, str, str, str]] = [
    (
        "camunda_user_result",
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


def run(context: dict[str, str]) -> None:
    models = Path(context["out_dir"]).resolve() / "camunda_orchestration_sdk" / "models"
    applied = []
    for module, wire_name, default, _reason in VERSION_SKEW_DEFAULTS:
        target = models / f"{module}.py"
        if not target.exists():
            raise SystemExit(
                f"hook 0460: {target.name} not found for {wire_name}; update "
                "VERSION_SKEW_DEFAULTS"
            )
        source = target.read_text(encoding="utf-8")
        updated = apply(source, wire_name, default)
        if updated != source:
            target.write_text(updated, encoding="utf-8")
        applied.append(f"{module}.{wire_name}")
    print(f"hook 0460: defaulted {len(applied)} version-skew field(s) {applied}")
