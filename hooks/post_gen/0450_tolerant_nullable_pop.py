"""Make ``DeploymentMetadataResult.from_dict`` tolerant of missing nullable fields.

Older gateways omit null-valued keys from the deployment response (e.g.
a BPMN-only deploy only returns ``processDefinition``).  The generator
emits bare ``d.pop("fieldName")`` which throws ``KeyError``.

This hook patches only ``deployment_metadata_result.py`` so those pops
default to ``None``, letting ``ExtendedDeploymentResult`` produce empty
lists for inapplicable resource types.
"""

from __future__ import annotations

import re
from pathlib import Path

# The nullable fields on DeploymentMetadataResult that the server may omit.
_NULLABLE_FIELDS = {
    "processDefinition",
    "decisionDefinition",
    "decisionRequirements",
    "form",
    "resource",
}

_BARE_POP = re.compile(r'd\.pop\("(\w+)"\)')


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"]).resolve()
    target = (
        out_dir
        / "camunda_orchestration_sdk"
        / "models"
        / "deployment_metadata_result.py"
    )

    if not target.exists():
        print(
            "[0450_tolerant_nullable_pop] deployment_metadata_result.py not found, skipping"
        )
        return

    content = target.read_text(encoding="utf-8")
    count = 0

    def _replace(m: re.Match[str]) -> str:
        nonlocal count
        field = m.group(1)
        if field in _NULLABLE_FIELDS:
            count += 1
            return f'd.pop("{field}", None)'
        return m.group(0)

    new_content = _BARE_POP.sub(_replace, content)
    if count > 0:
        target.write_text(new_content, encoding="utf-8")

    print(
        f"[0450_tolerant_nullable_pop] patched {count} d.pop() calls in deployment_metadata_result.py"
    )
