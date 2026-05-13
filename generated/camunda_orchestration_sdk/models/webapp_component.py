from enum import Enum


class WebappComponent(str, Enum):
    ADMIN = "admin"
    OPERATE = "operate"
    TASKLIST = "tasklist"

    def __str__(self) -> str:
        return str(self.value)
