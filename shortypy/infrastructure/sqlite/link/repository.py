from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from shortypy.domain.link import Link, LinkRepository
from shortypy.application.link import LinkCommandUseCaseUnitOfWork

from .link_dto import LinkDTO


class LinkRepositoryImpl(LinkRepository):
    """LinkRepositoryImpl implements CRUD operations related to Link entity using SQLAlchemy"""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, link: Link) -> Optional[Link]:
        link_dto = LinkDTO.from_entity(link)
        try:
            self.session.add(link_dto)
            return link
        except:
            raise

    def update(self, link: Link) -> Optional[Link]:
        dto = LinkDTO.from_entity(link)
        try:
            stored = self.session.query(LinkDTO).filter_by(code=dto.code).one()
            stored.code = dto.code
            stored.source = dto.source
            stored.created_at = dto.created_at
            stored.owner_id = dto.owner_id

            return link
        except:
            raise

    def delete_by_id(self, link_id) -> None:
        try:
            self.session.query(LinkDTO).filter_by(code=link_id).delete()
        except:
            raise

    def find_by_id(self, link_id) -> Optional[Link]:
        try:
            dto = self.session.query(LinkDTO).filter_by(code=link_id).one()
        except NoResultFound:
            return None
        except:
            raise

        # noinspection PyArgumentList
        return dto.to_entity()


class LinkCommandUseCaseUnitOfWorkImpl(LinkCommandUseCaseUnitOfWork):
    def __init__(
            self,
            session: Session,
            repository: LinkRepository
    ) -> None:
        self.session = session
        self._repository = repository

    @property
    def repository(self) -> LinkRepository:
        return self._repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
