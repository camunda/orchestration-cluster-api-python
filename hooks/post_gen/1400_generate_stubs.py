"""Post-generation hook: generate .pyi stub files for the SDK package.

Parses each generated .py file with the ast module and emits a .pyi
stub containing only type-relevant declarations (imports, class
definitions with field annotations, method signatures, and enums).
Implementation bodies are replaced with ``...``.

This enables downstream tooling (e.g. pyright-based API changelog
generation) to work with a clean type surface.
"""

from __future__ import annotations

import ast
import re
import textwrap
from collections.abc import Callable
from pathlib import Path


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"

    if not package_dir.exists():
        print(f"Package directory not found at {package_dir}")
        return

    # Output stubs to a separate directory (not alongside .py files)
    # to avoid overriding pyright's type inference on the source.
    stubs_dir = out_dir.parent / "stubs" / "camunda_orchestration_sdk"
    if stubs_dir.exists():
        import shutil

        shutil.rmtree(stubs_dir)
    stubs_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    # Files that are shims or not useful as stubs
    skip_names = {"str.py"}
    for py_file in sorted(package_dir.rglob("*.py")):
        # Skip __pycache__ and existing stubs
        if "__pycache__" in py_file.parts:
            continue
        if py_file.name in skip_names:
            continue

        stub = _generate_stub(py_file)
        if stub is None:
            continue

        # Mirror the relative path under the stubs directory
        rel = py_file.relative_to(package_dir)
        pyi_file = stubs_dir / rel.with_suffix(".pyi")
        pyi_file.parent.mkdir(parents=True, exist_ok=True)
        pyi_file.write_text(stub, encoding="utf-8")
        count += 1

    print(f"Generated {count} stub files (.pyi) in {stubs_dir.parent}")


def _generate_stub(py_file: Path) -> str | None:
    """Generate a .pyi stub from a .py file. Returns None if the file has no type-relevant content."""
    try:
        source = py_file.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except SyntaxError:
        return None

    # Pre-split source lines for fast segment extraction
    source_lines = source.splitlines(True)

    lines: list[str] = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ImportFrom):
            lines.append(_render_import_from(node))
        elif isinstance(node, ast.Import):
            lines.append(_render_import(node))
        elif isinstance(node, ast.If):
            # Promote `if TYPE_CHECKING:` imports to unconditional
            _collect_type_checking_imports(node, lines)
        elif isinstance(node, ast.ClassDef):
            lines.append(_render_class(node, source_lines))
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            lines.append(_render_function(node, source_lines, indent=""))
        elif isinstance(node, ast.Assign):
            line = _render_assign(node, source_lines)
            if line:
                lines.append(line)
        elif isinstance(node, ast.AnnAssign):
            line = _render_ann_assign(node, source_lines)
            if line:
                lines.append(line)
        elif isinstance(node, (ast.Expr,)):
            # Module-level string expression = docstring / __future__
            if isinstance(node.value, ast.Constant) and isinstance(
                node.value.value, str
            ):
                continue  # skip module docstrings in stubs

    # Filter out empty results
    content = [l for l in lines if l.strip()]
    if not content:
        return None

    # Prepend __future__ annotations if the source had it
    header = ""
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            header = "from __future__ import annotations\n\n"
            # Remove the duplicate from content
            future_line = _render_import_from(node)
            content = [l for l in content if l.strip() != future_line.strip()]
            break

    # Filter out unused imports: keep only imported names that appear
    # in the non-import content (class defs, annotations, assignments)
    content = _filter_unused_imports(content)

    return header + "\n".join(content) + "\n"


def _filter_unused_imports(lines: list[str]) -> list[str]:
    """Remove imported names that aren't referenced in the stub body."""
    import_lines: list[str] = []
    other_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            import_lines.append(line)
        else:
            other_lines.append(line)

    body_text = "\n".join(other_lines)

    def _name_used(name: str) -> bool:
        return bool(re.search(r'\b' + re.escape(name) + r'\b', body_text))

    result: list[str] = []
    for line in import_lines:
        stripped = line.strip()
        if stripped.startswith("from "):
            # Filter individual names in "from X import a, b, c"
            filtered = _filter_from_import(stripped, _name_used)
            if filtered:
                result.append(filtered)
        else:
            # "import X" — keep if X is used
            names = _extract_plain_import_names(stripped)
            if any(_name_used(name) for name in names):
                result.append(line)

    result.extend(other_lines)
    return result


def _filter_from_import(import_line: str, name_used: Callable[[str], bool]) -> str | None:
    """Filter a 'from X import a, b, c' line to only keep names used in the body."""
    idx = import_line.index(" import ")
    prefix = import_line[: idx + 8]  # "from X import "
    names_part = import_line[idx + 8:]

    kept: list[str] = []
    for part in names_part.split(","):
        part = part.strip()
        if not part:
            continue
        # Get the local name (after "as" if present)
        if " as " in part:
            local_name = part.split(" as ")[-1].strip()
        else:
            local_name = part.strip()
        if name_used(local_name):
            kept.append(part)

    if not kept:
        return None
    return prefix + ", ".join(kept)


def _extract_plain_import_names(import_line: str) -> list[str]:
    """Extract names from 'import X, Y as Z'."""
    names_part = import_line[7:]  # strip "import "
    names: list[str] = []
    for part in names_part.split(","):
        part = part.strip()
        if " as " in part:
            names.append(part.split(" as ")[-1].strip())
        else:
            names.append(part.split(".")[0].strip())
    return names


def _render_import(node: ast.Import) -> str:
    names = ", ".join(
        f"{alias.name} as {alias.asname}" if alias.asname else alias.name
        for alias in node.names
    )
    return f"import {names}"


def _render_import_from(node: ast.ImportFrom) -> str:
    module = node.module or ""
    dots = "." * (node.level or 0)
    names = ", ".join(
        f"{alias.name} as {alias.asname}" if alias.asname else alias.name
        for alias in node.names
    )
    return f"from {dots}{module} import {names}"


def _collect_type_checking_imports(node: ast.If, lines: list[str]) -> None:
    """If the node is `if TYPE_CHECKING:`, promote its imports to unconditional."""
    # Match `if TYPE_CHECKING:`
    test = node.test
    if isinstance(test, ast.Name) and test.id == "TYPE_CHECKING":
        pass
    elif isinstance(test, ast.Attribute) and test.attr == "TYPE_CHECKING":
        pass
    else:
        return

    for child in node.body:
        if isinstance(child, ast.ImportFrom):
            lines.append(_render_import_from(child))
        elif isinstance(child, ast.Import):
            lines.append(_render_import(child))


def _get_segment(source_lines: list[str], node: ast.expr | ast.stmt) -> str | None:
    """Fast replacement for ast.get_source_segment using pre-split lines."""
    start_line: int = node.lineno  # 1-based
    end_line: int = node.end_lineno or start_line
    col_offset: int = node.col_offset
    end_col: int | None = node.end_col_offset

    if start_line == end_line:
        line = source_lines[start_line - 1]
        if end_col is not None:
            return line[col_offset:end_col]
        return line[col_offset:].rstrip("\n\r")

    parts = [source_lines[start_line - 1][col_offset:]]
    for i in range(start_line, end_line - 1):
        parts.append(source_lines[i])
    last_line = source_lines[end_line - 1]
    if end_col is not None:
        parts.append(last_line[:end_col])
    else:
        parts.append(last_line.rstrip("\n\r"))
    return "".join(parts)


def _render_class(node: ast.ClassDef, source_lines: list[str]) -> str:
    bases = [_get_segment(source_lines, b) or "..." for b in node.bases]

    # Include decorator names (e.g. @_attrs_define)
    decorators: list[str] = []
    for dec in node.decorator_list:
        dec_src = _get_segment(source_lines, dec)
        if dec_src:
            decorators.append(f"@{dec_src}")

    base_str = f"({', '.join(bases)})" if bases else ""
    dec_lines = "\n".join(decorators)
    if dec_lines:
        dec_lines += "\n"
    header = f"{dec_lines}class {node.name}{base_str}:"

    body_lines: list[str] = []

    for child in node.body:
        if isinstance(child, ast.AnnAssign):
            line = _render_ann_assign(child, source_lines, indent="    ")
            if line:
                body_lines.append(line)
        elif isinstance(child, ast.Assign):
            line = _render_assign(child, source_lines, indent="    ")
            if line:
                body_lines.append(line)
        elif isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
            body_lines.append(_render_function(child, source_lines, indent="    "))
        elif isinstance(child, ast.Expr):
            # Skip docstrings
            pass

    if not body_lines:
        body_lines.append("    ...")

    return header + "\n" + "\n".join(body_lines)


def _render_function(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    indent: str,
) -> str:
    decorators: list[str] = []
    for dec in node.decorator_list:
        dec_src = _get_segment(source_lines, dec)
        if dec_src:
            decorators.append(f"{indent}@{dec_src}")

    args = _render_args(node.args, source_lines)
    returns = ""
    if node.returns:
        ret_src = _get_segment(source_lines, node.returns)
        if ret_src:
            returns = f" -> {ret_src}"

    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    dec_str = "\n".join(decorators)
    if dec_str:
        dec_str += "\n"
    return f"{dec_str}{indent}{prefix} {node.name}({args}){returns}: ..."


def _render_args(args: ast.arguments, source_lines: list[str]) -> str:
    parts: list[str] = []

    # positional args
    num_defaults = len(args.defaults)
    num_args = len(args.args)
    non_default_count = num_args - num_defaults

    for i, arg in enumerate(args.args):
        ann = ""
        if arg.annotation:
            ann_src = _get_segment(source_lines, arg.annotation)
            if ann_src:
                ann = f": {ann_src}"

        if i >= non_default_count:
            default_node = args.defaults[i - non_default_count]
            default_src = _get_segment(source_lines, default_node)
            if default_src:
                parts.append(f"{arg.arg}{ann} = {default_src}")
            else:
                parts.append(f"{arg.arg}{ann} = ...")
        else:
            parts.append(f"{arg.arg}{ann}")

    # *args
    if args.vararg:
        ann = ""
        if args.vararg.annotation:
            ann_src = _get_segment(source_lines, args.vararg.annotation)
            if ann_src:
                ann = f": {ann_src}"
        parts.append(f"*{args.vararg.arg}{ann}")

    # keyword-only args
    for i, arg in enumerate(args.kwonlyargs):
        ann = ""
        if arg.annotation:
            ann_src = _get_segment(source_lines, arg.annotation)
            if ann_src:
                ann = f": {ann_src}"
        default_node = args.kw_defaults[i]
        if default_node:
            default_src = _get_segment(source_lines, default_node)
            if default_src:
                parts.append(f"{arg.arg}{ann} = {default_src}")
            else:
                parts.append(f"{arg.arg}{ann} = ...")
        else:
            parts.append(f"{arg.arg}{ann}")

    # **kwargs
    if args.kwarg:
        ann = ""
        if args.kwarg.annotation:
            ann_src = _get_segment(source_lines, args.kwarg.annotation)
            if ann_src:
                ann = f": {ann_src}"
        parts.append(f"**{args.kwarg.arg}{ann}")

    return ", ".join(parts)


def _render_assign(
    node: ast.Assign, source_lines: list[str], indent: str = ""
) -> str:
    """Render module/class-level assignments like T = TypeVar(...)."""
    if len(node.targets) != 1:
        return ""
    target = node.targets[0]
    if not isinstance(target, ast.Name):
        return ""
    src = _get_segment(source_lines, node)
    if src:
        # Indent each line
        if indent:
            src = textwrap.indent(src, indent)
        return src
    return ""


def _render_ann_assign(
    node: ast.AnnAssign, source_lines: list[str], indent: str = ""
) -> str:
    """Render annotated assignments (field declarations)."""
    src = _get_segment(source_lines, node)
    if src:
        if indent:
            src = textwrap.indent(src, indent)
        return src
    return ""
