"""Build an ``ssl.SSLContext`` from the unified TLS configuration.

This module is the single place that translates ``CAMUNDA_MTLS_*`` config
fields into a stdlib ``ssl.SSLContext`` that can be handed to httpx.

It supports three modes:

1. **CA-only** — trust a self-signed server certificate (no client identity).
2. **Client cert + key** — present a client identity using system CAs.
3. **Full mTLS** — both a custom CA and a client cert/key pair.
"""

from __future__ import annotations

import ssl
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .configuration_resolver import CamundaSdkConfiguration


def build_ssl_context(config: CamundaSdkConfiguration) -> ssl.SSLContext | None:
    """Return an ``ssl.SSLContext`` configured for custom TLS, or ``None``.

    Supports three modes:

    1. **CA-only** — trust a self-signed server certificate without presenting
       a client identity (set ``CAMUNDA_MTLS_CA`` / ``CAMUNDA_MTLS_CA_PATH``).
    2. **Client cert + key** — present a client identity using system CAs.
    3. **Full mTLS** — both a custom CA *and* a client cert/key pair.

    Returns ``None`` when no ``CAMUNDA_MTLS_*`` fields are set.

    Inline PEM values (``CAMUNDA_MTLS_CERT``, ``CAMUNDA_MTLS_KEY``,
    ``CAMUNDA_MTLS_CA``) take precedence over their ``_PATH`` counterparts.
    """

    # Resolve cert material — inline takes precedence over path.
    cert_pem = config.CAMUNDA_MTLS_CERT or _read_path(config.CAMUNDA_MTLS_CERT_PATH)
    key_pem = config.CAMUNDA_MTLS_KEY or _read_path(config.CAMUNDA_MTLS_KEY_PATH)
    ca_pem = config.CAMUNDA_MTLS_CA or _read_path(config.CAMUNDA_MTLS_CA_PATH)
    passphrase = config.CAMUNDA_MTLS_KEY_PASSPHRASE

    if not cert_pem and not key_pem and not ca_pem:
        return None

    ctx = ssl.create_default_context()

    if ca_pem:
        ctx.load_verify_locations(cadata=ca_pem)

    # Client cert + key pair (for mutual TLS).
    if cert_pem and key_pem:
        _load_cert_chain(ctx, cert_pem, key_pem, passphrase)

    return ctx


def _read_path(path: str | None) -> str | None:
    """Read a PEM file and return its contents, or ``None``."""
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"mTLS certificate file not found: {path}")
    return p.read_text(encoding="utf-8")


def _load_cert_chain(
    ctx: ssl.SSLContext,
    cert_pem: str,
    key_pem: str,
    passphrase: str | None,
) -> None:
    """Load a cert+key pair into the SSL context.

    ``ssl.SSLContext.load_cert_chain`` requires file paths, so we write
    inline PEM material to secure temp files, load them, then clean up.
    """
    cert_path = _write_temp_pem(cert_pem)
    key_path = _write_temp_pem(key_pem)
    try:
        ctx.load_cert_chain(
            certfile=str(cert_path),
            keyfile=str(key_path),
            password=passphrase or None,
        )
    finally:
        cert_path.unlink(missing_ok=True)
        key_path.unlink(missing_ok=True)


def _write_temp_pem(pem: str) -> Path:
    """Write PEM material to a secure temporary file and return its path."""
    fd = tempfile.NamedTemporaryFile(
        mode="w", suffix=".pem", delete=False, encoding="utf-8"
    )
    try:
        fd.write(pem)
    finally:
        fd.close()
    return Path(fd.name)
