"""Tests for hooks/post_gen/_identifier_guard.py — spec-injection prevention.

Validates that all identifier validation helpers reject spec-controlled strings
that could escape their syntactic context in generated Python source (CWE-94).
"""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import pytest

# Import the guard module from hooks/post_gen/
_guard_path = Path(__file__).resolve().parents[2] / "hooks" / "post_gen" / "_identifier_guard.py"
_spec = importlib.util.spec_from_file_location("_identifier_guard", _guard_path)
assert _spec and _spec.loader
_guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_guard)

safe_py_identifier = _guard.safe_py_identifier
safe_py_identifiers = _guard.safe_py_identifiers
safe_docstring = _guard.safe_docstring
safe_version_string = _guard.safe_version_string
safe_numeric_value = _guard.safe_numeric_value
safe_dotted_import_path = _guard.safe_dotted_import_path


class TestSafePyIdentifier:
    """Validate that safe_py_identifier rejects all non-identifier strings."""

    @pytest.mark.parametrize(
        "value",
        [
            "ProcessInstanceKey",
            "MyType",
            "_private",
            "a1",
            "Foo_Bar_123",
        ],
    )
    def test_accepts_valid_identifiers(self, value: str) -> None:
        assert safe_py_identifier(value) == value

    @pytest.mark.parametrize(
        "value,description",
        [
            # Newline injection (primary attack vector from SFD-214)
            ('PwnedKey = "dummy"\nimport os; os.system("x")\n_sink', "newline injection"),
            # Quote injection
            ('Foo"Bar', "double quote"),
            ("Foo'Bar", "single quote"),
            # Space injection
            ("Foo Bar", "space"),
            # Semicolon injection
            ("Foo;Bar", "semicolon"),
            # Parenthesis injection
            ("Foo()", "parentheses"),
            # Empty string
            ("", "empty string"),
            # Starts with digit
            ("1Foo", "starts with digit"),
            # Contains special characters
            ("Foo$Bar", "dollar sign"),
            ("Foo\tBar", "tab character"),
            ("Foo\rBar", "carriage return"),
            # Backslash injection
            ("Foo\\nBar", "backslash-n"),
        ],
    )
    def test_rejects_unsafe_identifiers(self, value: str, description: str) -> None:
        with pytest.raises(ValueError, match="not a safe Python identifier"):
            safe_py_identifier(value)

    def test_rejects_trailing_newline_bypass(self) -> None:
        """Regression: $ in regex allows trailing newline. Must use \\Z."""
        with pytest.raises(ValueError, match="not a safe Python identifier"):
            safe_py_identifier("Foo\n")

    @pytest.mark.parametrize(
        "keyword",
        ["class", "def", "import", "return", "if", "for", "while", "try", "except"],
    )
    def test_rejects_python_keywords(self, keyword: str) -> None:
        with pytest.raises(ValueError, match="Python keyword"):
            safe_py_identifier(keyword)

    def test_context_appears_in_error(self) -> None:
        with pytest.raises(ValueError, match="x-semantic-type"):
            safe_py_identifier("bad value", "x-semantic-type")


class TestSafePyIdentifiers:
    """Validate batch identifier validation."""

    def test_accepts_valid_list(self) -> None:
        result = safe_py_identifiers(["Foo", "Bar", "Baz"])
        assert result == ["Foo", "Bar", "Baz"]

    def test_rejects_any_invalid(self) -> None:
        with pytest.raises(ValueError):
            safe_py_identifiers(["Foo", "Bad Value", "Baz"])


class TestSafeDocstring:
    """Validate that safe_docstring escapes docstring-terminating sequences."""

    def test_preserves_normal_text(self) -> None:
        assert safe_docstring("Hello world") == "Hello world"

    def test_escapes_triple_double_quotes(self) -> None:
        result = safe_docstring('Foo """bar""" baz')
        assert '"""' not in result

    def test_preserves_triple_single_quotes(self) -> None:
        """Triple single-quotes are safe inside triple double-quote delimiters."""
        result = safe_docstring("Foo '''bar''' baz")
        assert result == "Foo '''bar''' baz"

    def test_handles_none(self) -> None:
        assert safe_docstring(None) == ""

    def test_sanitised_docstring_is_valid_python(self) -> None:
        """Ensure a sanitised docstring can be embedded in triple-quoted string."""
        malicious = 'Inject """\nimport os\nos.system("x")\n"""'
        sanitised = safe_docstring(malicious)
        # Construct a Python source with the sanitised docstring
        source = f'def f():\n    """{sanitised}"""\n    pass\n'
        # Must parse without error
        compile(source, "<test>", "exec")

    def test_trailing_backslash_does_not_escape_closing_quotes(self) -> None:
        """Regression: trailing \\ escapes the first \" of closing \"\"\", breaking the docstring."""
        result = safe_docstring("test\\")
        source = f'def f():\n    """{result}"""\n    pass\n'
        # Must parse without error — if trailing backslash isn't handled,
        # the closing """ is escaped and the source fails to compile.
        compile(source, "<test>", "exec")

    def test_trailing_odd_backslashes_doubled(self) -> None:
        """An odd number of trailing backslashes must be made even."""
        result = safe_docstring("test\\\\\\")  # 3 trailing backslashes
        source = f'def f():\n    """{result}"""\n    pass\n'
        compile(source, "<test>", "exec")

    def test_trailing_even_backslashes_preserved(self) -> None:
        """An even number of trailing backslashes is already safe."""
        result = safe_docstring("test\\\\")  # 2 trailing backslashes
        assert result == "test\\\\"

    def test_combined_attack_quotes_and_backslash(self) -> None:
        """Combined attack: triple-quote preceded by backslash."""
        malicious = 'Inject \\"""\nimport os\nos.system("x")'
        sanitised = safe_docstring(malicious)
        source = f'def f():\n    """{sanitised}"""\n    pass\n'
        compile(source, "<test>", "exec")


class TestSafeVersionString:
    """Validate version string sanitisation."""

    @pytest.mark.parametrize(
        "value",
        ["8.5", "8.5.0", "8.5.0-alpha1", "1.0.0", "v2.3.4"],
    )
    def test_accepts_valid_versions(self, value: str) -> None:
        assert safe_version_string(value) == value

    @pytest.mark.parametrize(
        "value,description",
        [
            ('8.5"""\nimport os\n"""', "triple quote escape"),
            ("8.5\nimport os", "newline injection"),
            ("8.5; import os", "semicolon injection"),
            ("", "empty string"),
            ("8.5 or True", "space injection"),
        ],
    )
    def test_rejects_unsafe_versions(self, value: str, description: str) -> None:
        with pytest.raises(ValueError, match="not a safe version string"):
            safe_version_string(value)

    def test_rejects_trailing_newline_bypass(self) -> None:
        """Regression: $ in regex allows trailing newline. Must use \\Z."""
        with pytest.raises(ValueError, match="not a safe version string"):
            safe_version_string("8.5\n")


class TestSafeNumericValue:
    """Validate numeric constraint guard — prevents string injection via minimum/maximum."""

    @pytest.mark.parametrize("value", [0, 1, -1, 42, 3.14, -0.5, 1e10])
    def test_accepts_valid_numbers(self, value: int | float) -> None:
        assert safe_numeric_value(value) == value

    @pytest.mark.parametrize(
        "value,description",
        [
            ("0\nimport os\nos.system('x')\n#", "string with newline injection"),
            ("42", "string that looks numeric"),
            (True, "boolean True (subclass of int in Python)"),
            (False, "boolean False"),
            (None, "None"),
            ([1], "list"),
            (float("nan"), "NaN"),
            (float("inf"), "positive infinity"),
            (float("-inf"), "negative infinity"),
        ],
    )
    def test_rejects_non_numeric(self, value: object, description: str) -> None:
        with pytest.raises(ValueError):
            safe_numeric_value(value)


class TestSafeDottedImportPath:
    """Validate dotted import path guard for from-import statements."""

    @pytest.mark.parametrize(
        "value",
        [
            ".api.create_process_instance",
            "..foo.bar",
            ".module",
            "package.module",
        ],
    )
    def test_accepts_valid_paths(self, value: str) -> None:
        assert safe_dotted_import_path(value) == value

    @pytest.mark.parametrize(
        "value,description",
        [
            (".api.bad name", "space in segment"),
            (".api.import", "keyword segment"),
            (".api.\nimport os", "newline injection"),
            ("", "empty string"),
            (".", "dots only"),
        ],
    )
    def test_rejects_unsafe_paths(self, value: str, description: str) -> None:
        with pytest.raises(ValueError):
            safe_dotted_import_path(value)


class TestNoHookInterpolatesUnsafeIdentifiers:
    """Class-scoped regression guard: verify that all hooks that generate Python
    source import and use the identifier guard.

    This catches the defect CLASS (any hook that interpolates spec-controlled
    strings without validation), not just the specific instances from SFD-214.
    """

    # All hooks that interpolate spec-controlled strings into Python source
    HOOKS_REQUIRING_GUARD = [
        "0150_annotate_deprecated_enums.py",
        "0200_raise_exceptions.py",
        "0700_generate_semantic_types.py",
        "0800_generate_composite_alias_models.py",
        "0900_flatten_client.py",
        "1000_patch_semantic_types_in_models.py",
        "1375_reexport_models.py",
    ]

    @pytest.mark.parametrize("hook_file", HOOKS_REQUIRING_GUARD)
    def test_hook_imports_identifier_guard(self, hook_file: str) -> None:
        hook_path = Path(__file__).resolve().parents[2] / "hooks" / "post_gen" / hook_file
        source = hook_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=hook_file)
        has_import = any(
            isinstance(node, ast.ImportFrom) and node.module == "_identifier_guard"
            for node in ast.walk(tree)
        )
        assert has_import, (
            f"{hook_file} does not import from _identifier_guard — "
            f"spec-controlled strings may be interpolated into Python source without validation"
        )
