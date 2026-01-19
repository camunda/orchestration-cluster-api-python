#!/usr/bin/env python3
"""Post-process Sphinx-generated markdown for Docusaurus compatibility."""

import re
import sys
from pathlib import Path


def postprocess_markdown(content: str) -> str:
    """Apply all post-processing transformations to markdown content."""

    # Simplify class headings (strip parameters for cleaner TOC)
    content = re.sub(
        r'^(### \*class\* [\w.]+)\([^)]*\)\s*$',
        r'\1',
        content,
        flags=re.MULTILINE
    )

    # Promote heading levels for proper Docusaurus TOC hierarchy (H3->H2, H4->H3)
    content = re.sub(r'^### \*class\*', '## *class*', content, flags=re.MULTILINE)
    content = re.sub(r'^#### ', '### ', content, flags=re.MULTILINE)

    # Escape <...> and {...} to prevent MDX parsing as JSX
    content = re.sub(r'<([a-zA-Z_][^>]*)>', r'`<\1>`', content)
    content = re.sub(r'\{([a-zA-Z_][^}]*)\}', r'`{\1}`', content)

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
