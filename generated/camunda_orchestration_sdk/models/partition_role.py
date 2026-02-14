from enum import Enum


class PartitionRole(str, Enum):
    FOLLOWER = "follower"
    INACTIVE = "inactive"
    LEADER = "leader"

    def __str__(self) -> str:
        return str(self.value)
