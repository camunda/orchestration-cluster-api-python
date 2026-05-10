"""Test backward-compatible deprecated type aliases (v9 → v10).

Class-scoped: iterates the entire rename map and verifies each old name:
  (a) imports from camunda_orchestration_sdk.models
  (b) imports from camunda_orchestration_sdk (top-level)
  (c) is the same class object as the new name
  (d) emits a DeprecationWarning on access

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


class TestV9UsagePatterns:
    """Regression guard: real v9 usage patterns must keep working.

    These tests simulate code written against stable/9 that uses old type names
    in isinstance checks, dict round-trips, and attribute access. They would all
    fail with AttributeError on main (pre-PR) and must stay green going forward.
    """

    def test_isinstance_with_v9_name(self) -> None:
        """v9 code: `isinstance(result, SearchUsersResponse200)` must work.

        Since __getattr__ returns the exact same class object, identity (is)
        guarantees isinstance/issubclass equivalence. We assert both identity
        and issubclass to make the contract explicit.
        """
        models = importlib.import_module("camunda_orchestration_sdk.models")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            old_cls = getattr(models, "SearchUsersResponse200")
        new_cls = getattr(models, "UserSearchResult")
        assert old_cls is new_cls
        assert issubclass(new_cls, old_cls)  # type: ignore[arg-type]

    def test_issubclass_with_v9_name(self) -> None:
        """v9 code: `issubclass(MyResult, GetUserResponse200)` must work."""
        models = importlib.import_module("camunda_orchestration_sdk.models")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            old_cls = getattr(models, "GetUserResponse200")
        new_cls = getattr(models, "UserResult")
        assert issubclass(old_cls, new_cls)  # type: ignore[arg-type]
        assert issubclass(new_cls, old_cls)  # type: ignore[arg-type]

    def test_v9_name_in_all(self) -> None:
        """v9 names must be in __all__ so `from models import *` works."""
        models = importlib.import_module("camunda_orchestration_sdk.models")
        all_names = getattr(models, "__all__", [])
        missing = [
            old for old in RENAMES_V9_TO_V10 if old not in all_names
        ]
        assert not missing, f"v9 names missing from __all__: {missing}"

    def test_unknown_name_still_raises(self) -> None:
        """__getattr__ must not swallow errors for genuinely missing names."""
        models = importlib.import_module("camunda_orchestration_sdk.models")
        with pytest.raises(AttributeError, match="TotallyBogusName"):
            getattr(models, "TotallyBogusName")


class TestRenameMapCompleteness:
    """Guard: ensure the rename map isn't accidentally shrunk."""

    def test_minimum_rename_count(self) -> None:
        assert len(RENAMES_V9_TO_V10) >= 26, (
            f"Expected at least 26 renames, got {len(RENAMES_V9_TO_V10)}"
        )
