"""Post-gen hook: name the model and field when a response omits a required field (issue #287).

The generator decodes required fields with a bare ``d.pop("field")``, so a response missing one
raised ``KeyError: 'field'`` with no model, no context and no hint at the cause. Since Camunda 8.9
every response field is required and absent values are sent as explicit ``null``
(camunda/camunda#46165, #46175), so a missing key is a contract violation, usually an SDK/server
version mismatch. It must stay a failure, just a legible one.

This hook emits ``_required_fields.RequiredFields``, a ``dict`` with ``pop_required(key)`` that
raises ``errors.MissingRequiredFieldError(model, field)``, and rewrites every model's bare
``d.pop("field")`` to use it. ``MissingRequiredFieldError`` subclasses ``KeyError``, so code that
falls back on ``KeyError`` (union variant parsing) behaves as before. A separate method rather
than a ``pop`` override, because the stub generator flattens overloads and ``dict.pop``'s
signature can't be narrowed.

Runs after 1000 and 1200, which pattern-match on ``d.pop(``, and before 1400 generates stubs.
"""

from __future__ import annotations

import re
from pathlib import Path

_HELPER = '''\
"""Response-field access that names the model and field when a required one is missing."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TypeVar

from .errors import MissingRequiredFieldError

V = TypeVar("V")


class RequiredFields(dict[str, V]):
    """The dict a model's ``from_dict`` pops fields from; reports the model on a missing one."""

    def __init__(self, src: Mapping[str, V], model: str) -> None:
        super().__init__(src)
        self._model = model

    def pop_required(self, key: str) -> V:
        """Pop a required field, raising ``MissingRequiredFieldError`` if it is absent."""
        if key not in self:
            raise MissingRequiredFieldError(self._model, key)
        return self.pop(key)
'''

_FUTURE = "from __future__ import annotations\n"
_IMPORT = "from camunda_orchestration_sdk._required_fields import RequiredFields\n"
_PLAIN = "        d = dict(src_dict)\n"
_CHECKED = "        d = RequiredFields(src_dict, cls.__name__)\n"
_BARE_POP = re.compile(r'\bd\.pop\(("[^"]+")\)')


def rewrite_model(source: str) -> str:
    """Route a model's required-field pops through ``RequiredFields``. Idempotent."""
    if not _BARE_POP.search(source):
        return source
    if _PLAIN not in source or not source.startswith(_FUTURE):
        raise SystemExit(
            "hook 1260: a model pops required fields but does not build `d = dict(src_dict)` "
            "after `from __future__ import annotations`; its missing-field errors would stay bare."
        )
    source = _BARE_POP.sub(r"d.pop_required(\1)", source.replace(_PLAIN, _CHECKED))
    return _FUTURE + _IMPORT + source[len(_FUTURE) :]


def run(context: dict[str, str]) -> None:
    package = Path(context["out_dir"]) / "camunda_orchestration_sdk"
    (package / "_required_fields.py").write_text(_HELPER, encoding="utf-8")

    rewritten = 0
    for module in sorted((package / "models").glob("*.py")):
        source = module.read_text(encoding="utf-8")
        updated = rewrite_model(source)
        if updated != source:
            module.write_text(updated, encoding="utf-8")
            rewritten += 1
    if rewritten == 0:
        raise SystemExit("hook 1260: no model decodes a required field; generator output changed")
    print(f"[1260_required_field_errors] {rewritten} model(s) report missing required fields")
