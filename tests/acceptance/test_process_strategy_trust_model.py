"""Guards for the trust model of the ``process`` execution strategy (issue #411).

With ``execution_strategy="process"`` the worker hands each job to a ``ProcessPoolExecutor``.
Two things are pickled across that boundary, and both ends are processes the SDK itself
starts:

* parent -> child: the handler and a plain :class:`JobContext` built from the server's
  activated-job JSON;
* child -> parent: the :data:`JobAction` the handler produced, including the handler's own
  return value.

The trust model that follows, and which these tests pin so it cannot erode unnoticed:

1. The SDK never unpickles bytes from anywhere but its own process pool. Nothing from the
   server, the token cache or configuration files is ever fed to ``pickle`` (or to any
   other code-executing deserialiser).
2. Job data from the server stays JSON-shaped. It is parsed with ``json`` into plain
   ``dict``/``list``/``str``/``int``/``float``/``bool``/``None`` values, and the only
   non-primitive objects in a ``JobContext`` are the SDK's own models, enums and
   semantic-type strings. Which classes get instantiated at unpickle time is decided by the
   *type* of the objects the parent built, never by the content of the job data.
3. The handler is trusted code. Its return value is pickled back to the parent, so a
   handler (or a library it uses) that returns a non-JSON object has that object
   unpickled in the worker's parent process. Return a ``dict`` or a
   ``JobCompletionRequest``.

These are class-scoped guards: they scan the whole package and walk the whole context, so
a new field or a new deserialisation site fails here rather than only the ones foreseen.
"""

from __future__ import annotations

import ast
import asyncio
import enum
import io
import json
import pickle
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

import attrs
import pytest

import camunda_orchestration_sdk
from camunda_orchestration_sdk.models.activated_job_result import ActivatedJobResult
from camunda_orchestration_sdk.models.job_activation_result import JobActivationResult
from camunda_orchestration_sdk.models.job_completion_request import JobCompletionRequest
from camunda_orchestration_sdk.runtime.job_worker import (
    JobContext,
    _execute_task_isolated,  # pyright: ignore[reportPrivateUsage]
)
from camunda_orchestration_sdk.runtime.logging import SdkLogger

SDK_ROOT = Path(camunda_orchestration_sdk.__file__).resolve().parent
SDK_PACKAGE = "camunda_orchestration_sdk"

#: Modules that deserialise by running code chosen by the bytes. None may be imported
#: anywhere in the SDK: the process strategy relies on the standard library's pool doing the
#: only unpickling there is.
CODE_EXECUTING_DESERIALISERS = frozenset(
    {
        "pickle",
        "_pickle",
        "cPickle",
        "dill",
        "cloudpickle",
        "joblib",
        "jsonpickle",
        "marshal",
        "shelve",
    }
)

#: Lower-level ways to accept bytes from another process. The SDK has no reason to open a
#: listener, a manager or a raw connection; the pool's own queues are the only channel.
IPC_MODULES = frozenset({"multiprocessing"})

#: The one module allowed to create a process pool.
POOL_OWNER = Path("runtime") / "job_worker.py"


def _sdk_sources() -> list[Path]:
    return sorted(SDK_ROOT.rglob("*.py"))


def _imported_modules(tree: ast.AST) -> set[str]:
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            modules.add(node.module)
    return modules


def _root(module: str) -> str:
    return module.split(".", 1)[0]


class TestNoBytesFromOutsideThePoolAreUnpickled:
    """Claim 1: the only unpickling is the process pool's own."""

    def test_the_sdk_does_not_import_a_code_executing_deserialiser(self) -> None:
        offenders: list[str] = []
        for path in _sdk_sources():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for module in _imported_modules(tree):
                if _root(module) in CODE_EXECUTING_DESERIALISERS:
                    offenders.append(f"{path.relative_to(SDK_ROOT)} imports {module}")
        assert not offenders, (
            "The SDK must not deserialise with pickle-style loaders. Server responses, the "
            "token cache and configuration are parsed as JSON (or dotenv) only. If a new "
            "use is genuinely needed, update the trust model in the JobContext docstring "
            f"and README first: {offenders}"
        )

    def test_the_sdk_does_not_open_its_own_inter_process_channels(self) -> None:
        offenders: list[str] = []
        for path in _sdk_sources():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for module in _imported_modules(tree):
                if _root(module) in IPC_MODULES:
                    offenders.append(f"{path.relative_to(SDK_ROOT)} imports {module}")
        assert not offenders, (
            "Only ProcessPoolExecutor's private queues may carry pickled data. Listeners, "
            f"managers and raw connections accept bytes from elsewhere: {offenders}"
        )

    def test_only_the_job_worker_creates_a_process_pool_and_with_no_extras(self) -> None:
        creators: list[Path] = []
        for path in _sdk_sources():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
                if name != "ProcessPoolExecutor":
                    continue
                creators.append(path.relative_to(SDK_ROOT))
                # A custom mp_context, initializer or initargs would change who can feed
                # the pool; only the worker count is a legitimate knob.
                assert {kw.arg for kw in node.keywords} <= {"max_workers"}, (
                    f"{path.relative_to(SDK_ROOT)}: ProcessPoolExecutor may only be given "
                    "max_workers; see the trust model in the JobContext docstring"
                )
        assert set(creators) == {POOL_OWNER}, (
            f"ProcessPoolExecutor must be created only in {POOL_OWNER}, found {creators}"
        )

    def test_a_pickle_in_the_token_cache_is_never_executed(self, tmp_path: Path) -> None:
        """Dynamic counterpart of the import scan, for the one file the SDK reads back.

        The cache file is JSON. A pickle planted in its place must be rejected as
        unparseable, not loaded; the sentinel proves the payload did not run.
        """
        from camunda_orchestration_sdk.runtime.auth import (
            OAuthClientCredentialsAuthProvider,
        )

        sentinel = tmp_path / "executed"
        provider = OAuthClientCredentialsAuthProvider(
            oauth_url="https://login.example.com/oauth/token",
            client_id="id",
            client_secret="secret",
            audience="aud",
            cache_dir=str(tmp_path / "cache"),
        )
        try:
            cache_file = provider._token_cache_file()  # pyright: ignore[reportPrivateUsage]
            assert cache_file is not None
            for protocol in (0, pickle.HIGHEST_PROTOCOL):
                cache_file.write_bytes(
                    pickle.dumps(_WritesSentinel(str(sentinel)), protocol=protocol)
                )
                assert provider._try_load_file_cached_token() is None  # pyright: ignore[reportPrivateUsage]
                assert not sentinel.exists(), (
                    f"the token cache was unpickled (protocol {protocol})"
                )
        finally:
            provider.close()


class _WritesSentinel:
    """Pickling this and loading it anywhere creates the sentinel file."""

    def __init__(self, path: str) -> None:
        self.path = path

    def __reduce__(self) -> tuple[Any, tuple[str]]:
        return (_touch, (self.path,))


def _touch(path: str) -> str:
    Path(path).write_text("executed", encoding="utf-8")
    return path


# --------------------------------------------------------------------------------------
# Claim 2: job data stays JSON-shaped.
# --------------------------------------------------------------------------------------

#: Values chosen to look like deserialisation gadgets. They are data: if any of them ever
#: became a class, a callable or a module reference, the walk below would see it.
HOSTILE_JSON: dict[str, Any] = {
    "plain": {"a": [1, 2.5, True, None, "x", {"b": []}], "big": 10**40, "unicode": "é"},
    "py/object": "os.system",
    "__class__": "subprocess.Popen",
    "__reduce__": ["os.system", ["echo pwned"]],
    "pickle_protocol_0": "cos\nsystem\n(S'echo pwned'\ntR.",
    "module.attr": {"$type": "builtins.eval", "value": "__import__('os').system('id')"},
}

#: A populated activation: every nullable field set, so nothing is skipped by being None.
JOB_JSON: dict[str, Any] = {
    "type": "my-job",
    "processDefinitionId": "proc",
    "processDefinitionVersion": 3,
    "elementId": "elem",
    "customHeaders": HOSTILE_JSON,
    "worker": "w1",
    "retries": 5,
    "deadline": 9999,
    "variables": HOSTILE_JSON,
    "tenantId": "t1",
    "physicalTenantId": "t1",
    "jobKey": "99",
    "processInstanceKey": "1",
    "processDefinitionKey": "2",
    "elementInstanceKey": "3",
    "kind": "BPMN_ELEMENT",
    "listenerEventType": "UNSPECIFIED",
    "userTask": {
        "action": "complete",
        "assignee": "someone",
        "candidateGroups": ["g"],
        "candidateUsers": ["u"],
        "changedAttributes": ["assignee"],
        "dueDate": "2026-01-01T00:00:00Z",
        "followUpDate": "2026-01-02T00:00:00Z",
        "formKey": "11",
        "priority": 50,
        "userTaskKey": "12",
        "unmodelled": HOSTILE_JSON,
    },
    "tags": ["a", "b"],
    "rootProcessInstanceKey": "1",
    "businessId": "order-1",
    "priority": 7,
    "jobLeaseToken": "550e8400-e29b-41d4-a716-446655440000",
    "unmodelledTopLevel": HOSTILE_JSON,
}


def _activated_from_wire() -> ActivatedJobResult:
    """Build the job the way the worker does: parse the response body as JSON, then
    ``from_dict``. The round-trip through ``json`` is deliberate: it is what ``httpx``'s
    ``response.json()`` hands the generated client."""
    wire = json.dumps({"jobs": [JOB_JSON]})
    return JobActivationResult.from_dict(json.loads(wire)).jobs[0]


def _context() -> JobContext:
    return JobContext.from_job(_activated_from_wire())


_JSON_PRIMITIVES = (bool, int, float, str, type(None))


def _assert_json_shaped(value: Any, path: str) -> None:
    """Every leaf is a JSON primitive, or an SDK model/enum/semantic-type string/logger."""
    if type(value) in _JSON_PRIMITIVES:
        return
    if isinstance(value, dict):
        for key, item in value.items():  # pyright: ignore[reportUnknownVariableType]
            assert type(key) is str, f"{path}: non-string key {key!r}"
            _assert_json_shaped(item, f"{path}[{key!r}]")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):  # pyright: ignore[reportUnknownVariableType]
            _assert_json_shaped(item, f"{path}[{index}]")
        return
    cls = type(value)
    assert cls.__module__.split(".", 1)[0] == SDK_PACKAGE, (
        f"{path}: {cls.__module__}.{cls.__qualname__} is not an SDK type; a JobContext may "
        "hold only JSON data and the SDK's own types"
    )
    if isinstance(value, str):  # semantic types such as JobKey subclass str
        return
    if isinstance(value, enum.Enum):
        assert type(value.value) in _JSON_PRIMITIVES, f"{path}: enum with non-JSON value"
        return
    if isinstance(value, SdkLogger):
        return  # pickles as a silent logger; see SdkLogger.__reduce__
    assert attrs.has(cls), f"{path}: {cls.__qualname__} is neither an attrs model nor an enum"
    for field in attrs.fields(cls):
        _assert_json_shaped(getattr(value, field.name), f"{path}.{field.name}")


class TestJobVariablesStayJsonShaped:
    """Claim 2: variables, headers and the rest are never turned into arbitrary classes."""

    def test_the_fixture_populates_every_field(self) -> None:
        """So the walk below cannot pass vacuously on a field left None. A field added to
        ``ActivatedJobResult`` must be added to ``JOB_JSON`` (and so be walked) too."""
        context = _context()
        unset = [f.name for f in attrs.fields(JobContext) if getattr(context, f.name) is None]
        assert not unset, f"JOB_JSON leaves these fields None, so they are never walked: {unset}"

    def test_every_value_in_a_context_built_from_json_is_json_shaped(self) -> None:
        _assert_json_shaped(_context(), "JobContext")

    def test_variables_are_the_parsed_json_unchanged(self) -> None:
        context = _context()
        assert context.variables.to_dict() == HOSTILE_JSON
        assert context.custom_headers.to_dict() == HOSTILE_JSON

    def test_hostile_looking_strings_stay_strings(self) -> None:
        variables = _context().variables
        assert type(variables["py/object"]) is str
        assert type(variables["__reduce__"]) is list
        assert all(type(part) in (str, list) for part in variables["__reduce__"])
        assert type(variables["module.attr"]) is dict

    def test_the_walk_rejects_what_it_is_meant_to_reject(self) -> None:
        """The guard proves its own teeth: a live object anywhere in the context fails it."""
        context = _context()
        context.variables["smuggled"] = _WritesSentinel("x")
        with pytest.raises(AssertionError, match="not an SDK type"):
            _assert_json_shaped(context, "JobContext")


class _RecordingUnpickler(pickle.Unpickler):
    """Allows only SDK classes and records every global the stream asks to resolve."""

    def __init__(self, data: bytes) -> None:
        super().__init__(io.BytesIO(data))
        self.requested: list[str] = []

    def find_class(self, module: str, name: str) -> Any:
        self.requested.append(f"{module}.{name}")
        if module.split(".", 1)[0] != SDK_PACKAGE:
            raise pickle.UnpicklingError(f"forbidden global in JobContext pickle: {module}.{name}")
        return super().find_class(module, name)


class TestWhatTheParentSendsTheChild:
    """The bytes the parent writes for the child reference only SDK classes, whatever the
    job data contains."""

    @pytest.mark.parametrize("protocol", range(2, pickle.HIGHEST_PROTOCOL + 1))
    def test_the_pickled_context_resolves_only_sdk_globals(self, protocol: int) -> None:
        context = _context()
        unpickler = _RecordingUnpickler(pickle.dumps(context, protocol=protocol))
        restored = unpickler.load()

        assert unpickler.requested, "expected the SDK's own classes to be referenced"
        assert all(name.startswith(f"{SDK_PACKAGE}.") for name in unpickler.requested)
        assert isinstance(restored, JobContext)
        assert restored.variables.to_dict() == HOSTILE_JSON
        assert restored.job_key == context.job_key

    def test_the_logger_degrades_to_a_silent_one_across_the_boundary(self) -> None:
        context = _context()
        restored = pickle.loads(pickle.dumps(context))  # our own bytes
        assert isinstance(restored.log, SdkLogger)
        restored.log.info("must not raise or emit")


# --------------------------------------------------------------------------------------
# Claim 3: the handler's return value is pickled back to the parent.
# --------------------------------------------------------------------------------------


class HandlerResult:
    """A non-JSON object a handler might return. Module-level so the pool can pickle it."""

    def __init__(self, value: int) -> None:
        self.value = value


def returns_a_dict(job: JobContext) -> dict[str, Any]:
    return {"seen_key": str(job.job_key), "nested": {"x": [1, None, "y"]}}


def returns_a_completion_request(job: JobContext) -> JobCompletionRequest:
    return JobCompletionRequest()


def returns_an_arbitrary_object(job: JobContext) -> Any:
    return HandlerResult(42)


async def run_in_a_process_pool(handler: Any, context: JobContext) -> Any:
    """Exactly what ``JobWorker._execute_job`` does for the process strategy."""
    pool = ProcessPoolExecutor(max_workers=1)
    try:
        return await asyncio.get_running_loop().run_in_executor(
            pool, _execute_task_isolated, handler, context
        )
    finally:
        pool.shutdown(wait=True)


class TestWhatTheChildSendsTheParent:
    """Claim 3: the child's result is pickled back, so it is only as trustworthy as the
    handler."""

    @pytest.mark.asyncio
    async def test_the_handler_receives_the_context_and_returns_a_plain_dict(self) -> None:
        action = await run_in_a_process_pool(returns_a_dict, _context())

        assert action == (
            "complete",
            {"seen_key": "99", "nested": {"x": [1, None, "y"]}},
        )

    @pytest.mark.asyncio
    async def test_a_completion_request_comes_back_as_the_sdk_model(self) -> None:
        action = await run_in_a_process_pool(returns_a_completion_request, _context())

        assert action[0] == "complete"
        assert isinstance(action[1], JobCompletionRequest)

    @pytest.mark.asyncio
    async def test_an_arbitrary_return_value_is_pickled_back_not_coerced_to_json(self) -> None:
        """Documents why the handler is inside the trust boundary: whatever it returns is
        reconstructed in the parent by pickle. The SDK does not (and cannot) vet it."""
        action = await run_in_a_process_pool(returns_an_arbitrary_object, _context())

        assert action[0] == "complete"
        assert type(action[1]) is HandlerResult
        assert action[1].value == 42
