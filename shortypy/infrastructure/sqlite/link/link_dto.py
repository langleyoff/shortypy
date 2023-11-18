from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from shortypy.domain.link import Link
from shortypy.infrastructure.sqlite.database import Base
from shortypy.application.link import LinkReadModel


class LinkDTO(Base):
    __tablename__ = "links"

    code: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    source: Mapped[str] = mapped_column()
    created_at: Mapped[int] = mapped_column(index=True, nullable=False)
    owner_id: Mapped[Optional[int]] = mapped_column(index=True, nullable=True)

    def to_entity(self) -> Link:
        return Link(
            code=self.code,
            source=self.source,
            created_at=self.created_at,
            owner_id=self.owner_id
        )

    def to_read_model(self) -> LinkReadModel:
        return LinkReadModel(
            code=self.code,
            source=self.source,
            created_at=self.created_at,
            owner_id=self.owner_id
        )

    @classmethod
    def from_entity(cls, link: Link) -> 'LinkDTO':
        return LinkDTO(
            code=link.code,
            source=link.source,
            created_at=link.created_at,
            owner_id=link.owner_id
        )
