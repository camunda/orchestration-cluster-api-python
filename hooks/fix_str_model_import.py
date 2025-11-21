from pathlib import Path


def run(context: dict) -> None:
    out_dir = Path(context["out_dir"]).resolve()
    models_dir = out_dir / "camunda_orchestration_sdk" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    shim = models_dir / "str.py"
    # Provide a shim so imports like `from ...models.str import str` succeed.
    if not shim.exists():
        shim.write_text("""
# auto-generated shim to satisfy imports of a pseudo-model named `str`
str = str
""".lstrip(), encoding="utf-8")




