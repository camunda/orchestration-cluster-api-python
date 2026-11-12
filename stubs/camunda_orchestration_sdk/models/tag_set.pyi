from __future__ import annotations

from typing import Annotated
from pydantic import PlainValidator, RootModel, WithJsonSchema, field_validator
from ..semantic_types import Tag
def _as_tag(value: object) -> Tag: ...
class TagSet(RootModel[list[Annotated[Tag, PlainValidator(_as_tag), WithJsonSchema({'type': 'string'})]]]):
    @field_validator('root')
    @classmethod
    def _validate_array(cls, v: list[Tag]) -> list[Tag]: ...
