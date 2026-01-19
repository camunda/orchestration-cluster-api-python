#!/usr/bin/env python3
"""Post-process Sphinx-generated markdown for Docusaurus compatibility."""

import re
import sys
from pathlib import Path


def simplify_class_heading(match: re.Match) -> str:
    """Transform class heading: keep simple name, move full signature to code block."""
    hashes = match.group(1)
    full_name = match.group(2)  # e.g., "camunda_orchestration_sdk.AuthenticatedClient"
    params = match.group(3) or ""  # constructor parameters, may be empty

    # Extract just the class name
    simple_name = full_name.split(".")[-1]

    # Build the full signature for the code block
    if params:
        signature = f"class {full_name}({params})"
    else:
        signature = f"class {full_name}"

    return f"{hashes} {simple_name}\n\n```python\n{signature}\n```"


def simplify_method_heading(match: re.Match) -> str:
    """Transform method heading: keep simple name, move full signature to code block."""
    hashes = match.group(1)
    async_marker = match.group(2) or ""
    method_name = match.group(3)
    params = match.group(4)
    return_type = match.group(5) or ""

    # Build the full signature for the code block
    async_prefix = "async " if async_marker else ""
    if return_type:
        signature = f"{async_prefix}def {method_name}({params}) -> {return_type}"
    else:
        signature = f"{async_prefix}def {method_name}({params})"

    return f"{hashes} {method_name}()\n\n```python\n{signature}\n```"


def simplify_property_heading(match: re.Match) -> str:
    """Transform property heading: keep simple name, move type to code block."""
    hashes = match.group(1)
    prop_name = match.group(2)
    prop_type = match.group(3)

    return f"{hashes} {prop_name}\n\n```python\n{prop_name}: {prop_type}\n```"


def postprocess_markdown(content: str) -> str:
    """Apply all post-processing transformations to markdown content."""

    # Promote heading levels for proper Docusaurus TOC hierarchy (H3->H2, H4->H3)
    content = re.sub(r'^### \*class\*', '## *class*', content, flags=re.MULTILINE)
    content = re.sub(r'^#### ', '### ', content, flags=re.MULTILINE)

    # Simplify class headings and add signature code block
    # Pattern: "## *class* module.ClassName(params)" or "## *class* module.ClassName"
    content = re.sub(
        r'^(#{2,3}) \*class\* ([\w.]+)(?:\(([^)]*)\))?$',
        simplify_class_heading,
        content,
        flags=re.MULTILINE
    )

    # Simplify method headings and add signature code block
    # Pattern: "### method_name(...) → ReturnType" or "### *async* method_name(...) → ReturnType"
    content = re.sub(
        r'^(#{2,3}) (\*async\* )?(\w+)\(([^)]*)\)(?: → (.+))?$',
        simplify_method_heading,
        content,
        flags=re.MULTILINE
    )

    # Simplify property headings and add type code block
    # Pattern: "### property_name *: type*"
    content = re.sub(
        r'^(#{2,3}) (\w+) \*: (.+)\*$',
        simplify_property_heading,
        content,
        flags=re.MULTILINE
    )

    # Escape <...> and {...} to prevent MDX parsing as JSX (but not inside code blocks)
    # Split by code blocks, only transform non-code sections
    parts = re.split(r'(```[\s\S]*?```)', content)
    for i, part in enumerate(parts):
        if not part.startswith('```'):
            parts[i] = re.sub(r'<([a-zA-Z_][^>]*)>', r'`<\1>`', part)
            parts[i] = re.sub(r'\{([a-zA-Z_][^}]*)\}', r'`{\1}`', parts[i])
    content = ''.join(parts)

    # Remove malformed code blocks with :param/:type (RST leftovers)
    content = re.sub(r'^```default\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^:param\s+(\w+):\s*(.*)$', r'* **\1**: \2', content, flags=re.MULTILINE)
    content = re.sub(r'^:type\s+\w+:.*\n', '', content, flags=re.MULTILINE)

    # Fix broken admonition syntax (:: at end of :::info blocks)
    content = re.sub(r'^::\s*$', ':::', content, flags=re.MULTILINE)

    return content


def add_frontmatter(content: str) -> str:
    """Add Docusaurus frontmatter to the beginning of the content."""
    frontmatter = """---
id: api-reference
title: Python SDK API Reference
sidebar_label: API Reference
---

"""
    return frontmatter + content


def main():
    if len(sys.argv) < 2:
        print("Usage: postprocess_markdown.py <input_file> [output_file]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path

    content = input_path.read_text()
    content = postprocess_markdown(content)
    content = add_frontmatter(content)
    output_path.write_text(content)

    print(f"Processed: {input_path} -> {output_path}")


if __name__ == "__main__":
    main()
