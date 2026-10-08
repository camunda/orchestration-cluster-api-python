"""Tests for ``scripts/setup-hooks.sh``.

In a linked worktree ``.git`` is a file, so a hardcoded ``.git/hooks`` path made
``make install`` (and therefore ``make generate``) fail there.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _REPO_ROOT / "scripts" / "setup-hooks.sh"

# Never read the developer's git config or inherited GIT_DIR: a global core.hooksPath
# would point the script at their real hooks.
_GIT_ENV = {
    **{k: v for k, v in os.environ.items() if not k.startswith("GIT_")},
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.com",
}


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        env=_GIT_ENV,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


@pytest.fixture
def main_checkout(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "commit", "-q", "--allow-empty", "-m", "init")
    return repo


@pytest.fixture
def linked_worktree(main_checkout: Path, tmp_path: Path) -> Path:
    wt = tmp_path / "wt"
    _git(main_checkout, "worktree", "add", "-q", str(wt))
    assert (wt / ".git").is_file()
    return wt


@pytest.mark.parametrize("checkout", ["main_checkout", "linked_worktree"])
def test_installs_pre_push_hook_where_git_reads_it(
    checkout: str, request: pytest.FixtureRequest
) -> None:
    cwd: Path = request.getfixturevalue(checkout)

    subprocess.run(["bash", str(_SCRIPT)], cwd=cwd, env=_GIT_ENV, check=True)

    hook = (cwd / _git(cwd, "rev-parse", "--git-path", "hooks")) / "pre-push"
    assert hook.is_file()
    assert os.access(hook, os.X_OK)


@pytest.mark.parametrize("user_hooks", ["external_dir", "disabled"])
def test_leaves_a_user_configured_hooks_path_alone(
    user_hooks: str, main_checkout: Path, tmp_path: Path
) -> None:
    own_hook = tmp_path / "user-hooks" / "pre-push"
    own_hook.parent.mkdir()
    own_hook.write_text("#!/bin/sh\necho users-own-hook\n")
    hooks_path = str(own_hook.parent) if user_hooks == "external_dir" else os.devnull
    _git(main_checkout, "config", "core.hooksPath", hooks_path)

    subprocess.run(["bash", str(_SCRIPT)], cwd=main_checkout, env=_GIT_ENV, check=True)

    assert own_hook.read_text() == "#!/bin/sh\necho users-own-hook\n"
    common_dir = main_checkout / _git(main_checkout, "rev-parse", "--git-common-dir")
    assert not (common_dir / "hooks" / "pre-push").exists()


def test_repo_scripts_do_not_hardcode_git_dir_paths() -> None:
    files = [*sorted((_REPO_ROOT / "scripts").rglob("*")), _REPO_ROOT / "Makefile"]
    offenders = [
        str(f.relative_to(_REPO_ROOT))
        for f in files
        if f.is_file()
        and f.suffix in {".sh", ".py", ""}
        and re.search(r"\.git/", f.read_text(encoding="utf-8", errors="ignore"))
    ]
    assert offenders == [], f"use `git rev-parse --git-path` instead: {offenders}"
