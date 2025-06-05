from app.application.dto.factory_dto import FactoryDTO
from app.application.interfaces.use_cases.factory.update_factory_uc import (
    IUpdateFactoryUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.interfaces.repositories.factory_repository import IFactoryRepository


class UpdateFactoryUC(IUpdateFactoryUC):
    def __init__(self, factory_repository: IFactoryRepository):
        self.factory_repository = factory_repository

    def execute(self, factory_id: int, factory_dto: FactoryDTO) -> bool:
        query_entity = FactoryEntity(
            id=factory_id,
            abbr_name=factory_dto.abbr_name,
            name=factory_dto.name,
            description=factory_dto.description,
            location=factory_dto.location,
        )

        factory_entity = self.factory_repository.get_factory_by_id(
            factory_entity=query_entity
        )

        if not factory_entity:
            raise BadRequestError(
                error_code="ETB-nha_may_khong_ton_tai",
            )

        if query_entity.name:
            factory_entity.set_name(query_entity.name)

        if query_entity.abbr_name:
            factory_entity.set_abbr_name(query_entity.abbr_name)

        if query_entity.description:
            factory_entity.set_description(query_entity.description)

        if query_entity.location:
            factory_entity.set_location(query_entity.location)

        is_updated = self.factory_repository.update_factory(factory=factory_entity)

        if not is_updated:
            raise BadRequestError(
                error_code="ETB-cap_nhat_nha_may_that_bai",
            )

        return True
