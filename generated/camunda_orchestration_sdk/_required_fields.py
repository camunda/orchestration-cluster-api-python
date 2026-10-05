"""Response-field access that names the model and field when a required one is missing."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TypeVar

from .errors import MissingRequiredFieldError

V = TypeVar("V")


class RequiredFields(dict[str, V]):
    """The dict a model's ``from_dict`` pops fields from; reports the model on a missing one."""

    def __init__(self, src: Mapping[str, V], model: str) -> None:
        super().__init__(src)
        self._model = model

    def pop_required(self, key: str) -> V:
        """Pop a required field, raising ``MissingRequiredFieldError`` if it is absent."""
        if key not in self:
            raise MissingRequiredFieldError(self._model, key)
        return self.pop(key)
