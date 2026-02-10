import ast
import os
import re
from pathlib import Path
from collections.abc import Mapping
from typing import Any, cast

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

    def infer_return_type_from_if(if_node: ast.If) -> str | None:
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
                if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
                    if stmt.targets[0].id != returned_name:
                        continue
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

    for stmt in parse_func.body:
        if not isinstance(stmt, ast.If):
            continue

        # Match: if response.status_code == <int>:
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
        inferred = infer_return_type_from_if(stmt)
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

        # Pattern 2: _kwargs['method'] = 'post' / _kwargs['url'] = '/...'
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
    """Normalize path templates so param names don't matter.

    Example:
        "/tenants/{tenantId}/users/{username}" -> "/tenants/{}/users/{}"
        "/tenants/{tenant_id}/users/{username}" -> "/tenants/{}/users/{}"
    """
    return re.sub(r"\{[^}]+\}", "{}", path)


def _resolve_ref(spec: dict[str, Any], ref: str) -> dict[str, Any] | None:
    # Only support local refs like "#/components/responses/Foo"
    if not ref.startswith("#/"):
        return None
    current: Any = spec
    for part in ref[2:].split("/"):
        if not isinstance(current, dict):
            return None
        current_dict = cast(dict[str, Any], current)
        if part not in current_dict:
            return None
        current = current_dict[part]
    return cast(dict[str, Any], current) if isinstance(current, dict) else None


def _normalize_description(desc: str) -> str:
    # Collapse whitespace/newlines while keeping content.
    return re.sub(r"\s+", " ", desc).strip()


def _get_response_descriptions_for_endpoint(
    *, spec: dict[str, Any], method: str, url: str
) -> dict[int, str]:
    """Return mapping HTTP status code -> description for a given operation."""

    paths_obj = spec.get("paths")
    if not isinstance(paths_obj, dict):
        return {}
    paths = cast(dict[str, Any], paths_obj)

    # Try direct match first.
    operation: Any = None
    op_obj = paths.get(url)
    if isinstance(op_obj, dict):
        op_dict = cast(dict[str, Any], op_obj)
        operation = op_dict.get(method)

    # Fallback: match normalized templates (handles generated snake_case params).
    if not isinstance(operation, dict):
        normalized_url = _normalize_path_template(url)
        for candidate_url, candidate_ops in paths.items():
            if not isinstance(candidate_ops, dict):
                continue
            if _normalize_path_template(candidate_url) == normalized_url:
                ops_dict = cast(dict[str, Any], candidate_ops)
                operation = ops_dict.get(method)
                break

    if not isinstance(operation, dict):
        return {}

    operation_dict = cast(dict[str, Any], operation)

    responses_obj = operation_dict.get("responses")
    if not isinstance(responses_obj, dict):
        return {}
    responses = cast(dict[str, Any], responses_obj)

    out: dict[int, str] = {}
    for code_str, resp in responses.items():
        if not code_str.isdigit():
            continue
        code = int(code_str)
        resp_obj: Any = resp
        if isinstance(resp_obj, dict):
            resp_obj = cast(dict[str, Any], resp_obj)
            resp_dict = resp_obj
            ref_val = resp_dict.get("$ref")
            if isinstance(ref_val, str):
                resolved = _resolve_ref(spec, ref_val)
                if resolved is not None:
                    resp_obj = resolved

        if not isinstance(resp_obj, dict):
            continue
        resp_dict2 = cast(dict[str, Any], resp_obj)
        desc = resp_dict2.get("description")
        if isinstance(desc, str) and desc.strip():
            out[code] = _normalize_description(desc)
    return out


def _generate_errors_py(exceptions: list[tuple[str, int, str, str | None]]) -> str:
    # Sort for deterministic output
    exceptions_sorted = sorted(exceptions, key=lambda x: (x[0], x[1], x[2], x[3] or ""))

    lines: list[str] = []
    lines.append('"""Contains shared errors types that can be raised from API functions"""')
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Any")
    lines.append("")
    lines.append("")
    lines.append("class ApiError(Exception):")
    lines.append('    """Base class for API errors raised by convenience wrappers."""')
    lines.append("")
    lines.append("    def __init__(self, *, status_code: int, content: bytes, parsed: Any | None = None):")
    lines.append("        self.status_code = status_code")
    lines.append("        self.content = content")
    lines.append("        self.parsed = parsed")
    lines.append("")
    lines.append("        super().__init__(self._build_message())")
    lines.append("")
    lines.append("    def _build_message(self) -> str:")
    lines.append("        parsed_name = type(self.parsed).__name__ if self.parsed is not None else 'None'")
    lines.append("        try:")
    lines.append("            content_text = self.content.decode(errors='ignore')")
    lines.append("        except Exception:")
    lines.append("            content_text = '<binary>'")
    lines.append("        return f'HTTP {self.status_code} ({parsed_name})\\n\\nResponse content:\\n{content_text}'")
    lines.append("")
    lines.append("")
    lines.append("class UnexpectedStatus(ApiError):")
    lines.append('    """Raised when the server returns a status code that is not handled/parsed by the SDK."""')
    lines.append("")
    lines.append("    def __init__(self, status_code: int, content: bytes):")
    lines.append("        super().__init__(status_code=status_code, content=content, parsed=None)")
    lines.append("")
    lines.append("")

    exported: list[str] = ["ApiError", "UnexpectedStatus"]

    for exc_name, code, parsed_type, description in exceptions_sorted:
        exported.append(exc_name)
        lines.append(f"class {exc_name}(ApiError):")
        if description:
            lines.append(f"    \"\"\"Raised when the server returns HTTP {code}. {description}\"\"\"")
        else:
            lines.append(f"    \"\"\"Raised when the server returns HTTP {code}.\"\"\"")
        lines.append(f"    parsed: {parsed_type}")
        lines.append("")
        lines.append(f"    def __init__(self, *, status_code: int, content: bytes, parsed: {parsed_type}):")
        lines.append("        super().__init__(status_code=status_code, content=content, parsed=parsed)")
        lines.append("")
        lines.append("")

    lines.append(f"__all__ = {sorted(set(exported))!r}")
    lines.append("")

    return "\n".join(lines)


def run(context: Mapping[str, str]) -> None:
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    api_dir = package_dir / "api"

    spec_path = out_dir / "bundled_spec.yaml"
    spec: dict[str, Any] = {}
    if spec_path.exists():
        loaded = yaml.safe_load(spec_path.read_text())
        if isinstance(loaded, dict):
            spec = cast(dict[str, Any], loaded)

    if not api_dir.exists():
        print(f"API directory not found at {api_dir}")
        return

    exceptions: list[tuple[str, int, str, str | None]] = []

    for root, _dirs, files in os.walk(api_dir):
        for file in files:
            if not file.endswith(".py") or file == "__init__.py":
                continue

            file_path = Path(root) / file
            module_stem = file_path.stem
            endpoint_name = _to_camel_case(module_stem)

            code = file_path.read_text()
            try:
                tree = ast.parse(code)
            except SyntaxError:
                continue

            method_url = _extract_method_and_url(tree)
            response_desc: dict[int, str] = {}
            if method_url and spec:
                method, url = method_url
                response_desc = _get_response_descriptions_for_endpoint(spec=spec, method=method, url=url)

            status_map = _extract_status_type_map(tree)
            for status_code, parsed_type in status_map.items():
                # Only generate for non-2xx codes
                if 200 <= status_code < 300:
                    continue
                exc_name = f"{endpoint_name}{_status_suffix(status_code)}"
                exceptions.append((exc_name, status_code, parsed_type, response_desc.get(status_code)))

    errors_py = package_dir / "errors.py"
    errors_py.write_text(_generate_errors_py(exceptions))
    print(f"Generated typed errors at {errors_py}")
