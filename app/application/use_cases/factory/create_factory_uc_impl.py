from core.exception import BadRequestError
from application.interfaces.use_cases.factory.create_factory_uc import ICreateFactoryUC
from domain.entities.factory_entity import FactoryEntity
from domain.interfaces.repositories.factory_repository import IFactoryRepository


class CreateFactoryUC(ICreateFactoryUC):
    def __init__(self, factory_repository: IFactoryRepository):
        self.factory_repository = factory_repository

    def execute(self, factory: FactoryEntity) -> bool:
        is_created = self.factory_repository.create_factory(factory=factory)

        if not is_created:
            raise BadRequestError(
                error_code="ETB-tao_nha_may_that_bai",
            )

        return True
