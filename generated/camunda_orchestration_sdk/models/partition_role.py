from enum import StrEnum


class PartitionRole(StrEnum):
    FOLLOWER = "follower"
    INACTIVE = "inactive"
    LEADER = "leader"

    def __str__(self) -> str:
        return str(self.value)
