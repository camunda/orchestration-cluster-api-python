"""Tests for heritable worker configuration defaults (issue #25).

Worker config fields can be set via environment variables. The precedence is:
    explicit WorkerConfig value > CAMUNDA_WORKER_* env var > hardcoded default
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from camunda_orchestration_sdk.runtime.job_worker import (
    JobWorker,
    WorkerConfig,
    resolve_worker_config,
)
from camunda_orchestration_sdk.runtime.configuration_resolver import (
    CamundaSdkConfiguration,
)
from camunda_orchestration_sdk.models.job_activation_result import (
    JobActivationResult,
)


@pytest.fixture(autouse=True)
def _clear_worker_env(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    for key in (
        "CAMUNDA_WORKER_TIMEOUT",
        "CAMUNDA_WORKER_MAX_CONCURRENT_JOBS",
        "CAMUNDA_WORKER_REQUEST_TIMEOUT",
        "CAMUNDA_WORKER_NAME",
        "CAMUNDA_WORKER_STARTUP_JITTER_MAX_SECONDS",
    ):
        monkeypatch.delenv(key, raising=False)


def _make_config(**overrides: object) -> CamundaSdkConfiguration:
    """Create a minimal CamundaSdkConfiguration with worker overrides."""
    return CamundaSdkConfiguration.model_validate(overrides)


# -- resolve_worker_config tests --


def test_resolve_uses_env_var_for_timeout():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=5000)
    wc = WorkerConfig(job_type="test")
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.job_timeout_milliseconds == 5000


def test_resolve_explicit_timeout_overrides_env():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=5000)
    wc = WorkerConfig(job_type="test", job_timeout_milliseconds=9000)
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.job_timeout_milliseconds == 9000


def test_resolve_raises_when_no_timeout():
    cfg = _make_config()
    wc = WorkerConfig(job_type="test")
    with pytest.raises(ValueError, match="job_timeout_milliseconds is required"):
        resolve_worker_config(wc, cfg)


def test_resolve_uses_env_var_for_max_concurrent_jobs():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000, CAMUNDA_WORKER_MAX_CONCURRENT_JOBS=32)
    wc = WorkerConfig(job_type="test")
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.max_concurrent_jobs == 32


def test_resolve_explicit_max_concurrent_overrides_env():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000, CAMUNDA_WORKER_MAX_CONCURRENT_JOBS=32)
    wc = WorkerConfig(job_type="test", max_concurrent_jobs=8)
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.max_concurrent_jobs == 8


def test_resolve_defaults_max_concurrent_to_10():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000)
    wc = WorkerConfig(job_type="test")
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.max_concurrent_jobs == 10


def test_resolve_uses_env_var_for_request_timeout():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000, CAMUNDA_WORKER_REQUEST_TIMEOUT=3000)
    wc = WorkerConfig(job_type="test")
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.request_timeout_milliseconds == 3000


def test_resolve_defaults_request_timeout_to_0():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000)
    wc = WorkerConfig(job_type="test")
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.request_timeout_milliseconds == 0


def test_resolve_uses_env_var_for_worker_name():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000, CAMUNDA_WORKER_NAME="my-app-worker")
    wc = WorkerConfig(job_type="test")
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.worker_name == "my-app-worker"


def test_resolve_explicit_worker_name_overrides_env():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000, CAMUNDA_WORKER_NAME="env-name")
    wc = WorkerConfig(job_type="test", worker_name="explicit-name")
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.worker_name == "explicit-name"


def test_resolve_defaults_worker_name():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000)
    wc = WorkerConfig(job_type="test")
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.worker_name == "camunda-python-sdk-worker"


def test_resolve_preserves_job_type():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000)
    wc = WorkerConfig(job_type="payment-service")
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.job_type == "payment-service"


def test_resolve_preserves_fetch_variables():
    cfg = _make_config(CAMUNDA_WORKER_TIMEOUT=1000)
    wc = WorkerConfig(job_type="test", fetch_variables=["orderId", "amount"])
    resolved = resolve_worker_config(wc, cfg)
    assert resolved.fetch_variables == ["orderId", "amount"]


# -- JobWorker directly with WorkerConfig (backward compat) --


def test_worker_applies_hardcoded_defaults_when_none():
    """JobWorker.__init__ applies hardcoded defaults for None sentinel fields."""
    client = MagicMock()
    client.activate_jobs = AsyncMock(return_value=JobActivationResult(jobs=[]))

    wc = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(client, lambda j: None, wc)

    assert worker.config.max_concurrent_jobs == 10
    assert worker.config.request_timeout_milliseconds == 0
    assert worker.config.worker_name == "camunda-python-sdk-worker"


def test_worker_raises_on_missing_timeout():
    """JobWorker.__init__ raises if job_timeout_milliseconds is None and no env var."""
    client = MagicMock()
    wc = WorkerConfig(job_type="test")
    with pytest.raises(ValueError, match="job_timeout_milliseconds is required"):
        JobWorker(client, lambda j: None, wc)


# -- End-to-end via CamundaAsyncClient --


def test_client_worker_inherits_env_timeout(monkeypatch: pytest.MonkeyPatch):
    """CamundaAsyncClient.create_job_worker uses CAMUNDA_WORKER_TIMEOUT."""
    monkeypatch.setenv("CAMUNDA_WORKER_TIMEOUT", "7000")
    from camunda_orchestration_sdk import CamundaAsyncClient

    client = CamundaAsyncClient()
    wc = WorkerConfig(job_type="test")
    worker = client.create_job_worker(wc, lambda j: None, auto_start=False)
    assert worker.config.job_timeout_milliseconds == 7000


def test_client_worker_inherits_env_max_concurrent(monkeypatch: pytest.MonkeyPatch):
    """CamundaAsyncClient.create_job_worker uses CAMUNDA_WORKER_MAX_CONCURRENT_JOBS."""
    monkeypatch.setenv("CAMUNDA_WORKER_TIMEOUT", "1000")
    monkeypatch.setenv("CAMUNDA_WORKER_MAX_CONCURRENT_JOBS", "64")
    from camunda_orchestration_sdk import CamundaAsyncClient

    client = CamundaAsyncClient()
    wc = WorkerConfig(job_type="test")
    worker = client.create_job_worker(wc, lambda j: None, auto_start=False)
    assert worker.config.max_concurrent_jobs == 64


def test_client_worker_explicit_overrides_env(monkeypatch: pytest.MonkeyPatch):
    """Explicit WorkerConfig values win over CAMUNDA_WORKER_* env vars."""
    monkeypatch.setenv("CAMUNDA_WORKER_TIMEOUT", "7000")
    monkeypatch.setenv("CAMUNDA_WORKER_MAX_CONCURRENT_JOBS", "64")
    from camunda_orchestration_sdk import CamundaAsyncClient

    client = CamundaAsyncClient()
    wc = WorkerConfig(job_type="test", job_timeout_milliseconds=3000, max_concurrent_jobs=4)
    worker = client.create_job_worker(wc, lambda j: None, auto_start=False)
    assert worker.config.job_timeout_milliseconds == 3000
    assert worker.config.max_concurrent_jobs == 4


def test_client_worker_inherits_startup_jitter(monkeypatch: pytest.MonkeyPatch):
    """CamundaAsyncClient.create_job_worker uses CAMUNDA_WORKER_STARTUP_JITTER_MAX_SECONDS."""
    monkeypatch.setenv("CAMUNDA_WORKER_TIMEOUT", "1000")
    monkeypatch.setenv("CAMUNDA_WORKER_STARTUP_JITTER_MAX_SECONDS", "5.0")
    from camunda_orchestration_sdk import CamundaAsyncClient

    client = CamundaAsyncClient()
    wc = WorkerConfig(job_type="test")
    worker = client.create_job_worker(wc, lambda j: None, auto_start=False)
    assert worker._startup_jitter_max_seconds == 5.0  # pyright: ignore[reportPrivateUsage]


def test_client_constructor_worker_defaults():
    """CamundaAsyncClient accepts worker defaults via the config dict."""
    from camunda_orchestration_sdk import CamundaAsyncClient

    client = CamundaAsyncClient(
        configuration={
            "CAMUNDA_WORKER_TIMEOUT": "5000",
            "CAMUNDA_WORKER_MAX_CONCURRENT_JOBS": "16",
            "CAMUNDA_WORKER_NAME": "my-app",
        }
    )
    wc = WorkerConfig(job_type="test")
    worker = client.create_job_worker(wc, lambda j: None, auto_start=False)
    assert worker.config.job_timeout_milliseconds == 5000
    assert worker.config.max_concurrent_jobs == 16
    assert worker.config.worker_name == "my-app"
