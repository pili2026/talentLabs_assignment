from enum import StrEnum


class JobStatusEnum(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    SCHEDULED = "scheduled"
