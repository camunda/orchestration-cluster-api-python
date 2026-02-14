"""Post-generation hook: inject example code blocks into client docstrings.

Uses AST to locate method docstrings in CamundaClient and CamundaAsyncClient,
then injects example code blocks as Google-style ``Examples:`` sections.

This makes examples visible in Sphinx-generated API documentation.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path


def _extract_region(file_path: Path, region_name: str) -> str | None:
    """Extract code between ``# region Name`` and ``# endregion Name`` markers."""
    if not file_path.exists():
        return None
    lines = file_path.read_text(encoding="utf-8").splitlines()
    capturing = False
    captured: list[str] = []
    for line in lines:
        if line.strip() == f"# region {region_name}":
            capturing = True
            continue
        if line.strip() == f"# endregion {region_name}":
            break
        if capturing:
            captured.append(line)

    if not captured:
        return None

    # Dedent: remove common leading whitespace
    non_empty = [l for l in captured if l.strip()]
    if non_empty:
        min_indent = min(len(l) - len(l.lstrip()) for l in non_empty)
        captured = [l[min_indent:] if len(l) >= min_indent else l for l in captured]

    # Strip leading/trailing blank lines
    while captured and not captured[0].strip():
        captured.pop(0)
    while captured and not captured[-1].strip():
        captured.pop()

    return "\n".join(captured)


def _build_examples_text(
    examples: list[tuple[str, str]],
    base_indent: str,
) -> str:
    """Build a Google-style Examples section to append to a docstring.

    Uses RST ``.. code-block:: python`` directives so that Sphinx/Napoleon
    renders syntax-highlighted code blocks.

    Args:
        examples: List of (label, code) tuples.
        base_indent: Indentation for section headers (matches Args/Returns).
    """
    inner = base_indent + "    "
    code_indent = inner + "    "
    blocks: list[str] = []
    for label, code in examples:
        indented_lines: list[str] = []
        for line in code.splitlines():
            if line.strip():
                indented_lines.append(code_indent + line)
            else:
                indented_lines.append("")
        indented_code = "\n".join(indented_lines)
        blocks.append(
            f"{inner}**{label}:**\n\n"
            f"{inner}.. code-block:: python\n\n"
            f"{indented_code}"
        )
    return f"\n\n{base_indent}Examples:\n" + "\n\n".join(blocks) + "\n"


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"]).resolve()
    examples_dir = (
        Path(context["examples_dir"]).resolve()
        if context.get("examples_dir")
        else Path(__file__).resolve().parent.parent.parent / "examples"
    )
    map_path = examples_dir / "operation-map.json"

    if not map_path.exists():
        print("examples/operation-map.json not found — skipping example injection")
        return

    with open(map_path, "r", encoding="utf-8") as f:
        operation_map: dict[str, list[dict[str, str]]] = json.load(f)

    client_file = out_dir / "camunda_orchestration_sdk" / "client.py"
    if not client_file.exists():
        print("client.py not found — skipping example injection")
        return

    source = client_file.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # Build line-start byte-offset table: line_starts[i] = byte offset of line i (0-indexed)
    source_lines = source.splitlines(keepends=True)
    line_starts = [0]
    for line in source_lines:
        line_starts.append(line_starts[-1] + len(line))

    # Collect replacements: (start_byte, end_byte, new_literal)
    replacements: list[tuple[int, int, str]] = []

    for class_node in ast.iter_child_nodes(tree):
        if not isinstance(class_node, ast.ClassDef):
            continue
        if class_node.name not in ("CamundaClient", "CamundaAsyncClient"):
            continue

        for method_node in class_node.body:
            if not isinstance(method_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if method_node.name not in operation_map:
                continue

            # Verify the first statement is a docstring
            if not (
                method_node.body
                and isinstance(method_node.body[0], ast.Expr)
                and isinstance(method_node.body[0].value, ast.Constant)
                and isinstance(method_node.body[0].value.value, str)
            ):
                continue

            ds_node = method_node.body[0].value  # ast.Constant
            assert isinstance(ds_node.value, str)
            raw_ds: str = ds_node.value

            # Collect snippets for this method
            snippets: list[tuple[str, str]] = []
            for ref in operation_map[method_node.name]:
                code = _extract_region(examples_dir / ref["file"], ref["region"])
                if code:
                    snippets.append((ref["label"], code))

            if not snippets:
                continue

            # Detect base indent from existing section headers in the raw docstring.
            # Hook 0900 uses ast.get_docstring (cleaned), so headers like Args: are
            # at column 0 within the raw string.  Use [ \t]* (not \s+) to match that.
            m = re.search(r"^([ \t]*)(Args|Raises|Returns):", raw_ds, re.MULTILINE)
            base_indent = m.group(1) if m else ""

            # Build and append examples section
            examples_text = _build_examples_text(snippets, base_indent)
            new_ds = raw_ds.rstrip() + examples_text + base_indent

            # Locate the docstring literal in the source via AST positions
            assert ds_node.end_lineno is not None and ds_node.end_col_offset is not None
            start = line_starts[ds_node.lineno - 1] + ds_node.col_offset
            end = line_starts[ds_node.end_lineno - 1] + ds_node.end_col_offset

            # Detect quote style from actual source
            original_literal = source[start:end]
            if original_literal.startswith('"""'):
                quote = '"""'
            elif original_literal.startswith("'''"):
                quote = "'''"
            else:
                continue

            new_literal = f"{quote}{new_ds}{quote}"
            replacements.append((start, end, new_literal))

    if not replacements:
        print("[inject-examples] No examples injected into client.py")
        return

    # Apply replacements in reverse source order to preserve byte offsets
    replacements.sort(key=lambda r: r[0], reverse=True)
    for start, end, text in replacements:
        source = source[:start] + text + source[end:]

    client_file.write_text(source, encoding="utf-8")
    print(f"[inject-examples] Injected {len(replacements)} example blocks into client.py")
