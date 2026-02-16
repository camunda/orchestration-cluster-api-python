#!/usr/bin/env python3
"""Post-process Sphinx-generated markdown for Docusaurus compatibility.

Supports both single-file and multi-file (directory) modes:
  postprocess_markdown.py <file.md>           # single file (legacy)
  postprocess_markdown.py <directory/>         # all .md files in dir
"""

import re
import sys
from pathlib import Path

# Deployment depth: directory levels from Docusaurus docs/ root to the
# API reference directory (apis-tools/python-sdk/api-reference/ = 3).
DEPLOYMENT_DEPTH = 3

# Known URL-path → file-path mappings for docs.camunda.io links whose
# URL slugs don't match the actual file paths (e.g. directory renames).
_URL_PATH_OVERRIDES: dict[str, str] = {
    "apis-tools/camunda-api-rest/camunda-api-rest-overview": (
        "apis-tools/orchestration-cluster-api-rest/orchestration-cluster-api-rest-overview"
    ),
}

# Mapping from Sphinx output filename (stem) to Docusaurus frontmatter.
# Files not listed here get auto-generated frontmatter from their H1.
PAGE_METADATA: dict[str, dict[str, str]] = {
    "index": {
        "title": "Python SDK API Reference",
        "sidebar_label": "Overview",
        "sidebar_position": "1",
    },
    "client": {
        "title": "CamundaClient",
        "sidebar_label": "CamundaClient",
        "sidebar_position": "2",
    },
    "async-client": {
        "title": "CamundaAsyncClient",
        "sidebar_label": "CamundaAsyncClient",
        "sidebar_position": "3",
    },
    "configuration": {
        "title": "Configuration",
        "sidebar_label": "Configuration",
        "sidebar_position": "4",
    },
    "runtime": {
        "title": "Runtime",
        "sidebar_label": "Runtime",
        "sidebar_position": "5",
    },
    "types": {
        "title": "Semantic Types",
        "sidebar_label": "Semantic Types",
        "sidebar_position": "6",
    },
}


def simplify_class_heading(match: re.Match[str]) -> str:
    """Transform class heading: keep simple name, move full signature to code block."""
    hashes = match.group(1)
    class_name = match.group(2)
    params = match.group(3) or ""

    if params:
        signature = f"class {class_name}({params})"
    else:
        signature = f"class {class_name}"

    return f"{hashes} {class_name}\n\n```python\n{signature}\n```"


def simplify_method_heading(match: re.Match[str]) -> str:
    """Transform method heading: keep simple name, move full signature to code block."""
    hashes = match.group(1)
    async_marker = match.group(2) or ""
    method_name = match.group(3)
    params = match.group(4)
    return_type = match.group(5) or ""

    async_prefix = "async " if async_marker else ""
    if return_type:
        signature = f"{async_prefix}def {method_name}({params}) -> {return_type}"
    else:
        signature = f"{async_prefix}def {method_name}({params})"

    return f"{hashes} {method_name}()\n\n```python\n{signature}\n```"


def simplify_property_heading(match: re.Match[str]) -> str:
    """Transform property heading: keep simple name, move type to code block."""
    hashes = match.group(1)
    prop_name = match.group(2)
    prop_type = match.group(3)

    return f"{hashes} {prop_name}\n\n```python\n{prop_name}: {prop_type}\n```"


def fix_anchor_links(content: str) -> str:
    """Fix Sphinx-generated anchor links to match Docusaurus heading anchors.

    Sphinx generates links like #camunda_orchestration_sdk.ClassName but Docusaurus
    creates anchors from headings by lowercasing (e.g., ## ClassName -> #classname).
    """

    def fix_anchor(match: re.Match[str]) -> str:
        link_text = match.group(1)
        anchor = match.group(2)

        parts = anchor.split(".")
        name = parts[-1]

        new_anchor = name.lower()

        return f"[{link_text}](#{new_anchor})"

    content = re.sub(
        r"\[([^\]]+)\]\(#(camunda_orchestration_sdk\.[^)]+)\)",
        fix_anchor,
        content,
    )

    return content


def rewrite_camunda_docs_links(content: str, depth: int = DEPLOYMENT_DEPTH) -> str:
    """Rewrite absolute docs.camunda.io links to relative Docusaurus paths.

    Converts ``[text](https://docs.camunda.io/docs/path)`` to a relative
    file-path link so Docusaurus versioning works correctly.
    """
    base_url = "https://docs.camunda.io/docs/"
    prefix = "../" * depth

    def _replace(match: re.Match[str]) -> str:
        text = match.group(1)
        url = match.group(2)

        rel_path = url[len(base_url) :]

        # Separate fragment
        fragment = ""
        if "#" in rel_path:
            rel_path, fragment = rel_path.rsplit("#", 1)
            fragment = "#" + fragment

        rel_path = rel_path.strip("/")

        # Apply known path overrides (directory renames, etc.)
        rel_path = _URL_PATH_OVERRIDES.get(rel_path, rel_path)

        # Ensure .md extension
        if rel_path and not rel_path.endswith((".md", ".mdx")):
            rel_path += ".md"

        # If link text is the URL itself, derive descriptive text
        if text.startswith("http"):
            name = rel_path.rsplit("/", 1)[-1].removesuffix(".md").removesuffix(".mdx")
            text = name.replace("-", " ")

        return f"[{text}]({prefix}{rel_path}{fragment})"

    return re.sub(
        r"\[([^\]]+)\]\((https://docs\.camunda\.io/docs/[^)]+)\)",
        _replace,
        content,
    )


def postprocess_markdown(content: str) -> str:
    """Apply all post-processing transformations to markdown content."""

    # Fix anchor links before other transformations
    content = fix_anchor_links(content)

    # Rewrite absolute docs.camunda.io links to relative Docusaurus paths
    content = rewrite_camunda_docs_links(content)

    # Promote heading levels for proper Docusaurus TOC hierarchy (H3->H2, H4->H3)
    content = re.sub(r"^### \*class\*", "## *class*", content, flags=re.MULTILINE)
    content = re.sub(r"^#### ", "### ", content, flags=re.MULTILINE)

    # Simplify class headings and add signature code block
    content = re.sub(
        r"^(#{2,3}) \*class\* ([\w.]+)(?:\(([^)]*)\))?$",
        simplify_class_heading,
        content,
        flags=re.MULTILINE,
    )

    # Simplify method headings and add signature code block
    content = re.sub(
        r"^(#{2,3}) (\*async\* )?(\w+)\(([^)]*)\)(?: → (.+))?$",
        simplify_method_heading,
        content,
        flags=re.MULTILINE,
    )

    # Simplify property headings and add type code block
    content = re.sub(
        r"^(#{2,3}) (\w+) \*: (.+)\*$",
        simplify_property_heading,
        content,
        flags=re.MULTILINE,
    )

    # No longer need to escape <...> or {...} for MDX since we use
    # mdx.format: md in frontmatter (CommonMark mode).

    # Remove malformed code blocks with :param/:type (RST leftovers)
    content = re.sub(r"^```default\s*\n", "", content, flags=re.MULTILINE)
    content = re.sub(
        r"^:param\s+(\w+):\s*(.*)$", r"* **\1**: \2", content, flags=re.MULTILINE
    )
    content = re.sub(r"^:type\s+\w+:.*\n", "", content, flags=re.MULTILINE)

    # Fix broken admonition syntax (:: at end of :::info blocks)
    content = re.sub(r"^::\s*$", ":::", content, flags=re.MULTILINE)

    # Rewrite Sphinx cross-page links for Docusaurus.
    # Sphinx emits links like [CamundaClient](client.md#...) which work as-is,
    # but also toctree links that use .md extensions. Keep .md extensions since
    # Docusaurus resolves them correctly when slug-based routing is configured.

    return content


def add_frontmatter(content: str, stem: str) -> str:
    """Add Docusaurus frontmatter. Uses PAGE_METADATA if available, else derives from the H1."""
    # Skip if frontmatter already exists
    if content.startswith("---\n"):
        return content

    if stem in PAGE_METADATA:
        meta = PAGE_METADATA[stem]
    else:
        # Derive from the first H1 heading in the content
        h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = (
            h1_match.group(1).strip() if h1_match else stem.replace("-", " ").title()
        )
        meta = {"title": title, "sidebar_label": title}

    lines = ["---"]
    for key, value in meta.items():
        lines.append(f"{key}: {value}")
    lines.append("mdx:")
    lines.append("  format: md")
    lines.append("---")
    lines.append("")
    lines.append("")

    return "\n".join(lines) + content


def process_file(path: Path) -> None:
    """Post-process a single markdown file in-place."""
    content = path.read_text()
    content = postprocess_markdown(content)
    content = add_frontmatter(content, stem=path.stem)
    path.write_text(content)


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: postprocess_markdown.py <file_or_directory>",
            file=sys.stderr,
        )
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_dir():
        md_files = sorted(target.glob("*.md"))
        for md_file in md_files:
            process_file(md_file)
            print(f"Processed: {md_file}")
        print(f"Post-processed {len(md_files)} markdown files in {target}")
    else:
        output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else target
        content = target.read_text()
        content = postprocess_markdown(content)
        content = add_frontmatter(content, stem=target.stem)
        output_path.write_text(content)
        print(f"Processed: {target} -> {output_path}")


if __name__ == "__main__":
    main()
