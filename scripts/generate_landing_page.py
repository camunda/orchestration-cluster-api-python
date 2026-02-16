#!/usr/bin/env python3
"""Generate Docusaurus pages from the SDK README.

Reads README.md, strips sections between <!-- docs:cut:start --> and
<!-- docs:cut:end --> markers, and splits it into individual pages:

- Landing page (python-sdk.md): H1 title + content before the first H2
- One page per H2 section (e.g., installing-the-sdk-to-your-project.md)

Each page gets Docusaurus frontmatter with sidebar_position for ordering.
If an api-reference/ subdirectory exists in the output directory, a
_category_.json is generated for it.

Usage:
    python scripts/generate_landing_page.py [--output-dir public/markdown]
"""

import argparse
import json
import re
from pathlib import Path

# Deployment depth: directory levels from Docusaurus docs/ root to the
# page directory (apis-tools/python-sdk/ = 2).
_PAGE_DEPTH = 2

# Known URL-path → file-path mappings for docs.camunda.io links whose
# URL slugs don't match the actual file paths (e.g. directory renames).
_URL_PATH_OVERRIDES: dict[str, str] = {
    "apis-tools/camunda-api-rest/camunda-api-rest-overview": (
        "apis-tools/orchestration-cluster-api-rest/orchestration-cluster-api-rest-overview"
    ),
}

# sidebar_position for the API Reference category (must be last).
_API_REFERENCE_POSITION = 100


def rewrite_camunda_docs_links(content: str, depth: int = _PAGE_DEPTH) -> str:
    """Rewrite absolute docs.camunda.io links to relative Docusaurus paths."""
    base_url = "https://docs.camunda.io/docs/"
    prefix = "../" * depth

    def _replace(match: re.Match[str]) -> str:
        text = match.group(1)
        url = match.group(2)

        rel_path = url[len(base_url) :]

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


def slugify(title: str) -> str:
    """Convert a heading title to a URL-friendly slug."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug


def promote_headings(content: str) -> str:
    """Promote all headings by one level (## → #, ### → ##, etc.)."""

    def _promote(match: re.Match[str]) -> str:
        hashes = match.group(1)
        rest = match.group(2)
        if len(hashes) > 1:
            return f"{'#' * (len(hashes) - 1)} {rest}"
        return match.group(0)

    return re.sub(r"^(#{1,6}) (.+)$", _promote, content, flags=re.MULTILINE)


def make_frontmatter(
    doc_id: str,
    title: str,
    sidebar_label: str,
    sidebar_position: int,
) -> str:
    """Generate Docusaurus frontmatter."""
    return (
        f"---\n"
        f"id: {doc_id}\n"
        f"title: {title}\n"
        f"sidebar_label: {sidebar_label}\n"
        f"sidebar_position: {sidebar_position}\n"
        f"mdx:\n"
        f"  format: md\n"
        f"---\n\n"
    )


def split_by_h2(content: str) -> tuple[str, list[tuple[str, str]]]:
    """Split content into preamble (before first H2) and H2 sections.

    Returns:
        preamble: Content before the first H2 (includes the H1 line)
        sections: List of (title, body) tuples for each H2 section
    """
    parts = re.split(r"(?=^## )", content, flags=re.MULTILINE)
    preamble = parts[0]
    sections: list[tuple[str, str]] = []
    for part in parts[1:]:
        h2_match = re.match(r"^## (.+)\n", part)
        if h2_match:
            sections.append((h2_match.group(1).strip(), part))
    return preamble, sections


def generate_pages(readme_path: Path, output_dir: Path) -> None:
    """Generate landing page + per-section pages from the README."""
    content = readme_path.read_text()
    content = strip_cut_sections(content)
    content = promote_title(content)
    content = rewrite_camunda_docs_links(content)
    content = clean_empty_lines(content)
    content = content.strip() + "\n"

    preamble, sections = split_by_h2(content)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- Landing page: content under H1, before first H2 ---
    landing_fm = make_frontmatter("python-sdk", "Python SDK", "Python SDK", 1)
    landing_path = output_dir / "python-sdk.md"
    landing_path.write_text(landing_fm + preamble.strip() + "\n")
    print(f"Generated landing page: {landing_path}")

    # --- Section pages: one per H2 ---
    for i, (title, body) in enumerate(sections):
        slug = slugify(title)
        position = i + 2  # landing page is 1, sections start at 2
        page_content = promote_headings(body).strip() + "\n"
        fm = make_frontmatter(slug, title, title, position)
        page_path = output_dir / f"{slug}.md"
        page_path.write_text(fm + page_content)
        print(f"Generated section: {page_path}")

    # --- API Reference category metadata ---
    api_ref_dir = output_dir / "api-reference"
    if api_ref_dir.is_dir():
        category = {
            "label": "API Reference",
            "position": _API_REFERENCE_POSITION,
        }
        category_path = api_ref_dir / "_category_.json"
        category_path.write_text(json.dumps(category, indent=2) + "\n")
        print(f"Generated category metadata: {category_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Docusaurus pages from README"
    )
    parser.add_argument(
        "--readme",
        default="README.md",
        help="Path to README.md (default: README.md)",
    )
    parser.add_argument(
        "--output-dir",
        default="public/markdown",
        help="Output directory (default: public/markdown)",
    )
    args = parser.parse_args()

    readme_path = Path(args.readme)
    output_dir = Path(args.output_dir)

    if not readme_path.exists():
        print(f"Error: {readme_path} not found", file=__import__("sys").stderr)
        raise SystemExit(1)

    generate_pages(readme_path, output_dir)


if __name__ == "__main__":
    main()
