def test_can_import_generated_package():
    # Import a couple of common entry points to ensure the generated SDK is loadable
    from camunda_orchestration_sdk import Client  # noqa: F401  # pyright: ignore[reportUnusedImport]


def test_api_client_constructible():
    # The generated client should be importable and constructible without side effects
    from camunda_orchestration_sdk import semantic_types

    from camunda_orchestration_sdk import Client

    client = Client(base_url="http://localhost")

    assert client is not None
    # semantic type constructor smoke
    assert hasattr(semantic_types, "ProcessDefinitionId")
    assert semantic_types.ProcessDefinitionKey("123") == "123"


def test_camunda_client_constructible():
    from camunda_orchestration_sdk import CamundaClient, CamundaAsyncClient

    client = CamundaClient()
    assert client is not None
    assert client.client is not None

    async_client = CamundaAsyncClient()
    assert async_client is not None
    assert async_client.client is not None


def test_all_semantic_type_imports_in_models_are_defined():
    """Every name a generated model imports from semantic_types must exist.

    Guards the defect class where a model brands a field to a semantic key that
    the semantic-types generator did not emit -- e.g. an integer-backed key that
    camunda-schema-bundler dropped from the spec metadata's semanticKeys, which
    would otherwise produce an ImportError at package load time.
    """
    import ast
    from pathlib import Path

    from camunda_orchestration_sdk import semantic_types

    models_dir = Path(semantic_types.__file__).parent / "models"
    assert models_dir.is_dir()

    missing: dict[str, list[str]] = {}
    for model_file in models_dir.glob("*.py"):
        tree = ast.parse(model_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ImportFrom)
                and node.module == "camunda_orchestration_sdk.semantic_types"
            ):
                for alias in node.names:
                    if not hasattr(semantic_types, alias.name):
                        missing.setdefault(model_file.name, []).append(alias.name)

    assert not missing, f"Models import undefined semantic types: {missing}"


def test_nullable_list_parse_helpers_are_type_annotated():
    """Nullable list-of-model ``_parse_`` helpers must alias data via cast.

    Guards the defect class where a line-wrapped (multi-line) ``.from_dict()``
    call -- produced when the field's variable name is long -- causes the
    typing-fix hook to miss the helper, leaving the ``from_dict`` argument
    typed ``object`` and producing a ty error at the SDK boundary.
    """
    import re
    from pathlib import Path

    from camunda_orchestration_sdk import semantic_types

    models_dir = Path(semantic_types.__file__).parent / "models"

    # The *unfixed* shape: a bare ``_var = data`` alias feeding a ``from_dict``
    # loop. The fix rewrites the alias to ``cast(list[Any], data)``, so any
    # match here means a helper escaped the hook. ``\s*..\s*`` tolerates both
    # single-line and line-wrapped ``from_dict`` calls, and ``,?`` tolerates a
    # magic trailing comma inside a wrapped call -- kept in lockstep with hook
    # 1200's ``_PARSE_HELPER_LIST_RE`` so the guard cannot miss a shape the hook
    # is meant to fix.
    unfixed_re = re.compile(
        r"^([ \t]+)(\w+) = \[\]\n"
        r"\1_\2 = data\n"
        r"\1for \2_item_data in _\2:\n"
        r"\1    \2_item = \w+\.from_dict\(\s*\2_item_data\s*,?\s*\)",
        re.MULTILINE,
    )

    offenders: list[str] = []
    for model_file in models_dir.glob("*.py"):
        if unfixed_re.search(model_file.read_text(encoding="utf-8")):
            offenders.append(model_file.name)

    assert not offenders, (
        f"Nullable list parse helpers not type-annotated: {sorted(offenders)}"
    )
