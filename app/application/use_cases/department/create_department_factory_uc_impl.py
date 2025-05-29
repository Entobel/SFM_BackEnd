from application.interfaces.use_cases.department.create_department_factory_uc import (
    ICreateDepartmentFactoryUC,
)
from application.schemas.department_dto import DepartmentDTO
from application.schemas.factory_dto import FactoryDTO
from core.exception import BadRequestError, NotFoundError
from domain.entities.department_entity import DepartmentEntity
from domain.entities.department_factory_entity import DepartmentFactoryEntity
from domain.entities.factory_entity import FactoryEntity
from domain.interfaces.repositories.department_factory_repository import (
    IDepartmentFactoryRepository,
)
from domain.interfaces.repositories.department_repository import IDepartmentRepository
from domain.interfaces.repositories.factory_repository import IFactoryRepository


class CreateDepartmentFactoryUC(ICreateDepartmentFactoryUC):
    def __init__(
        self,
        factory_repo: IFactoryRepository,
        department_repo: IDepartmentRepository,
        department_factory_repo: IDepartmentFactoryRepository,
    ) -> None:
        self.factory_repo = factory_repo
        self.department_repo = department_repo
        self.department_factory_repo = department_factory_repo

    def execute(self, department_dto: DepartmentDTO, factory_dto: FactoryDTO) -> bool:
        department_entity = self.department_repo.get_department_by_id(
            id=department_dto.id
        )

        factory_entity = self.factory_repo.get_factory_by_id(id=factory_dto.id)

        if not department_entity:
            raise NotFoundError("ETB-phong_ban_khong_ton_tai")

        if not factory_entity:
            raise NotFoundError("ETB-nha_may_khong_ton_tai")

        department_factory_entity = DepartmentFactoryEntity(
            department=DepartmentEntity(
                id=department_entity.id,
            ),
            factory=FactoryEntity(
                id=factory_entity.id,
            ),
        )

        is_department_factory_exists = self.department_factory_repo.get_department_factory_by_department_id_and_factory_id(
            department_factory_entity=department_factory_entity,
        )

        if is_department_factory_exists:
            raise BadRequestError("ETB-phong_ban_nha_may_da_ton_tai")

        is_created = self.department_factory_repo.create_department_factory(
            department_factory_entity=department_factory_entity
        )

        if not is_created:
            raise BadRequestError("ETB-tao_phong_ban_nha_may_that_bai")

        return True
