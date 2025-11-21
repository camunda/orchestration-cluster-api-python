from pathlib import Path


def ensure_element_instance_key_model(models_dir: Path) -> None:
    target = models_dir / "element_instance_key.py"
    if target.exists():
        return
    target.write_text(
        """
# Minimal model to satisfy references to ElementInstanceKey in generated code
from pydantic import RootModel, StrictStr


class ElementInstanceKey(RootModel[StrictStr]):
    pass
""".lstrip(),
        encoding="utf-8",
    )


def ensure_import_in_wrapper(models_dir: Path) -> None:
    wrapper = models_dir / "process_instance_modification_activate_instruction_ancestor_element_instance_key.py"
    if not wrapper.exists():
        return
    content = wrapper.read_text(encoding="utf-8")
    import_line = "from camunda_orchestration_sdk.models.element_instance_key import ElementInstanceKey\n"
    if import_line in content:
        return
    # Insert after the typing imports block
    insert_after = "from typing_extensions import Literal, Self\n"
    if insert_after in content:
        content = content.replace(insert_after, insert_after + import_line)
    else:
        # Fallback: prepend at top after header docstring
        marker = '"""  # noqa: E501\n\n\n'
        if marker in content:
            content = content.replace(marker, marker + import_line)
        else:
            content = import_line + content
    wrapper.write_text(content, encoding="utf-8")


def run(context: dict) -> None:
    models_dir = Path(context["out_dir"]).resolve() / "camunda_orchestration_sdk" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    ensure_element_instance_key_model(models_dir)
    ensure_import_in_wrapper(models_dir)





