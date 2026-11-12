from __future__ import annotations
import re
from typing import Annotated
from pydantic import PlainValidator, RootModel, WithJsonSchema, field_validator

from ..semantic_types import Tag


def _as_tag(value: object) -> Tag:
    if isinstance(value, Tag):
        return value
    if not (isinstance(value, str)):
        raise ValueError(f"expected str, got {type(value).__name__}")
    try:
        return Tag(value)
    except TypeError as exc:
        raise ValueError(str(exc)) from exc


class TagSet(
    RootModel[
        list[
            Annotated[Tag, PlainValidator(_as_tag), WithJsonSchema({"type": "string"})]
        ]
    ]
):
    @field_validator("root")
    @classmethod
    def _validate_array(cls, v: list[Tag]) -> list[Tag]:
        if len(v) > 10:
            raise ValueError("maxItems 10")
        if len(v) != len(set(v)):
            raise ValueError("uniqueItems violated")
        _pat = re.compile("^[A-Za-z][A-Za-z0-9_\\-:.]{0,99}$")
        for _i, _x in enumerate(v):
            if _pat.fullmatch(str(_x)) is None:
                raise ValueError(f"item {_i} pattern mismatch")
            if len(str(_x)) < 1:
                raise ValueError(f"item {_i} minLength 1")
            if len(str(_x)) > 100:
                raise ValueError(f"item {_i} maxLength 100")
        return v
