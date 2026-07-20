"""Tests for the flatten-client hook's docstring handling.

The flattened client renames the generated ``body`` request parameter to
``data`` in method signatures; the docstring must follow so the rendered API
reference does not show a phantom ``body`` parameter alongside ``data``.
"""

import importlib.util
import sys
from pathlib import Path

_HOOK_DIR = Path(__file__).resolve().parents[2] / "hooks" / "post_gen"
_HOOK = _HOOK_DIR / "0900_flatten_client.py"

# The hook imports a sibling module (_identifier_guard); make it resolvable
# only while loading, then restore sys.path so the mutation does not leak into
# other tests running in the same process.
_added_to_path = str(_HOOK_DIR) not in sys.path
if _added_to_path:
    sys.path.insert(0, str(_HOOK_DIR))
try:
    _spec = importlib.util.spec_from_file_location("flatten_client", _HOOK)
    assert _spec and _spec.loader
    _flatten = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_flatten)
finally:
    if _added_to_path:
        sys.path.remove(str(_HOOK_DIR))

rename = _flatten._rename_body_arg_in_docstring


class TestRenameBodyArgInDocstring:
    def test_body_arg_renamed_to_data(self):
        doc = "Restore from a backup\n\nArgs:\n    body (RestoreRequest): The request.\n\nReturns:\n    X\n"
        result = rename(doc)
        assert "    data (RestoreRequest): The request." in result
        assert "    body (RestoreRequest)" not in result

    def test_body_without_type_renamed(self):
        doc = "Do it\n\nArgs:\n    body: The request.\n"
        assert "    data: The request." in rename(doc)

    def test_prose_mentioning_body_untouched(self):
        doc = "Sends the request body to the server.\n\nArgs:\n    key (str): The key.\n"
        result = rename(doc)
        assert "Sends the request body to the server." in result

    def test_body_outside_args_untouched(self):
        doc = "Args:\n    key (str): The key.\n\nReturns:\n    body of the response.\n"
        result = rename(doc)
        assert "body of the response." in result

    def test_none_docstring(self):
        assert rename(None) is None
