from __future__ import annotations
import re
from pathlib import Path


def run(context: dict) -> None:
    out_dir = Path(context["out_dir"]).resolve()
    models_dir = out_dir / "camunda_orchestration_sdk" / "models"
    if not models_dir.exists():
        return

    # Fix invalid imports like models.str and models.null<str>
    for path in models_dir.glob("*.py"):
        txt = path.read_text(encoding="utf-8")
        new = txt
        # from camunda_orchestration_sdk.models.str import str -> builtin alias
        new = new.replace(
            "from camunda_orchestration_sdk.models.str import str",
            "from builtins import str as str",
        )

        # Replace any import of null<...> with builtins or remove; then fix class base
        new = re.sub(r"from camunda_orchestration_sdk\.models\.null<[^>]+> import null<[^>]+>", "", new)
        new = re.sub(r"class (\w+)\(null<[^>]+>\):", r"class \1(object):", new)

        if new != txt:
            path.write_text(new, encoding="utf-8")
            print(f'Patched {path}')








