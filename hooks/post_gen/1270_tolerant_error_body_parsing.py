"""Keep the HTTP status when an error response body cannot be decoded.

The generator decodes every documented error status in ``_parse_response`` with
``ProblemDetail.from_dict(response.json())``. An empty, HTML or incomplete error body (a
proxy 500, an empty 503 or 404) then raises a decoding error *before* the status-bearing
``errors.*Error`` is raised, so callers lose the status: a 503 is not retried, a 404 is
not recognised as "job not found", a 500 is not treated as an unknown outcome.

This hook wraps each 4xx/5xx body decode so a decoding failure yields ``parsed=None``;
the typed status exception is still raised with the raw ``content``. Success bodies are
left strict. Fails closed if the generator output no longer matches.
"""

from __future__ import annotations

import re
from pathlib import Path

_ERROR_DECODE = re.compile(
    r"(?P<indent>[ ]+)if response\.status_code == (?P<code>[45]\d\d):\n"
    r"(?P=indent)    response_(?P=code) = (?P<expr>[^\n]*response\.json\(\)[^\n]*)\n"
)


def _patch(text: str) -> tuple[str, int]:
    def repl(m: re.Match[str]) -> str:
        ind = m.group("indent")
        code = m.group("code")
        return (
            f"{ind}if response.status_code == {code}:\n"
            f"{ind}    try:\n"
            f"{ind}        response_{code} = {m.group('expr')}\n"
            f"{ind}    except Exception:  # undecodable error body: keep the status\n"
            f"{ind}        return None\n"
        )

    return _ERROR_DECODE.subn(repl, text)


def run(context: dict[str, str]) -> None:
    api_dir = Path(context["out_dir"]).resolve() / "camunda_orchestration_sdk" / "api"
    total = 0
    for path in sorted(api_dir.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        new, n = _patch(text)
        if n:
            path.write_text(new, encoding="utf-8")
            total += n
    if total == 0:
        raise SystemExit(
            "hook 1270: no error-body decode found in _parse_response; generator output changed"
        )
    print(f"[1270_tolerant_error_body_parsing] wrapped {total} error-body decodes")
