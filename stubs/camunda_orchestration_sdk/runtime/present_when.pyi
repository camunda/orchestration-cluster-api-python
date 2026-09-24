from __future__ import annotations

from camunda_orchestration_sdk.runtime.present_when_generated import PresentWhenCoupling

LEASE_COUPLING_KEY = "ActivatedJobResult.jobLeaseToken"
ENFORCED_COUPLINGS: tuple[str, ...] = (LEASE_COUPLING_KEY,)

class LeaseNotHonoredError(Exception):
    def __init__(self, job_key: str, request_flag: str) -> None: ...

def coupling_key(c: PresentWhenCoupling) -> str: ...
def lease_request_flag() -> str: ...
def require_lease_presence(
    requested: bool, job_key: str, token: str | None
) -> None: ...
