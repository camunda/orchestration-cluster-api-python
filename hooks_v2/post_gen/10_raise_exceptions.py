import ast
import os
from pathlib import Path


def _is_docstring_stmt(stmt: ast.stmt) -> bool:
    return (
        isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Constant)
        and isinstance(stmt.value.value, str)
    )


def _set_docstring(func_node: ast.AST, docstring: str) -> None:
    if not isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return

    doc_stmt = ast.Expr(value=ast.Constant(value=docstring))
    if func_node.body and _is_docstring_stmt(func_node.body[0]):
        func_node.body[0] = doc_stmt
    else:
        func_node.body.insert(0, doc_stmt)


def _get_success_type_from_union(type_expr: ast.expr) -> ast.expr:
    """Heuristic: pick the left-most type from a PEP604 union (A | B | C)."""
    current = type_expr
    while isinstance(current, ast.BinOp) and isinstance(current.op, ast.BitOr):
        current = current.left
    return current


def _get_success_type_from_detailed_return(return_annotation: ast.expr | None) -> ast.expr | None:
    """Given detailed's return annotation (typically Response[T]), returns the success type expr."""
    if return_annotation is None:
        return None
    if not isinstance(return_annotation, ast.Subscript):
        return None

    # detailed returns Response[T] where T is (Success | Error1 | Error2 ...)
    slice_val = return_annotation.slice
    if isinstance(slice_val, ast.Tuple) and slice_val.elts:
        # Very defensive; shouldn't happen for our generator output.
        slice_val = slice_val.elts[0]
    return _get_success_type_from_union(slice_val)


def _rewrite_docstring(docstring: str, return_type_str: str) -> str:
    lines = docstring.splitlines()
    if not lines:
        return docstring

    def is_section_header(line: str) -> bool:
        stripped = line.strip()
        return stripped.endswith(":") and stripped[:-1] in {"Args", "Raises", "Returns", "Attributes"}

    def find_section(name: str) -> int | None:
        for i, line in enumerate(lines):
            if line.strip() == f"{name}:":
                return i
        return None

    # Update/insert Raises section for UnexpectedStatus
    raises_i = find_section("Raises")
    returns_i = find_section("Returns")

    if raises_i is None:
        insert_at = returns_i if returns_i is not None else len(lines)
        block = [
            "",
            "Raises:",
            "    errors.UnexpectedStatus: If the response status code is not 2xx.",
            "    httpx.TimeoutException: If the request takes longer than Client.timeout.",
        ]
        lines[insert_at:insert_at] = block
        # refresh indices
        raises_i = find_section("Raises")
        returns_i = find_section("Returns")
    else:
        # Replace the UnexpectedStatus description if present; otherwise insert it.
        j = raises_i + 1
        inserted = False
        while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith(" ") or lines[j].startswith("\t")):
            if lines[j].lstrip().startswith("errors.UnexpectedStatus:"):
                indent = lines[j][: len(lines[j]) - len(lines[j].lstrip())]
                lines[j] = f"{indent}errors.UnexpectedStatus: If the response status code is not 2xx."
                inserted = True
                break
            j += 1

        if not inserted:
            # Insert right after the Raises: header
            lines.insert(raises_i + 1, "    errors.UnexpectedStatus: If the response status code is not 2xx.")

    # Update Returns section to match the rewritten return annotation.
    returns_i = find_section("Returns")
    if returns_i is not None:
        content_start = returns_i + 1
        content_end = content_start
        while content_end < len(lines) and not is_section_header(lines[content_end]):
            content_end += 1

        # Determine indentation to use for the content line
        indent = "    "
        if content_start < len(lines) and lines[content_start].strip() != "":
            indent = lines[content_start][: len(lines[content_start]) - len(lines[content_start].lstrip())]

        lines[content_start:content_end] = [f"{indent}{return_type_str}"]

    return "\n".join(lines)

def modify_api_file(file_path):
    with open(file_path, "r") as f:
        code = f.read()
    
    tree = ast.parse(code)
    modified = False
    
    # We need to find the sync and asyncio functions
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name not in {"sync", "asyncio"}:
            continue

        # Ensure the function accepts **kwargs if it doesn't already.
        # Needed for the flattened client which passes extra kwargs.
        if not node.args.kwarg:
            node.args.kwarg = ast.arg(arg="kwargs", annotation=None)
            modified = True

        detailed_func_name = f"{node.name}_detailed"
        detailed_node = next(
            (
                n
                for n in tree.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == detailed_func_name
            ),
            None,
        )

        success_type = _get_success_type_from_detailed_return(detailed_node.returns if detailed_node else None)
        if success_type is not None:
            node.returns = success_type
            modified = True
        return_type_str = ast.unparse(node.returns) if node.returns is not None else "Any"

        # Rewrite body if it doesn't already raise on non-2xx
        already_raises = "raise errors.UnexpectedStatus" in ast.unparse(node)
        if not already_raises:
            func_call = f"{detailed_func_name}(\n"
            for arg in node.args.args:
                if arg.arg != "self":  # module functions have no self, but be safe
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
            modified = True

        # Rewrite docstring so it matches the rewritten behavior/signature.
        docstring = ast.get_docstring(node)
        if not docstring and detailed_node:
            docstring = ast.get_docstring(detailed_node)

        if docstring:
            updated_docstring = _rewrite_docstring(docstring, return_type_str)
            _set_docstring(node, updated_docstring)
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
