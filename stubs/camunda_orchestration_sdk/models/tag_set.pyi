from __future__ import annotations

from pydantic import RootModel, field_validator
from ..semantic_types import Tag

class TagSet(RootModel[list[Tag]]):
    @field_validator("root")
    @classmethod
    def _validate_array(cls, v: list[Tag]) -> list[Tag]: ...
