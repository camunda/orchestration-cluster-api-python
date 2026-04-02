import ast
import json
import os
from pathlib import Path
import re
from typing import Any, cast

# Methods that must bypass backpressure gating (drain work / complete execution).
_BP_EXEMPT_METHODS: frozenset[str] = frozenset(
    {"complete_job", "fail_job", "throw_job_error", "complete_user_task"}
)


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


ImportNode = ast.Import | ast.ImportFrom


def _build_semantic_type_map(package_path: Path) -> dict[str, str]:
    """Map snake_case param names to PascalCase semantic type names from semantic_types.py."""
    semantic_types_file = package_path / "semantic_types.py"
    if not semantic_types_file.exists():
        return {}
    with open(semantic_types_file, "r") as f:
        tree = ast.parse(f.read())
    mapping: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(call.func, ast.Name) and call.func.id == "NewType":
                    type_name = target.id
                    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", type_name)
                    snake = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
                    mapping[snake] = type_name
    return mapping


def _lift_semantic_annotations(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    semantic_type_map: dict[str, str],
    semantic_types_used: set[str],
) -> None:
    """Replace str annotations on path parameters with semantic types in-place."""
    for arg in func.args.posonlyargs + func.args.args:
        if (
            arg.annotation
            and isinstance(arg.annotation, ast.Name)
            and arg.annotation.id == "str"
            and arg.arg in semantic_type_map
        ):
            semantic_type = semantic_type_map[arg.arg]
            arg.annotation = ast.Name(id=semantic_type, ctx=ast.Load())
            semantic_types_used.add(semantic_type)


def _status_class_name(code: int) -> str:
    """Return the per-status exception class name for a given HTTP status code."""
    mapping = {
        400: "BadRequestError",
        401: "UnauthorizedError",
        402: "PaymentRequiredError",
        403: "ForbiddenError",
        404: "NotFoundError",
        405: "MethodNotAllowedError",
        408: "RequestTimeoutError",
        409: "ConflictError",
        410: "GoneError",
        412: "PreconditionFailedError",
        413: "PayloadTooLargeError",
        415: "UnsupportedMediaTypeError",
        422: "UnprocessableEntityError",
        429: "TooManyRequestsError",
        500: "InternalServerErrorError",
        501: "NotImplementedError_",
        502: "BadGatewayError",
        503: "ServiceUnavailableError",
        504: "GatewayTimeoutError",
    }
    return mapping.get(code, f"Http{code}Error")


def _extract_documented_status_codes(tree: ast.Module) -> list[int]:
    """Extract HTTP status codes from the ``_parse_response`` function in an endpoint module.

    Returns a sorted list of integer status codes that appear as ``response.status_code == <int>``
    comparisons in the function body.
    """
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "_parse_response":
            codes: list[int] = []
            for stmt in ast.walk(node):
                if (
                    isinstance(stmt, ast.Compare)
                    and len(stmt.ops) == 1
                    and isinstance(stmt.ops[0], ast.Eq)
                    and len(stmt.comparators) == 1
                    and isinstance(stmt.comparators[0], ast.Constant)
                    and isinstance(stmt.comparators[0].value, int)
                    # Only match comparisons against response.status_code
                    and isinstance(stmt.left, ast.Attribute)
                    and stmt.left.attr == "status_code"
                ):
                    codes.append(stmt.comparators[0].value)
            return sorted(codes)
    return []


def _synthesize_convenience_func(
    detailed_func: ast.FunctionDef | ast.AsyncFunctionDef,
    name: str,
    *,
    is_async: bool,
    operation_id: str,
    error_status_codes: list[int],
) -> ast.FunctionDef | ast.AsyncFunctionDef:
    """Create a synthetic ``sync`` or ``asyncio`` function from a ``*_detailed`` variant.

    The generated function mirrors the detailed variant's signature (plus ``**kwargs: Any``
    for compatibility with the flatten-client calling convention) but returns ``None``.
    Non-2xx responses raise per-status typed errors (matching the pattern emitted by
    ``0200_raise_exceptions.py``) with ``operation_id``, and a fallback ``UnexpectedStatus``
    for any undocumented status codes.
    """
    import copy

    func = copy.deepcopy(detailed_func)
    func.name = name
    # Convenience wrappers intentionally declare a None return type; callers needing
    # the full HTTP response or body should use the corresponding *_detailed function.
    func.returns = ast.Constant(value=None)

    # Build the call to the *_detailed function using only the original parameters.
    # We must do this BEFORE adding **kwargs to the signature, because kwargs must
    # NOT be forwarded to the *_detailed call.
    call_args: list[ast.keyword] = []
    for arg in func.args.args + func.args.posonlyargs:
        call_args.append(ast.keyword(arg=arg.arg, value=ast.Name(id=arg.arg, ctx=ast.Load())))
    for arg in func.args.kwonlyargs:
        call_args.append(ast.keyword(arg=arg.arg, value=ast.Name(id=arg.arg, ctx=ast.Load())))
    # Intentionally skip func.args.kwarg — do not forward **kwargs to *_detailed.

    # Add **kwargs: Any to match the generated convenience-function calling convention.
    # The kwargs are intentionally NOT forwarded to the *_detailed call.
    if func.args.kwarg is None:
        func.args.kwarg = ast.arg(arg="kwargs", annotation=ast.Name(id="Any", ctx=ast.Load()))

    inner_call = ast.Call(
        func=ast.Name(id=detailed_func.name, ctx=ast.Load()),
        args=[],
        keywords=call_args,
    )

    # Store the response so we can inspect the status code.
    response_var = ast.Name(id="response", ctx=ast.Store())
    if is_async:
        assign_stmt = ast.Assign(
            targets=[response_var],
            value=ast.Await(value=inner_call),
            lineno=0,
        )
    else:
        assign_stmt = ast.Assign(
            targets=[response_var],
            value=inner_call,
            lineno=0,
        )

    status_attr = ast.Attribute(
        value=ast.Name(id="response", ctx=ast.Load()),
        attr="status_code",
        ctx=ast.Load(),
    )
    content_attr = ast.Attribute(
        value=ast.Name(id="response", ctx=ast.Load()),
        attr="content",
        ctx=ast.Load(),
    )

    # Build per-status typed error branches for documented non-2xx codes,
    # matching the pattern from 0200_raise_exceptions.py.
    non_2xx_codes = [c for c in error_status_codes if c < 200 or c >= 300]
    per_status_branches: list[ast.If] = []
    for code in non_2xx_codes:
        cls_name = _status_class_name(code)
        branch = ast.If(
            test=ast.Compare(
                left=status_attr,
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=code)],
            ),
            body=[
                ast.Raise(
                    exc=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="errors", ctx=ast.Load()),
                            attr=cls_name,
                            ctx=ast.Load(),
                        ),
                        args=[],
                        keywords=[
                            ast.keyword(arg="status_code", value=status_attr),
                            ast.keyword(arg="content", value=content_attr),
                            ast.keyword(
                                arg="operation_id",
                                value=ast.Constant(value=operation_id),
                            ),
                        ],
                    ),
                    cause=None,
                )
            ],
            orelse=[],
        )
        per_status_branches.append(branch)

    # Fallback: raise UnexpectedStatus for any other non-2xx code.
    fallback_raise = ast.Raise(
        exc=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="errors", ctx=ast.Load()),
                attr="UnexpectedStatus",
                ctx=ast.Load(),
            ),
            args=[status_attr, content_attr],
            keywords=[
                ast.keyword(
                    arg="operation_id",
                    value=ast.Constant(value=operation_id),
                ),
            ],
        ),
        cause=None,
    )

    # Assemble the if-body: per-status branches + fallback raise
    if_body: list[ast.stmt] = []
    for branch in per_status_branches:
        if_body.append(branch)
    if_body.append(fallback_raise)

    error_check = ast.If(
        test=ast.BoolOp(
            op=ast.Or(),
            values=[
                ast.Compare(
                    left=status_attr,
                    ops=[ast.Lt()],
                    comparators=[ast.Constant(value=200)],
                ),
                ast.Compare(
                    left=status_attr,
                    ops=[ast.GtE()],
                    comparators=[ast.Constant(value=300)],
                ),
            ],
        ),
        body=if_body,
        orelse=[],
    )

    # Build the Raises: docstring lines for documented error codes.
    raises_lines: list[str] = []
    for code in non_2xx_codes:
        cls_name = _status_class_name(code)
        raises_lines.append(
            f"errors.{cls_name}: If the response status code is {code}."
        )
    raises_lines.append(
        "errors.UnexpectedStatus: If the response status code is not documented."
    )
    raises_lines.append(
        "httpx.TimeoutException: If the request takes longer than Client.timeout."
    )

    # Extract summary from the original docstring (first paragraph).
    old_docstring = ast.get_docstring(detailed_func) or ""
    summary = old_docstring.split("\n\n")[0].strip() if old_docstring else name

    raises_block = "\n".join(f"        {r}" for r in raises_lines)
    new_docstring = (
        f"{summary}\n\n"
        f"    Raises:\n"
        f"{raises_block}\n"
        f"    Returns:\n"
        f"        None"
    )

    # Build function body: docstring + call + error check + return None
    body: list[ast.stmt] = [
        ast.Expr(value=ast.Constant(value=new_docstring)),
        assign_stmt,
        error_check,
        ast.Return(value=ast.Constant(value=None)),
    ]

    func.body = body

    if is_async:
        return func  # already AsyncFunctionDef
    else:
        # Convert to regular FunctionDef if needed (deep copy preserves original type)
        return func


def get_imports_and_signature(
    file_path: Path,
    package_root: Path,
) -> tuple[list[ImportNode], ast.FunctionDef | None, ast.AsyncFunctionDef | None]:
    with open(file_path, "r") as f:
        code = f.read()

    tree = ast.parse(code)

    imports: list[ImportNode] = []
    sync_func: ast.FunctionDef | None = None
    async_func: ast.AsyncFunctionDef | None = None

    sync_detailed_func: ast.FunctionDef | None = None
    async_detailed_func: ast.AsyncFunctionDef | None = None

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == "sync":
            sync_func = node
        elif isinstance(node, ast.AsyncFunctionDef) and node.name == "asyncio":
            async_func = node
        elif isinstance(node, ast.FunctionDef) and node.name == "sync_detailed":
            sync_detailed_func = node
        elif isinstance(node, ast.AsyncFunctionDef) and node.name == "asyncio_detailed":
            async_detailed_func = node

    # For endpoints that only have *_detailed variants (e.g. body-less 204 responses),
    # synthesize sync/asyncio functions that delegate to the detailed variant and
    # return None.  This ensures the flatten-client hook picks them up.
    synthesized_sync = False
    synthesized_async = False
    if sync_func is None and sync_detailed_func is not None:
        operation_id = file_path.stem  # e.g. "get_status"
        error_status_codes = _extract_documented_status_codes(tree)
        sync_func = cast(ast.FunctionDef, _synthesize_convenience_func(
            sync_detailed_func, "sync", is_async=False,
            operation_id=operation_id, error_status_codes=error_status_codes,
        ))
        synthesized_sync = True
    if async_func is None and async_detailed_func is not None:
        operation_id = file_path.stem
        error_status_codes = _extract_documented_status_codes(tree)
        async_func = cast(ast.AsyncFunctionDef, _synthesize_convenience_func(
            async_detailed_func, "asyncio", is_async=True,
            operation_id=operation_id, error_status_codes=error_status_codes,
        ))
        synthesized_async = True

    # Write synthesized convenience functions back to the endpoint module so they
    # are importable at runtime (the flatten-client does ``from ... import sync``).
    if synthesized_sync or synthesized_async:
        append_lines: list[str] = []
        if synthesized_sync and sync_func is not None:
            append_lines.append(ast.unparse(sync_func))
        if synthesized_async and async_func is not None:
            append_lines.append(ast.unparse(async_func))
        if append_lines:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write("\n\n" + "\n\n".join(append_lines) + "\n")

    rel_path = file_path.relative_to(package_root)
    # depth = number of parts in parent directory
    # e.g. api/group/module.py -> api/group -> depth=2

    adjusted_imports: list[ImportNode] = []
    for node in imports:
        if isinstance(node, ast.ImportFrom) and node.level > 0:
            steps_up = node.level - 1
            current_parts = list(rel_path.parent.parts)

            if steps_up > len(current_parts):
                continue

            target_parts = current_parts[: len(current_parts) - steps_up]
            base_module = ".".join(target_parts)

            if node.module:
                if base_module:
                    final_module = f"{base_module}.{node.module}"
                else:
                    final_module = node.module
            else:
                final_module = base_module

            if final_module == "client" or (
                final_module and final_module.startswith("client.")
            ):
                continue

            new_node = ast.ImportFrom(
                module=final_module,
                names=node.names,
                level=1,
            )
            adjusted_imports.append(new_node)
        else:
            adjusted_imports.append(node)

    return adjusted_imports, sync_func, async_func


# Template for body tenant injection code.  Handles both attrs model objects
# (tenant_id attribute, snake_case) and dict-like bodies (tenantId key, camelCase).
_BODY_TENANT_INJECTION = """
        _body = _kwargs.get("body")
        if _body is not None and self.configuration.CAMUNDA_TENANT_ID is not None:
            if hasattr(_body, "tenant_id"):
                if _body.tenant_id is None or _body.tenant_id is UNSET:
                    _body.tenant_id = self.configuration.CAMUNDA_TENANT_ID
            elif isinstance(_body, dict) and ("tenantId" not in _body or _body["tenantId"] is None):
                _body["tenantId"] = self.configuration.CAMUNDA_TENANT_ID"""


def _compute_body_tenant_ops(spec_path: Path | None) -> set[str]:
    """Return snake_case method names for operations with optional tenantId in request body.

    These are 'tenant-as-context' operations where the SDK should inject the
    configured default tenant ID into the body when the caller does not supply one.
    Path-param tenant IDs (tenant-as-subject) are NOT included — those identify
    which tenant to operate on and must always be provided explicitly.
    """
    if spec_path is None or not spec_path.exists():
        return set()

    with open(spec_path, "r", encoding="utf-8") as f:
        if spec_path.suffix == ".json":
            spec: dict[str, Any] = json.load(f)
        else:
            import yaml
            spec = yaml.safe_load(f)

    def resolve_ref(ref: str) -> dict[str, Any]:
        parts = ref.lstrip("#/").split("/")
        node: Any = spec
        for p in parts:
            node = node[p]
        return cast(dict[str, Any], node)

    def has_optional_tenant_id(schema: dict[str, Any], depth: int = 0) -> bool:
        if depth > 5:
            return False
        if "$ref" in schema:
            return has_optional_tenant_id(resolve_ref(schema["$ref"]), depth + 1)
        props: dict[str, Any] = schema.get("properties", {})
        if "tenantId" in props and "tenantId" not in schema.get("required", []):
            return True
        variants: list[dict[str, Any]] = schema.get("oneOf", []) + schema.get("anyOf", [])
        for variant in variants:
            if has_optional_tenant_id(variant, depth + 1):
                return True
        return False

    ops: set[str] = set()
    paths: dict[str, Any] = spec.get("paths", {})
    for _path, methods in paths.items():
        for method, op in methods.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            op_id: str = op.get("operationId", "")
            body: dict[str, Any] = op.get("requestBody", {}).get("content", {})
            for _ct, ct_data in body.items():
                schema: dict[str, Any] = ct_data.get("schema", {})
                if has_optional_tenant_id(schema):
                    # Convert camelCase operationId to snake_case method name
                    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", op_id)
                    snake = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
                    ops.add(snake)
                    break

    if ops:
        print(f"[flatten-client] body-tenant-injection ops ({len(ops)}): {sorted(ops)}")
    return ops


def generate_flat_client(package_path: Path, spec_path: Path | None = None) -> None:
    api_dir = package_path / "api"
    if not api_dir.exists():
        print(f"API directory not found at {api_dir}")
        return

    body_tenant_ops = _compute_body_tenant_ops(spec_path)

    sync_methods: list[str] = []
    async_methods: list[str] = []
    all_imports: set[str] = set()
    needed_type_names: set[str] = set()
    semantic_type_map = _build_semantic_type_map(package_path)
    semantic_types_used: set[str] = set()

    def _extract_annotation_names(node: ast.expr | None) -> set[str]:
        """Extract all Name identifiers from a type annotation AST node."""
        if node is None:
            return set()
        return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}

    for root, _dirs, files in os.walk(api_dir):
        _dirs.sort()
        for file in sorted(files):
            if file == "__init__.py" or not file.endswith(".py"):
                continue

            file_path = Path(root) / file
            imports, sync_func, async_func = get_imports_and_signature(
                file_path, package_path
            )

            for imp in imports:
                if isinstance(imp, ast.ImportFrom):
                    module = imp.module
                    names = ", ".join(
                        n.name + (f" as {n.asname}" if n.asname else "")
                        for n in imp.names
                    )
                    level = "." * imp.level
                    import_stmt = (
                        f"from {level}{module} import {names}"
                        if module
                        else f"from {level} import {names}"
                    )
                    all_imports.add(import_stmt)
                else:
                    names = ", ".join(
                        n.name + (f" as {n.asname}" if n.asname else "")
                        for n in imp.names
                    )
                    import_stmt = f"import {names}"
                    all_imports.add(import_stmt)

            rel_path = Path(root).relative_to(package_path)
            module_name = file[:-3]
            import_path = f".{'.'.join(rel_path.parts)}.{module_name}"
            method_name = module_name

            # Lift path parameter annotations from str to semantic types
            for func in [f for f in [sync_func, async_func] if f is not None]:
                _lift_semantic_annotations(func, semantic_type_map, semantic_types_used)

            if sync_func:
                args = sync_func.args
                # Track type names used in annotations for TYPE_CHECKING imports
                needed_type_names.update(_extract_annotation_names(sync_func.returns))
                for _arg in args.args + args.kwonlyargs + args.posonlyargs:
                    needed_type_names.update(_extract_annotation_names(_arg.annotation))
                new_args: list[ast.arg] = []
                for arg in args.posonlyargs:
                    if arg.arg != "client":
                        new_args.append(arg)
                for arg in args.args:
                    if arg.arg != "client":
                        new_args.append(arg)

                new_kwonlyargs: list[ast.arg] = []
                new_kw_defaults: list[ast.expr | None] = []
                for arg, default in zip(args.kwonlyargs, args.kw_defaults):
                    if arg.arg != "client":
                        new_kwonlyargs.append(arg)
                        new_kw_defaults.append(default)

                arg_strs: list[str] = ["self"]
                for arg in new_args:
                    arg_name = "data" if arg.arg == "body" else arg.arg
                    ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                    arg_strs.append(f"{arg_name}{ann}")

                if args.vararg:
                    ann = (
                        f": {ast.unparse(args.vararg.annotation)}"
                        if args.vararg.annotation
                        else ""
                    )
                    arg_strs.append(f"*{args.vararg.arg}{ann}")
                elif new_kwonlyargs:
                    arg_strs.append("*")

                for arg, default in zip(new_kwonlyargs, new_kw_defaults):
                    arg_name = "data" if arg.arg == "body" else arg.arg
                    ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                    default_str = f" = {ast.unparse(default)}" if default else ""
                    arg_strs.append(f"{arg_name}{ann}{default_str}")

                if args.kwarg:
                    ann = (
                        f": {ast.unparse(args.kwarg.annotation)}"
                        if args.kwarg.annotation
                        else ": Any"
                    )
                    arg_strs.append(f"**{args.kwarg.arg}{ann}")
                else:
                    arg_strs.append("**kwargs: Any")

                sig_str = ", ".join(arg_strs)
                return_ann = (
                    f" -> {ast.unparse(sync_func.returns)}" if sync_func.returns else ""
                )
                docstring = ast.get_docstring(sync_func)
                docstring_str = f'        """{docstring}"""\n' if docstring else ""

                # Body-tenant injection: for operations where tenantId is an optional
                # field in the request body (tenant-as-context), inject the configured
                # default tenant ID into the body model when the caller omits it.
                tenant_id_injection = _BODY_TENANT_INJECTION if method_name in body_tenant_ops else ""

                if method_name in _BP_EXEMPT_METHODS:
                    sync_methods.append(f"""
    def {method_name}({sig_str}){return_ann}:
{docstring_str}        from {import_path} import sync as {method_name}_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data"){tenant_id_injection}
        return {method_name}_sync(**_kwargs)
""")
                else:
                    sync_methods.append(f"""
    def {method_name}({sig_str}){return_ann}:
{docstring_str}        from {import_path} import sync as {method_name}_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data"){tenant_id_injection}
        self._bp.acquire()
        try:
            _result = {method_name}_sync(**_kwargs)
            self._bp.record_healthy_hint()
            return _result
        except Exception as _exc:
            if is_backpressure_error(_exc):
                self._bp.record_backpressure()
            raise
        finally:
            self._bp.release()
""")

            if async_func:
                args = async_func.args
                # Track type names used in annotations for TYPE_CHECKING imports
                needed_type_names.update(_extract_annotation_names(async_func.returns))
                for _arg in args.args + args.kwonlyargs + args.posonlyargs:
                    needed_type_names.update(_extract_annotation_names(_arg.annotation))
                new_args: list[ast.arg] = []
                for arg in args.posonlyargs:
                    if arg.arg != "client":
                        new_args.append(arg)
                for arg in args.args:
                    if arg.arg != "client":
                        new_args.append(arg)

                new_kwonlyargs: list[ast.arg] = []
                new_kw_defaults: list[ast.expr | None] = []
                for arg, default in zip(args.kwonlyargs, args.kw_defaults):
                    if arg.arg != "client":
                        new_kwonlyargs.append(arg)
                        new_kw_defaults.append(default)

                arg_strs: list[str] = ["self"]
                for arg in new_args:
                    arg_name = "data" if arg.arg == "body" else arg.arg
                    ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                    arg_strs.append(f"{arg_name}{ann}")

                if args.vararg:
                    ann = (
                        f": {ast.unparse(args.vararg.annotation)}"
                        if args.vararg.annotation
                        else ""
                    )
                    arg_strs.append(f"*{args.vararg.arg}{ann}")
                elif new_kwonlyargs:
                    arg_strs.append("*")

                for arg, default in zip(new_kwonlyargs, new_kw_defaults):
                    arg_name = "data" if arg.arg == "body" else arg.arg
                    ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                    default_str = f" = {ast.unparse(default)}" if default else ""
                    arg_strs.append(f"{arg_name}{ann}{default_str}")

                if args.kwarg:
                    ann = (
                        f": {ast.unparse(args.kwarg.annotation)}"
                        if args.kwarg.annotation
                        else ": Any"
                    )
                    arg_strs.append(f"**{args.kwarg.arg}{ann}")
                else:
                    arg_strs.append("**kwargs: Any")

                sig_str = ", ".join(arg_strs)
                return_ann = (
                    f" -> {ast.unparse(async_func.returns)}"
                    if async_func.returns
                    else ""
                )
                docstring = ast.get_docstring(async_func)
                docstring_str = f'        """{docstring}"""\n' if docstring else ""

                # Body-tenant injection: same logic as sync methods
                tenant_id_injection = _BODY_TENANT_INJECTION if method_name in body_tenant_ops else ""

                if method_name in _BP_EXEMPT_METHODS:
                    async_methods.append(f"""
    async def {method_name}({sig_str}){return_ann}:
{docstring_str}        from {import_path} import asyncio as {method_name}_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data"){tenant_id_injection}
        return await {method_name}_asyncio(**_kwargs)
""")
                else:
                    async_methods.append(f"""
    async def {method_name}({sig_str}){return_ann}:
{docstring_str}        from {import_path} import asyncio as {method_name}_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data"){tenant_id_injection}
        await self._bp.acquire()
        try:
            _result = await {method_name}_asyncio(**_kwargs)
            await self._bp.record_healthy_hint()
            return _result
        except Exception as _exc:
            if is_backpressure_error(_exc):
                await self._bp.record_backpressure()
            raise
        finally:
            await self._bp.release()
""")

    # Add semantic type import for TYPE_CHECKING block
    if semantic_types_used:
        all_imports.add(
            f"from .semantic_types import {', '.join(sorted(semantic_types_used))}"
        )

    client_file = package_path / "client.py"
    if not client_file.exists():
        print(f"Client file not found at {client_file}. Skipping flattening.")
        return

    with open(client_file, "r") as f:
        content = f.read()

    # Split content
    lines = content.splitlines()
    import_lines: list[str] = []
    class_lines: list[str] = []
    in_classes = False

    for line in lines:
        if line.startswith("class ") or line.startswith("@define"):
            in_classes = True

        if in_classes:
            class_lines.append(line)
        else:
            import_lines.append(line)

    # Remove existing CamundaClient
    class_content = "\n".join(class_lines)
    if "class CamundaClient" in class_content:
        class_content = class_content.split("class CamundaClient")[0]

    # Prepare imports
    imports_content = "\n".join(import_lines)
    if "from __future__ import annotations" not in imports_content:
        imports_content = "from __future__ import annotations\n" + imports_content

    if "from .types import UNSET, Unset" not in imports_content:
        imports_content += "\nfrom .types import UNSET, Unset"

    if "from typing import TYPE_CHECKING" not in imports_content:
        imports_content += "\nfrom typing import TYPE_CHECKING"

    imports_content += "\nimport asyncio"
    imports_content += "\nfrom .runtime.job_worker import JobWorker, WorkerConfig, ConnectedJobHandler, IsolatedJobHandler, JobHandler, resolve_worker_config"
    imports_content += "\nfrom typing import Literal, overload"
    imports_content += "\nfrom .runtime.configuration_resolver import CamundaSdkConfigPartial, CamundaSdkConfiguration, ConfigurationResolver, read_environment"
    imports_content += "\nfrom .runtime.auth import AuthProvider, BasicAuthProvider, NullAuthProvider, OAuthClientCredentialsAuthProvider, AsyncOAuthClientCredentialsAuthProvider, inject_auth_event_hooks"
    imports_content += "\nfrom .runtime.tls import build_ssl_context"
    imports_content += "\nfrom .runtime.logging import CamundaLogger, NullLogger, SdkLogger, create_logger"
    imports_content += "\nfrom .runtime.backpressure import BackpressureManager, AsyncBackpressureManager, is_backpressure_error"
    imports_content += "\nfrom pathlib import Path"
    imports_content += "\nfrom .models.deployment_result import DeploymentResult"
    imports_content += "\nfrom .models.deployment_metadata_result_process_definition import DeploymentMetadataResultProcessDefinition"
    imports_content += "\nfrom .models.deployment_metadata_result_decision_definition import DeploymentMetadataResultDecisionDefinition"
    imports_content += "\nfrom .models.deployment_metadata_result_decision_requirements import DeploymentMetadataResultDecisionRequirements"
    imports_content += "\nfrom .models.deployment_metadata_result_form import DeploymentMetadataResultForm"

    # Prepare TYPE_CHECKING block — only include imports that provide type names
    # actually used in method signatures (return types and parameter types).
    # Skip imports already available at the top level of this file.
    top_level_modules = {
        "UNSET",
        "Unset",  # from .types
        "Any",  # from typing
        "Callable",  # from typing
        "cast",  # from typing
        "Response",  # from .types (not needed for annotations)
        "ssl",  # import ssl
    }
    type_checking_block = "\nif TYPE_CHECKING:\n"
    type_checking_has_imports = False
    sorted_imports = sorted(list(all_imports))
    for imp in sorted_imports:
        # Extract imported names from the import statement
        import_match = re.search(r"import\s+(.+)$", imp)
        if not import_match:
            continue
        imported_names = [
            n.strip().split(" as ")[-1].strip()
            for n in import_match.group(1).split(",")
        ]
        # Skip if all imported names are already available at the top level
        if all(name in top_level_modules for name in imported_names):
            continue
        # Filter out individual top_level_modules names from the import
        filtered_names = [n for n in imported_names if n not in top_level_modules]
        if not filtered_names:
            continue
        # Only include if at least one filtered name is needed for annotations
        if any(name in needed_type_names for name in filtered_names):
            # Rebuild import statement with only needed names
            module_match = re.match(r"(from\s+\S+\s+import\s+)", imp)
            if module_match and len(filtered_names) < len(imported_names):
                # Reconstruct import with filtered names only
                rebuilt_imp = module_match.group(1) + ", ".join(filtered_names)
                type_checking_block += f"    {rebuilt_imp}\n"
            else:
                type_checking_block += f"    {imp}\n"
            type_checking_has_imports = True

    if not type_checking_has_imports:
        type_checking_block = ""

    new_sync_methods = "\n".join(sync_methods)
    new_async_methods = "\n".join(async_methods)

    extended_result_code = """
class ExtendedDeploymentResult(DeploymentResult):
    processes: list[DeploymentMetadataResultProcessDefinition]
    decisions: list[DeploymentMetadataResultDecisionDefinition]
    decision_requirements: list[DeploymentMetadataResultDecisionRequirements]
    forms: list[DeploymentMetadataResultForm]
    
    def __init__(self, response: DeploymentResult):
        self.deployment_key = response.deployment_key
        self.tenant_id = response.tenant_id
        self.deployments = response.deployments
        self.additional_properties = response.additional_properties
        
        self.processes = [d.process_definition for d in self.deployments if not isinstance(d.process_definition, Unset) and d.process_definition is not None]
        self.decisions = [d.decision_definition for d in self.deployments if not isinstance(d.decision_definition, Unset) and d.decision_definition is not None]
        self.decision_requirements = [d.decision_requirements for d in self.deployments if not isinstance(d.decision_requirements, Unset) and d.decision_requirements is not None]
        self.forms = [d.form for d in self.deployments if not isinstance(d.form, Unset) and d.form is not None]
"""

    camunda_client_code = f'''
class CamundaClient:
    client: Client | AuthenticatedClient
    configuration: CamundaSdkConfiguration
    auth_provider: AuthProvider

    def __init__(self, configuration: CamundaSdkConfigPartial | None = None, auth_provider: AuthProvider | None = None, logger: CamundaLogger | None = None, **kwargs: Any):
        resolved = ConfigurationResolver(
            environment=read_environment(),
            explicit_configuration=configuration,
        ).resolve()
        self.configuration = resolved.effective
        self._sdk_logger: SdkLogger = create_logger(logger)

        if "base_url" in kwargs:
            raise TypeError(
                "CamundaClient no longer accepts base_url; set CAMUNDA_REST_ADDRESS (or ZEEBE_REST_ADDRESS) via configuration/environment instead."
            )
        if "token" in kwargs:
            raise TypeError(
                "CamundaClient no longer accepts token; use configuration-based auth (CAMUNDA_AUTH_STRATEGY) instead."
            )

        # mTLS: build an ssl.SSLContext from CAMUNDA_MTLS_* config and
        # inject it as verify_ssl (unless the caller supplied one explicitly).
        _ssl_ctx = build_ssl_context(self.configuration)
        if _ssl_ctx is not None and "verify_ssl" not in kwargs:
            kwargs["verify_ssl"] = _ssl_ctx

        if auth_provider is None:
            if self.configuration.CAMUNDA_AUTH_STRATEGY == "NONE":
                auth_provider = NullAuthProvider()
            elif self.configuration.CAMUNDA_AUTH_STRATEGY == "BASIC":
                auth_provider = BasicAuthProvider(
                    username=self.configuration.CAMUNDA_BASIC_AUTH_USERNAME or "",
                    password=self.configuration.CAMUNDA_BASIC_AUTH_PASSWORD or "",
                )
            elif self.configuration.CAMUNDA_AUTH_STRATEGY == "OAUTH":
                httpx_args: dict[str, Any] = kwargs.get("httpx_args") or {{}}
                transport: Any = httpx_args.get("transport")
                # Pass the same TLS verification settings used by the main client
                # to the OAuth token client via transport, so both behave consistently.
                if transport is None:
                    if "verify_ssl" in kwargs:
                        verify_for_oauth = kwargs["verify_ssl"]
                    elif _ssl_ctx is not None:
                        verify_for_oauth = _ssl_ctx
                    else:
                        verify_for_oauth = None

                    if verify_for_oauth is not None:
                        import httpx as _httpx
                        transport = _httpx.HTTPTransport(verify=verify_for_oauth)
                auth_provider = OAuthClientCredentialsAuthProvider(
                    oauth_url=self.configuration.CAMUNDA_OAUTH_URL,
                    client_id=self.configuration.CAMUNDA_CLIENT_ID or "",
                    client_secret=self.configuration.CAMUNDA_CLIENT_SECRET or "",
                    audience=self.configuration.CAMUNDA_TOKEN_AUDIENCE,
                    cache_dir=self.configuration.CAMUNDA_TOKEN_CACHE_DIR,
                    disk_cache_disable=self.configuration.CAMUNDA_TOKEN_DISK_CACHE_DISABLE,
                    transport=transport,
                    logger=self._sdk_logger,
                )
            else:
                auth_provider = NullAuthProvider()

        self.auth_provider = auth_provider

        # Ensure every request gets auth headers via httpx event hooks.
        kwargs["httpx_args"] = inject_auth_event_hooks(
            kwargs.get("httpx_args"),
            auth_provider,
            async_client=False,
            log_level=self.configuration.CAMUNDA_SDK_LOG_LEVEL,
            logger=self._sdk_logger,
        )

        self.client = Client(base_url=self.configuration.CAMUNDA_REST_ADDRESS, **kwargs)
        self._bp = BackpressureManager(
            profile=self.configuration.CAMUNDA_SDK_BACKPRESSURE_PROFILE,
            logger=self._sdk_logger,
        )

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any):
        try:
            return self.client.__exit__(*args, **kwargs)
        finally:
            close = getattr(self.auth_provider, "close", None)
            if callable(close):
                close()

    def close(self) -> None:
        """Close underlying HTTP clients.

        This closes both the API client's httpx client and, when available, the
        auth provider's token client.
        """

        try:
            close = getattr(self.auth_provider, "close", None)
            if callable(close):
                close()
        finally:
            try:
                self.client.get_httpx_client().close()
            except Exception:
                return

    def deploy_resources_from_files(self, files: list[str | Path], tenant_id: str | None = None) -> ExtendedDeploymentResult:
        """Deploy BPMN/DMN/Form resources from local files.

        This is a convenience wrapper around :meth:`create_deployment` that:

        - Reads each path in ``files`` as bytes.
        - Wraps the bytes in :class:`camunda_orchestration_sdk.types.File` using the file's basename
          as ``file_name``.
        - Builds :class:`camunda_orchestration_sdk.models.CreateDeploymentData` and calls
          :meth:`create_deployment`.
        - Returns an :class:`ExtendedDeploymentResult`, which is the deployment response plus
          convenience lists (``processes``, ``decisions``, ``decision_requirements``, ``forms``).

        Args:
            files: File paths (``str`` or ``Path``) to deploy.
            tenant_id: Optional tenant identifier. If not provided, the default tenant is used.

        Returns:
            ExtendedDeploymentResult: The deployment result with extracted resource lists.

        Raises:
            FileNotFoundError: If any file path does not exist.
            PermissionError: If any file path cannot be read.
            IsADirectoryError: If any file path is a directory.
            OSError: For other I/O failures while reading files.
            Exception: Propagates any exception raised by :meth:`create_deployment` (including
                typed API errors in :mod:`camunda_orchestration_sdk.errors` and ``httpx.TimeoutException``).
        """
        from .models.create_deployment_data import CreateDeploymentData
        from .semantic_types import TenantId
        from .types import File, UNSET
        import io
        import os

        resources: list[File] = []
        for file_path in files:
            file_path = str(file_path)
            with open(file_path, "rb") as f:
                content = f.read()
            resources.append(File(payload=io.BytesIO(content), file_name=os.path.basename(file_path)))

        _effective_tenant_id = tenant_id if tenant_id is not None else self.configuration.CAMUNDA_TENANT_ID
        data = CreateDeploymentData(resources=resources, tenant_id=TenantId(_effective_tenant_id) if _effective_tenant_id is not None else UNSET)
        return ExtendedDeploymentResult(self.create_deployment(data=data))

{new_sync_methods}


class CamundaAsyncClient:
    client: Client | AuthenticatedClient
    configuration: CamundaSdkConfiguration
    auth_provider: AuthProvider
    _workers: list[JobWorker]

    def __init__(self, configuration: CamundaSdkConfigPartial | None = None, auth_provider: AuthProvider | None = None, logger: CamundaLogger | None = None, **kwargs: Any):
        resolved = ConfigurationResolver(
            environment=read_environment(),
            explicit_configuration=configuration,
        ).resolve()
        self.configuration = resolved.effective
        self._sdk_logger: SdkLogger = create_logger(logger)

        if "base_url" in kwargs:
            raise TypeError(
                "CamundaAsyncClient no longer accepts base_url; set CAMUNDA_REST_ADDRESS (or ZEEBE_REST_ADDRESS) via configuration/environment instead."
            )
        if "token" in kwargs:
            raise TypeError(
                "CamundaAsyncClient no longer accepts token; use configuration-based auth (CAMUNDA_AUTH_STRATEGY) instead."
            )

        # mTLS: build an ssl.SSLContext from CAMUNDA_MTLS_* config and
        # inject it as verify_ssl (unless the caller supplied one explicitly).
        _ssl_ctx = build_ssl_context(self.configuration)
        if _ssl_ctx is not None and "verify_ssl" not in kwargs:
            kwargs["verify_ssl"] = _ssl_ctx

        if auth_provider is None:
            if self.configuration.CAMUNDA_AUTH_STRATEGY == "NONE":
                auth_provider = NullAuthProvider()
            elif self.configuration.CAMUNDA_AUTH_STRATEGY == "BASIC":
                auth_provider = BasicAuthProvider(
                    username=self.configuration.CAMUNDA_BASIC_AUTH_USERNAME or "",
                    password=self.configuration.CAMUNDA_BASIC_AUTH_PASSWORD or "",
                )
            elif self.configuration.CAMUNDA_AUTH_STRATEGY == "OAUTH":
                httpx_args: dict[str, Any] = kwargs.get("httpx_args") or {{}}
                transport: Any = httpx_args.get("transport")
                # Pass the same TLS verification settings used by the main client
                # to the OAuth token client via transport, so both behave consistently.
                if transport is None:
                    if "verify_ssl" in kwargs:
                        verify_for_oauth = kwargs["verify_ssl"]
                    elif _ssl_ctx is not None:
                        verify_for_oauth = _ssl_ctx
                    else:
                        verify_for_oauth = None

                    if verify_for_oauth is not None:
                        import httpx as _httpx
                        transport = _httpx.AsyncHTTPTransport(verify=verify_for_oauth)
                auth_provider = AsyncOAuthClientCredentialsAuthProvider(
                    oauth_url=self.configuration.CAMUNDA_OAUTH_URL,
                    client_id=self.configuration.CAMUNDA_CLIENT_ID or "",
                    client_secret=self.configuration.CAMUNDA_CLIENT_SECRET or "",
                    audience=self.configuration.CAMUNDA_TOKEN_AUDIENCE,
                    cache_dir=self.configuration.CAMUNDA_TOKEN_CACHE_DIR,
                    disk_cache_disable=self.configuration.CAMUNDA_TOKEN_DISK_CACHE_DISABLE,
                    transport=transport,
                    logger=self._sdk_logger,
                )
            else:
                auth_provider = NullAuthProvider()

        self.auth_provider = auth_provider

        # Ensure every request gets auth headers via httpx event hooks.
        kwargs["httpx_args"] = inject_auth_event_hooks(
            kwargs.get("httpx_args"),
            auth_provider,
            async_client=True,
            log_level=self.configuration.CAMUNDA_SDK_LOG_LEVEL,
            logger=self._sdk_logger,
        )

        self.client = Client(base_url=self.configuration.CAMUNDA_REST_ADDRESS, **kwargs)
        self._workers = []
        self._bp = AsyncBackpressureManager(
            profile=self.configuration.CAMUNDA_SDK_BACKPRESSURE_PROFILE,
            logger=self._sdk_logger,
        )

    async def __aenter__(self) -> "CamundaAsyncClient":
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        try:
            await self.client.__aexit__(*args, **kwargs)
        finally:
            aclose = getattr(self.auth_provider, "aclose", None)
            if callable(aclose):
                try:
                    await aclose()  # type: ignore[reportGeneralTypeIssues]
                except Exception:
                    pass
            else:
                close = getattr(self.auth_provider, "close", None)
                if callable(close):
                    try:
                        close()
                    except Exception:
                        pass

    async def aclose(self) -> None:
        """Close underlying HTTP clients.

        This closes both the API client's async httpx client and, when available,
        the auth provider's token client.
        """

        aclose = getattr(self.auth_provider, "aclose", None)
        if callable(aclose):
            try:
                await aclose()  # type: ignore[reportGeneralTypeIssues]
            except Exception:
                pass
        else:
            close = getattr(self.auth_provider, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass

        try:
            await self.client.get_async_httpx_client().aclose()
        except Exception:
            return

    @overload
    def create_job_worker(self, config: WorkerConfig, callback: ConnectedJobHandler, auto_start: bool = True, *, execution_strategy: Literal["auto", "async", "thread"] = "auto", startup_jitter_max_seconds: float | None = None) -> JobWorker:
        ...

    @overload
    def create_job_worker(self, config: WorkerConfig, callback: IsolatedJobHandler, auto_start: bool = True, *, execution_strategy: Literal["process"], startup_jitter_max_seconds: float | None = None) -> JobWorker:
        ...

    def create_job_worker(self, config: WorkerConfig, callback: JobHandler, auto_start: bool = True, *, execution_strategy: Literal["auto", "async", "thread", "process"] = "auto", startup_jitter_max_seconds: float | None = None) -> JobWorker:
        resolved_config = resolve_worker_config(config, self.configuration)
        effective_jitter = startup_jitter_max_seconds
        if effective_jitter is None:
            effective_jitter = self.configuration.CAMUNDA_WORKER_STARTUP_JITTER_MAX_SECONDS or 0
        worker = JobWorker(self, callback, resolved_config, logger=self._sdk_logger, execution_strategy=execution_strategy, startup_jitter_max_seconds=effective_jitter)
        self._workers.append(worker)
        if auto_start:
            worker.start()
        return worker

    async def run_workers(self):
        stop_event = asyncio.Event()
        try:
            await stop_event.wait()
        except asyncio.CancelledError:
            pass
        finally:
            for worker in self._workers:
                worker.stop()

    async def deploy_resources_from_files(self, files: list[str | Path], tenant_id: str | None = None) -> ExtendedDeploymentResult:
        """Deploy BPMN/DMN/Form resources from local files.

        Async variant of :meth:`CamundaClient.deploy_resources_from_files`.

        This reads each file path in ``files`` as bytes, wraps them into
        :class:`camunda_orchestration_sdk.types.File`, calls :meth:`create_deployment`, and returns
        an :class:`ExtendedDeploymentResult`.

        Note: file reads are currently performed using blocking I/O (``open(...).read()``). If you
        need fully non-blocking file access, load the bytes yourself and call :meth:`create_deployment`.

        Args:
            files: File paths (``str`` or ``Path``) to deploy.
            tenant_id: Optional tenant identifier. If not provided, the default tenant is used.

        Returns:
            ExtendedDeploymentResult: The deployment result with extracted resource lists.

        Raises:
            FileNotFoundError: If any file path does not exist.
            PermissionError: If any file path cannot be read.
            IsADirectoryError: If any file path is a directory.
            OSError: For other I/O failures while reading files.
            Exception: Propagates any exception raised by :meth:`create_deployment` (including
                typed API errors in :mod:`camunda_orchestration_sdk.errors` and ``httpx.TimeoutException``).
        """
        from .models.create_deployment_data import CreateDeploymentData
        from .semantic_types import TenantId
        from .types import File, UNSET
        import io
        import os

        resources: list[File] = []
        for file_path in files:
            file_path = str(file_path)
            with open(file_path, "rb") as f:
                content = f.read()
            resources.append(File(payload=io.BytesIO(content), file_name=os.path.basename(file_path)))

        _effective_tenant_id = tenant_id if tenant_id is not None else self.configuration.CAMUNDA_TENANT_ID
        data = CreateDeploymentData(resources=resources, tenant_id=TenantId(_effective_tenant_id) if _effective_tenant_id is not None else UNSET)
        return ExtendedDeploymentResult(await self.create_deployment(data=data))

{new_async_methods}
'''

    final_content = f"{imports_content}\n{type_checking_block}\n{class_content}\n{extended_result_code}\n{camunda_client_code}"

    with open(client_file, "w") as f:
        f.write(final_content)

    print(f"Successfully added CamundaClient and CamundaAsyncClient to {client_file}")

    init_file = package_path / "__init__.py"
    if init_file.exists():
        with open(init_file, "r") as f:
            init_content = f.read()

        def _ensure_all_tuple_exports(content: str, exports: list[str]) -> str:
            lines = content.splitlines()
            out: list[str] = []
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.startswith("__all__"):
                    out.append(line)
                    i += 1

                    tuple_lines: list[str] = []
                    while i < len(lines) and lines[i].strip() != ")":
                        tuple_lines.append(lines[i])
                        i += 1

                    closing = lines[i] if i < len(lines) else ")"

                    existing: set[str] = set()
                    for tl in tuple_lines:
                        stripped = tl.strip()
                        if stripped.startswith('"') and stripped.endswith(","):
                            existing.add(stripped.strip(",").strip('"'))

                    indent = "    "
                    for tl in tuple_lines:
                        m = re.match(r"^(\s*)\"", tl)
                        if m:
                            indent = m.group(1)
                            break

                    for export in exports:
                        if export not in existing:
                            tuple_lines.append(f'{indent}"{export}",')

                    out.extend(tuple_lines)
                    out.append(closing)
                    i += 1
                    continue

                out.append(line)
                i += 1

            return "\n".join(out) + "\n"

        # Ensure clients are exported
        if (
            "from .client import AuthenticatedClient, Client, CamundaClient, CamundaAsyncClient"
            not in init_content
        ):
            if (
                "from .client import AuthenticatedClient, Client, CamundaClient"
                in init_content
            ):
                init_content = init_content.replace(
                    "from .client import AuthenticatedClient, Client, CamundaClient",
                    "from .client import AuthenticatedClient, Client, CamundaClient, CamundaAsyncClient",
                )
            else:
                init_content = init_content.replace(
                    "from .client import AuthenticatedClient, Client",
                    "from .client import AuthenticatedClient, Client, CamundaClient, CamundaAsyncClient",
                )

        init_content = _ensure_all_tuple_exports(
            init_content,
            [
                "CamundaClient",
                "CamundaAsyncClient",
                "WorkerConfig",
                "CamundaLogger",
                "NullLogger",
            ],
        )

        if "from .runtime.job_worker import WorkerConfig" not in init_content:
            init_content += "\nfrom .runtime.job_worker import WorkerConfig"

        if "from .runtime.logging import CamundaLogger, NullLogger" not in init_content:
            init_content += "\nfrom .runtime.logging import CamundaLogger, NullLogger"

        with open(init_file, "w") as f:
            f.write(init_content)
        print(
            f"Successfully exported CamundaClient, CamundaAsyncClient, and WorkerConfig in {init_file}"
        )


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    if not package_dir.exists():
        print(f"Could not find package directory in {out_dir}")
        return
    spec_path_str = context.get("bundled_spec_path", "")
    spec_path = Path(spec_path_str) if spec_path_str else None
    generate_flat_client(package_dir, spec_path)


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent.parent
    package_dir = base_dir / "generated" / "camunda_orchestration_sdk"
    spec_path = base_dir / "external-spec" / "bundled" / "rest-api.bundle.json"
    generate_flat_client(package_dir, spec_path if spec_path.exists() else None)
