"""A response missing a required field fails clearly (issue #287).

Since Camunda 8.9 every response field is required and absent values are sent as explicit null
(camunda/camunda#46165, #46175), so a missing key is a contract violation, usually SDK/server
version skew. It used to surface as a bare ``KeyError: 'jobLeaseToken'``, which the job worker
logged and retried forever until it reached the caller as a gateway 504. It must stay a failure,
but name the model and field, and stop the worker rather than loop.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from camunda_orchestration_sdk.errors import MissingRequiredFieldError
from camunda_orchestration_sdk.models.agent_tool import AgentTool
from camunda_orchestration_sdk.models.job_activation_result import JobActivationResult
from camunda_orchestration_sdk.runtime.clock import ManualClock
from camunda_orchestration_sdk.runtime.job_worker import JobWorker, WorkerConfig

REPO_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = REPO_ROOT / "generated" / "camunda_orchestration_sdk" / "models"

_hook_path = REPO_ROOT / "hooks" / "post_gen" / "1260_required_field_errors.py"
_loader = importlib.util.spec_from_file_location("_required_field_errors_hook", _hook_path)
assert _loader and _loader.loader
_hook = importlib.util.module_from_spec(_loader)
_loader.loader.exec_module(_hook)


# --- behaviour --------------------------------------------------------------------------------


def test_a_missing_required_field_names_the_model_and_field() -> None:
    with pytest.raises(MissingRequiredFieldError) as raised:
        AgentTool.from_dict({"name": "lookup", "elementId": None})
    assert (raised.value.model, raised.value.field) == ("AgentTool", "description")
    message = str(raised.value)
    assert "AgentTool" in message and "'description'" in message and "version" in message


def test_it_is_still_a_key_error() -> None:
    # Union parsers fall back to the next variant on KeyError; that must keep working.
    with pytest.raises(KeyError):
        AgentTool.from_dict({})


def test_explicit_null_still_decodes() -> None:
    tool = AgentTool.from_dict({"name": "lookup", "description": None, "elementId": None})
    assert (tool.description, tool.element_id) == (None, None)


def test_a_nested_model_reports_itself_not_its_parent() -> None:
    with pytest.raises(MissingRequiredFieldError) as raised:
        JobActivationResult.from_dict({"jobs": [{"type": "t"}]})
    assert raised.value.model == "ActivatedJobResult"


@pytest.mark.asyncio
async def test_the_job_worker_stops_instead_of_retrying_forever() -> None:
    polls = 0

    async def activate_jobs(**_: object) -> JobActivationResult:
        nonlocal polls
        polls += 1
        if polls > 3:  # bound a regression that retries, so it fails instead of hanging
            worker.running = False
            return JobActivationResult(jobs=[])
        raise MissingRequiredFieldError("ActivatedJobResult", "jobLeaseToken")

    client = MagicMock()
    client.activate_jobs = activate_jobs
    worker = JobWorker(
        client,
        lambda job: {},
        WorkerConfig(job_type="t", job_timeout_milliseconds=1000),
        clock=ManualClock(),
    )
    worker.running = True  # poll_loop is a no-op otherwise

    with pytest.raises(MissingRequiredFieldError):
        await worker.poll_loop()
    assert (polls, worker.running) == (1, False)


# --- hook -------------------------------------------------------------------------------------

_MODEL = (
    "from __future__ import annotations\n"
    "from ..types import UNSET, Unset\n"
    "\n"
    "class Thing:\n"
    "    @classmethod\n"
    "    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:\n"
    "        d = dict(src_dict)\n"
    '        name = d.pop("name")\n'
)


def test_rewrite_is_idempotent_and_leaves_defaulted_pops_alone() -> None:
    source = _MODEL + '        tags = d.pop("tags", UNSET)\n'
    once = _hook.rewrite_model(source)
    assert "d = RequiredFields(src_dict, cls.__name__)" in once
    assert 'd.pop_required("name")' in once
    assert 'd.pop("tags", UNSET)' in once
    assert _hook.rewrite_model(once) == once


def test_a_model_with_required_pops_but_an_unknown_dict_shape_is_an_error() -> None:
    with pytest.raises(SystemExit):
        _hook.rewrite_model(_MODEL.replace("d = dict(src_dict)", "d = {**src_dict}"))


# --- class guard over the real generated tree -------------------------------------------------


def test_every_model_with_required_fields_reports_them_by_name() -> None:
    bare_pop = re.compile(r'\bd\.pop\("[^"]+"\)')
    checked, unguarded = 0, []
    for module in sorted(MODELS_DIR.glob("*.py")):
        source = module.read_text(encoding="utf-8")
        if bare_pop.search(source):
            unguarded.append(f"{module.name}: bare d.pop() of a required field")
        elif "d.pop_required(" in source:
            checked += 1
            if "d = RequiredFields(src_dict, cls.__name__)" not in source:
                unguarded.append(f"{module.name}: pop_required on a plain dict")
    assert checked > 0, "no generated model pops a required field; the guard would be vacuous"
    assert unguarded == []
