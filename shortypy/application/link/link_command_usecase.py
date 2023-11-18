from abc import ABC, abstractmethod
from time import time
from typing import Optional

from shortypy.domain.link import (
    Link,
    LinkRepository,
    LinkCodeAlreadyExistsError,
    LinkNotFoundError
)
from shortypy.application.code_generation import CodeGenerator

from .link_command_model import LinkCreateModel
from .link_query_model import LinkReadModel


def epoch_timestamp() -> int:
    return int(time())


class LinkCommandUseCase(ABC):
    @abstractmethod
    def create_link(self, data: LinkCreateModel) -> Optional[LinkReadModel]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, link_id):
        raise NotImplementedError


class LinkCommandUseCaseUnitOfWork(ABC):
    @property
    @abstractmethod
    def repository(self) -> LinkRepository:
        raise NotImplementedError

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class LinkCommandUseCaseImpl(LinkCommandUseCase):
    def __init__(
            self,
            uow: LinkCommandUseCaseUnitOfWork,
            code_generator: CodeGenerator
    ) -> None:
        self.uow = uow
        self.code_generator = code_generator

    def create_link(self, data: LinkCreateModel) -> Optional[LinkReadModel]:
        try:
            code = self.code_generator.generate()
            link = Link(
                code=code,
                source=data.source,
                owner_id=data.owner_id,
                created_at=epoch_timestamp()
            )

            existing_link = self.uow.repository.find_by_id(123)
            if existing_link is not None:
                raise LinkCodeAlreadyExistsError()

            self.uow.repository.create(link)
            self.uow.commit()

            created_link = self.uow.repository.find_by_id(code)
        except:
            self.uow.rollback()
            raise

        return LinkReadModel.from_entity(created_link)

    def delete_by_id(self, link_id):
        try:
            existing_link = self.uow.repository.find_by_id(link_id)

            if existing_link is None:
                raise LinkNotFoundError()

            self.uow.repository.delete_by_id(link_id)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise
