"""Post-generation hook: strip redundant ``Type0`` suffixes from model names.

The ``openapi-python-client`` generator appends ``Type0`` when a schema is
nullable (``nullable: true``) — it splits the type into a union where the
non-null variant gets the suffix.  When there is no ``Type1`` or higher,
the suffix is noise.

This hook renames files, classes, and all references across the generated
package so users see clean names (e.g. ``Changeset`` instead of
``ChangesetType0``).
"""

from __future__ import annotations

from pathlib import Path


def _class_name_from_filename(filename: str) -> str:
    """Convert snake_case filename (without .py) to PascalCase class name."""
    return "".join(part.capitalize() for part in filename.split("_"))


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    models_dir = package_dir / "models"

    if not models_dir.exists():
        print("Warning: models/ not found, skipping Type0 rename")
        return

    # Discover Type0 files and build rename map
    renames: list[
        tuple[str, str, str, str]
    ] = []  # (old_file_stem, new_file_stem, old_class, new_class)

    for py_file in sorted(models_dir.glob("*_type_0.py")):
        old_stem = py_file.stem  # e.g. "changeset_type_0"
        new_stem = old_stem.removesuffix("_type_0")  # e.g. "changeset"

        old_class = _class_name_from_filename(old_stem)  # e.g. "ChangesetType0"
        new_class = _class_name_from_filename(new_stem)  # e.g. "Changeset"

        # Fail if the target file already exists (collision)
        if (models_dir / f"{new_stem}.py").exists():
            raise RuntimeError(
                f"Cannot rename {old_stem}.py -> {new_stem}.py: target already exists. "
                f"A new upstream schema may have introduced a naming collision."
            )

        # Fail if there are Type1+ variants (multi-variant union)
        has_higher = any(models_dir.glob(f"{new_stem}_type_[1-9]*.py"))
        if has_higher:
            raise RuntimeError(
                f"Cannot strip Type0 suffix from {old_class}: higher variants "
                f"(Type1, Type2, ...) exist for {new_stem}. This is a multi-variant "
                f"union that needs manual handling."
            )

        renames.append((old_stem, new_stem, old_class, new_class))

    if not renames:
        print("No Type0 renames needed")
        return

    # Step 1: Rename files
    for old_stem, new_stem, _, _ in renames:
        old_path = models_dir / f"{old_stem}.py"
        new_path = models_dir / f"{new_stem}.py"
        old_path.rename(new_path)

    # Step 2: Text replacement across all .py files in the package
    all_py_files = sorted(package_dir.rglob("*.py"))

    for py_file in all_py_files:
        if "__pycache__" in py_file.parts:
            continue

        text = py_file.read_text(encoding="utf-8")
        original = text

        for old_stem, new_stem, old_class, new_class in renames:
            # Replace module references (imports like "from .changeset_type_0 import")
            text = text.replace(f".{old_stem}", f".{new_stem}")
            # Replace class name references
            text = text.replace(old_class, new_class)

        if text != original:
            py_file.write_text(text, encoding="utf-8")

    print(
        f"Renamed {len(renames)} Type0 models: {', '.join(nc for _, _, _, nc in renames)}"
    )
