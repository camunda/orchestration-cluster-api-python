"""Test backward-compatible deprecated type aliases.

Class-scoped: iterates the entire rename map (v9 → v10 plus the 10.0 → 10.1
backport renames) and verifies each old name:
  (a) imports from camunda_orchestration_sdk.models
  (b) imports from camunda_orchestration_sdk (top-level)
  (c) is the same class object as the new name
  (d) emits a DeprecationWarning on access

Adding a future rename without a deprecation alias will fail this test.
"""

from __future__ import annotations

import importlib
import importlib.util
import re
import sys
import warnings
from pathlib import Path
from typing import cast

import pytest

# Import the rename map (single source of truth) via importlib to avoid sys.path mutation.
_alias_map_path = Path(__file__).resolve().parents[2] / "hooks" / "post_gen" / "_api_compat_alias_map.py"
_spec = importlib.util.spec_from_file_location("_api_compat_alias_map", _alias_map_path)
assert _spec and _spec.loader
_alias_map = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_alias_map)

RENAMES_V9_TO_V10: dict[str, str] = cast(
    dict[str, str], _alias_map.RENAMES_V9_TO_V10  # pyright: ignore[reportUnknownMemberType]
)

RENAMES_V10_0_TO_V10_1: dict[str, str] = cast(
    dict[str, str], _alias_map.RENAMES_V10_0_TO_V10_1  # pyright: ignore[reportUnknownMemberType]
)

ALL_RENAMES: dict[str, str] = cast(
    dict[str, str], _alias_map.ALL_RENAMES  # pyright: ignore[reportUnknownMemberType]
)


@pytest.fixture(params=sorted(ALL_RENAMES.items()), ids=lambda x: x[0])
def rename_pair(request: pytest.FixtureRequest) -> tuple[str, str]:
    """Yields (old_name, new_name) for each rename entry."""
    return request.param  # type: ignore[return-value]


@pytest.fixture(params=sorted(RENAMES_V10_0_TO_V10_1.items()), ids=lambda x: x[0])
def rename_pair_v10(request: pytest.FixtureRequest) -> tuple[str, str]:
    """Yields (old_name, new_name) for each within-minor (10.0 -> 10.1) rename."""
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
            old_cls = models.SearchUsersResponse200
        new_cls = models.UserSearchResult
        assert old_cls is new_cls
        assert issubclass(new_cls, old_cls)  # type: ignore[arg-type]

    def test_issubclass_with_v9_name(self) -> None:
        """v9 code: `issubclass(MyResult, GetUserResponse200)` must work."""
        models = importlib.import_module("camunda_orchestration_sdk.models")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            old_cls = models.GetUserResponse200
        new_cls = models.UserResult
        assert issubclass(old_cls, new_cls)  # type: ignore[arg-type]
        assert issubclass(new_cls, old_cls)  # type: ignore[arg-type]

    def test_v9_name_in_all(self) -> None:
        """Deprecated names must be in __all__ so `from models import *` works."""
        models = importlib.import_module("camunda_orchestration_sdk.models")
        all_names = getattr(models, "__all__", [])
        missing = [
            old for old in ALL_RENAMES if old not in all_names
        ]
        assert not missing, f"deprecated names missing from __all__: {missing}"

    def test_unknown_name_still_raises(self) -> None:
        """__getattr__ must not swallow errors for genuinely missing names."""
        models = importlib.import_module("camunda_orchestration_sdk.models")
        with pytest.raises(AttributeError, match="TotallyBogusName"):
            _ = models.TotallyBogusName


class TestProcessCreationVariablesAliases:
    """Regression guard for the 10.0 → 10.1 process-creation Variables rename.

    The upstream stable/8.10 backport folded the shared process-creation fields
    into ProcessInstanceCreationInstructionBase, so the generator stopped emitting
    the per-reference *Variables classes. v10.0.0 exported both old names publicly,
    so they must survive as deprecated aliases for the 10.x line.
    """

    OLD_NAMES = (
        "ProcessInstanceCreationInstructionByKeyVariables",
        "ProcessInstanceCreationInstructionByIdVariables",
    )
    NEW_NAME = "ProcessInstanceCreationInstructionBaseVariables"

    def test_map_contains_both_renames(self) -> None:
        for old in self.OLD_NAMES:
            assert RENAMES_V10_0_TO_V10_1.get(old) == self.NEW_NAME

    @pytest.mark.parametrize("old_name", OLD_NAMES)
    def test_old_name_is_base_variables_from_models(self, old_name: str) -> None:
        models = importlib.import_module("camunda_orchestration_sdk.models")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            old_cls = getattr(models, old_name)
        new_cls = getattr(models, self.NEW_NAME)
        assert old_cls is new_cls
        deprecation_warnings = [
            w for w in caught if issubclass(w.category, DeprecationWarning)
        ]
        assert len(deprecation_warnings) >= 1, (
            f"No DeprecationWarning emitted when accessing {old_name}"
        )
        assert old_name in str(deprecation_warnings[0].message)

    @pytest.mark.parametrize("old_name", OLD_NAMES)
    def test_old_name_is_base_variables_from_top_level(self, old_name: str) -> None:
        pkg = importlib.import_module("camunda_orchestration_sdk")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            old_cls = getattr(pkg, old_name)
        new_cls = getattr(pkg, self.NEW_NAME)
        assert old_cls is new_cls
        deprecation_warnings = [
            w for w in caught if issubclass(w.category, DeprecationWarning)
        ]
        assert len(deprecation_warnings) >= 1, (
            f"No DeprecationWarning emitted when accessing {old_name} from top-level"
        )
        assert old_name in str(deprecation_warnings[0].message)


def _snake_case(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


class TestWithinMinorRenameCompatModules:
    """Class-scoped guard for within-minor (10.0 -> 10.1) module-path removals.

    When an upstream backport drops a per-class ``*Variables`` module within the
    10.x line, v10.0.0 callers that imported the old *module path* directly
    (``from camunda_orchestration_sdk.models.<old_module> import <OldName>``) must
    keep working, not only package-attribute access. This iterates every
    10.0 -> 10.1 rename, so a future within-minor removal without a compat module
    fails here rather than silently breaking a direct import.
    """

    def test_direct_module_import_resolves_to_new_class(
        self, rename_pair_v10: tuple[str, str]
    ) -> None:
        old_name, new_name = rename_pair_v10
        old_module = f"camunda_orchestration_sdk.models.{_snake_case(old_name)}"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            mod = importlib.import_module(old_module)
            old_cls = getattr(mod, old_name)
        new_cls = getattr(
            importlib.import_module("camunda_orchestration_sdk.models"), new_name
        )
        assert old_cls is new_cls, (
            f"{old_module}.{old_name} is not the same object as {new_name}"
        )

    def test_direct_module_import_emits_deprecation_warning(
        self, rename_pair_v10: tuple[str, str]
    ) -> None:
        old_name, _ = rename_pair_v10
        old_module = f"camunda_orchestration_sdk.models.{_snake_case(old_name)}"
        # Force a fresh import so the module-level warning fires.
        sys.modules.pop(old_module, None)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.import_module(old_module)
        deprecation_warnings = [
            w for w in caught if issubclass(w.category, DeprecationWarning)
        ]
        assert len(deprecation_warnings) >= 1, (
            f"No DeprecationWarning emitted when importing {old_module}"
        )

    def test_old_module_path_not_in_new_module(
        self, rename_pair_v10: tuple[str, str]
    ) -> None:
        """The shim must live at the old path, distinct from the surviving module."""
        old_name, new_name = rename_pair_v10
        assert _snake_case(old_name) != _snake_case(new_name)


class TestRenameMapCompleteness:
    """Guard: ensure the rename maps aren't accidentally shrunk."""

    def test_minimum_rename_count(self) -> None:
        assert len(RENAMES_V9_TO_V10) >= 26, (
            f"Expected at least 26 renames, got {len(RENAMES_V9_TO_V10)}"
        )

    def test_v10_0_to_v10_1_renames_present(self) -> None:
        assert len(RENAMES_V10_0_TO_V10_1) >= 2, (
            f"Expected at least 2 10.0→10.1 renames, got {len(RENAMES_V10_0_TO_V10_1)}"
        )

    def test_all_renames_is_merged_view(self) -> None:
        assert ALL_RENAMES == {**RENAMES_V9_TO_V10, **RENAMES_V10_0_TO_V10_1}
