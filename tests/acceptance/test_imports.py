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


def test_every_generated_module_imports():
    """Every module in the generated package must import, not only the eager ones.

    Guards the defect class where a module the package does not import at load
    time is broken and ships unnoticed -- e.g. ``models.tag_set``, whose pydantic
    ``RootModel`` could not build a schema for the ``Tag`` semantic type (#394), or
    a module using a name newer than the package's Python floor (#386). The
    pre-publish smoke gate runs the same check against the built wheel.

    Deprecated compatibility modules announce themselves with a
    ``DeprecationWarning`` on import; that is intended, so it is not a failure.
    """
    import importlib
    import pkgutil
    import warnings

    import camunda_orchestration_sdk

    failures: dict[str, str] = {}
    for module in pkgutil.walk_packages(
        camunda_orchestration_sdk.__path__, prefix="camunda_orchestration_sdk."
    ):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                importlib.import_module(module.name)
        except Exception as exc:  # collect every failing module, then fail once
            failures[module.name] = f"{type(exc).__name__}: {exc}".splitlines()[0]

    assert not failures, f"Generated modules fail to import: {failures}"


def test_every_literal_regex_in_generated_code_compiles():
    """Every regex literal passed to ``re`` in generated code must compile.

    Guards the defect class where a hook double-escapes a spec ``pattern`` (e.g.
    ``r`` + ``repr()`` in hook 0800 turned ``\\-`` into ``\\\\-``, a bad character
    range), which only fails when validation first runs (#394).
    """
    import ast
    import re
    from pathlib import Path

    import camunda_orchestration_sdk

    pkg_dir = Path(camunda_orchestration_sdk.__file__).parent
    functions = {"compile", "fullmatch", "match", "search"}
    failures: dict[str, str] = {}
    checked = 0
    for py in sorted(pkg_dir.rglob("*.py")):
        for node in ast.walk(ast.parse(py.read_text(encoding="utf-8"))):
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in functions
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "re"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                continue
            checked += 1
            try:
                re.compile(node.args[0].value)
            except re.error as exc:
                failures[f"{py.relative_to(pkg_dir).as_posix()}:{node.lineno}"] = str(exc)

    assert checked, "found no regex literals: the guard is not looking at generated code"
    assert not failures, f"Regex literals that do not compile: {failures}"
