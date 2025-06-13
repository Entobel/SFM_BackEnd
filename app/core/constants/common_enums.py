from enum import Enum


class ZoneLevelStatusEnum(Enum):
    ACTIVE = 2
    INACTIVE = 0
    ON_HOLD = 1


class GrowingStatusEnum(Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2


class GrowingZoneLevelStatusEnum(Enum):
    ARCHIVED = 2
    IN_USE = 1
    TEMPORARY = 0
