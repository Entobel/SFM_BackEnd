from abc import ABC, abstractmethod


class IListDepartmentFactoryUC(ABC):
    @abstractmethod
    def execute(
        self,
        page: int,
        page_size: int,
        search: str,
        is_active: bool,
        department_id: int,
        factory_id: int,
    ) -> dict:
        pass
