import os
import re
from pathlib import Path

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def generate_flat_client(package_path):
    api_dir = package_path / "api"
    if not api_dir.exists():
        print(f"API directory not found at {api_dir}")
        return

    methods = []

    # Walk through the api directory
    for root, dirs, files in os.walk(api_dir):
        for file in files:
            if file == "__init__.py" or not file.endswith(".py"):
                continue

            # Get the module path relative to the package
            rel_path = Path(root).relative_to(package_path)
            module_name = file[:-3]
            
            # Construct import path
            import_path = f".{'.'.join(rel_path.parts)}.{module_name}"
            
            # The function name is usually the same as the file name in this generator
            method_name = module_name
            
            # Add sync method with local import
            methods.append(f"""
    def {method_name}(self, *args, **kwargs):
        from {import_path} import sync as {method_name}_sync
        return {method_name}_sync(client=self.client, *args, **kwargs)
""")
            
            # Add async method with local import
            methods.append(f"""
    async def {method_name}_async(self, *args, **kwargs):
        from {import_path} import asyncio as {method_name}_asyncio
        return await {method_name}_asyncio(client=self.client, *args, **kwargs)
""")

    # Read the existing client.py
    client_file = package_path / "client.py"
    if not client_file.exists():
        print(f"Client file not found at {client_file}. Skipping flattening.")
        return

    with open(client_file, "r") as f:
        content = f.read()

    # Prepare the new content
    new_methods = "\n".join(methods)

    camunda_client_code = f"""
class CamundaClient:
    client: Client | AuthenticatedClient

    def __init__(self, base_url: str, token: str | None = None, **kwargs):
        if token:
            self.client = AuthenticatedClient(base_url=base_url, token=token, **kwargs)
        else:
            self.client = Client(base_url=base_url, **kwargs)

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        return self.client.__exit__(*args, **kwargs)

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.client.__aexit__(*args, **kwargs)

{new_methods}
"""
    
    # Append CamundaClient to the end of the file
    if "class CamundaClient" not in content:
        content += f"\n{camunda_client_code}"

    with open(client_file, "w") as f:
        f.write(content)
    
    print(f"Successfully added CamundaClient to {client_file}")

    # Update __init__.py to export CamundaClient
    init_file = package_path / "__init__.py"
    if init_file.exists():
        with open(init_file, "r") as f:
            init_content = f.read()
        
        if "CamundaClient" not in init_content:
            init_content = init_content.replace(
                '"Client",',
                '"Client",\n    "CamundaClient",'
            )
            init_content = init_content.replace(
                "from .client import AuthenticatedClient, Client",
                "from .client import AuthenticatedClient, Client, CamundaClient"
            )
            
            with open(init_file, "w") as f:
                f.write(init_content)
            print(f"Successfully exported CamundaClient in {init_file}")

# def run(context):
#     out_dir = Path(context["out_dir"])
#     package_dir = out_dir / "camunda_orchestration_sdk"
#     if not package_dir.exists():
#         print(f"Could not find package directory in {out_dir}")
#         return
#     generate_flat_client(package_dir)

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    package_dir = base_dir / "generated" / "camunda_orchestration_sdk"
    generate_flat_client(package_dir)
