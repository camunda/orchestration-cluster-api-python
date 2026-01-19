from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping, TypedDict, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator


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


class CamundaSdkConfigPartial(TypedDict, total=False):
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

    # Optional OAuth disk cache / tarpit persistence
    CAMUNDA_TOKEN_CACHE_DIR: str
    CAMUNDA_TOKEN_DISK_CACHE_DISABLE: bool

    # Optional .env file loading
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


def _dotenv_values_for(load_envfile: Any) -> dict[str, str]:
    """Return values from a .env file, without mutating os.environ.

    This is a resolver-only feature flag; it must not leak into the validated
    Pydantic configuration model.
    """

    if load_envfile in (None, "", False):
        return {}

    try:
        from dotenv import dotenv_values
        from pathlib import Path

        if load_envfile is True:
            value = "true"
        else:
            value = str(load_envfile).strip()

        if not value:
            return {}

        if value.lower() in ("true", "1", "yes"):
            envfile_path = Path.cwd() / ".env"
        else:
            envfile_path = Path(value).expanduser().resolve()

        if not envfile_path.exists():
            return {}

        raw = dotenv_values(envfile_path)
        return {k: v for k, v in raw.items() if k and v is not None}
    except ImportError:
        # python-dotenv not installed, silently skip
        return {}
    except Exception:
        # Any other error loading .env file, silently skip
        return {}


def read_environment(environ: Mapping[str, str] | None = None) -> CamundaSdkConfigPartial:
    # Always operate on a copy to avoid mutating global process state while still
    # allowing us to merge .env-derived values.
    env: dict[str, str] = dict(os.environ) if environ is None else dict(environ)
    
    # Check if we should load a .env file
    load_envfile = env.get("CAMUNDA_LOAD_ENVFILE", "").strip()
    if load_envfile:
        dotenv_dict = _dotenv_values_for(load_envfile)
        # Merge with existing env, giving precedence to existing env vars
        for key, value in dotenv_dict.items():
            if key not in env:
                env[key] = value
    
    out: dict[str, str] = {}
    for key in CAMUNDA_SDK_CONFIG_KEYS:
        if key in env:
            out[key] = env[key]
    return out  # type: ignore[return-value]


class CamundaSdkConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # REST
    ZEEBE_REST_ADDRESS: str = Field(default="http://localhost:8080/v2")
    CAMUNDA_REST_ADDRESS: str = Field(default="http://localhost:8080/v2")

    # OAuth
    CAMUNDA_TOKEN_AUDIENCE: str = Field(default="zeebe.camunda.io")
    CAMUNDA_OAUTH_URL: str = Field(default="https://login.cloud.camunda.io/oauth/token")

    CAMUNDA_CLIENT_ID: str | None = None
    CAMUNDA_CLIENT_SECRET: str | None = None

    CAMUNDA_CLIENT_AUTH_CLIENTID: str | None = None
    CAMUNDA_CLIENT_AUTH_CLIENTSECRET: str | None = None

    # Auth strategy
    CAMUNDA_AUTH_STRATEGY: CamundaAuthStrategy = Field(default="NONE")

    CAMUNDA_BASIC_AUTH_USERNAME: str | None = None
    CAMUNDA_BASIC_AUTH_PASSWORD: str | None = None

    # Logging
    CAMUNDA_SDK_LOG_LEVEL: CamundaSdkLogLevel = Field(default="error")

    # OAuth disk cache / tarpit persistence
    # If CAMUNDA_TOKEN_CACHE_DIR is unset/None, the SDK will not write tokens to disk.
    CAMUNDA_TOKEN_CACHE_DIR: str | None = None
    CAMUNDA_TOKEN_DISK_CACHE_DISABLE: bool = Field(default=False)

    @staticmethod
    def _normalize_rest_address(value: str) -> str:
        value = value.strip()
        if not value:
            return value
        normalized = value.rstrip("/")
        if normalized.endswith("/v2"):
            return normalized
        return normalized + "/v2"

    @model_validator(mode="after")
    def _validate_required_when(self) -> "CamundaSdkConfiguration":
        # Normalize REST endpoints so users can supply either
        #   https://host/<clusterId>
        # or
        #   https://host/<clusterId>/v2
        # and the SDK will consistently call /v2/...
        self.ZEEBE_REST_ADDRESS = self._normalize_rest_address(self.ZEEBE_REST_ADDRESS)
        self.CAMUNDA_REST_ADDRESS = self._normalize_rest_address(self.CAMUNDA_REST_ADDRESS)

        if self.CAMUNDA_AUTH_STRATEGY == "BASIC":
            if not self.CAMUNDA_BASIC_AUTH_USERNAME:
                raise ValueError(
                    "CAMUNDA_BASIC_AUTH_USERNAME is required when CAMUNDA_AUTH_STRATEGY=BASIC"
                )
            if not self.CAMUNDA_BASIC_AUTH_PASSWORD:
                raise ValueError(
                    "CAMUNDA_BASIC_AUTH_PASSWORD is required when CAMUNDA_AUTH_STRATEGY=BASIC"
                )

        if self.CAMUNDA_AUTH_STRATEGY == "OAUTH":
            if not self.CAMUNDA_CLIENT_ID:
                raise ValueError(
                    "CAMUNDA_CLIENT_ID is required when CAMUNDA_AUTH_STRATEGY=OAUTH"
                )
            if not self.CAMUNDA_CLIENT_SECRET:
                raise ValueError(
                    "CAMUNDA_CLIENT_SECRET is required when CAMUNDA_AUTH_STRATEGY=OAUTH"
                )

        return self


@dataclass(frozen=True)
class ResolvedCamundaSdkConfiguration:
    effective: CamundaSdkConfiguration
    environment: CamundaSdkConfigPartial
    explicit: CamundaSdkConfigPartial | None


class ConfigurationResolver:
    """Resolves an effective configuration from environment + explicit overrides."""

    _ALIAS_PAIRS: tuple[tuple[str, str, str | None], ...] = (
        ("ZEEBE_REST_ADDRESS", "CAMUNDA_REST_ADDRESS", "http://localhost:8080/v2"),
        ("CAMUNDA_CLIENT_ID", "CAMUNDA_CLIENT_AUTH_CLIENTID", None),
        ("CAMUNDA_CLIENT_SECRET", "CAMUNDA_CLIENT_AUTH_CLIENTSECRET", None),
    )

    def __init__(
        self,
        environment: CamundaSdkConfigPartial | Mapping[str, Any],
        explicit_configuration: CamundaSdkConfigPartial | Mapping[str, Any] | None = None,
    ):
        self._environment: dict[str, Any] = dict(environment)
        self._explicit: dict[str, Any] | None = (
            dict(explicit_configuration) if explicit_configuration is not None else None
        )

    def resolve(self) -> ResolvedCamundaSdkConfiguration:
        explicit_envfile = None
        if self._explicit is not None and "CAMUNDA_LOAD_ENVFILE" in self._explicit:
            explicit_envfile = self._explicit.get("CAMUNDA_LOAD_ENVFILE")

        envfile_values = _dotenv_values_for(
            explicit_envfile
            if explicit_envfile not in (None, "")
            else self._environment.get("CAMUNDA_LOAD_ENVFILE")
        )

        # Precedence: .env < environment < explicit
        merged: dict[str, Any] = {**envfile_values, **self._environment, **(self._explicit or {})}
        merged.pop("CAMUNDA_LOAD_ENVFILE", None)

        # Alias resolution needs to consider .env-provided values as "environment"
        # input, otherwise it may incorrectly drop them.
        env_for_alias = {**envfile_values, **self._environment}
        merged = self._apply_alias_resolution(merged, env_for_alias, self._explicit)

        # Infer an auth strategy only if the user did NOT explicitly set one.
        # (Defaults do not count as explicit.)
        if "CAMUNDA_AUTH_STRATEGY" not in merged:
            def _non_empty(value: Any) -> bool:
                if value is None:
                    return False
                if isinstance(value, str):
                    return bool(value.strip())
                return True

            has_oauth_creds = _non_empty(merged.get("CAMUNDA_CLIENT_ID")) and _non_empty(
                merged.get("CAMUNDA_CLIENT_SECRET")
            )
            has_basic_creds = _non_empty(merged.get("CAMUNDA_BASIC_AUTH_USERNAME")) and _non_empty(
                merged.get("CAMUNDA_BASIC_AUTH_PASSWORD")
            )

            if has_oauth_creds:
                merged["CAMUNDA_AUTH_STRATEGY"] = "OAUTH"
            elif has_basic_creds:
                merged["CAMUNDA_AUTH_STRATEGY"] = "BASIC"

        try:
            effective = CamundaSdkConfiguration.model_validate(merged)
        except ValidationError as e:
            # Surface as-is; tests rely on pydantic's rich errors.
            raise e

        return ResolvedCamundaSdkConfiguration(
            effective=effective,
            environment=self._environment, # type: ignore
            explicit=self._explicit, # type: ignore
        )

    @classmethod
    def _apply_alias_resolution(
        cls,
        merged: dict[str, Any],
        environment: Mapping[str, Any],
        explicit: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        explicit_map: Mapping[str, Any] = explicit or {}

        for left, right, default in cls._ALIAS_PAIRS:
            value = cls._resolve_alias_value(
                left=left,
                right=right,
                environment=environment,
                explicit=explicit_map,
                default=default,
            )

            # Ensure the effective config always has both keys.
            if value is not None:
                merged[left] = value
                merged[right] = value
            else:
                merged.pop(left, None)
                merged.pop(right, None)

        return merged

    @staticmethod
    def _resolve_alias_value(
        *,
        left: str,
        right: str,
        environment: Mapping[str, Any],
        explicit: Mapping[str, Any],
        default: str | None,
    ) -> Any:
        def _is_set(source: Mapping[str, Any], key: str) -> bool:
            return key in source and source[key] is not None

        # Explicit wins over environment even if it uses the other alias.
        explicit_left_set = _is_set(explicit, left)
        explicit_right_set = _is_set(explicit, right)

        if explicit_left_set and explicit_right_set and explicit[left] != explicit[right]:
            raise ValueError(
                f"Conflicting explicit configuration: {left}={explicit[left]!r} != {right}={explicit[right]!r}"
            )
        if explicit_left_set or explicit_right_set:
            return explicit[left] if explicit_left_set else explicit[right]

        env_left_set = _is_set(environment, left)
        env_right_set = _is_set(environment, right)

        if env_left_set and env_right_set and environment[left] != environment[right]:
            raise ValueError(
                f"Conflicting environment configuration: {left}={environment[left]!r} != {right}={environment[right]!r}"
            )
        if env_left_set or env_right_set:
            return environment[left] if env_left_set else environment[right]

        return default
