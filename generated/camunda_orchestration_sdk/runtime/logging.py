"""Pluggable logger abstraction for the Camunda SDK.

Users can inject any logger that implements :class:`CamundaLogger` (stdlib
``logging.Logger``, ``loguru.logger``, or a custom object with
``debug``/``info``/``warning``/``error`` methods).

When no logger is provided, loguru is used if installed, otherwise logging is
silently disabled.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CamundaLogger(Protocol):
    """Protocol for a logger injectable into the SDK.

    Compatible with Python's ``logging.Logger``, ``loguru.logger``, or any
    object that exposes these four methods.
    """

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...


class NullLogger:
    """Logger that silently discards all messages."""

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        pass

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        pass

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        pass

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        pass

    def trace(self, msg: str, *args: Any, **kwargs: Any) -> None:
        pass


def _get_default_logger() -> CamundaLogger:
    """Return loguru's logger if available, otherwise a silent :class:`NullLogger`."""
    try:
        from loguru import logger

        return logger  # type: ignore[return-value]
    except ImportError:
        return NullLogger()


class SdkLogger:
    """Internal wrapper that normalises logger implementations.

    Adds ``trace()`` support (falls back to ``debug()`` on loggers that lack
    it) and ``bind()`` support (uses loguru's native ``bind`` when available,
    otherwise prepends a ``[key=value ...]`` prefix to messages).
    """

    def __init__(self, logger: CamundaLogger, prefix: str = ""):
        self._logger = logger
        self._prefix = prefix

    def _fmt(self, msg: str) -> str:
        return f"[{self._prefix}] {msg}" if self._prefix else msg

    def debug(self, msg: str) -> None:
        self._logger.debug(self._fmt(msg))

    def info(self, msg: str) -> None:
        self._logger.info(self._fmt(msg))

    def warning(self, msg: str) -> None:
        self._logger.warning(self._fmt(msg))

    def error(self, msg: str) -> None:
        self._logger.error(self._fmt(msg))

    def trace(self, msg: str) -> None:
        trace_fn = getattr(self._logger, "trace", None)
        if callable(trace_fn):
            trace_fn(self._fmt(msg))
        else:
            self._logger.debug(self._fmt(msg))

    def bind(self, **kwargs: str) -> SdkLogger:
        """Create a child logger with additional context.

        If the underlying logger supports ``bind()`` (e.g. loguru), the native
        method is used.  Otherwise context is rendered as a ``[k=v ...]``
        prefix on each message.
        """
        native_bind = getattr(self._logger, "bind", None)
        if callable(native_bind):
            return SdkLogger(native_bind(**kwargs))  # type: ignore[arg-type]
        ctx = " ".join(f"{k}={v}" for k, v in kwargs.items())
        new_prefix = f"{self._prefix} {ctx}".strip() if self._prefix else ctx
        return SdkLogger(self._logger, new_prefix)

    def __reduce__(self) -> tuple[type[SdkLogger], tuple[NullLogger]]:
        """Pickle support: deserialise as a silent logger.

        Loguru and other loggers are not always picklable, so when a
        ``SdkLogger`` is sent across process boundaries (e.g.
        ``ProcessPoolExecutor``) it degrades to a :class:`NullLogger`.
        """
        return (SdkLogger, (NullLogger(),))


def create_logger(logger: CamundaLogger | None = None) -> SdkLogger:
    """Create an :class:`SdkLogger`.

    Parameters
    ----------
    logger:
        A user-supplied logger.  When ``None``, loguru is used if installed,
        otherwise a :class:`NullLogger` is used.
    """
    if logger is None:
        return SdkLogger(_get_default_logger())
    return SdkLogger(logger)  # type: ignore[arg-type]
