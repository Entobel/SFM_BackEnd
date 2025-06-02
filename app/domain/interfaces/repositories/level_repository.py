from abc import ABC, abstractmethod

from app.domain.entities.level_entity import LevelEntity


class ILevelRepository(ABC):
    @abstractmethod
    def get_list_levels(self, page: int, page_size: int, search: str, is_active: bool) -> dict[
                                                                                          "items": list[LevelEntity],
                                                                                          "total":int,
                                                                                          "page":int,
                                                                                          "page_size":int,
                                                                                          "total_pages":int,
                                                                                          ]: ...

    @abstractmethod
    def get_level_by_id(self, level_entity: LevelEntity) -> LevelEntity | None: ...

    @abstractmethod
    def get_level_by_name(self, level_entity: LevelEntity) -> LevelEntity | None: ...

    @abstractmethod
    def create_level(self, level_entity: LevelEntity) -> bool: ...

    @abstractmethod
    def update_level(self, level_entity: LevelEntity) -> bool: ...

    @abstractmethod
    def update_status_level(self, level_entity: LevelEntity) -> bool: ...
