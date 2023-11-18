from abc import ABC, abstractmethod
from typing import Optional

from shortypy.domain.link import Link


class LinkRepository(ABC):
    @abstractmethod
    def create(self, link: Link) -> Optional[Link]:
        raise NotImplementedError

    @abstractmethod
    def update(self, link: Link) -> Optional[Link]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, link_id) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, link_id) -> Optional[Link]:
        raise NotImplementedError
