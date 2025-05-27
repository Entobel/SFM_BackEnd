from pydantic import BaseModel

from application.schemas.department_schemas import DepartmentDTO
from application.schemas.factory_schemas import FactoryDTO


class DepartmentFactoryDTO(BaseModel):
    id: int
    department: DepartmentDTO
    factory: FactoryDTO
    is_active: bool
