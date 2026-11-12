"""Smoke-test an *installed* camunda-orchestration-sdk, as a user would get it from PyPI.

Run by scripts/smoke-test-wheel.sh inside a clean virtualenv that contains only the built
wheel and its runtime dependencies: no dev dependencies, and not run from the repository, so
nothing from the source tree can mask a packaging defect.

Catches the class of defect behind 9.0.2 (#386, post-mortem #389): code that imports or runs
only on a newer Python than the package's Requires-Python floor, a module that fails to
import, or a client that cannot be constructed.

Exits non-zero, with a reason, on the first failed check.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import os
import pkgutil
import sys
import sysconfig
from pathlib import Path

DIST = "camunda-orchestration-sdk"
PACKAGE = "camunda_orchestration_sdk"

# The Orchestration Cluster API sends UTC timestamps with a "Z" suffix, sometimes with
# nanosecond precision. datetime.fromisoformat() rejects both before Python 3.11.
GATEWAY_TIMESTAMPS = ("2026-11-12T03:30:43.2Z", "2026-11-12T03:30:43.123456789Z")


def check(condition: bool, message: str) -> None:
    if not condition:
        sys.exit(f"SMOKE FAIL: {message}")


def main() -> None:
    version = importlib.metadata.version(DIST)
    print(f"Python {sys.version.split()[0]} | {DIST} {version}")

    try:
        package = importlib.import_module(PACKAGE)
    except Exception as exc:
        sys.exit(f"SMOKE FAIL: import {PACKAGE}: {type(exc).__name__}: {exc}")
    location = Path(package.__file__ or "").resolve()
    site_packages = Path(sysconfig.get_paths()["purelib"]).resolve()
    check(
        site_packages in location.parents,
        f"{PACKAGE} was imported from {location}, not from the installed wheel in {site_packages}",
    )

    # Every module must import: a 3.11-only name (StrEnum, typing.Self) in any module is a
    # failure here, not only in the ones the top-level package happens to import eagerly.
    failures: list[str] = []
    count = 0
    for module in pkgutil.walk_packages(package.__path__, prefix=f"{PACKAGE}."):
        count += 1
        try:
            importlib.import_module(module.name)
        except Exception as exc:  # report every failing module, then fail once
            failures.append(f"{module.name}: {type(exc).__name__}: {str(exc).splitlines()[0]}")
    check(not failures, f"{len(failures)} of {count} modules fail to import:\n  " + "\n  ".join(failures))
    print(f"imported {count} modules")

    os.environ.setdefault("CAMUNDA_REST_ADDRESS", "http://localhost:8080")
    from camunda_orchestration_sdk import CamundaAsyncClient, CamundaClient

    CamundaClient()
    CamundaAsyncClient()
    print("constructed CamundaClient and CamundaAsyncClient")

    from camunda_orchestration_sdk.models.document_link import DocumentLink

    for timestamp in GATEWAY_TIMESTAMPS:
        try:
            link = DocumentLink.from_dict({"url": "https://example.com", "expiresAt": timestamp})
        except Exception as exc:
            sys.exit(f"SMOKE FAIL: cannot decode gateway timestamp {timestamp!r}: {type(exc).__name__}: {exc}")
        check(
            link.expires_at.utcoffset() is not None,
            f"decoded {timestamp!r} without a timezone: {link.expires_at!r}",
        )
    print(f"decoded gateway timestamps {', '.join(GATEWAY_TIMESTAMPS)}")

    print("SMOKE OK")


if __name__ == "__main__":
    main()
