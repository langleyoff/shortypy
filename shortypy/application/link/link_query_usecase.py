from abc import ABC, abstractmethod
from typing import Optional

from shortypy.domain.link import LinkNotFoundError

from .link_query_model import LinkReadModel
from .link_query_service import LinkQueryService


class LinkQueryUseCase(ABC):
    """LinkQueryUseCase defines a query usecase interface related to book entity."""

    @abstractmethod
    def fetch_link_by_id(self, link_id) -> Optional[LinkReadModel]:
        raise NotImplementedError


class LinkQueryUseCaseImpl(LinkQueryUseCase):
    def __init__(
            self,
            query_service: LinkQueryService
    ) -> None:
        self.query_service = query_service

    def fetch_link_by_id(self, link_id) -> Optional[LinkReadModel]:
        try:
            link = self.query_service.find_by_id(link_id)
            if link is None:
                raise LinkNotFoundError()
        except:
            raise

        return link
