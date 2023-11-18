from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from shortypy.application.link import LinkQueryService, LinkReadModel

from .link_dto import LinkDTO


class LinkQueryServiceImpl(LinkQueryService):
    def __init__(
            self,
            session: Session
    ) -> None:
        self.session = session

    def find_by_id(self, link_id: str) -> Optional[LinkReadModel]:
        try:
            link_dto = self.session.query(LinkDTO).filter_by(code=link_id).one()
        except NoResultFound:
            return None
        except:
            raise

        return link_dto.to_read_model()
