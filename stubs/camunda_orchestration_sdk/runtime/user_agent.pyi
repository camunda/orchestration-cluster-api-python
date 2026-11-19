from __future__ import annotations

from functools import lru_cache
import httpx
from .cluster_admin_url import HttpxArgs

SDK_USER_AGENT_PRODUCT = "camunda-orchestration-sdk-python"
_DISTRIBUTION_NAME = "camunda-orchestration-sdk"
_HTTPX_DEFAULT_PREFIX = "python-httpx/"

@lru_cache(maxsize=1)
def sdk_version() -> str: ...
def sdk_user_agent() -> str: ...
def build_user_agent(application_user_agent: str | None = None) -> str: ...
def _is_httpx_default(value: str) -> bool: ...
def _apply_user_agent(request: httpx.Request, user_agent: str) -> None: ...
def inject_user_agent_hook(
    httpx_args: HttpxArgs | None,
    *,
    application_user_agent: str | None = None,
    async_client: bool = False,
) -> HttpxArgs: ...
