from typing import Optional

from pydantic import BaseModel, ConfigDict

from shortypy.domain.link import Link


class LinkReadModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    source: str
    created_at: Optional[int]
    owner_id: Optional[int]

    @classmethod
    def from_entity(cls, link: Link) -> 'LinkReadModel':
        return cls(
            code=link.code,
            source=link.source,
            created_at=link.created_at,
            owner_id=link.owner_id
        )
