from application.interfaces.use_cases.factory.create_factory_uc import \
    ICreateFactoryUC
from core.exception import BadRequestError
from domain.entities.factory_entity import FactoryEntity
from domain.interfaces.repositories.factory_repository import \
    IFactoryRepository


class CreateFactoryUC(ICreateFactoryUC):
    def __init__(self, factory_repository: IFactoryRepository):
        self.factory_repository = factory_repository

    def execute(self, factory: FactoryEntity) -> bool:
        is_exist_name = self.factory_repository.get_factory_by_name(factory.name)

        if is_exist_name:
            raise BadRequestError(error_code="ETB-ten_nha_may_da_ton_tai")

        is_created = self.factory_repository.create_factory(factory=factory)

        if not is_created:
            raise BadRequestError(
                error_code="ETB-tao_nha_may_that_bai",
            )

        return True
