"""Test backward-compatible deprecated type aliases (v9 → v10).

Class-scoped: iterates the entire rename map and verifies each old name:
  (a) imports from camunda_orchestration_sdk.models
  (b) imports from camunda_orchestration_sdk (top-level)
  (c) is the same class object as the new name
  (d) emits a DeprecationWarning at import time

Adding a future rename without a deprecation alias will fail this test.
"""

from __future__ import annotations

import importlib
import importlib.util
import warnings
from pathlib import Path
from typing import cast

import pytest

# Import the rename map (single source of truth) via importlib to avoid sys.path mutation.
_rename_map_path = Path(__file__).resolve().parents[2] / "hooks" / "post_gen" / "_rename_map.py"
_spec = importlib.util.spec_from_file_location("_rename_map", _rename_map_path)
assert _spec and _spec.loader
_rename_map = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rename_map)

RENAMES_V9_TO_V10: dict[str, str] = cast(
    dict[str, str], _rename_map.RENAMES_V9_TO_V10  # pyright: ignore[reportUnknownMemberType]
)


@pytest.fixture(params=sorted(RENAMES_V9_TO_V10.items()), ids=lambda x: x[0])
def rename_pair(request: pytest.FixtureRequest) -> tuple[str, str]:
    """Yields (old_name, new_name) for each rename entry."""
    return request.param  # type: ignore[return-value]


class TestDeprecatedAliasesFromModels:
    """Test imports from camunda_orchestration_sdk.models."""

    def test_old_name_importable(self, rename_pair: tuple[str, str]) -> None:
        old_name, _ = rename_pair
        models = importlib.import_module("camunda_orchestration_sdk.models")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            obj = getattr(models, old_name, None)
        assert obj is not None, (
            f"{old_name} is not importable from camunda_orchestration_sdk.models"
        )

    def test_old_name_is_new_class(self, rename_pair: tuple[str, str]) -> None:
        old_name, new_name = rename_pair
        models = importlib.import_module("camunda_orchestration_sdk.models")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            old_cls = getattr(models, old_name)
        new_cls = getattr(models, new_name)
        assert old_cls is new_cls, (
            f"{old_name} is not the same object as {new_name}"
        )

    def test_old_name_emits_deprecation_warning(
        self, rename_pair: tuple[str, str]
    ) -> None:
        old_name, new_name = rename_pair
        models = importlib.import_module("camunda_orchestration_sdk.models")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            getattr(models, old_name)

        deprecation_warnings = [
            w for w in caught if issubclass(w.category, DeprecationWarning)
        ]
        assert len(deprecation_warnings) >= 1, (
            f"No DeprecationWarning emitted when accessing {old_name}"
        )
        msg = str(deprecation_warnings[0].message)
        assert old_name in msg
        assert new_name in msg


class TestDeprecatedAliasesFromTopLevel:
    """Test imports from camunda_orchestration_sdk (top-level package)."""

    def test_old_name_importable(self, rename_pair: tuple[str, str]) -> None:
        old_name, _ = rename_pair
        pkg = importlib.import_module("camunda_orchestration_sdk")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            obj = getattr(pkg, old_name, None)
        assert obj is not None, (
            f"{old_name} is not importable from camunda_orchestration_sdk"
        )

    def test_old_name_is_new_class(self, rename_pair: tuple[str, str]) -> None:
        old_name, new_name = rename_pair
        pkg = importlib.import_module("camunda_orchestration_sdk")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            old_cls = getattr(pkg, old_name)
        new_cls = getattr(pkg, new_name)
        assert old_cls is new_cls, (
            f"{old_name} is not the same object as {new_name} at top level"
        )

    def test_old_name_emits_deprecation_warning(
        self, rename_pair: tuple[str, str]
    ) -> None:
        old_name, new_name = rename_pair
        pkg = importlib.import_module("camunda_orchestration_sdk")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            getattr(pkg, old_name)

        deprecation_warnings = [
            w for w in caught if issubclass(w.category, DeprecationWarning)
        ]
        assert len(deprecation_warnings) >= 1, (
            f"No DeprecationWarning emitted when accessing {old_name} from top-level"
        )
        msg = str(deprecation_warnings[0].message)
        assert old_name in msg
        assert new_name in msg


class TestRenameMapCompleteness:
    """Guard: ensure the rename map isn't accidentally shrunk."""

    def test_minimum_rename_count(self) -> None:
        assert len(RENAMES_V9_TO_V10) >= 26, (
            f"Expected at least 26 renames, got {len(RENAMES_V9_TO_V10)}"
        )
