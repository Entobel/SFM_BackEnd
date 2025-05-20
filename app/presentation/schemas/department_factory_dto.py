from pydantic import BaseModel

from application.schemas.factory_schemas import FactoryDTO
from application.schemas.department_schemas import DepartmentDTO


class DepartmentFactoryDTO(BaseModel):
    id: int
    department: DepartmentDTO
    factory: FactoryDTO
    is_active: bool
