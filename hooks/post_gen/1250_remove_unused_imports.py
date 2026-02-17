"""Post-gen hook: Remove unused imports from generated Python files.

Uses pyright's reportUnusedImport diagnostic to find and remove import
statements whose imported names are never referenced in the file.
This avoids maintaining brittle per-file fixups whenever the generator
or upstream spec introduces a new unused import.
"""

from __future__ import annotations

import ast
from pathlib import Path


def _find_unused_imports(source: str, *, is_init: bool = False) -> set[str]:
    """Return imported names that are never referenced elsewhere in *source*.

    Only considers top-level ``import X`` and ``from Y import X`` statements.
    A name is "used" if it appears as an ``ast.Name`` node outside import
    statements or inside ``__all__``.

    Special cases:
    - ``from __future__ import ...`` is always kept.
    - In ``__init__.py`` files, all imports are kept (they are re-exports).
    - Imports guarded by ``if TYPE_CHECKING:`` are kept.
    """
    if is_init:
        return set()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()

    # Collect every imported name → the ast node that imports it.
    imported: dict[str, ast.stmt] = {}
    import_nodes: set[int] = set()
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            import_nodes.add(id(node))
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                imported[name] = node
        elif isinstance(node, ast.ImportFrom):
            # Never remove __future__ imports.
            if node.module == "__future__":
                continue
            import_nodes.add(id(node))
            if node.names:
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imported[name] = node
        # Skip imports inside if TYPE_CHECKING blocks
        elif isinstance(node, ast.If):
            test = node.test
            if isinstance(test, ast.Name) and test.id == "TYPE_CHECKING":
                continue

    if not imported:
        return set()

    # Walk the entire tree; record every Name reference that is NOT part of
    # an import statement.
    used_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)
        elif isinstance(node, ast.Attribute):
            # ``foo.bar`` — ``foo`` counts as used.
            inner = node
            while isinstance(inner, ast.Attribute):
                inner = inner.value  # type: ignore[assignment]
            if isinstance(inner, ast.Name):
                used_names.add(inner.id)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            # String annotations like ``"dict[str, Any]"`` — try parsing
            # them as type expressions to capture referenced names.
            try:
                str_tree = ast.parse(node.value, mode="eval")
                for inner_node in ast.walk(str_tree):
                    if isinstance(inner_node, ast.Name):
                        used_names.add(inner_node.id)
            except SyntaxError:
                pass

    # An imported name is unused if it never appears outside import stmts.
    # We already collected all Name references; the AST walker visits import
    # alias nodes too, but that's fine — „re" in ``import re`` creates an
    # ast.alias, not ast.Name, so it won't pollute used_names.
    unused: set[str] = set()
    for name in imported:
        if name not in used_names:
            unused.add(name)

    return unused


def _remove_names_from_source(source: str, names_to_remove: set[str]) -> str:
    """Remove *names_to_remove* from import lines in *source*.

    If an entire import line becomes empty after removal, delete the line.
    Handles ``from X import A, B, C`` multi-name imports by keeping only
    the names that are still needed.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    lines = source.splitlines(keepends=True)
    # Process in reverse so line-number edits don't shift later nodes.
    removals: list[tuple[int, int]] = []  # (start_line_0, end_line_0)
    replacements: list[tuple[int, int, str]] = []  # (start_0, end_0, new_text)

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            remaining = [
                a for a in node.names if (a.asname or a.name) not in names_to_remove
            ]
            if not remaining:
                removals.append((node.lineno - 1, (node.end_lineno or node.lineno) - 1))
            elif len(remaining) < len(node.names):
                parts = ", ".join(
                    f"{a.name} as {a.asname}" if a.asname else a.name for a in remaining
                )
                replacements.append(
                    (
                        node.lineno - 1,
                        (node.end_lineno or node.lineno) - 1,
                        f"import {parts}\n",
                    )
                )
        elif isinstance(node, ast.ImportFrom):
            if not node.names:
                continue
            remaining = [
                a for a in node.names if (a.asname or a.name) not in names_to_remove
            ]
            if not remaining:
                removals.append((node.lineno - 1, (node.end_lineno or node.lineno) - 1))
            elif len(remaining) < len(node.names):
                module = node.module or ""
                dots = "." * (node.level or 0)
                parts = ", ".join(
                    f"{a.name} as {a.asname}" if a.asname else a.name for a in remaining
                )
                replacements.append(
                    (
                        node.lineno - 1,
                        (node.end_lineno or node.lineno) - 1,
                        f"from {dots}{module} import {parts}\n",
                    )
                )

    # Apply in reverse line order.
    edits = [(s, e, None) for s, e in removals] + [
        (s, e, t) for s, e, t in replacements
    ]
    edits.sort(key=lambda x: x[0], reverse=True)

    for start, end, text in edits:
        if text is None:
            del lines[start : end + 1]
        else:
            lines[start : end + 1] = [text]

    return "".join(lines)


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"]).resolve()
    package_dir = out_dir / "camunda_orchestration_sdk"
    if not package_dir.exists():
        return

    fixed_count = 0
    for py_file in sorted(package_dir.rglob("*.py")):
        source = py_file.read_text(encoding="utf-8")
        is_init = py_file.name == "__init__.py"
        unused = _find_unused_imports(source, is_init=is_init)
        if not unused:
            continue
        new_source = _remove_names_from_source(source, unused)
        if new_source != source:
            py_file.write_text(new_source, encoding="utf-8")
            fixed_count += 1
            for name in sorted(unused):
                print(f"Removed unused import '{name}' from {py_file.name}")

    print(f"Cleaned unused imports in {fixed_count} files")
