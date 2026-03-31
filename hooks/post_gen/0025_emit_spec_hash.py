"""Post-generation hook: embed specHash from spec-metadata.json.

Writes a ``_spec_hash.py`` module into the generated package so the
hash is accessible at runtime via::

    from camunda_orchestration_sdk import SPEC_HASH

and is included in the published PyPI package automatically.
"""

from __future__ import annotations

import json
from pathlib import Path


def run(context: dict[str, str]) -> None:
    metadata_path = context.get("metadata_path", "")
    if not metadata_path or not Path(metadata_path).exists():
        print("[emit-spec-hash] spec-metadata.json not found, skipping")
        return

    with open(metadata_path, encoding="utf-8") as f:
        metadata = json.load(f)

    spec_hash: str = metadata.get("specHash", "")
    if not spec_hash.startswith("sha256:"):
        print(f"[emit-spec-hash] Unexpected specHash format: {spec_hash}")

    out_dir = Path(context["out_dir"]) / "camunda_orchestration_sdk"
    output_file = out_dir / "_spec_hash.py"

    content = (
        '# Auto-generated \u2014 do not edit.\n'
        '# SHA-256 digest of the OpenAPI spec this SDK was generated from.\n'
        f'SPEC_HASH = "{spec_hash}"\n'
    )

    output_file.write_text(content, encoding="utf-8")
    print(f"[emit-spec-hash] Wrote {output_file}")
