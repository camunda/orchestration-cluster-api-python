from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, TypedDict, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

CamundaAuthStrategy = Literal["NONE", "OAUTH", "BASIC"]
CamundaSdkLogLevel = Literal[
    "silent",
    "error",
    "warn",
    "info",
    "debug",
    "trace",
    "silly",
]

class CamundaSdkConfigPartial(TypedDict):
    ZEEBE_REST_ADDRESS: str
    CAMUNDA_REST_ADDRESS: str
    CAMUNDA_TOKEN_AUDIENCE: str
    CAMUNDA_OAUTH_URL: str
    CAMUNDA_AUTH_STRATEGY: CamundaAuthStrategy
    CAMUNDA_BASIC_AUTH_USERNAME: str
    CAMUNDA_BASIC_AUTH_PASSWORD: str
    CAMUNDA_CLIENT_ID: str
    CAMUNDA_CLIENT_SECRET: str
    CAMUNDA_CLIENT_AUTH_CLIENTID: str
    CAMUNDA_CLIENT_AUTH_CLIENTSECRET: str
    CAMUNDA_SDK_LOG_LEVEL: CamundaSdkLogLevel
    CAMUNDA_TOKEN_CACHE_DIR: str
    CAMUNDA_TOKEN_DISK_CACHE_DISABLE: bool
    CAMUNDA_LOAD_ENVFILE: str

CAMUNDA_SDK_CONFIG_KEYS: tuple[str, ...] = (
    "ZEEBE_REST_ADDRESS",
    "CAMUNDA_REST_ADDRESS",
    "CAMUNDA_TOKEN_AUDIENCE",
    "CAMUNDA_OAUTH_URL",
    "CAMUNDA_AUTH_STRATEGY",
    "CAMUNDA_BASIC_AUTH_USERNAME",
    "CAMUNDA_BASIC_AUTH_PASSWORD",
    "CAMUNDA_CLIENT_ID",
    "CAMUNDA_CLIENT_SECRET",
    "CAMUNDA_CLIENT_AUTH_CLIENTID",
    "CAMUNDA_CLIENT_AUTH_CLIENTSECRET",
    "CAMUNDA_SDK_LOG_LEVEL",
    # Optional OAuth disk cache / tarpit persistence
    "CAMUNDA_TOKEN_CACHE_DIR",
    "CAMUNDA_TOKEN_DISK_CACHE_DISABLE",
)

def _dotenv_values_for(load_envfile: Any) -> dict[str, str]: ...
def read_environment(
    environ: Mapping[str, str] | None = None,
) -> CamundaSdkConfigPartial: ...

class CamundaSdkConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ZEEBE_REST_ADDRESS: str = Field(
        default="http://localhost:8080/v2",
        description="REST API base URL (alias for CAMUNDA_REST_ADDRESS).",
    )
    CAMUNDA_REST_ADDRESS: str = Field(
        default="http://localhost:8080/v2",
        description="REST API base URL. `/v2` is appended automatically if missing.",
    )
    CAMUNDA_TOKEN_AUDIENCE: str = Field(
        default="zeebe.camunda.io",
        description="OAuth token audience.",
    )
    CAMUNDA_OAUTH_URL: str = Field(
        default="https://login.cloud.camunda.io/oauth/token",
        description="OAuth token endpoint URL.",
    )
    CAMUNDA_CLIENT_ID: str | None = Field(
        default=None,
        description="OAuth client ID.",
    )
    CAMUNDA_CLIENT_SECRET: str | None = Field(
        default=None,
        description="OAuth client secret.",
    )
    CAMUNDA_CLIENT_AUTH_CLIENTID: str | None = Field(
        default=None,
        description="Alias for CAMUNDA_CLIENT_ID.",
    )
    CAMUNDA_CLIENT_AUTH_CLIENTSECRET: str | None = Field(
        default=None,
        description="Alias for CAMUNDA_CLIENT_SECRET.",
    )
    CAMUNDA_AUTH_STRATEGY: CamundaAuthStrategy = Field(
        default="NONE",
        description="Authentication strategy: NONE, OAUTH, or BASIC. Auto-inferred from credentials if omitted.",
    )
    CAMUNDA_BASIC_AUTH_USERNAME: str | None = Field(
        default=None,
        description="Basic auth username. Required when CAMUNDA_AUTH_STRATEGY=BASIC.",
    )
    CAMUNDA_BASIC_AUTH_PASSWORD: str | None = Field(
        default=None,
        description="Basic auth password. Required when CAMUNDA_AUTH_STRATEGY=BASIC.",
    )
    CAMUNDA_SDK_LOG_LEVEL: CamundaSdkLogLevel = Field(
        default="error",
        description="SDK log level: silent, error, warn, info, debug, trace, or silly.",
    )
    CAMUNDA_TOKEN_CACHE_DIR: str | None = Field(
        default=None,
        description="Directory for OAuth token disk cache. Disabled if unset.",
    )
    CAMUNDA_TOKEN_DISK_CACHE_DISABLE: bool = Field(
        default=False,
        description="Disable OAuth token disk caching.",
    )
    @staticmethod
    def _normalize_rest_address(value: str) -> str: ...
    @model_validator(mode="after")
    def _validate_required_when(self) -> "CamundaSdkConfiguration": ...

@dataclass(frozen=True)
class ResolvedCamundaSdkConfiguration:
    effective: CamundaSdkConfiguration
    environment: CamundaSdkConfigPartial
    explicit: CamundaSdkConfigPartial | None

class ConfigurationResolver:
    _ALIAS_PAIRS: tuple[tuple[str, str, str | None], ...] = (
        ("ZEEBE_REST_ADDRESS", "CAMUNDA_REST_ADDRESS", "http://localhost:8080/v2"),
        ("CAMUNDA_CLIENT_ID", "CAMUNDA_CLIENT_AUTH_CLIENTID", None),
        ("CAMUNDA_CLIENT_SECRET", "CAMUNDA_CLIENT_AUTH_CLIENTSECRET", None),
    )
    def __init__(
        self,
        environment: CamundaSdkConfigPartial | Mapping[str, Any],
        explicit_configuration: CamundaSdkConfigPartial
        | Mapping[str, Any]
        | None = None,
    ) -> None: ...
    def resolve(self) -> ResolvedCamundaSdkConfiguration: ...
    @classmethod
    def _apply_alias_resolution(
        cls,
        merged: dict[str, Any],
        environment: Mapping[str, Any],
        explicit: Mapping[str, Any] | None,
    ) -> dict[str, Any]: ...
    @staticmethod
    def _resolve_alias_value(
        left: str,
        right: str,
        environment: Mapping[str, Any],
        explicit: Mapping[str, Any],
        default: str | None,
    ) -> Any: ...
