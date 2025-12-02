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
    # imports = [] # No global imports to avoid circular dependency

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
            
            # imports.append(f"from {import_path} import sync as {method_name}_sync, asyncio as {method_name}_asyncio")
            
            # Add sync method with local import
            methods.append(f"""
    def {method_name}(self, *args, **kwargs):
        from {import_path} import sync as {method_name}_sync
        return {method_name}_sync(client=self, *args, **kwargs)
""")
            
            # Add async method with local import
            methods.append(f"""
    async def {method_name}_async(self, *args, **kwargs):
        from {import_path} import asyncio as {method_name}_asyncio
        return await {method_name}_asyncio(client=self, *args, **kwargs)
""")

    # Read the existing client.py
    client_file = package_path / "client.py"
    if not client_file.exists():
        print(f"Client file not found at {client_file}. Skipping flattening.")
        return

    with open(client_file, "r") as f:
        content = f.read()

    # Prepare the new content
    # new_imports = "\n".join(imports)
    new_methods = "\n".join(methods)

    # Inject imports - No longer needed
    # content = content.replace("import ssl", f"{new_imports}\nimport ssl")

    # Inject methods into Client class
    # We look for the end of the Client class. It ends before "class AuthenticatedClient"
    client_split = content.split("class AuthenticatedClient")
    
    # Add methods to Client
    client_part = client_split[0]
    # Find the last method in Client to append after
    # A simple heuristic is to append before the class ends. 
    # But since we are splitting by AuthenticatedClient, the first part is the Client class + imports.
    
    # Actually, let's just append a Mixin and make Client inherit from it.
    # That's safer than regex replacement inside the class.
    
    mixin_code = f"""
class ClientMixin:
{new_methods}
"""
    
    # Insert Mixin definition before Client
    content = content.replace("@define\nclass Client:", f"{mixin_code}\n@define\nclass Client(ClientMixin):")
    
    # Also update AuthenticatedClient to inherit from Mixin
    content = content.replace("@define\nclass AuthenticatedClient:", "@define\nclass AuthenticatedClient(ClientMixin):")

    with open(client_file, "w") as f:
        f.write(content)
    
    print(f"Successfully flattened client in {client_file}")

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
