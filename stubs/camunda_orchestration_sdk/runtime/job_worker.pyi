from __future__ import annotations

import attrs
from typing import Callable, Literal, Any, Coroutine, Union, Tuple
from dataclasses import dataclass
from .logging import SdkLogger, NullLogger
from camunda_orchestration_sdk.models.activated_job_result import ActivatedJobResult
from camunda_orchestration_sdk.models.job_completion_request import JobCompletionRequest
from camunda_orchestration_sdk import CamundaAsyncClient, CamundaClient
_EFFECTIVE_EXECUTION_STRATEGY = Literal["thread", "process", "async"]
EXECUTION_STRATEGY = _EFFECTIVE_EXECUTION_STRATEGY | Literal["auto"]
ActionComplete = Tuple[
    Literal["complete"], Union[dict[str, Any], JobCompletionRequest, None]
]
ActionFail = Tuple[Literal["fail"], Tuple[str, int | None, int]]
ActionError = Tuple[Literal["error"], Tuple[str, str]]
ActionSubprocessError = Tuple[Literal["subprocess_error"], str]
JobAction = Union[ActionComplete, ActionFail, ActionError, ActionSubprocessError]
@attrs.define
class JobContext(ActivatedJobResult):
    log: SdkLogger = attrs.field(factory=lambda: SdkLogger(NullLogger()))
    @classmethod
    def from_job(cls, job: ActivatedJobResult, logger: SdkLogger | None = None) -> "JobContext": ...
@attrs.define
class ConnectedJobContext(JobContext):
    client: "CamundaAsyncClient" = attrs.field(kw_only=True, repr=False, eq=False)
    @classmethod
    def create(cls, job: ActivatedJobResult, client: "CamundaAsyncClient", logger: SdkLogger | None = None) -> "ConnectedJobContext": ...
AsyncJobContext = ConnectedJobContext
@attrs.define
class SyncJobContext(JobContext):
    client: "CamundaClient" = attrs.field(kw_only=True, repr=False, eq=False)
    @classmethod
    def create(cls, job: ActivatedJobResult, client: "CamundaClient", logger: SdkLogger | None = None) -> "SyncJobContext": ...
ConnectedAsyncJobHandler = Callable[
    [ConnectedJobContext],
    Coroutine[Any, Any, dict[str, Any] | JobCompletionRequest | None],
]
ConnectedSyncJobHandler = Callable[[SyncJobContext], dict[str, Any] | JobCompletionRequest | None]
ConnectedJobHandler = ConnectedAsyncJobHandler | ConnectedSyncJobHandler
IsolatedAsyncJobHandler = Callable[
    [JobContext], Coroutine[Any, Any, dict[str, Any] | JobCompletionRequest | None]
]
IsolatedSyncJobHandler = Callable[[JobContext], dict[str, Any] | JobCompletionRequest | None]
IsolatedJobHandler = IsolatedAsyncJobHandler | IsolatedSyncJobHandler
JobHandler = ConnectedJobHandler | IsolatedJobHandler
AsyncJobHandler = IsolatedAsyncJobHandler
SyncJobHandler = IsolatedSyncJobHandler
@dataclass
class WorkerConfig:
    job_type: str
    job_timeout_milliseconds: int | None = None
    request_timeout_milliseconds: int | None = None
    max_concurrent_jobs: int | None = None
    fetch_variables: list[str] | None = None
    worker_name: str | None = None
def resolve_worker_config(config: WorkerConfig, configuration: Any) -> WorkerConfig: ...
@dataclass
class _ResolvedWorkerConfig:
    job_type: str
    job_timeout_milliseconds: int
    request_timeout_milliseconds: int
    max_concurrent_jobs: int
    fetch_variables: list[str] | None
    worker_name: str
class JobError(Exception):
    def __init__(self, error_code: str, message: str = "") -> None: ...
class JobFailure(Exception):
    def __init__(self, message: str, retries: int | None = None, retry_back_off: int = 0) -> None: ...
def _execute_task_isolated(callback: JobHandler, job_context: JobContext) -> JobAction | None: ...
class JobWorker:
    _strategy: _EFFECTIVE_EXECUTION_STRATEGY = "async"
    def __init__(self, client: "CamundaAsyncClient", callback: JobHandler, config: WorkerConfig, logger: SdkLogger | None = None, execution_strategy: EXECUTION_STRATEGY = "auto", startup_jitter_max_seconds: float = 0) -> None: ...
    def _run_worker_loop(self) -> None: ...
    def _determine_strategy(self) -> _EFFECTIVE_EXECUTION_STRATEGY: ...
    def _validate_strategy(self) -> None: ...
    def _get_sync_client(self) -> "CamundaClient": ...
    def _decrement_active_jobs(self) -> None: ...
    def start(self) -> None: ...
    async def _start_with_jitter(self, jitter: float) -> None: ...
    def stop(self) -> None: ...
    async def poll_loop(self) -> None: ...
    async def _poll_for_jobs(self) -> None: ...
    async def _execute_job(self, job_item: ActivatedJobResult) -> None: ...
