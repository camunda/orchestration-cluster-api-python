from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping, TypedDict, Literal, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


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
CamundaBackpressureProfile = Literal["BALANCED", "LEGACY"]


#: Configuration keys whose value is a credential. Configuration errors fire at client
#: construction, so their messages land in application logs and crash reporters; these
#: values are replaced with a placeholder before any error text is built from them.
SECRET_CONFIG_KEYS: frozenset[str] = frozenset(
    {
        "CAMUNDA_CLIENT_SECRET",
        "CAMUNDA_CLIENT_AUTH_CLIENTSECRET",
        "CAMUNDA_BASIC_AUTH_PASSWORD",
        "CAMUNDA_MTLS_KEY",
        "CAMUNDA_MTLS_KEY_PASSPHRASE",
    }
)

REDACTED = "***redacted***"


def _render_config_value(key: str, value: object) -> str:
    """Render ``value`` for an error message, as a placeholder if it is a credential."""

    return REDACTED if key in SECRET_CONFIG_KEYS else repr(value)


def _redact_secret_values(values: Mapping[str, object]) -> dict[str, object]:
    """Copy ``values`` with every non-empty credential replaced by a placeholder.

    An empty or absent credential is left as it is. It is not a secret, and replacing
    it with a non-empty placeholder would let the redacted copy pass a presence check
    that the real configuration failed -- costing the user the diagnosis they came for.
    """

    return {
        k: (REDACTED if k in SECRET_CONFIG_KEYS and v not in (None, "") else v)
        for k, v in values.items()
    }


def _configuration_error_without_secrets(
    merged: Mapping[str, object], original: ValidationError
) -> Exception:
    """Return the error to raise for a rejected configuration, carrying no credential.

    Pydantic records the input it was handed on every error, so the rendered message
    repeats the whole merged configuration -- credentials included -- into whatever log
    or crash reporter catches a start-up failure. Validating a redacted copy yields the
    same diagnosis without them: the model's validators test for presence, not content,
    so a placeholder is rejected exactly where the real value was.

    The redacted copy is only a faithful diagnosis if it is rejected for the same reasons
    as the original. When the rejected value is a credential itself (a non-string passed
    in an explicit configuration dict, since environment variables are always strings) the
    placeholder is accepted, so that error is missing from the redacted copy -- whether
    the copy validates outright or fails only on some other invalid field. The original
    cannot be reused then, so the original's errors are rendered without their input.
    ``ValidationError`` is a ``ValueError``, so that narrower type still satisfies
    callers catching ``ValueError``.
    """

    redacted = _redact_secret_values(merged)
    if redacted == merged:
        return original
    try:
        CamundaSdkConfiguration.model_validate(redacted)
    except ValidationError as safe:
        if _error_signatures(safe) == _error_signatures(original):
            return safe
    details = "; ".join(
        "{loc}: {msg}".format(
            loc=".".join(str(part) for part in error["loc"]) or "<configuration>",
            msg=error["msg"],
        )
        for error in original.errors(include_input=False)
    )
    return ValueError(f"Invalid Camunda SDK configuration: {details}")


def _error_signatures(
    error: ValidationError,
) -> list[tuple[tuple[str | int, ...], str, str]]:
    """The location, type and message of each error, without the input it rejected."""

    return [(e["loc"], e["type"], e["msg"]) for e in error.errors(include_input=False)]


class CamundaSdkConfigPartial(TypedDict, total=False):
    ZEEBE_REST_ADDRESS: str
    CAMUNDA_REST_ADDRESS: str
    CAMUNDA_REST_ADDRESS_EXACT: str | bool

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
    CAMUNDA_TOKEN_DISK_CACHE_DISABLE: str

    # Backpressure profile
    CAMUNDA_SDK_BACKPRESSURE_PROFILE: str

    # Tenant
    CAMUNDA_TENANT_ID: str
    CAMUNDA_TENANT_IDS: str | list[str]

    # Worker defaults
    CAMUNDA_WORKER_TIMEOUT: str
    CAMUNDA_WORKER_MAX_CONCURRENT_JOBS: str
    CAMUNDA_WORKER_REQUEST_TIMEOUT: str
    CAMUNDA_WORKER_NAME: str
    CAMUNDA_WORKER_STARTUP_JITTER_MAX_SECONDS: str

    # HTTP connection pool
    CAMUNDA_HTTP_MAX_CONNECTIONS: str

    # Optional .env file loading
    CAMUNDA_LOAD_ENVFILE: str

    # mTLS
    CAMUNDA_MTLS_CERT_PATH: str
    CAMUNDA_MTLS_KEY_PATH: str
    CAMUNDA_MTLS_CA_PATH: str
    CAMUNDA_MTLS_CERT: str
    CAMUNDA_MTLS_KEY: str
    CAMUNDA_MTLS_CA: str
    CAMUNDA_MTLS_KEY_PASSPHRASE: str


CAMUNDA_SDK_CONFIG_KEYS: tuple[str, ...] = (
    "ZEEBE_REST_ADDRESS",
    "CAMUNDA_REST_ADDRESS",
    "CAMUNDA_REST_ADDRESS_EXACT",
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
    # Backpressure
    "CAMUNDA_SDK_BACKPRESSURE_PROFILE",
    # Tenant
    "CAMUNDA_TENANT_ID",
    "CAMUNDA_TENANT_IDS",
    # Worker defaults
    "CAMUNDA_WORKER_TIMEOUT",
    "CAMUNDA_WORKER_MAX_CONCURRENT_JOBS",
    "CAMUNDA_WORKER_REQUEST_TIMEOUT",
    "CAMUNDA_WORKER_NAME",
    "CAMUNDA_WORKER_STARTUP_JITTER_MAX_SECONDS",
    # HTTP connection pool
    "CAMUNDA_HTTP_MAX_CONNECTIONS",
    # mTLS
    "CAMUNDA_MTLS_CERT_PATH",
    "CAMUNDA_MTLS_KEY_PATH",
    "CAMUNDA_MTLS_CA_PATH",
    "CAMUNDA_MTLS_CERT",
    "CAMUNDA_MTLS_KEY",
    "CAMUNDA_MTLS_CA",
    "CAMUNDA_MTLS_KEY_PASSPHRASE",
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


def read_environment(
    environ: Mapping[str, str] | None = None,
) -> CamundaSdkConfigPartial:
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
    return cast(CamundaSdkConfigPartial, out)


class CamundaSdkConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # REST
    ZEEBE_REST_ADDRESS: str = Field(
        default="http://localhost:8080/v2",
        description="REST API base URL (alias for CAMUNDA_REST_ADDRESS).",
    )
    CAMUNDA_REST_ADDRESS: str = Field(
        default="http://localhost:8080/v2",
        description=(
            "REST API base URL. `/v2` is appended automatically if missing, "
            "unless CAMUNDA_REST_ADDRESS_EXACT is true."
        ),
    )
    CAMUNDA_REST_ADDRESS_EXACT: bool = Field(
        default=False,
        description=(
            "Use CAMUNDA_REST_ADDRESS / ZEEBE_REST_ADDRESS exactly as provided, "
            "without appending the `/v2` suffix. Useful for gateway- or "
            "proxy-fronted deployments whose base path does not follow the "
            "`.../v2` convention."
        ),
    )

    # OAuth
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
        # repr=False: a credential must not render in repr()/str() of the config, which
        # is where print(client.configuration), an f-string's %r and any traceback
        # renderer that shows locals would otherwise write it out.
        repr=False,
    )

    CAMUNDA_CLIENT_AUTH_CLIENTID: str | None = Field(
        default=None,
        description="Alias for CAMUNDA_CLIENT_ID.",
    )
    CAMUNDA_CLIENT_AUTH_CLIENTSECRET: str | None = Field(
        default=None,
        description="Alias for CAMUNDA_CLIENT_SECRET.",
        repr=False,
    )

    # Auth strategy
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
        repr=False,
    )

    # Logging
    CAMUNDA_SDK_LOG_LEVEL: CamundaSdkLogLevel = Field(
        default="error",
        description="SDK log level: silent, error, warn, info, debug, trace, or silly.",
    )

    # OAuth disk cache / tarpit persistence
    CAMUNDA_TOKEN_CACHE_DIR: str | None = Field(
        default=None,
        description="Directory for OAuth token disk cache. Disabled if unset.",
    )
    CAMUNDA_TOKEN_DISK_CACHE_DISABLE: bool = Field(
        default=False,
        description="Disable OAuth token disk caching.",
    )

    # Backpressure
    CAMUNDA_SDK_BACKPRESSURE_PROFILE: CamundaBackpressureProfile = Field(
        default="BALANCED",
        description="Backpressure profile: BALANCED (adaptive gating, default) or LEGACY (observe-only, no gating).",
    )

    # Tenant
    CAMUNDA_TENANT_ID: str | None = Field(
        default=None,
        description="Default tenant ID applied to all operations that accept a tenant_id parameter.",
    )
    CAMUNDA_TENANT_IDS: list[str] | None = Field(
        default=None,
        description=(
            "Default tenant IDs applied to operations whose request body accepts a "
            "plural ``tenantIds`` array (currently job activation). Accepts a "
            "comma-separated list when supplied via environment variable. "
            "Falls back to ``[CAMUNDA_TENANT_ID]`` when only the singular form is set."
        ),
    )

    @field_validator("CAMUNDA_TENANT_IDS", mode="before")
    @classmethod
    def _parse_tenant_ids(cls, value: Any) -> Any:
        # Env-derived values arrive as comma-separated strings; programmatic
        # callers may supply a list directly. Empty / whitespace-only entries
        # are dropped so trailing commas or spurious blanks don't produce
        # phantom tenant filters in outgoing requests.
        if value is None:
            return None
        if isinstance(value, str):
            parts = [p.strip() for p in value.split(",")]
            cleaned = [p for p in parts if p]
            return cleaned or None
        if isinstance(value, (list, tuple)):
            cleaned = [str(p).strip() for p in value if str(p).strip()]
            return cleaned or None
        return value

    # Worker defaults
    CAMUNDA_WORKER_TIMEOUT: int | None = Field(
        default=None,
        description="Default job timeout in milliseconds for all workers.",
    )
    CAMUNDA_WORKER_MAX_CONCURRENT_JOBS: int | None = Field(
        default=None,
        description="Default maximum concurrent jobs per worker.",
    )
    CAMUNDA_WORKER_REQUEST_TIMEOUT: int | None = Field(
        default=None,
        description="Default long-poll request timeout in milliseconds for all workers.",
    )
    CAMUNDA_WORKER_NAME: str | None = Field(
        default=None,
        description="Default worker name for all workers.",
    )
    CAMUNDA_WORKER_STARTUP_JITTER_MAX_SECONDS: float | None = Field(
        default=None,
        description="Default maximum startup jitter in seconds for all workers.",
    )

    # HTTP connection pool
    CAMUNDA_HTTP_MAX_CONNECTIONS: int | None = Field(
        default=None,
        gt=0,
        description=(
            "Maximum number of connections in the httpx connection pool. When set, "
            "the SDK builds its httpx clients with "
            "``httpx.Limits(max_connections=N, max_keepalive_connections=N)``. "
            "An explicit ``limits`` entry in ``httpx_args`` takes precedence over "
            "this setting."
        ),
    )

    # mTLS
    CAMUNDA_MTLS_CERT_PATH: str | None = Field(
        default=None,
        description="Path to client certificate (PEM) for mTLS.",
    )
    CAMUNDA_MTLS_KEY_PATH: str | None = Field(
        default=None,
        description="Path to client private key (PEM) for mTLS.",
    )
    CAMUNDA_MTLS_CA_PATH: str | None = Field(
        default=None,
        description="Path to CA certificate bundle (PEM) for mTLS. Optional.",
    )
    CAMUNDA_MTLS_CERT: str | None = Field(
        default=None,
        description="Inline PEM client certificate. Overrides CAMUNDA_MTLS_CERT_PATH.",
    )
    CAMUNDA_MTLS_KEY: str | None = Field(
        default=None,
        description="Inline PEM client private key. Overrides CAMUNDA_MTLS_KEY_PATH.",
        repr=False,
    )
    CAMUNDA_MTLS_CA: str | None = Field(
        default=None,
        description="Inline PEM CA bundle. Overrides CAMUNDA_MTLS_CA_PATH.",
    )
    CAMUNDA_MTLS_KEY_PASSPHRASE: str | None = Field(
        default=None,
        description="Passphrase for encrypted private key.",
        repr=False,
    )

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
        #
        # When CAMUNDA_REST_ADDRESS_EXACT is set, the configured addresses are
        # used verbatim (no /v2 appended, no trailing-slash trimming) so
        # gateway- / proxy-fronted deployments whose base path does not follow
        # the `.../v2` convention can be expressed through configuration alone.
        if not self.CAMUNDA_REST_ADDRESS_EXACT:
            self.ZEEBE_REST_ADDRESS = self._normalize_rest_address(  # pyright: ignore[reportConstantRedefinition]
                self.ZEEBE_REST_ADDRESS
            )
            self.CAMUNDA_REST_ADDRESS = self._normalize_rest_address(  # pyright: ignore[reportConstantRedefinition]
                self.CAMUNDA_REST_ADDRESS
            )

        # Tenant defaults: when only the singular CAMUNDA_TENANT_ID is set,
        # mirror it into the plural CAMUNDA_TENANT_IDS so generated code that
        # defaults plural ``tenantIds`` arrays gets the same effective tenant
        # filter without forcing users to set both.
        if self.CAMUNDA_TENANT_IDS is None and self.CAMUNDA_TENANT_ID is not None:
            self.CAMUNDA_TENANT_IDS = [self.CAMUNDA_TENANT_ID]  # pyright: ignore[reportConstantRedefinition]

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

        # TLS / mTLS validation.
        # - CA-only is valid (trust a self-signed server cert without client identity).
        # - Client cert and key must come as a pair.
        # - A passphrase without a client key is invalid.
        mtls_cert_provided = bool(self.CAMUNDA_MTLS_CERT or self.CAMUNDA_MTLS_CERT_PATH)
        mtls_key_provided = bool(self.CAMUNDA_MTLS_KEY or self.CAMUNDA_MTLS_KEY_PATH)
        if mtls_cert_provided != mtls_key_provided:
            raise ValueError(
                "Incomplete mTLS configuration: both certificate "
                "(CAMUNDA_MTLS_CERT or CAMUNDA_MTLS_CERT_PATH) and key "
                "(CAMUNDA_MTLS_KEY or CAMUNDA_MTLS_KEY_PATH) must be provided together."
            )
        if self.CAMUNDA_MTLS_KEY_PASSPHRASE and not mtls_key_provided:
            raise ValueError(
                "CAMUNDA_MTLS_KEY_PASSPHRASE is set but no client key was provided."
            )

        return self


@dataclass(frozen=True)
class ResolvedCamundaSdkConfiguration:
    effective: CamundaSdkConfiguration
    environment: CamundaSdkConfigPartial
    explicit: CamundaSdkConfigPartial | None

    def __repr__(self) -> str:
        """Render without echoing the raw partials.

        ``environment`` and ``explicit`` are the values as the user supplied them,
        credentials included, and nothing filters them -- the generated repr nested
        both dicts whole. Their shape is reported instead. ``effective`` renders
        itself; its own credential fields are declared ``repr=False``.
        """

        explicit_summary = (
            "None" if self.explicit is None else f"<{len(self.explicit)} keys>"
        )
        return (
            f"{type(self).__name__}("
            f"effective={self.effective!r}, "
            f"environment=<{len(self.environment)} keys>, "
            f"explicit={explicit_summary})"
        )


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
        explicit_configuration: CamundaSdkConfigPartial
        | Mapping[str, Any]
        | None = None,
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
        merged: dict[str, Any] = {
            **envfile_values,
            **self._environment,
            **(self._explicit or {}),
        }
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

            has_oauth_creds = _non_empty(
                merged.get("CAMUNDA_CLIENT_ID")
            ) and _non_empty(merged.get("CAMUNDA_CLIENT_SECRET"))
            has_basic_creds = _non_empty(
                merged.get("CAMUNDA_BASIC_AUTH_USERNAME")
            ) and _non_empty(merged.get("CAMUNDA_BASIC_AUTH_PASSWORD"))

            # If both OAuth and Basic credentials are present, require an explicit strategy
            # instead of silently picking one to avoid surprising behavior.
            if has_oauth_creds and has_basic_creds:
                raise ValueError(
                    "Both OAuth (CAMUNDA_CLIENT_ID/SECRET) and Basic auth "
                    "(CAMUNDA_BASIC_AUTH_USERNAME/PASSWORD) credentials are set, "
                    "but CAMUNDA_AUTH_STRATEGY is not explicitly configured. "
                    "Please set CAMUNDA_AUTH_STRATEGY to either 'OAUTH' or 'BASIC'."
                )
            elif has_oauth_creds:
                merged["CAMUNDA_AUTH_STRATEGY"] = "OAUTH"
            elif has_basic_creds:
                merged["CAMUNDA_AUTH_STRATEGY"] = "BASIC"

        # Strip keys not recognised by the configuration model so that
        # unrelated env vars (from .env files or explicit dicts) don't
        # trigger Pydantic's extra="forbid" validation error.
        allowed = CamundaSdkConfiguration.model_fields
        merged = {k: v for k, v in merged.items() if k in allowed}

        try:
            effective = CamundaSdkConfiguration.model_validate(merged)
        except ValidationError as original:
            # `from None`: the original error is the one holding the credentials, and a
            # chained traceback would print it in full underneath the safe one.
            raise _configuration_error_without_secrets(merged, original) from None

        return ResolvedCamundaSdkConfiguration(
            effective=effective,
            environment=self._filter_partial_config(self._environment),
            explicit=self._filter_partial_config(self._explicit)
            if self._explicit is not None
            else None,
        )

    @staticmethod
    def _filter_partial_config(values: Mapping[str, Any]) -> CamundaSdkConfigPartial:
        allowed = CamundaSdkConfiguration.model_fields
        return cast(
            CamundaSdkConfigPartial, {k: v for k, v in values.items() if k in allowed}
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

        if (
            explicit_left_set
            and explicit_right_set
            and explicit[left] != explicit[right]
        ):
            raise ValueError(
                f"Conflicting explicit configuration: "
                f"{left}={_render_config_value(left, explicit[left])} != "
                f"{right}={_render_config_value(right, explicit[right])}"
            )
        if explicit_left_set or explicit_right_set:
            return explicit[left] if explicit_left_set else explicit[right]

        env_left_set = _is_set(environment, left)
        env_right_set = _is_set(environment, right)

        if env_left_set and env_right_set and environment[left] != environment[right]:
            raise ValueError(
                f"Conflicting environment configuration: "
                f"{left}={_render_config_value(left, environment[left])} != "
                f"{right}={_render_config_value(right, environment[right])}"
            )
        if env_left_set or env_right_set:
            return environment[left] if env_left_set else environment[right]

        return default
