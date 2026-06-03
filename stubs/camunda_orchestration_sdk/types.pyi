from collections.abc import Mapping, MutableMapping
from http import HTTPStatus
from typing import Any, IO, BinaryIO, Generic, Literal, TypeVar
from attrs import define
class Unset:
    def __bool__(self) -> Literal[False]: ...
UNSET: Unset = Unset()
FileContent = IO[bytes] | bytes | str
FileTypes = (
    # (filename, file (or bytes), content_type)
    tuple[str | None, FileContent, str | None]
    # (filename, file (or bytes), content_type, headers)
    | tuple[str | None, FileContent, str | None, Mapping[str, str]]
)
RequestFiles = list[tuple[str, FileTypes]]
@define
class File:
    payload: BinaryIO
    file_name: str | None = None
    mime_type: str | None = None
    def to_tuple(self) -> FileTypes: ...
T = TypeVar("T")
@define
class Response(Generic[T]):
    status_code: HTTPStatus
    content: bytes
    headers: MutableMapping[str, str]
    parsed: T | None
__all__ = ["UNSET", "File", "FileTypes", "RequestFiles", "Response", "Unset", "str_any_dict_factory", "str_str_dict_factory"]
def str_any_dict_factory() -> "dict[str, Any]": ...
def str_str_dict_factory() -> dict[str, str]: ...
