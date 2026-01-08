from pathlib import Path
import shutil

def run(context):
    out_dir = Path(context["out_dir"])
    root_dir = Path(__file__).parents[1]
    runtime_dir = root_dir / "runtime"
    
    # The user specified generated/camunda_orchestration_sdk
    # context["out_dir"] is likely "generated"
    # We need to find the package directory. 
    # Based on the user request, it is "camunda_orchestration_sdk".
    
    dest_dir = out_dir / "camunda_orchestration_sdk" / "runtime"
    
    print(f"Copying runtime from {runtime_dir} to {dest_dir}")
    
    if not runtime_dir.exists():
        print(f"Warning: Runtime directory {runtime_dir} does not exist. Skipping copy.")
        return

    if not dest_dir.parent.exists():
        print(f"Warning: Destination parent {dest_dir.parent} does not exist. Skipping copy.")
        return

    if dest_dir.exists():
        shutil.rmtree(dest_dir)
        
    shutil.copytree(runtime_dir, dest_dir)
    print("Runtime directory copied successfully.")
