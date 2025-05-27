from application.interfaces.use_cases.factory.update_factory_uc import \
    IUpdateFactoryUC
from application.schemas.factory_schemas import FactoryDTO
from core.exception import BadRequestError
from domain.entities.factory_entity import FactoryEntity
from domain.interfaces.repositories.factory_repository import \
    IFactoryRepository


class UpdateFactoryUC(IUpdateFactoryUC):
    def __init__(self, factory_repository: IFactoryRepository):
        self.factory_repository = factory_repository

    def execute(self, factory_id: int, factory_dto: FactoryDTO) -> bool:
        factory = self.factory_repository.get_factory_by_id(id=factory_id)

        if not factory:
            raise BadRequestError(
                error_code="ETB-nha_may_khong_ton_tai",
            )

        if factory_dto.name:
            factory.set_name(factory_dto.name)

        if factory_dto.abbr_name:
            factory.set_abbr_name(factory_dto.abbr_name)

        if factory_dto.description:
            factory.set_description(factory_dto.description)

        if factory_dto.location:
            factory.set_location(factory_dto.location)

        is_updated = self.factory_repository.update_factory(factory=factory)

        if not is_updated:
            raise BadRequestError(
                error_code="ETB-cap_nhat_nha_may_that_bai",
            )

        return True
