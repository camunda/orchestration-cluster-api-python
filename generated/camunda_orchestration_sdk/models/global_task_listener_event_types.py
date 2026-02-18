from __future__ import annotations
from pydantic import RootModel, field_validator


class GlobalTaskListenerEventTypes(RootModel[list[str]]):
    @field_validator("root")
    @classmethod
    def _validate_array(cls, v: list[str]) -> list[str]:
        for _i, _x in enumerate(v):
            if _x not in [
                "all",
                "creating",
                "assigning",
                "updating",
                "completing",
                "canceling",
            ]:
                raise ValueError(f"item {_i} not in enum")
        return v
