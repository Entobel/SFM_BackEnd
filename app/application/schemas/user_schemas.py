from dataclasses import dataclass


@dataclass(frozen=True)
class UserDTO:
    id: int
    email: str
    phone: str
    first_name: str
    phone: str
    last_name: str
    department_factory_id: int
    department_role_id: int
