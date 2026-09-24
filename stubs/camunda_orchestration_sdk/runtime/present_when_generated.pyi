from __future__ import annotations

from typing import NamedTuple

class PresentWhenCoupling(NamedTuple):
    response_schema: str
    response_field: str
    request_flag: str

PRESENT_WHEN_COUPLINGS: tuple[PresentWhenCoupling, ...] = (
    PresentWhenCoupling("ActivatedJobResult", "jobLeaseToken", "withLease"),
)
