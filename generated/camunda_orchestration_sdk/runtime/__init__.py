"""Runtime helpers injected into the generated SDK.

Do not import from ``generated/`` directly; edit this package and re-run generation.
"""

from .auth import AuthProvider, NullAuthProvider, inject_auth_event_hooks

__all__ = [
	"AuthProvider",
	"NullAuthProvider",
	"inject_auth_event_hooks",
]