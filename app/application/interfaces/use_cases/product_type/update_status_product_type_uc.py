from abc import ABC, abstractmethod

from app.application.dto.product_type_dto import ProductTypeDTO


class IUpdateStatusProductTypeUC(ABC):
    @abstractmethod
    def execute(self, product_type_dto: ProductTypeDTO) -> bool: ...
