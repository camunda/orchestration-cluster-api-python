from __future__ import annotations

import attrs
from typing import Callable, Literal, Protocol, Any, runtime_checkable, Awaitable, Coroutine, Union, Tuple
from dataclasses import dataclass
from .logging import SdkLogger, NullLogger
from camunda_orchestration_sdk.models.activate_jobs_jobs_item import ActivateJobsJobsItem
from camunda_orchestration_sdk.models.complete_job_data import CompleteJobData
from camunda_orchestration_sdk import CamundaAsyncClient
_EFFECTIVE_EXECUTION_STRATEGY = Literal["thread", "process", "async"]
EXECUTION_STRATEGY = _EFFECTIVE_EXECUTION_STRATEGY | Literal["auto"]
ActionComplete = Tuple[
    Literal["complete"], Union[dict[str, Any], CompleteJobData, None]
]
ActionFail = Tuple[Literal["fail"], Tuple[str, int | None, int]]
ActionError = Tuple[Literal["error"], Tuple[str, str]]
ActionSubprocessError = Tuple[Literal["subprocess_error"], str]
JobAction = Union[ActionComplete, ActionFail, ActionError, ActionSubprocessError]
@runtime_checkable
class HintedCallable(Protocol):
    _execution_hint: _EFFECTIVE_EXECUTION_STRATEGY
    def __call__(self, job: Any) -> dict[str, Any] | None | Awaitable[dict[str, Any] | None]: ...
@attrs.define
class JobContext(ActivateJobsJobsItem):
    log: SdkLogger = attrs.field(factory=lambda: SdkLogger(NullLogger()))
    @classmethod
    def from_job(cls, job: ActivateJobsJobsItem, logger: SdkLogger | None = None) -> "JobContext": ...
AsyncJobHandler = Callable[
    [JobContext], Coroutine[Any, Any, dict[str, Any] | CompleteJobData | None]
]
SyncJobHandler = Callable[[JobContext], dict[str, Any] | None]
JobHandler = AsyncJobHandler | SyncJobHandler | HintedCallable
@dataclass
class WorkerConfig:
    job_type: str
    job_timeout_milliseconds: int
    request_timeout_milliseconds: int = 0
    max_concurrent_jobs: int = 10
    execution_strategy: EXECUTION_STRATEGY = "auto"
    fetch_variables: list[str] | None = None
    worker_name: str = "camunda-python-sdk-worker"
class ExecutionHint:
    @staticmethod
    def prefer(strategy: _EFFECTIVE_EXECUTION_STRATEGY) -> Callable[[Callable[..., Any]], HintedCallable]: ...
    @staticmethod
    def permit(strategy: _EFFECTIVE_EXECUTION_STRATEGY) -> Callable[[Callable[..., Any]], HintedCallable]: ...
class JobError(Exception):
    def __init__(self, error_code: str, message: str = "") -> None: ...
class JobFailure(Exception):
    def __init__(self, message: str, retries: int | None = None, retry_back_off: int = 0) -> None: ...
def _execute_task_isolated(callback: JobHandler, job_context: JobContext) -> JobAction | None: ...
class JobWorker:
    _strategy: _EFFECTIVE_EXECUTION_STRATEGY = "async"
    def __init__(self, client: "CamundaAsyncClient", callback: JobHandler, config: WorkerConfig, logger: SdkLogger | None = None) -> None: ...
    def _run_worker_loop(self) -> None: ...
    def _determine_strategy(self) -> _EFFECTIVE_EXECUTION_STRATEGY: ...
    def _validate_strategy(self) -> None: ...
    def _decrement_active_jobs(self) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    async def poll_loop(self) -> None: ...
    async def _poll_for_jobs(self) -> None: ...
    async def _execute_job(self, job_item: ActivateJobsJobsItem) -> None: ...
