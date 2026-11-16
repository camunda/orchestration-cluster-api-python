"""Tests for the stable-branch API compatibility checker (``scripts/api_compat.py``).

Every case starts from one baseline package shaped like the generated SDK (attrs models
with ``Unset``, an enum, a client class, module-level functions). A break case applies a
single textual mutation to it and must be reported; a compatible case must not be. The
baseline compared with itself is asserted green first, so a break case can only fail
because of its mutation.
"""

import importlib.util
import json
import sys
import textwrap
from pathlib import Path
from typing import Any

import pytest

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

        from .models.request_model import RequestModel
        from .models.result_model import ResultModel

        class Client:
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
    broken = _write(tmp_path / "broken", _mutate("client.py", "-> int:", "-> str:"))
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
