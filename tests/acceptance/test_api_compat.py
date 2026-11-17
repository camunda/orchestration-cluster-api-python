"""Tests for the stable-branch API compatibility checker (``scripts/api_compat.py``).

Every case starts from one baseline package shaped like the generated SDK (attrs models
with ``Unset``, an enum, a client class, module-level functions). A break case applies a
single textual mutation to it and must be reported; a compatible case must not be. The
baseline compared with itself is asserted green first, so a break case can only fail
because of its mutation.
"""

import importlib.util
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any

import pytest

pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="stdlib overload signatures are only introspectable on Python 3.11+",
)

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "api_compat.py"
_spec = importlib.util.spec_from_file_location("api_compat", _SCRIPT)
assert _spec and _spec.loader
api_compat = importlib.util.module_from_spec(_spec)
sys.modules["api_compat"] = api_compat
_spec.loader.exec_module(api_compat)

PKG = "acfix"

BASELINE: dict[str, str] = {
    "__init__.py": """
        from .client import Client
        from .models import Color, RequestModel, ResultModel
    """,
    "types.py": """
        class Unset:
            def __bool__(self) -> bool:
                return False

        UNSET: Unset = Unset()
    """,
    "models/__init__.py": """
        from .color import Color
        from .request_model import RequestModel
        from .result_model import ResultModel

        __all__ = ("Color", "RequestModel", "ResultModel")
    """,
    "models/color.py": """
        from enum import Enum

        class Color(str, Enum):
            RED = "red"
            BLUE = "blue"
    """,
    "models/page.py": """
        # No `from __future__ import annotations`: 3.14 then adds __annotate_func__.
        class Page:
            total: int
    """,
    "models/payload.py": """
        from __future__ import annotations

        from typing import TypedDict

        try:
            from typing import NotRequired
        except ImportError:
            from typing_extensions import NotRequired

        class Payload(TypedDict):
            required: str
            optional: NotRequired[str]
    """,
    "models/settings.py": """
        from __future__ import annotations

        import dataclasses

        @dataclasses.dataclass
        class Settings:
            name: str
            flag: bool = False

            @classmethod
            def from_dict(cls, data: dict[str, str]) -> Settings:
                return cls(name=data["name"])

            @staticmethod
            def default() -> Settings:
                return Settings(name="")
    """,
    "models/orphan.py": """
        from __future__ import annotations

        import attrs

        @attrs.define
        class Orphan:
            value: str
    """,
    "models/request_model.py": """
        from __future__ import annotations

        import attrs

        from ..types import UNSET, Unset

        @attrs.define
        class RequestModel:
            name: str
            limit: int | None = None
            color: Color | Unset = UNSET

            @classmethod
            def from_dict(cls, src_dict: dict[str, object]) -> RequestModel:
                return cls(name=str(src_dict["name"]))

        from .color import Color
    """,
    "models/result_model.py": """
        from __future__ import annotations

        from typing import TYPE_CHECKING

        import attrs

        from ..types import UNSET, Unset

        if TYPE_CHECKING:
            from .color import Color

        @attrs.define
        class ResultModel:
            name: str
            count: int
            color: Color
            tags: list[str] | Unset = UNSET
    """,
    "client.py": """
        from __future__ import annotations

        from collections.abc import Sequence
        from typing import Generic, TypeVar, overload

        from .models.request_model import RequestModel
        from .models.result_model import ResultModel
        from .models.page import Page
        from .models.payload import Payload
        from .models.settings import Settings

        T = TypeVar("T")
        B = TypeVar("B", bound=str | bytes)
        C = TypeVar("C", str, bytes, int)

        DEFAULT_LIMIT = 10

        class ApiError(Exception):
            def __init__(self, status_code: int, content: bytes) -> None:
                self.status_code = status_code
                self.content = content

        class Box(Generic[T]):
            def get(self) -> T:
                raise NotImplementedError

        class GenericBase(Generic[T]):
            value: T

        class IntBox(GenericBase[int]):
            pass

        class Limits:
            MAX = 10

        class OverloadedCtor:
            @overload
            def __init__(self, value: int) -> None: ...

            @overload
            def __init__(self, value: str) -> None: ...

            def __init__(self, value: int | str) -> None:
                pass

        def echo_bound(value: B) -> B:
            return value

        def echo_constraints(value: C) -> C:
            return value

        class Client:
            def int_box(self) -> IntBox:
                raise NotImplementedError

            def limits(self) -> Limits:
                raise NotImplementedError

            def submit(self, payload: Payload) -> None:
                pass

            def page(self) -> Page:
                raise NotImplementedError

            def settings(self) -> Settings:
                raise NotImplementedError

            def __enter__(self) -> Client:
                return self

            def __exit__(self, *args: object) -> None:
                pass

            async def __aenter__(self) -> Client:
                return self

            def __getitem__(self, key: str) -> ResultModel:
                raise NotImplementedError

            @overload
            def pick(self, x: int) -> int: ...

            @overload
            def pick(self, x: str) -> str: ...

            def pick(self, x: int | str) -> int | str:
                return x

            def put_all(self, items: list[str]) -> None:
                pass

            def put_seq(self, items: Sequence[str]) -> None:
                pass

            def names(self) -> list[str | None]:
                return []

            def opts(self, *args: str, **options: str) -> None:
                pass

            def deploy(
                self, files: str, tenant_id: str | None = None, region: str | None = None
            ) -> None:
                pass

            def get_thing(self, key: str, *, verbose: bool = False) -> ResultModel:
                raise NotImplementedError

            def create_thing(self, data: RequestModel) -> None:
                raise NotImplementedError

            def count(self, n: int) -> int:
                raise NotImplementedError

            def find(self, key: str) -> ResultModel | None:
                raise NotImplementedError

            async def aget(self, key: str) -> ResultModel:
                raise NotImplementedError

        def helper(x: str) -> str:
            return x
    """,
}

# (id, file, old text, new text, expected substring of one reported break)
BREAKS: list[tuple[str, str, str | None, str | None, str]] = [
    (
        "module-removed",
        "models/orphan.py",
        None,
        None,
        "acfix.models.orphan: module removed",
    ),
    (
        "class-removed",
        "models/orphan.py",
        "class Orphan:",
        "class Orphan2:",
        "acfix.models.orphan:Orphan: class removed",
    ),
    (
        "re-export-removed",
        "models/__init__.py",
        '"RequestModel", "ResultModel")',
        '"RequestModel")',
        "acfix.models:ResultModel: class removed",
    ),
    (
        "function-removed",
        "client.py",
        "def helper(x: str) -> str:",
        "def helper2(x: str) -> str:",
        "acfix.client:helper: function removed",
    ),
    (
        "method-removed",
        "client.py",
        "def count(self, n: int)",
        "def total(self, n: int)",
        "acfix.client:Client.count: method removed",
    ),
    (
        "result-attribute-removed",
        "models/result_model.py",
        "    count: int\n",
        "",
        "ResultModel.count: attribute removed",
    ),
    (
        "enum-member-removed",
        "models/color.py",
        '    BLUE = "blue"\n',
        "",
        "Color.BLUE: enum member removed",
    ),
    (
        "enum-value-changed",
        "models/color.py",
        'BLUE = "blue"',
        'BLUE = "navy"',
        "Color.BLUE: enum value changed",
    ),
    (
        "new-required-param",
        "client.py",
        "def get_thing(self, key: str, *,",
        "def get_thing(self, key: str, scope: str, *,",
        "Client.get_thing: new required parameter 'scope'",
    ),
    (
        "optional-param-now-required",
        "client.py",
        "verbose: bool = False",
        "verbose: bool",
        "Client.get_thing: parameter 'verbose' is now required",
    ),
    (
        "param-removed",
        "client.py",
        "def get_thing(self, key: str, *, verbose: bool = False)",
        "def get_thing(self, key: str)",
        "Client.get_thing: parameter 'verbose' removed",
    ),
    (
        "param-renamed",
        "client.py",
        "def count(self, n: int)",
        "def count(self, m: int)",
        "Client.count: parameter 'n' removed",
    ),
    (
        "param-narrowed",
        "client.py",
        "def count(self, n: int)",
        "def count(self, n: bool)",
        "Client.count: parameter 'n' no longer accepts int",
    ),
    (
        "return-widened-to-optional",
        "client.py",
        "def count(self, n: int) -> int:",
        "def count(self, n: int) -> int | None:",
        "Client.count: return type widened from int to int | None",
    ),
    (
        "return-type-changed",
        "client.py",
        "def helper(x: str) -> str:",
        "def helper(x: str) -> bytes:",
        "acfix.client:helper: return type widened from str to bytes",
    ),
    (
        "result-field-optional",
        "models/result_model.py",
        "    name: str\n",
        "    name: str | None\n",
        "ResultModel.name: type widened from str to str | None",
    ),
    (
        "result-field-unset",
        "models/result_model.py",
        "    count: int\n    color: Color\n",
        "    color: Color\n    count: int | Unset = UNSET\n",
        "ResultModel.count: type widened from int to int | Unset",
    ),
    (
        "result-nested-field-optional",
        "models/result_model.py",
        "tags: list[str] | Unset",
        "tags: list[str | None] | Unset",
        "ResultModel.tags: type widened",
    ),
    (
        "request-new-required-field",
        "models/request_model.py",
        "    name: str\n",
        "    name: str\n    extra: str\n",
        "RequestModel(): new required parameter 'extra'",
    ),
    (
        "request-field-narrowed",
        "models/request_model.py",
        "limit: int | None = None",
        "limit: int = 0",
        "RequestModel(): parameter 'limit' no longer accepts int | None",
    ),
    (
        "sync-to-async",
        "client.py",
        "    def find(self",
        "    async def find(self",
        "Client.find: changed between sync and async",
    ),
    (
        "output-defaulted-dataclass-field-widened",
        "models/settings.py",
        "flag: bool = False",
        "flag: bool | None = None",
        "Settings.flag: type widened from bool to bool | None",
    ),
    (
        "classmethod-to-instance-method",
        "models/settings.py",
        "    @classmethod\n    def from_dict(cls,",
        "    def from_dict(self,",
        "Settings.from_dict: changed from class method to instance method",
    ),
    (
        "generated-from-dict-removed",
        "models/request_model.py",
        "    @classmethod\n    def from_dict(cls, src_dict: dict[str, object]) -> RequestModel:\n"
        "        return cls(name=str(src_dict[\"name\"]))\n",
        "",
        "RequestModel.from_dict: method removed",
    ),
    (
        "staticmethod-to-instance-method",
        "models/settings.py",
        "    @staticmethod\n    def default() -> Settings:",
        "    def default(self) -> Settings:",
        "Settings.default: changed from static method to instance method",
    ),
    (
        "init-attribute-removed",
        "client.py",
        "        self.content = content\n",
        "",
        "ApiError.content: attribute removed",
    ),
    (
        "init-attribute-widened",
        "client.py",
        "self.status_code = status_code",
        "self.status_code: int | None = status_code",
        "ApiError.status_code: type widened from int to int | None",
    ),
    (
        "typevar-return-made-concrete",
        "client.py",
        "def get(self) -> T:",
        "def get(self) -> str:",
        "Box.get: return type widened from T to str",
    ),
    (
        "module-value-widened",
        "types.py",
        "UNSET: Unset = Unset()",
        "UNSET: Unset | None = Unset()",
        "acfix.types:UNSET: type widened from Unset to Unset | None",
    ),
    (
        "class-value-widened",
        "client.py",
        "MAX = 10",
        "MAX = None",
        "Limits.MAX: type widened from int to None",
    ),
    (
        "constructor-overload-removed",
        "client.py",
        "    @overload\n    def __init__(self, value: str) -> None: ...\n\n",
        "",
        "OverloadedCtor(): no longer supports the signature (value: str) -> None",
    ),
    (
        "inherited-generic-field-specialization-changed",
        "client.py",
        "class IntBox(GenericBase[int]):",
        "class IntBox(GenericBase[str]):",
        "IntBox.value: type widened from int to str",
    ),
    (
        "unannotated-module-value-changed",
        "client.py",
        "DEFAULT_LIMIT = 10",
        "DEFAULT_LIMIT = None",
        "acfix.client:DEFAULT_LIMIT: type widened from int to None",
    ),
    (
        "field-to-wider-property",
        "models/page.py",
        "class Page:\n    total: int\n",
        "class Page:\n    @property\n    def total(self) -> int | None:\n        return 0\n",
        "Page.total: type widened from int to int | None",
    ),
    (
        "field-to-method",
        "models/page.py",
        "class Page:\n    total: int\n",
        "class Page:\n    def total(self) -> int:\n        return 0\n",
        "Page.total: changed from attribute to method",
    ),
    (
        "new-keyword-param-captures-kwargs",
        "client.py",
        "def opts(self, *args: str, **options: str)",
        "def opts(self, *args: str, label: int = 0, **options: str)",
        "Client.opts: new parameter 'label' no longer accepts str passed through **options",
    ),
    (
        "new-positional-param-captures-args",
        "client.py",
        "def opts(self, *args: str, **options: str)",
        "def opts(self, first: int = 0, *args: str, **options: str)",
        "Client.opts: new parameter 'first' no longer accepts str passed through *args",
    ),
    (
        "new-parameter-binds-both-variadic-channels",
        "client.py",
        "def opts(self, *args: str, **options: str)",
        'def opts(self, first: str = "", *args: str, **options: str)',
        "Client.opts: new parameter 'first' can bind both positional and keyword arguments",
    ),
    (
        "typevar-bound-narrowed",
        "client.py",
        'B = TypeVar("B", bound=str | bytes)',
        'B = TypeVar("B", bound=str)',
        "acfix.client:echo_bound: parameter 'value' no longer accepts B",
    ),
    (
        "typevar-constraints-narrowed",
        "client.py",
        'C = TypeVar("C", str, bytes, int)',
        'C = TypeVar("C", str, bytes)',
        "acfix.client:echo_constraints: parameter 'value' no longer accepts C",
    ),
    (
        "typed-dict-notrequired-becomes-required",
        "models/payload.py",
        "optional: NotRequired[str]",
        "optional: str",
        "Payload['optional']: key is now required",
    ),
    (
        "special-method-removed",
        "client.py",
        "    def __getitem__(self, key: str)",
        "    def get_item(self, key: str)",
        "Client.__getitem__: method removed",
    ),
    (
        "async-special-method-removed",
        "client.py",
        "    async def __aenter__(self)",
        "    async def aenter(self)",
        "Client.__aenter__: method removed",
    ),
    (
        "overload-removed",
        "client.py",
        "    @overload\n    def pick(self, x: str) -> str: ...\n",
        "",
        "Client.pick: no longer supports the signature (x: str) -> str",
    ),
    (
        "overload-return-widened",
        "client.py",
        "def pick(self, x: int) -> int: ...",
        "def pick(self, x: int) -> int | None: ...",
        "Client.pick: no longer supports the signature (x: int) -> int",
    ),
    (
        "invariant-input-arg-widened",
        "client.py",
        "items: list[str]",
        "items: list[str | None]",
        "Client.put_all: parameter 'items' no longer accepts list[str]",
    ),
    (
        "invariant-output-arg-narrowed",
        "client.py",
        "def names(self) -> list[str | None]:",
        "def names(self) -> list[str]:",
        "Client.names: return type widened from list[str | None] to list[str]",
    ),
    (
        "var-positional-narrowed",
        "client.py",
        "*args: str",
        "*args: int",
        "Client.opts: parameter '*args' no longer accepts str",
    ),
    (
        "var-keyword-narrowed",
        "client.py",
        "**options: str",
        "**options: int",
        "Client.opts: parameter '**options' no longer accepts str",
    ),
    (
        "optional-param-keyword-only",
        "client.py",
        "files: str, tenant_id",
        "files: str, *, tenant_id",
        "Client.deploy: parameter 'tenant_id' can no longer be passed positionally",
    ),
    (
        "optional-params-reordered",
        "client.py",
        "tenant_id: str | None = None, region: str | None = None",
        "region: str | None = None, tenant_id: str | None = None",
        "Client.deploy: parameter 'tenant_id' moved from position 1 to 2",
    ),
]

COMPATIBLE: list[tuple[str, str, str, str]] = [
    (
        "new-function",
        "client.py",
        "def helper(x: str) -> str:",
        "def other() -> None:\n    pass\n\ndef helper(x: str) -> str:",
    ),
    (
        "new-optional-param",
        "client.py",
        "verbose: bool = False)",
        "verbose: bool = False, page: int = 1)",
    ),
    (
        "param-widened",
        "client.py",
        "def count(self, n: int)",
        "def count(self, n: int | str)",
    ),
    (
        "return-narrowed",
        "client.py",
        "-> ResultModel | None:",
        "-> ResultModel:",
    ),
    (
        "request-new-optional-field",
        "models/request_model.py",
        "    color: Color | Unset = UNSET\n",
        "    color: Color | Unset = UNSET\n    offset: int | Unset = UNSET\n",
    ),
    (
        "request-field-becomes-optional",
        "models/request_model.py",
        "    name: str\n",
        "    name: str | None = None\n",
    ),
    (
        "request-field-widened",
        "models/request_model.py",
        "limit: int | None = None",
        "limit: int | str | None = None",
    ),
    (
        "result-new-required-field",
        "models/result_model.py",
        "    color: Color\n",
        "    color: Color\n    extra: str\n",
    ),
    (
        "result-field-narrowed",
        "models/result_model.py",
        "tags: list[str] | Unset = UNSET",
        "tags: list[str] = attrs.field(factory=list)",
    ),
    (
        "new-enum-member",
        "models/color.py",
        '    BLUE = "blue"\n',
        '    BLUE = "blue"\n    GREEN = "green"\n',
    ),
    (
        # A model nothing accepts or returns only has to keep existing.
        "orphan-field-changed",
        "models/orphan.py",
        "value: str",
        "value: str | None = None",
    ),
    (
        "covariant-input-arg-widened",
        "client.py",
        "items: Sequence[str]",
        "items: Sequence[str | None]",
    ),
    (
        "new-overload",
        "client.py",
        "    def pick(self, x: int | str) -> int | str:",
        "    @overload\n    def pick(self, x: bytes) -> bytes: ...\n\n"
        "    def pick(self, x: int | str | bytes) -> int | str | bytes:",
    ),
    (
        "new-keyword-param-matching-kwargs",
        "client.py",
        "def opts(self, *args: str, **options: str)",
        'def opts(self, *args: str, label: str = "", **options: str)',
    ),
    (
        "init-attribute-added",
        "client.py",
        "        self.content = content\n",
        "        self.content = content\n        self.retryable = False\n",
    ),
    (
        "field-to-property-same-type",
        "models/page.py",
        "class Page:\n    total: int\n",
        "class Page:\n    @property\n    def total(self) -> int:\n        return 0\n",
    ),
    (
        "staticmethod-to-classmethod",
        "models/settings.py",
        "    @staticmethod\n    def default() -> Settings:\n        return Settings(name=\"\")",
        "    @classmethod\n    def default(cls) -> Settings:\n        return cls(name=\"\")",
    ),
    (
        "output-dataclass-field-gains-default",
        "models/settings.py",
        "    name: str\n",
        "    name: str = \"\"\n",
    ),
    (
        "new-special-method",
        "client.py",
        "    def __getitem__(self, key: str)",
        "    def __len__(self) -> int:\n        return 0\n\n    def __getitem__(self, key: str)",
    ),
]


def _write(root: Path, files: dict[str, str]) -> Path:
    for rel, body in files.items():
        path = root / PKG / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(body).lstrip(), encoding="utf-8")
    return root


def _mutate(file: str, old: str | None, new: str | None) -> dict[str, str]:
    files = {k: textwrap.dedent(v).lstrip() for k, v in BASELINE.items()}
    if old is None:
        del files[file]
        return files
    assert files[file].count(old) == 1, f"mutation anchor {old!r} not unique in {file}"
    files[file] = files[file].replace(old, new or "")
    return files


def _describe(root: Path) -> Any:
    return api_compat.describe_in_subprocess(root, PKG)


@pytest.fixture(scope="module")
def baseline(tmp_path_factory: pytest.TempPathFactory) -> Any:
    return _describe(_write(tmp_path_factory.mktemp("baseline"), BASELINE))


def test_baseline_is_compatible_with_itself(baseline: Any, tmp_path: Path) -> None:
    assert api_compat.find_breaks(baseline, _describe(_write(tmp_path, BASELINE))) == []


def test_baseline_classifies_model_directions(baseline: Any) -> None:
    checker = api_compat.Checker(baseline, baseline)
    checker.run()
    assert checker.model_directions(f"{PKG}.models.result_model:ResultModel") == {
        api_compat.OUTPUT
    }
    assert checker.model_directions(f"{PKG}.models.request_model:RequestModel") == {
        api_compat.INPUT
    }
    assert checker.model_directions(f"{PKG}.models.orphan:Orphan") == set()


@pytest.mark.parametrize(
    ("file", "old", "new", "expected"),
    [case[1:] for case in BREAKS],
    ids=[case[0] for case in BREAKS],
)
def test_reports_break(
    baseline: Any,
    tmp_path: Path,
    file: str,
    old: str | None,
    new: str | None,
    expected: str,
) -> None:
    current = _describe(_write(tmp_path, _mutate(file, old, new)))
    breaks = api_compat.find_breaks(baseline, current)
    assert any(expected in b for b in breaks), breaks


@pytest.mark.parametrize(
    ("file", "old", "new"),
    [case[1:] for case in COMPATIBLE],
    ids=[case[0] for case in COMPATIBLE],
)
def test_accepts_compatible_change(
    baseline: Any, tmp_path: Path, file: str, old: str, new: str
) -> None:
    current = _describe(_write(tmp_path, _mutate(file, old, new)))
    assert api_compat.find_breaks(baseline, current) == []


# ---- CLI exit codes ------------------------------------------------------------------


def test_cli_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    base = _write(tmp_path / "base", BASELINE)
    same = _write(tmp_path / "same", BASELINE)
    broken = _write(tmp_path / "broken", _mutate("client.py", "n: int) -> int:", "n: int) -> str:"))
    args = ["--package", PKG, "--baseline-dir", str(base), "--current"]

    assert api_compat.main([*args, str(same)]) == 0
    assert api_compat.main([*args, str(broken)]) == 1
    assert "Client.count: return type widened from int to str" in capsys.readouterr().out
    assert api_compat.main([*args, str(tmp_path / "missing")]) == 2


def test_cli_passes_with_notice_when_no_release_of_the_major(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        api_compat, "fetch_pypi_metadata", lambda: {"releases": {"11.0.0rc1": [{}]}}
    )
    assert api_compat.main(["--baseline-major", "11"]) == 0
    assert "::notice::" in capsys.readouterr().out
    assert api_compat.main(["--print-baseline-major", "11"]) == 0
    assert capsys.readouterr().out == "\n"


# ---- baseline resolution -------------------------------------------------------------


def _metadata(*versions: str, yanked: tuple[str, ...] = ()) -> Any:
    return {
        "releases": {
            v: [{"filename": f"x-{v}.whl", "yanked": v in yanked}] for v in versions
        }
    }


def test_latest_release_compares_numerically_and_skips_prereleases() -> None:
    meta = _metadata(
        "10.1.9", "10.1.10", "10.2.0.dev3", "10.2.0rc1", "11.0.0", "9.9.9", "10.0.0"
    )
    assert api_compat.latest_release(meta, 10) == "10.1.10"
    assert api_compat.latest_release(meta, 9) == "9.9.9"
    assert api_compat.latest_release(meta, 12) is None


def test_latest_release_skips_yanked_and_empty_releases() -> None:
    meta = _metadata("10.1.4", "10.1.5", yanked=("10.1.5",))
    meta["releases"]["10.1.6"] = []
    assert api_compat.latest_release(meta, 10) == "10.1.4"


def test_print_baseline_major(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        api_compat, "fetch_pypi_metadata", lambda: _metadata("10.1.9", "10.1.10")
    )
    assert api_compat.main(["--print-baseline-major", "10"]) == 0
    assert capsys.readouterr().out.strip() == "10.1.10"


def test_describe_output_is_json_serialisable(baseline: Any) -> None:
    assert json.loads(json.dumps(baseline)) == baseline


# ---- release gate scripts (uv, git, gh and sleep stubbed on PATH) --------------------

_SCRIPTS = _SCRIPT.parent

_STUBS = {
    "uv": """
        case "$*" in
          *--print-baseline-major*) echo 10.1.5 ;;
          *--baseline-version*) exit "${FAKE_COMPAT_RC:-1}" ;;
          *"semantic-release version --print"*) echo 10.2.0 ;;
          *"semantic-release version"*)
            n=$(( $(cat "$FAKE_STATE/releases" 2>/dev/null || echo 0) + 1 ))
            echo "$n" > "$FAKE_STATE/releases"
            if [ "$n" -eq 1 ]; then echo "Upstream branch has changed"; exit 1; fi ;;
        esac
    """,
    "git": """
        case "$1 $2" in
          "rev-parse --show-toplevel") echo "$FAKE_STATE" ;;
          "rev-parse HEAD"|"rev-parse --short") echo abc123 ;;
          "log --format=%H") [ -z "${FAKE_GIT_LOG_FAIL:-}" ] || exit 128; echo abc123 ;;
          "log -1") echo "fix: something" ;;
          "merge-base "*) exit 1 ;;
        esac
    """,
    "gh": 'printf "%s\\n" "${FAKE_APPROVED_PRS:-}"',
    "sleep": "exit 0",
}


def _run_script(tmp_path: Path, script: str, **env: str) -> tuple[int, str]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    for name, body in _STUBS.items():
        stub = bin_dir / name
        stub.write_text("#!/usr/bin/env bash\n" + textwrap.dedent(body), encoding="utf-8")
        stub.chmod(0o755)
    full_env = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "FAKE_STATE": str(tmp_path),
        "RUNNER_TEMP": str(tmp_path),
        "GITHUB_REF_NAME": "stable/10",
        "GITHUB_REPOSITORY": "camunda/example",
        **env,
    }
    proc = subprocess.run(
        ["bash", str(_SCRIPTS / script), "stable/10"],
        cwd=tmp_path,
        env=full_env,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _releases(tmp_path: Path) -> int:
    return int((tmp_path / "releases").read_text())


@pytest.mark.parametrize(("compat_rc", "expected_rc", "releases"), [(1, 1, 1), (0, 0, 2)])
def test_release_retry_regates_the_new_branch_tip(
    tmp_path: Path, compat_rc: int, expected_rc: int, releases: int
) -> None:
    # The first attempt loses a race; the retry must not release unchecked code.
    rc, out = _run_script(
        tmp_path, "semantic-release-with-retry.sh", FAKE_COMPAT_RC=str(compat_rc)
    )
    assert (rc, _releases(tmp_path)) == (expected_rc, releases), out


@pytest.mark.parametrize(("git_log_fail", "expected_rc"), [("", 1), ("1", 2)])
def test_gate_is_a_setup_error_when_commits_cannot_be_listed(
    tmp_path: Path, git_log_fail: str, expected_rc: int
) -> None:
    rc, out = _run_script(tmp_path, "api-compat-gate.sh", FAKE_GIT_LOG_FAIL=git_log_fail)
    assert rc == expected_rc, out


@pytest.mark.parametrize("compat_rc", [0, 1, 2])
@pytest.mark.parametrize("approval", ["none", "dispatch", "label"])
def test_gate_approval_only_waives_breaks(
    tmp_path: Path, compat_rc: int, approval: str
) -> None:
    rc, out = _run_script(
        tmp_path,
        "api-compat-gate.sh",
        FAKE_COMPAT_RC=str(compat_rc),
        DISPATCH_APPROVED="true" if approval == "dispatch" else "false",
        FAKE_APPROVED_PRS="#123" if approval == "label" else "",
    )
    expected_rc = 0 if compat_rc == 1 and approval != "none" else compat_rc
    assert rc == expected_rc, out


@pytest.mark.parametrize(
    ("workflow", "job_name"), [("api-compat.yml", "api-compat"), ("publish.yml", "release")]
)
def test_guard_jobs_use_supported_tool_python(workflow: str, job_name: str) -> None:
    import yaml

    path = _SCRIPTS.parent / ".github" / "workflows" / workflow
    job = yaml.safe_load(path.read_text())["jobs"][job_name]
    assert job["env"]["UV_PYTHON"] == "3.12"
    setup = next(step for step in job["steps"] if "setup-python@" in step.get("uses", ""))
    assert setup["with"]["python-version"] == "3.12"
