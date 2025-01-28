from enum import Enum


class BorrowStatus(Enum):
    PENDING = 1
    APPROVED = 2
    DENIED = 3
    REVIVED = 4