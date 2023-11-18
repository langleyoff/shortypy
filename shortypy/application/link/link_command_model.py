from typing import Optional

from pydantic import BaseModel


class LinkCreateModel(BaseModel):
    """LinkCreateModel represents a write model to create a Link."""
    source: str
    owner_id: Optional[int]
