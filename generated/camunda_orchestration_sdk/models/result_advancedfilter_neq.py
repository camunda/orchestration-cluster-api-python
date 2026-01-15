from enum import Enum


class ResultAdvancedfilterNeq(str, Enum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"

    def __str__(self) -> str:
        return str(self.value)
