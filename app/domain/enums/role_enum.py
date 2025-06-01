from enum import Enum


class Role(Enum):
    ADMIN = 1
    MANAGER = 2
    PRODUCTION_CLERK = 3
    SHIFT_LEADER = 4
    Staff = 8

    @classmethod
    def get_admin_roles(cls) -> list[int]:
        """Roles có quyền admin"""
        return [cls.ADMIN.value]

    @classmethod
    def get_management_roles(cls) -> list[int]:
        """Roles có quyền quản lý"""
        return [cls.ADMIN.value, cls.MANAGER.value]
