"""Runtime helpers injected into the generated SDK.

Do not import from ``generated/`` directly; edit this package and re-run generation.
"""

from .auth import (
    AsyncAuthProvider,
    AsyncOAuthClientCredentialsAuthProvider,
    AuthProvider,
    BasicAuthProvider,
    NullAuthProvider,
    OAuthClientCredentialsAuthProvider,
    inject_auth_event_hooks,
)
from .backpressure import (
    AsyncBackpressureManager,
    BackpressureManager,
    BackpressureProfile,
    BackpressureQueueFull,
    EXEMPT_METHODS,
    is_backpressure_error,
    is_backpressure_response,
)
from .eventual import (
    ConsistencyOptions,
    EventualConsistencyTimeoutError,
    eventual_poll,
    eventual_poll_async,
)
from .logging import (
    CamundaLogger,
    NullLogger,
    create_logger,
)

__all__ = [
    "AsyncAuthProvider",
    "AsyncBackpressureManager",
    "AsyncOAuthClientCredentialsAuthProvider",
    "AuthProvider",
    "BackpressureManager",
    "BackpressureProfile",
    "BackpressureQueueFull",
    "BasicAuthProvider",
    "CamundaLogger",
    "ConsistencyOptions",
    "EXEMPT_METHODS",
    "EventualConsistencyTimeoutError",
    "NullAuthProvider",
    "NullLogger",
    "OAuthClientCredentialsAuthProvider",
    "create_logger",
    "eventual_poll",
    "eventual_poll_async",
    "inject_auth_event_hooks",
    "is_backpressure_error",
    "is_backpressure_response",
]
