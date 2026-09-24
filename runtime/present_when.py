"""Runtime enforcement of the dependent-presence couplings the specification declares with
``x-present-when`` (see ``present_when_generated.py``).

Python cannot express, in the type system, that a response field is present only when a
request set a runtime flag, so the coupling is enforced here at the activation boundary. The
generated table is the ground truth; the acceptance tests assert the runtime still matches
it, so an upstream change to the markers fails the build rather than drifting silently.
"""

from __future__ import annotations

# Absolute import (not relative): `present_when_generated` is emitted into the generated
# package by hook 0350 and does not exist in the `runtime/` source tree, so it must resolve
# through the installed package path the way the worker imports generated models.
from camunda_orchestration_sdk.runtime.present_when_generated import (
    PRESENT_WHEN_COUPLINGS,
    PresentWhenCoupling,
)

# The one coupling this runtime enforces: ActivatedJobResult.jobLeaseToken is present only
# when an activation set the lease flag.
LEASE_COUPLING_KEY = "ActivatedJobResult.jobLeaseToken"

# Couplings the runtime actively enforces, by "Schema.field" key. A coupling in
# PRESENT_WHEN_COUPLINGS absent here is one the specification declares and the worker
# silently ignores; the acceptance guard makes that visible. Verification metadata only —
# the runtime path is hardcoded to the lease.
ENFORCED_COUPLINGS: tuple[str, ...] = (LEASE_COUPLING_KEY,)


class LeaseNotHonoredError(Exception):
    """A worker activated jobs with a lease but the server returned a job with no token.

    The specification declares the token present exactly when the activation sets the lease
    flag. A server that predates job leases, or one that ignores the flag, breaks that
    quietly: the worker would go on to complete, fail, or throw an error for the job with no
    token, so the engine could not fence the command against a superseded activation. The
    caller asked for fencing and would not be getting it, which is worth failing over.
    """

    def __init__(self, job_key: str, request_flag: str) -> None:
        super().__init__(
            f"activation for job {job_key} set {request_flag!r} but the server returned no "
            "lease token; the server does not support job leases"
        )
        self.job_key = job_key
        self.request_flag = request_flag


def coupling_key(c: PresentWhenCoupling) -> str:
    """The ``Schema.field`` key for a coupling."""
    return f"{c.response_schema}.{c.response_field}"


def lease_request_flag() -> str:
    """The request flag governing the lease coupling, read from the generated table so a
    rename upstream is reflected here rather than hardcoded."""
    for c in PRESENT_WHEN_COUPLINGS:
        if coupling_key(c) == LEASE_COUPLING_KEY:
            return c.request_flag
    return "withLease"


def require_lease_presence(requested: bool, job_key: str, token: str | None) -> None:
    """Enforce the lease coupling for a single activated job.

    ``requested`` reports whether the activation set the lease flag; ``token`` is the lease
    token the server returned. A lease that was asked for but not returned is rejected,
    because every fenced command would otherwise go out unfenced.
    """
    if not requested or token:
        return
    raise LeaseNotHonoredError(job_key, lease_request_flag())
