import ast
import os
from pathlib import Path

def get_success_type(return_annotation):
    """
    Extracts the success type from a return annotation.
    Assumes the success type is the first one in the Union or the only one if not a Union.
    This is a heuristic and might need adjustment based on actual generated code structure.
    """
    if isinstance(return_annotation, ast.BinOp) and isinstance(return_annotation.op, ast.BitOr):
        # Handle TypeA | TypeB | ...
        # We assume the first type is the success type (200 OK)
        # Recursively get the left-most type
        return get_success_type(return_annotation.left)
    elif isinstance(return_annotation, ast.Name):
        return return_annotation
    elif isinstance(return_annotation, ast.Subscript): # Optional[Type] or Union[Type, None]
        # If it's Optional[Type], we want Type.
        # But wait, the generated code uses | None for optional.
        # If it is Response[Type], we want Type.
        return return_annotation
    return return_annotation

def modify_api_file(file_path):
    with open(file_path, "r") as f:
        code = f.read()
    
    tree = ast.parse(code)
    modified = False
    
    # We need to find the sync and asyncio functions
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in ["sync", "asyncio"]:
                # Check if it already raises exceptions (heuristic)
                if "raise errors.UnexpectedStatus" in ast.unparse(node):
                    continue

                # Find the detailed function call
                detailed_func_name = f"{node.name}_detailed"
                
                # Find the detailed function definition to get the return type and docstring
                detailed_node = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == detailed_func_name), None)
                
                success_type = None
                if detailed_node and detailed_node.returns:
                    # detailed returns Response[Union[...]]
                    # We want the first type in the Union inside Response
                    if isinstance(detailed_node.returns, ast.Subscript):
                        slice_val = detailed_node.returns.slice
                        success_type = get_success_type(slice_val)

                if success_type:
                    node.returns = success_type
                    modified = True
                
                # Rewrite body
                func_call = f"{detailed_func_name}(\n"
                for arg in node.args.args:
                    if arg.arg != 'self': # self is not there for module functions
                        func_call += f"    {arg.arg}={arg.arg},\n"
                for arg in node.args.kwonlyargs:
                     func_call += f"    {arg.arg}={arg.arg},\n"
                func_call += ")"
                
                if isinstance(node, ast.AsyncFunctionDef):
                    func_call = f"await {func_call}"
                
                new_body_code = f"""
def temp():
    response = {func_call}
    if response.status_code < 200 or response.status_code >= 300:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return response.parsed
"""
                new_body_ast = ast.parse(new_body_code).body[0].body
                node.body = new_body_ast
                
                # Update docstring
                docstring = ast.get_docstring(node)
                if not docstring and detailed_node:
                    docstring = ast.get_docstring(detailed_node)
                
                if docstring:
                    # Add Raises section if not present
                    if "Raises:" not in docstring:
                        docstring += "\n\n    Raises:\n        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True."
                    else:
                        # Append to existing Raises
                        pass # Simplified for now
                    
                    node.body.insert(0, ast.Expr(value=ast.Constant(value=docstring)))
                
                modified = True

    if modified:
        # We need to unparse. ast.unparse is available in Python 3.9+
        with open(file_path, "w") as f:
            f.write(ast.unparse(tree))
        print(f"Modified {file_path}")

def run(context):
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    api_dir = package_dir / "api"
    
    if not api_dir.exists():
        print(f"API directory not found at {api_dir}")
        return

    for root, dirs, files in os.walk(api_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                modify_api_file(Path(root) / file)

if __name__ == "__main__":
    # For testing
    pass
