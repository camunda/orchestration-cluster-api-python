"""Post-generation hook: embed specHash from spec-metadata.json.

Writes a ``_spec_hash.py`` module into the generated package so the
hash is accessible at runtime via::

    from camunda_orchestration_sdk import SPEC_HASH

and is included in the published PyPI package automatically.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


_SPEC_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def run(context: dict[str, str]) -> None:
    metadata_path_str = context.get("metadata_path", "")
    metadata_path = Path(metadata_path_str) if metadata_path_str else None

    if not metadata_path or not metadata_path.exists():
        raise FileNotFoundError(
            f"[emit-spec-hash] spec-metadata.json not found at "
            f"{metadata_path_str!r} — cannot emit SPEC_HASH"
        )

    with open(metadata_path, encoding="utf-8") as f:
        metadata = json.load(f)

    spec_hash: str = metadata.get("specHash", "") or ""

    if not _SPEC_HASH_RE.match(spec_hash):
        raise ValueError(
            f"[emit-spec-hash] specHash is missing or invalid "
            f"(expected sha256:<64 hex chars>): {spec_hash!r}"
        )

    out_dir = Path(context["out_dir"]) / "camunda_orchestration_sdk"
    output_file = out_dir / "_spec_hash.py"

    content = (
        '# Auto-generated \u2014 do not edit.\n'
        '# SHA-256 digest of the OpenAPI spec this SDK was generated from.\n'
        f'SPEC_HASH = "{spec_hash}"\n'
    )

    output_file.write_text(content, encoding="utf-8")
    print(f"[emit-spec-hash] Wrote {output_file}")
