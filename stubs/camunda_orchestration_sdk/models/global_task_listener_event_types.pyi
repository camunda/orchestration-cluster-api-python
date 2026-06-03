from __future__ import annotations

from pydantic import RootModel, field_validator
class GlobalTaskListenerEventTypes(RootModel[list[str]]):
    @field_validator('root')
    @classmethod
    def _validate_array(cls, v: list[str]) -> list[str]: ...
