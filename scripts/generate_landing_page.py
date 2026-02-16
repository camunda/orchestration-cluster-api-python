#!/usr/bin/env python3
"""Generate the Docusaurus landing page from the SDK README.

Reads README.md, strips sections between <!-- docs:cut:start --> and
<!-- docs:cut:end --> markers, demotes the H2 title to H1, adjusts
relative links for the Docusaurus context, and writes the result with
frontmatter.

Usage:
    python scripts/generate_landing_page.py [--output public/markdown/python-sdk.md]
"""

import argparse
import re
from pathlib import Path

FRONTMATTER = """\
---
id: python-sdk
title: Python SDK
sidebar_label: Python SDK
mdx:
  format: md
---

"""

# Deployment depth: directory levels from Docusaurus docs/ root to the
# landing page directory (apis-tools/python-sdk/ = 2).
_LANDING_PAGE_DEPTH = 2

# Known URL-path → file-path mappings for docs.camunda.io links whose
# URL slugs don't match the actual file paths (e.g. directory renames).
_URL_PATH_OVERRIDES: dict[str, str] = {
    "apis-tools/camunda-api-rest/camunda-api-rest-overview": (
        "apis-tools/orchestration-cluster-api-rest/orchestration-cluster-api-rest-overview"
    ),
}


def rewrite_camunda_docs_links(content: str, depth: int = _LANDING_PAGE_DEPTH) -> str:
    """Rewrite absolute docs.camunda.io links to relative Docusaurus paths."""
    base_url = "https://docs.camunda.io/docs/"
    prefix = "../" * depth

    def _replace(match: re.Match[str]) -> str:
        text = match.group(1)
        url = match.group(2)

        rel_path = url[len(base_url):]

        fragment = ""
        if "#" in rel_path:
            rel_path, fragment = rel_path.rsplit("#", 1)
            fragment = "#" + fragment

        rel_path = rel_path.strip("/")
        rel_path = _URL_PATH_OVERRIDES.get(rel_path, rel_path)

        if rel_path and not rel_path.endswith((".md", ".mdx")):
            rel_path += ".md"

        if text.startswith("http"):
            name = rel_path.rsplit("/", 1)[-1].removesuffix(".md").removesuffix(".mdx")
            text = name.replace("-", " ")

        return f"[{text}]({prefix}{rel_path}{fragment})"

    return re.sub(
        r"\[([^\]]+)\]\((https://docs\.camunda\.io/docs/[^)]+)\)",
        _replace,
        content,
    )


def strip_cut_sections(content: str) -> str:
    """Remove content between <!-- docs:cut:start --> and <!-- docs:cut:end --> markers."""
    return re.sub(
        r"<!-- docs:cut:start -->.*?<!-- docs:cut:end -->\n?",
        "",
        content,
        flags=re.DOTALL,
    )


def promote_title(content: str) -> str:
    """Convert the first H2 heading to H1 (README uses ## as top-level)."""
    return re.sub(r"^## ", "# ", content, count=1)


def clean_empty_lines(content: str) -> str:
    """Collapse 3+ consecutive blank lines to 2."""
    return re.sub(r"\n{4,}", "\n\n\n", content)


def generate_landing_page(readme_path: Path, output_path: Path) -> None:
    content = readme_path.read_text()
    content = strip_cut_sections(content)
    content = promote_title(content)
    content = rewrite_camunda_docs_links(content)
    content = clean_empty_lines(content)
    content = content.strip() + "\n"

    # Add API Reference link at the end
    content += "\n## API Reference\n\nSee the [API Reference](api-reference/index.md) for full class and method documentation.\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(FRONTMATTER + content)
    print(f"Generated landing page: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Docusaurus landing page from README")
    parser.add_argument(
        "--readme",
        default="README.md",
        help="Path to README.md (default: README.md)",
    )
    parser.add_argument(
        "--output",
        default="public/markdown/python-sdk.md",
        help="Output path (default: public/markdown/python-sdk.md)",
    )
    args = parser.parse_args()

    readme_path = Path(args.readme)
    output_path = Path(args.output)

    if not readme_path.exists():
        print(f"Error: {readme_path} not found", file=__import__("sys").stderr)
        raise SystemExit(1)

    generate_landing_page(readme_path, output_path)


if __name__ == "__main__":
    main()
