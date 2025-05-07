from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.role import Role

# create abstract base class


class IRoleRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Role]:
        pass
