import asyncio

from application.interfaces.use_cases.department.create_department_factory_uc import (
    ICreateDepartmentFactoryUC,
)
from application.schemas.department_schemas import DepartmentDTO
from application.schemas.factory_schemas import FactoryDTO
from domain.interfaces.repositories.department_repository import IDepartmentRepository
from domain.interfaces.repositories.factory_repository import IFactoryRepository


class CreateDepartmentFactoryUC(ICreateDepartmentFactoryUC):
    def __init__(
        self, factory_repo: IFactoryRepository, department_repo: IDepartmentRepository
    ) -> None:
        self.factory_repo = factory_repo
        self.department_repo = department_repo

    async def execute(
        self, department_dto: DepartmentDTO, factory_dto: FactoryDTO
    ) -> bool:

        value = await asyncio.gather(
            self.department_repo.get_department_by_id(id=department_dto.id),
            self.factory_repo.get_factory_by_id(id=factory_dto.id),
        )

        print(value[0], value[1])
