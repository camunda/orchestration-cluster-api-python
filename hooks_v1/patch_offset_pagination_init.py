from pathlib import Path
from typing import Any, Dict

def run(context: Dict[str, Any]) -> None:
    """
    Patch OffsetPagination to add an explicit __init__ method.
    This helps IDEs like Pylance understand the constructor arguments,
    especially 'var_from' which is an alias for the reserved keyword 'from'.
    """
    out_dir = Path(context["out_dir"])
    file_path = out_dir / "camunda_orchestration_sdk" / "models" / "offset_pagination.py"
    
    if not file_path.exists():
        print(f"Warning: {file_path} does not exist, skipping patch.")
        return

    print(f"Patching {file_path} to add explicit __init__...")
    content = file_path.read_text(encoding="utf-8")
    
    # Check if already patched
    if "def __init__(self, var_from: Optional[int] = 0" in content:
        print("Already patched.")
        return

    # The insertion point is after model_config
    target_string = """    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )"""
    
    replacement_string = """    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def __init__(self, var_from: Optional[int] = 0, limit: Optional[int] = 100, **kwargs):
        \"\"\"
        OffsetPagination
        \"\"\"
        super().__init__(var_from=var_from, limit=limit, **kwargs)"""

    if target_string in content:
        content = content.replace(target_string, replacement_string)
        file_path.write_text(content, encoding="utf-8")
        print("Successfully patched OffsetPagination.")
    else:
        print("Warning: Could not find target string to patch in OffsetPagination.")
