import ast
import os
import re
from pathlib import Path

import yaml


def _to_camel_case(snake_str: str) -> str:
    parts = snake_str.split("_")
    return "".join(p.title() for p in parts if p)


def _status_suffix(code: int) -> str:
    mapping = {
        400: "BadRequest",
        401: "Unauthorized",
        402: "PaymentRequired",
        403: "Forbidden",
        404: "NotFound",
        405: "MethodNotAllowed",
        408: "RequestTimeout",
        409: "Conflict",
        410: "Gone",
        412: "PreconditionFailed",
        413: "PayloadTooLarge",
        415: "UnsupportedMediaType",
        422: "UnprocessableEntity",
        429: "TooManyRequests",
        500: "InternalServerError",
        501: "NotImplemented",
        502: "BadGateway",
        503: "ServiceUnavailable",
        504: "GatewayTimeout",
    }
    return mapping.get(code, f"Http{code}")


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


def _infer_return_type_from_if(if_node: ast.If) -> str | None:
    # Find the returned expression.
    return_expr: ast.expr | None = None
    for stmt in if_node.body:
        if isinstance(stmt, ast.Return):
            return_expr = stmt.value
            break

    if return_expr is None:
        return None

    # Common pattern: response_XXX = Model.from_dict(...); return response_XXX
    if isinstance(return_expr, ast.Name):
        returned_name = return_expr.id
        for stmt in if_node.body:
            if (
                isinstance(stmt, ast.Assign)
                and len(stmt.targets) == 1
                and isinstance(stmt.targets[0], ast.Name)
                and stmt.targets[0].id == returned_name
            ):
                value = stmt.value
                if isinstance(value, ast.Call):
                    # Model.from_dict(...)
                    if isinstance(value.func, ast.Attribute) and isinstance(value.func.value, ast.Name):
                        return value.func.value.id
                    # cast(Type, ...)
                    if isinstance(value.func, ast.Name) and value.func.id == "cast" and value.args:
                        return ast.unparse(value.args[0])
                return ast.unparse(value)
        return None

    # Other patterns: return Model.from_dict(...)
    if isinstance(return_expr, ast.Call):
        if isinstance(return_expr.func, ast.Attribute) and isinstance(return_expr.func.value, ast.Name):
            return return_expr.func.value.id
        if isinstance(return_expr.func, ast.Name) and return_expr.func.id == "cast" and return_expr.args:
            return ast.unparse(return_expr.args[0])

    return ast.unparse(return_expr)


def _extract_status_type_map(tree: ast.Module) -> dict[int, str]:
    """Return mapping status_code -> parsed model type string from _parse_response."""

    parse_func: ast.FunctionDef | None = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "_parse_response":
            parse_func = node
            break

    if parse_func is None:
        return {}

    status_to_type: dict[int, str] = {}
    for stmt in parse_func.body:
        if not isinstance(stmt, ast.If):
            continue

        test = stmt.test
        if not (
            isinstance(test, ast.Compare)
            and len(test.ops) == 1
            and isinstance(test.ops[0], ast.Eq)
            and len(test.comparators) == 1
            and isinstance(test.comparators[0], ast.Constant)
            and isinstance(test.comparators[0].value, int)
        ):
            continue

        left = test.left
        if not (
            isinstance(left, ast.Attribute)
            and left.attr == "status_code"
            and isinstance(left.value, ast.Name)
            and left.value.id == "response"
        ):
            continue

        code = int(test.comparators[0].value)
        inferred = _infer_return_type_from_if(stmt)
        if inferred:
            status_to_type[code] = inferred

    return status_to_type


def _extract_method_and_url(tree: ast.Module) -> tuple[str, str] | None:
    """Extract (method, url) from the generated `_get_kwargs` function."""

    get_kwargs: ast.FunctionDef | None = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "_get_kwargs":
            get_kwargs = node
            break
    if get_kwargs is None:
        return None

    def _string_template_from_node(node: ast.AST) -> str | None:
        """Best-effort extraction of a URL template string from an AST node.

        Handles:
        - string literals: "/foo"
        - "...".format(...)
        - f-strings: f"/foo/{bar}" (returns "/foo/{}")
        """
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value

        # Pattern: '/path/{x}'.format(x=...)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "format":
            base = node.func.value
            if isinstance(base, ast.Constant) and isinstance(base.value, str):
                return base.value

        # Pattern: f"/path/{x}/..." -> "/path/{}/..."
        if isinstance(node, ast.JoinedStr):
            parts: list[str] = []
            for value in node.values:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    parts.append(value.value)
                elif isinstance(value, ast.FormattedValue):
                    parts.append("{}")
            return "".join(parts)

        return None

    method: str | None = None
    url: str | None = None

    for stmt in get_kwargs.body:
        dict_value: ast.Dict | None = None

        # Pattern 1: _kwargs = {'method': 'post', 'url': '/process-instances'}
        if (
            isinstance(stmt, ast.Assign)
            and len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Name)
            and stmt.targets[0].id == "_kwargs"
            and isinstance(stmt.value, ast.Dict)
        ):
            dict_value = stmt.value

        # Pattern 1b: _kwargs: dict[str, Any] = {'method': 'post', 'url': '/process-instances'}
        if (
            isinstance(stmt, ast.AnnAssign)
            and isinstance(stmt.target, ast.Name)
            and stmt.target.id == "_kwargs"
            and isinstance(stmt.value, ast.Dict)
        ):
            dict_value = stmt.value

        if dict_value is not None:
            for k, v in zip(dict_value.keys, dict_value.values, strict=False):
                if not isinstance(k, ast.Constant) or not isinstance(k.value, str):
                    continue
                if k.value == "method" and isinstance(v, ast.Constant) and isinstance(v.value, str):
                    method = v.value
                elif k.value == "url":
                    url = _string_template_from_node(v)

        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Subscript):
            target = stmt.targets[0]
            if not (isinstance(target.value, ast.Name) and target.value.id == "_kwargs"):
                continue
            value_str = _string_template_from_node(stmt.value)

            key_node = target.slice
            if isinstance(key_node, ast.Constant) and isinstance(key_node.value, str):
                if key_node.value == "method":
                    if isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                        method = stmt.value.value
                elif key_node.value == "url":
                    url = value_str

    if method and url:
        return method.lower(), url
    return None


def _normalize_path_template(path: str) -> str:
    """Normalize path templates so param names don't matter."""
    return re.sub(r"\{[^}]+\}", "{}", path)


def _resolve_ref(spec: dict, ref: str) -> dict | None:
    if not ref.startswith("#/"):
        return None
    current: object = spec
    for part in ref[2:].split("/"):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current if isinstance(current, dict) else None


def _normalize_description(desc: str) -> str:
    return re.sub(r"\s+", " ", desc).strip()


def _get_response_descriptions_for_endpoint(
    *, spec: dict, method: str, url: str
) -> dict[int, str]:
    paths = spec.get("paths") or {}
    if not isinstance(paths, dict):
        return {}

    # Try direct match first.
    operation = ((paths.get(url) or {}).get(method))

    # Fallback: match normalized templates (handles generated snake_case params).
    if not isinstance(operation, dict):
        normalized_url = _normalize_path_template(url)
        for candidate_url, candidate_ops in paths.items():
            if not isinstance(candidate_url, str) or not isinstance(candidate_ops, dict):
                continue
            if _normalize_path_template(candidate_url) == normalized_url:
                operation = candidate_ops.get(method)
                break

    if not isinstance(operation, dict):
        return {}

    responses = operation.get("responses")
    if not isinstance(responses, dict):
        return {}

    out: dict[int, str] = {}
    for code_str, resp in responses.items():
        if not isinstance(code_str, str) or not code_str.isdigit():
            continue
        code = int(code_str)
        if isinstance(resp, dict) and "$ref" in resp and isinstance(resp["$ref"], str):
            resolved = _resolve_ref(spec, resp["$ref"])
            resp = resolved if resolved is not None else resp
        if not isinstance(resp, dict):
            continue
        desc = resp.get("description")
        if isinstance(desc, str) and desc.strip():
            out[code] = _normalize_description(desc)
    return out


def _ensure_typing_import(tree: ast.Module, name: str) -> None:
    """Ensure `from typing import <name>` exists (prefer augmenting existing typing imports)."""

    for stmt in tree.body:
        if isinstance(stmt, ast.ImportFrom) and stmt.module == "typing" and stmt.level == 0:
            if any(alias.name == name for alias in stmt.names):
                return
            stmt.names.append(ast.alias(name=name, asname=None))
            return

    # Insert a new import after any __future__ import / module docstring and other imports.
    insert_at = 0
    if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str):
        insert_at = 1
    while insert_at < len(tree.body) and isinstance(tree.body[insert_at], ast.ImportFrom) and tree.body[insert_at].module == "__future__":
        insert_at += 1
    while insert_at < len(tree.body) and isinstance(tree.body[insert_at], (ast.Import, ast.ImportFrom)):
        insert_at += 1

    tree.body.insert(insert_at, ast.ImportFrom(module="typing", names=[ast.alias(name=name, asname=None)], level=0))


def _rewrite_docstring(docstring: str, return_type_str: str, raise_lines: list[str]) -> str:
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

    # Replace/insert Raises section to list typed exceptions
    raises_i = find_section("Raises")
    returns_i = find_section("Returns")
    indent = "    "

    new_raises_block = ["", "Raises:"]
    new_raises_block.extend([f"{indent}{line}" for line in raise_lines])
    new_raises_block.append(f"{indent}httpx.TimeoutException: If the request takes longer than Client.timeout.")

    if raises_i is None:
        insert_at = returns_i if returns_i is not None else len(lines)
        lines[insert_at:insert_at] = new_raises_block
    else:
        content_start = raises_i + 1
        content_end = content_start
        while content_end < len(lines) and not is_section_header(lines[content_end]):
            content_end += 1
        # replace from just before Raises: (keeping any single preceding blank line stable)
        # We will replace the section header + its content.
        section_start = raises_i
        # remove a blank line right before Raises: if present, we insert our own
        if section_start > 0 and lines[section_start - 1].strip() == "":
            section_start -= 1
        lines[section_start:content_end] = new_raises_block

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

def modify_api_file(file_path: Path, *, spec: dict) -> None:
    with open(file_path, "r") as f:
        code = f.read()
    
    tree = ast.parse(code)
    modified = False
    
    module_stem = Path(file_path).stem
    endpoint_name = _to_camel_case(module_stem)
    status_type_map = _extract_status_type_map(tree)
    error_codes = sorted([c for c in status_type_map.keys() if not (200 <= c < 300)])

    response_desc: dict[int, str] = {}
    method_url = _extract_method_and_url(tree)
    if method_url and spec:
        method, url = method_url
        response_desc = _get_response_descriptions_for_endpoint(spec=spec, method=method, url=url)

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

        # Ensure cast is available if we need to cast parsed error models.
        needs_cast = any(status_type_map.get(c) not in {None, "Any"} for c in error_codes)
        if needs_cast:
            _ensure_typing_import(tree, "cast")
            modified = True

        func_call = f"{detailed_func_name}(\n"
        for arg in node.args.args:
            if arg.arg != "self":  # module functions have no self, but be safe
                func_call += f"    {arg.arg}={arg.arg},\n"
        for arg in node.args.kwonlyargs:
            func_call += f"    {arg.arg}={arg.arg},\n"
        func_call += ")"
        if isinstance(node, ast.AsyncFunctionDef):
            func_call = f"await {func_call}"

        raise_blocks = ""
        raise_lines: list[str] = []
        for code in error_codes:
            parsed_type = status_type_map.get(code, "Any")
            exc_name = f"{endpoint_name}{_status_suffix(code)}"
            desc = response_desc.get(code)
            if desc:
                raise_lines.append(f"errors.{exc_name}: If the response status code is {code}. {desc}")
            else:
                raise_lines.append(f"errors.{exc_name}: If the response status code is {code}.")

            if parsed_type and parsed_type != "Any":
                parsed_expr = f"cast({parsed_type}, response.parsed)"
            else:
                parsed_expr = "response.parsed"

            # NOTE: this block is nested under `if response.status_code < 200 or response.status_code >= 300:`
            # so it must be indented by 8+ spaces inside the temp() function.
            raise_blocks += (
                f"        if response.status_code == {code}:\n"
                f"            raise errors.{exc_name}(status_code=response.status_code, content=response.content, parsed={parsed_expr})\n"
            )

        raise_lines.append("errors.UnexpectedStatus: If the response status code is not documented.")

        new_body_code = f"""
def temp():
    response = {func_call}
    if response.status_code < 200 or response.status_code >= 300:
{raise_blocks}        raise errors.UnexpectedStatus(response.status_code, response.content)
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
            updated_docstring = _rewrite_docstring(docstring, return_type_str, raise_lines)
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

    spec_path = out_dir / "bundled_spec.yaml"
    spec: dict = {}
    if spec_path.exists():
        spec = yaml.safe_load(spec_path.read_text()) or {}
    
    if not api_dir.exists():
        print(f"API directory not found at {api_dir}")
        return

    for root, dirs, files in os.walk(api_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                modify_api_file(Path(root) / file, spec=spec)

if __name__ == "__main__":
    # For testing
    pass
