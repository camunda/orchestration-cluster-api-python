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

__all__ = [
    "AsyncAuthProvider",
    "AsyncOAuthClientCredentialsAuthProvider",
    "AuthProvider",
    "BasicAuthProvider",
    "NullAuthProvider",
    "OAuthClientCredentialsAuthProvider",
    "inject_auth_event_hooks",
]