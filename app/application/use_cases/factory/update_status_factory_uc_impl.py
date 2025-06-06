from app.application.interfaces.use_cases.factory.update_status_factory_uc import (
    IUpdateStatusFactoryUC,
)
from app.core.exception import BadRequestError
from app.domain.entities.factory_entity import FactoryEntity
from app.domain.interfaces.repositories.factory_repository import IFactoryRepository


class UpdateStatusFactoryUC(IUpdateStatusFactoryUC):
    def __init__(self, factory_repository: IFactoryRepository):
        self.factory_repository = factory_repository

    def execute(self, factory_id: int, is_active: bool) -> bool:
        query_entity = FactoryEntity(id=factory_id)

        factory = self.factory_repository.get_factory_by_id(factory=query_entity)

        if not factory:
            raise BadRequestError(
                error_code="ETB-nha_may_khong_ton_tai",
            )

        if not is_active:
            is_in_use = self.factory_repository.is_factory_in_use(factory=factory)

            if is_in_use:
                raise BadRequestError(
                    error_code="ETB-nha_may_dang_duoc_su_dung_khong_the_deactivate"
                )

        if factory.is_active == is_active:
            return True

        factory.set_is_active(is_active)

        is_updated = self.factory_repository.update_status_factory(factory=factory)

        if not is_updated:
            raise BadRequestError(
                error_code="ETB-cap_nhat_trang_thai_nha_may_that_bai",
            )
        return True
