from typing import Optional


class Link:
    """Link represents a shortened link as an entity."""

    def __init__(
            self,
            code: str,
            source: str,
            created_at: Optional[int],
            owner_id: Optional[int]
    ):
        self.code = code
        self.source = source
        self.created_at = created_at
        self.owner_id = owner_id

    def __eq__(self, other) -> bool:
        if not isinstance(other, Link):
            return False
        return self.code == other.code
