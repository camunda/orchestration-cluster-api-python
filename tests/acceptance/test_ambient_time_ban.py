"""The ambient-time ban is enforced by lint, and this proves the lint works.

A config that silently matches nothing is worse than no config: it reports success while
the contract it claims to enforce is unguarded. So rather than trusting `TID251` to
understand every spelling of a clock read, these tests run ruff against fixtures that use
each one and assert it objects.

The evasions are not hypothetical. `import time as _t` is exactly how `runtime/clock.py`
imports the module it is exempt from, and `from time import monotonic` is what a
well-meaning "tidy up the imports" change produces.

See camunda/orchestration-cluster-api-js#450.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Every spelling that must be caught. The bare-module cases matter most: TID251 resolves
#: qualified names, so `import time; time.time()` has to be understood as a `time.time`
#: reference rather than an attribute access it cannot see through.
BANNED_SPELLINGS = pytest.mark.parametrize(
    ("label", "source"),
    [
        ("time.time", "import time\n\nx = time.time()\n"),
        ("time.monotonic", "import time\n\nx = time.monotonic()\n"),
        ("time.sleep", "import time\n\ntime.sleep(1)\n"),
        ("asyncio.sleep", "import asyncio\n\n\nasync def f():\n    await asyncio.sleep(1)\n"),
        ("aliased module", "import time as _t\n\nx = _t.monotonic()\n"),
        ("from-import", "from time import monotonic\n\nx = monotonic()\n"),
        ("aliased from-import", "from time import sleep as nap\n\nnap(1)\n"),
    ],
    ids=lambda v: v if isinstance(v, str) and "\n" not in v else "",
)


def _lint(source: str, tmp_path: Path) -> str:
    """Lint a fixture as if it lived in `runtime/`, which is where the ban applies."""
    target = REPO_ROOT / "runtime" / f"_ban_fixture_{tmp_path.name}.py"
    target.write_text(source, encoding="utf-8")
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--select", "TID251",
             "--output-format", "concise", str(target)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=False,
        )
        return completed.stdout + completed.stderr
    finally:
        target.unlink(missing_ok=True)


@BANNED_SPELLINGS
def test_ambient_time_is_rejected_in_the_runtime(label: str, source: str, tmp_path: Path) -> None:
    output = _lint(source, tmp_path)

    assert "TID251" in output, (
        f"ruff did not object to `{label}` in runtime/. The ban does not cover this "
        f"spelling, so the contract is unenforced for it.\nruff said:\n{output}"
    )


def test_the_message_points_somewhere_useful(tmp_path: Path) -> None:
    """A ban that only says "banned" invites a `noqa` rather than a fix."""
    output = _lint("import time\n\nx = time.time()\n", tmp_path)

    assert "clock" in output.lower(), (
        f"the diagnostic should name the alternative, not just refuse; got:\n{output}"
    )


def test_the_injected_clock_is_not_rejected(tmp_path: Path) -> None:
    """The complement: the ban must not be so broad that the correct code trips it."""
    source = (
        "from .clock import Clock\n\n\n"
        "async def f(clock: Clock) -> float:\n"
        "    await clock.sleep(1)\n"
        "    clock.sleep_sync(1)\n"
        "    return clock.now()\n"
    )
    output = _lint(source, tmp_path)

    assert "TID251" not in output, (
        f"using the injected clock must be allowed; ruff said:\n{output}"
    )


def test_the_runtime_is_currently_clean() -> None:
    """Guards the state slices 1-3 established, not just the config that describes it."""
    completed = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--select", "TID251",
         "--output-format", "concise", "runtime"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )

    assert completed.returncode == 0, (
        "runtime/ reads ambient time somewhere it should be using the injected clock:\n"
        f"{completed.stdout}{completed.stderr}"
    )
