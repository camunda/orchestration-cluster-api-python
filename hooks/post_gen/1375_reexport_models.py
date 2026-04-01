"""Post-generation hook: re-export models and user-facing runtime types from the top-level package.

This allows users to write:

    from camunda_orchestration_sdk import CamundaAsyncClient, CreateDeploymentData, File, JobError

instead of importing from nested subpackages.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path


def _parse_all_names(init_path: Path) -> list[str]:
    """Extract the names listed in ``__all__`` from a Python file."""
    source = init_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            # __all__ = [...] or __all__: list[str] = [...]
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if isinstance(target, ast.Name) and target.id == "__all__":
                value = node.value
                if isinstance(value, (ast.List, ast.Tuple)):
                    return [
                        elt.value
                        for elt in value.elts
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                    ]
    return []


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    init_file = package_dir / "__init__.py"
    models_init = package_dir / "models" / "__init__.py"

    if not init_file.exists():
        print(f"Warning: {init_file} not found, skipping model re-exports")
        return
    if not models_init.exists():
        print(f"Warning: {models_init} not found, skipping model re-exports")
        return

    # Collect names to re-export
    model_names = _parse_all_names(models_init)
    # User-facing types beyond models: File, worker context/exceptions, handler aliases
    _job_worker_names = [
        "AsyncJobContext",
        "ConnectedJobContext",
        "SyncJobContext",
        "JobContext",
        "JobError",
        "JobFailure",
        "ConnectedAsyncJobHandler",
        "ConnectedSyncJobHandler",
        "ConnectedJobHandler",
        "IsolatedAsyncJobHandler",
        "IsolatedSyncJobHandler",
        "IsolatedJobHandler",
        "AsyncJobHandler",
        "SyncJobHandler",
    ]
    extra_imports: dict[str, str] = {
        "File": "from .types import File",
        "Unset": "from .types import Unset",
    }

    # Only re-export SPEC_HASH if the backing module exists to avoid import errors
    spec_hash_path = package_dir / "_spec_hash.py"
    if spec_hash_path.exists():
        extra_imports["SPEC_HASH"] = "from ._spec_hash import SPEC_HASH"
    # Build a single grouped import for all job_worker names
    _jw_import = (
        "from .runtime.job_worker import (\n"
        + "".join(f"    {n},\n" for n in _job_worker_names)
        + ")"
    )
    for n in _job_worker_names:
        extra_imports[n] = _jw_import

    if not model_names:
        print("Warning: no model names found in models/__init__.py __all__")
        return

    init_text = init_file.read_text(encoding="utf-8")

    # --- Add import lines ---
    new_imports: list[str] = []

    # Explicit model imports (avoids ruff F403/F405 from star imports)
    models_import = (
        "from camunda_orchestration_sdk.models import (\n"
        + "".join(f"    {n},\n" for n in sorted(model_names))
        + ")"
    )
    if "from camunda_orchestration_sdk.models import" not in init_text:
        new_imports.append(models_import)

    # Deduplicate import lines (multiple names may share one grouped import)
    seen_imports: set[str] = set()
    for import_line in extra_imports.values():
        if import_line not in init_text and import_line not in seen_imports:
            new_imports.append(import_line)
            seen_imports.add(import_line)

    if new_imports:
        init_text = init_text.rstrip("\n") + "\n\n" + "\n".join(new_imports) + "\n"

    # --- Rebuild __all__ as list[str] (pyright needs explicit annotation for large exports) ---
    all_match = re.search(
        r"__all__(?::\s*list\[str\])?\s*=\s*[\(\[]([^\)\]]*)[\)\]]",
        init_text,
        re.DOTALL,
    )
    if all_match:
        existing_all = all_match.group(0)

        # Parse existing names in __all__
        existing_names: list[str] = re.findall(r'"([^"]+)"', all_match.group(1))

        # Merge existing + new names, deduplicated and sorted
        all_names = sorted(
            set(existing_names) | set(model_names) | set(extra_imports.keys())
        )

        quoted = [f'    "{n}",' for n in all_names]
        new_all = "__all__: list[str] = [\n" + "\n".join(quoted) + "\n]"
        init_text = init_text.replace(existing_all, new_all, 1)

    init_file.write_text(init_text, encoding="utf-8")

    total = len(model_names) + len(extra_imports)
    print(
        f"Re-exported {total} names (models + File + JobContext) in top-level __init__.py"
    )
