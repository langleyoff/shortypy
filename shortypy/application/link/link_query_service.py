from abc import ABC, abstractmethod
from typing import Optional

from .link_query_model import LinkReadModel


class LinkQueryService(ABC):
    """LinkQueryService defines an interface for query services related to Link model."""

    @abstractmethod
    def find_by_id(self, link_id: str) -> Optional[LinkReadModel]:
        raise NotImplementedError
