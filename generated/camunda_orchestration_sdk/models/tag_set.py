from __future__ import annotations
import re
from pydantic import RootModel, field_validator

from ..semantic_types import Tag


class TagSet(RootModel[list[Tag]]):
    @field_validator("root")
    @classmethod
    def _validate_array(cls, v: list[Tag]) -> list[Tag]:
        if len(v) > 10:
            raise ValueError("maxItems 10")
        if len(v) != len(set(v)):
            raise ValueError("uniqueItems violated")
        _pat = re.compile(r"^[A-Za-z][A-Za-z0-9_\\-:.]{0,99}$")
        for _i, _x in enumerate(v):
            if _pat.fullmatch(str(_x)) is None:
                raise ValueError("item {_i} pattern mismatch")
            if len(str(_x)) < 1:
                raise ValueError(f"item {_i} minLength 1")
            if len(str(_x)) > 100:
                raise ValueError(f"item {_i} maxLength 100")
        return v
