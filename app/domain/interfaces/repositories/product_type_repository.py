from abc import ABC, abstractmethod

from app.domain.entities.product_type_entity import ProductTypeEntity


class IProductTypeRepository(ABC):
    @abstractmethod
    def get_all_product_types(self) -> list[ProductTypeEntity]: ...

    @abstractmethod
    def get_product_type_by_id(
        self, product_type_entity: ProductTypeEntity
    ) -> ProductTypeEntity | None: ...

    @abstractmethod
    def get_product_type_by_name(
        self, name: str
    ) -> ProductTypeEntity | None: ...

    @abstractmethod
    def create_product_type(
        self, product_type_entity: ProductTypeEntity
    ) -> bool: ...

    @abstractmethod
    def update_product_type(
        self, product_type_entity: ProductTypeEntity
    ) -> bool: ...

    @abstractmethod
    def update_status_product_type(
        self, product_type_entity: ProductTypeEntity
    ) -> bool: ...
