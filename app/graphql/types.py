import strawberry
from typing import Optional

@strawberry.type
class ItemType:
    id: int
    title: str
    description: Optional[str]