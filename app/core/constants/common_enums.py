from enum import Enum


class ZoneLevelStatusEnum(Enum):
    ON_HARVESTING = 3
    ON_GROWING = 2
    ON_HOLD = 1
    INACTIVE = 0


class FormStatusEnum(Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2


class GrowingZoneLevelStatusEnum(Enum):
    ARCHIVED = 2
    IN_USE = 1
    TEMPORARY = 0


class HarvestZoneLevelStatusEnum(Enum):
    ACTIVE = 1
    TEMPORARY = 0

