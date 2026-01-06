from pathlib import Path

def run(context):
    """
    Creates a py.typed file in the package root to indicate that the package supports type checking.
    """
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    
    if not package_dir.exists():
        print(f"Package directory not found at {package_dir}")
        return

    py_typed_file = package_dir / "py.typed"
    
    # Create empty file
    py_typed_file.touch()
    print(f"Created {py_typed_file}")
