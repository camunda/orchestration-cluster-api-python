"""Tests for mTLS configuration and ssl.SSLContext construction."""

from __future__ import annotations

import ssl
import textwrap
from pathlib import Path

import pytest

from camunda_orchestration_sdk.runtime.configuration_resolver import (
    CamundaSdkConfiguration,
    ConfigurationResolver,
)
from camunda_orchestration_sdk.runtime.tls import build_ssl_context


# ---------------------------------------------------------------------------
# Fixtures: self-signed CA + client cert/key for testing
# ---------------------------------------------------------------------------

_CA_CERT_PEM = textwrap.dedent("""\
    -----BEGIN CERTIFICATE-----
    MIICoDCCAYgCCQDBC2iny88sMDANBgkqhkiG9w0BAQsFADASMRAwDgYDVQQDDAd0
    ZXN0LWNhMB4XDTI2MDQwMjAwMjI0NFoXDTM2MDMzMDAwMjI0NFowEjEQMA4GA1UE
    AwwHdGVzdC1jYTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANeuANi1
    1pNvH3LA0bmu0bc13zxQjUeDCJIxf0vzmTeJj1zsvwg/MRz0LOmjOxx7wES7R9O0
    ERtA6yReGg/fgps3FMB07L5lvmBTNF96ZhuES+GwZRtuu5ylbeQXML3d1dD0lVIa
    PAtjvsiDFcP5+TUJOjBd5awkjA2w2S6r9ukY1SE+4U3U284S8L2dRuouR9kXi/TU
    9YOSm/7d7q4AlD0agjiNaSDR8pwJ+DBXvnE5Flyw1a8TjeairJ22NYDZaYm/vz+4
    fX6fohD4c052XrX8ntgzpS5cCAUHoFTFjQYU4CFc6WwDeAV4fSJC8DkXAQWpmNFI
    8G1CxG8PFO2z4WECAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAdrzD8FE6OYhIJLNO
    eyPqRbP5j0KteskvS0B1waQBQwNmah6p8lcflQN9q2s6h7wIn6+jmP9erdkoHipm
    8NmYxoY9LTWVVdRmipa7R4yrvrZxdyfiza8Hrnl8o1MHY8qZcCZdoRfnx3/q5Fo+
    s8M2/LAZ0mSC2zuzzukYpRMQTJEQsfVfclASzv4+15g5kh31nzAw71J2W8wV8tse
    OOgpNMBdQvhd4kP46kTJ7GtrusIzAVNll4vzLaLYE1RRKqNlIxdDv0/gIQRJPhm7
    9rDYx+XGBmqbsZIjT+I/D4hxbRTCGIKvPDAQyY0zrU5gPqQoT+owqms0Ett31ZT+
    XFUgRw==
    -----END CERTIFICATE-----
""")

_CLIENT_CERT_PEM = textwrap.dedent("""\
    -----BEGIN CERTIFICATE-----
    MIICpDCCAYwCCQDrTHsD/Zr2bzANBgkqhkiG9w0BAQsFADASMRAwDgYDVQQDDAd0
    ZXN0LWNhMB4XDTI2MDQwMjAwMjI0NFoXDTM2MDMzMDAwMjI0NFowFjEUMBIGA1UE
    AwwLdGVzdC1jbGllbnQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDV
    /qHEYVaPLo7yl6tnfprRlViqpnXLNVLv6JU+YFZdRkSBFLg4Gpwzt95N9ZUxQBfo
    jIdwP/dKqTcAB3adUuUPUxke2Bpb6EJjrC4ks0+2s2NjXviEgFnA7GWYQIxjremO
    D61UHmdEh+ZPnB7CbjDlmtH4RfZPg4EZj7Xvc0Xa8tC5DSWWPK/AbdQevOnPZ27b
    uowSIbC2JKow9JWspvzA4b0Ow7+YLKuqj43+6hSqDz/jHqmBl7C5P3YmveakBnSw
    2tjw7M+mEVHaidg5WLQnGRrj5McLgypEQKZvUCM9+PF1iGB/FDdHnftlLylA61V1
    vsSktqrwF0yxYGBhK1CvAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAKeSbEsMkUoA
    TXLJQdc/TPHRZFHgMx2d+hKclKvK9I4+pYAT5KG5FxFRnGTtIPz2YchXZ6AqDA/M
    Hct5x+gHEiO+wIA3DM48+KCwhNK6SNYuCR6mNKmikYi++5RJJszex3/Nw7YSLUDN
    pZTj3XqKOXq9uzd1FqecF5K/We6FnPlU6RCgzD5ONOQtQ551+qRSJJi/cPm9edKx
    u3cL8OmCTNWHkWKekGR6eeIf723alqAb04V3/tzDrskpNkMraLZs8pmtlB5BB40I
    ieC0B9uQun4s4gngm2QgO6LOjD0P8U88Lw9jjh7dThlxRntR+9vxufdMvBFiIq4J
    6ZZ3OgdyudM=
    -----END CERTIFICATE-----
""")

_CLIENT_KEY_PEM = textwrap.dedent("""\
    -----BEGIN PRIVATE KEY-----
    MIIEwAIBADANBgkqhkiG9w0BAQEFAASCBKowggSmAgEAAoIBAQDV/qHEYVaPLo7y
    l6tnfprRlViqpnXLNVLv6JU+YFZdRkSBFLg4Gpwzt95N9ZUxQBfojIdwP/dKqTcA
    B3adUuUPUxke2Bpb6EJjrC4ks0+2s2NjXviEgFnA7GWYQIxjremOD61UHmdEh+ZP
    nB7CbjDlmtH4RfZPg4EZj7Xvc0Xa8tC5DSWWPK/AbdQevOnPZ27buowSIbC2JKow
    9JWspvzA4b0Ow7+YLKuqj43+6hSqDz/jHqmBl7C5P3YmveakBnSw2tjw7M+mEVHa
    idg5WLQnGRrj5McLgypEQKZvUCM9+PF1iGB/FDdHnftlLylA61V1vsSktqrwF0yx
    YGBhK1CvAgMBAAECggEBAM+SaLOmf2HvlXU3LWn8Yow9Q350bPopxUM05d9VbzCW
    wkg7It444Z9BEP+p4YeeVhKajZ2STns7XEBI/QNprwqIXmuOzzKrPgqUr0WmMQJV
    S2jObF2KaoU6SOnAYu0letDz3/siaqUM9ZfvJd8PJ5rv7A/ZPSyvsIBs59tWg0H2
    U+VG+9wcZraXDAm2EI3181foyviaaO4OIr9EeMyBUsq7UITOOKb8ZKN8pGSLO2ww
    uqCK+OfreLQvrXAOyenz/yNDoi3ClidG9ljPdB6/w1icVbDt/jX5Fg4nVs74l+/G
    x5LiZCYdl/tt0zNOfOXqVVn/AIQkBicUJz2s6mEtnqECgYEA7X6VL/lWFLLHzjx5
    YMpkBwGytjNVKWJvrGcHTcgZSYx5iekmoVrKannE1nBEqaa4YoIQdMFVahJjGFVR
    HXb2vmk7qkfYb/mUq1tITty9sR2X87tcwrukB0wXtWUXQYcOc5gnT5+MNZCfkO31
    MbXgBcDKzNZ3+94wTArG5b9lUPkCgYEA5qtJfZw5JBLu2IMQU3vZhu7dtXiWMHxT
    4TL2tkEec42GfoyO9g+duk0AEWVk/kjrDqIJpk93skfBnLrVDfSFmH+msvGUYtsP
    Mk0i1J5aCfhf66QyCNrKtATbC93vXj7oJHk35a1Kbr9OcnNrCCQbjzhi+9w9oKos
    FNXHpy3JQOcCgYEAp9SBRwKzczMYAcU4nU7JOy5XBWznLLS0aCfywGO8gv4zUWMi
    +nm3e2EL2eJCk4UO3gY97NRHMQtHXgXEqcbM/ahOErps2EyOZD3AroJNxuE75XCt
    T6vccY+zXWvP8G2pp8SJWzpLkfre2ENgt71oT4h7iB+zcJkGlmYzQl5sEbkCgYEA
    mGxTMaeLsqS4I2Xn4eKTCTDKXGIEjKF7I/JzSFebcavxVao3xazoAvViuBwSMl2o
    xZCZY8ZbR/lWnORwaLpNlUm0s8Yi0XgDgK+r9md1A+WWLLXhQiyhiXcz75GF3Pcg
    mwlmwGRULP5JLiPKdCS3+Vm/PsJ4DrSkUFg7h+Mfe70CgYEA2hW87IO7OhWSgGK4
    Uk6YTvwyMSk4u+DGIy35iho3iOevKDMoB72WKhEy5jODDu5jPrOjCQzPdv20Ww2P
    kKdXAKkteicPak8ejYqzlUlVJM9L16W4oQ4LzDgUnnzHNskJmOfWBMX7zA+kIqhx
    TQaR7e0nIcvij6IJKpyEoXxvLcI=
    -----END PRIVATE KEY-----
""")


@pytest.fixture
def cert_dir(tmp_path: Path) -> dict[str, Path]:
    """Write test PEM files to a temp dir and return their paths."""
    cert = tmp_path / "client.crt"
    key = tmp_path / "client.key"
    ca = tmp_path / "ca.crt"
    cert.write_text(_CLIENT_CERT_PEM)
    key.write_text(_CLIENT_KEY_PEM)
    ca.write_text(_CA_CERT_PEM)
    return {"cert": cert, "key": key, "ca": ca}


# ---------------------------------------------------------------------------
# Config validation tests
# ---------------------------------------------------------------------------


class TestMtlsConfigValidation:
    """Test that configuration resolver validates mTLS field completeness."""

    def test_cert_without_key_raises(self) -> None:
        with pytest.raises(Exception, match="Incomplete mTLS"):
            ConfigurationResolver(
                environment={},
                explicit_configuration={"CAMUNDA_MTLS_CERT": _CLIENT_CERT_PEM},
            ).resolve()

    def test_key_without_cert_raises(self) -> None:
        with pytest.raises(Exception, match="Incomplete mTLS"):
            ConfigurationResolver(
                environment={},
                explicit_configuration={"CAMUNDA_MTLS_KEY": _CLIENT_KEY_PEM},
            ).resolve()

    def test_cert_path_without_key_raises(self, cert_dir: dict[str, Path]) -> None:
        with pytest.raises(Exception, match="Incomplete mTLS"):
            ConfigurationResolver(
                environment={},
                explicit_configuration={
                    "CAMUNDA_MTLS_CERT_PATH": str(cert_dir["cert"]),
                },
            ).resolve()

    def test_key_path_without_cert_raises(self, cert_dir: dict[str, Path]) -> None:
        with pytest.raises(Exception, match="Incomplete mTLS"):
            ConfigurationResolver(
                environment={},
                explicit_configuration={
                    "CAMUNDA_MTLS_KEY_PATH": str(cert_dir["key"]),
                },
            ).resolve()

    def test_ca_only_raises(self) -> None:
        with pytest.raises(Exception, match="Incomplete mTLS"):
            ConfigurationResolver(
                environment={},
                explicit_configuration={"CAMUNDA_MTLS_CA": _CA_CERT_PEM},
            ).resolve()

    def test_passphrase_only_raises(self) -> None:
        with pytest.raises(Exception, match="Incomplete mTLS"):
            ConfigurationResolver(
                environment={},
                explicit_configuration={
                    "CAMUNDA_MTLS_KEY_PASSPHRASE": "secret",
                },
            ).resolve()

    def test_cert_and_key_accepted(self) -> None:
        resolved = ConfigurationResolver(
            environment={},
            explicit_configuration={
                "CAMUNDA_MTLS_CERT": _CLIENT_CERT_PEM,
                "CAMUNDA_MTLS_KEY": _CLIENT_KEY_PEM,
            },
        ).resolve()
        assert resolved.effective.CAMUNDA_MTLS_CERT == _CLIENT_CERT_PEM
        assert resolved.effective.CAMUNDA_MTLS_KEY == _CLIENT_KEY_PEM

    def test_cert_path_and_key_path_accepted(
        self, cert_dir: dict[str, Path]
    ) -> None:
        resolved = ConfigurationResolver(
            environment={},
            explicit_configuration={
                "CAMUNDA_MTLS_CERT_PATH": str(cert_dir["cert"]),
                "CAMUNDA_MTLS_KEY_PATH": str(cert_dir["key"]),
            },
        ).resolve()
        assert resolved.effective.CAMUNDA_MTLS_CERT_PATH == str(cert_dir["cert"])
        assert resolved.effective.CAMUNDA_MTLS_KEY_PATH == str(cert_dir["key"])

    def test_no_mtls_fields_accepted(self) -> None:
        """No mTLS fields → no error."""
        resolved = ConfigurationResolver(
            environment={},
            explicit_configuration={},
        ).resolve()
        assert resolved.effective.CAMUNDA_MTLS_CERT is None


# ---------------------------------------------------------------------------
# build_ssl_context tests
# ---------------------------------------------------------------------------


class TestBuildSslContext:
    """Test ssl.SSLContext construction from config."""

    def test_returns_none_when_no_mtls(self) -> None:
        config = CamundaSdkConfiguration()
        assert build_ssl_context(config) is None

    def test_builds_context_from_inline_cert_key(self) -> None:
        config = CamundaSdkConfiguration(
            CAMUNDA_MTLS_CERT=_CLIENT_CERT_PEM,
            CAMUNDA_MTLS_KEY=_CLIENT_KEY_PEM,
        )
        ctx = build_ssl_context(config)
        assert ctx is not None
        assert isinstance(ctx, ssl.SSLContext)

    def test_builds_context_from_paths(self, cert_dir: dict[str, Path]) -> None:
        config = CamundaSdkConfiguration(
            CAMUNDA_MTLS_CERT_PATH=str(cert_dir["cert"]),
            CAMUNDA_MTLS_KEY_PATH=str(cert_dir["key"]),
        )
        ctx = build_ssl_context(config)
        assert ctx is not None
        assert isinstance(ctx, ssl.SSLContext)

    def test_inline_overrides_path(self, cert_dir: dict[str, Path]) -> None:
        """When both inline and path are set, inline wins."""
        config = CamundaSdkConfiguration(
            CAMUNDA_MTLS_CERT=_CLIENT_CERT_PEM,
            CAMUNDA_MTLS_KEY=_CLIENT_KEY_PEM,
            CAMUNDA_MTLS_CERT_PATH=str(cert_dir["cert"]),
            CAMUNDA_MTLS_KEY_PATH=str(cert_dir["key"]),
        )
        ctx = build_ssl_context(config)
        assert ctx is not None

    def test_with_ca(self, cert_dir: dict[str, Path]) -> None:
        config = CamundaSdkConfiguration(
            CAMUNDA_MTLS_CERT=_CLIENT_CERT_PEM,
            CAMUNDA_MTLS_KEY=_CLIENT_KEY_PEM,
            CAMUNDA_MTLS_CA=_CA_CERT_PEM,
        )
        ctx = build_ssl_context(config)
        assert ctx is not None

    def test_with_ca_path(self, cert_dir: dict[str, Path]) -> None:
        config = CamundaSdkConfiguration(
            CAMUNDA_MTLS_CERT_PATH=str(cert_dir["cert"]),
            CAMUNDA_MTLS_KEY_PATH=str(cert_dir["key"]),
            CAMUNDA_MTLS_CA_PATH=str(cert_dir["ca"]),
        )
        ctx = build_ssl_context(config)
        assert ctx is not None

    def test_missing_cert_file_raises(self, tmp_path: Path) -> None:
        config = CamundaSdkConfiguration(
            CAMUNDA_MTLS_CERT_PATH=str(tmp_path / "nonexistent.crt"),
            CAMUNDA_MTLS_KEY_PATH=str(tmp_path / "nonexistent.key"),
        )
        with pytest.raises(FileNotFoundError, match="nonexistent.crt"):
            build_ssl_context(config)

    def test_missing_key_file_raises(
        self, cert_dir: dict[str, Path], tmp_path: Path
    ) -> None:
        config = CamundaSdkConfiguration(
            CAMUNDA_MTLS_CERT_PATH=str(cert_dir["cert"]),
            CAMUNDA_MTLS_KEY_PATH=str(tmp_path / "nonexistent.key"),
        )
        with pytest.raises(FileNotFoundError, match="nonexistent.key"):
            build_ssl_context(config)
