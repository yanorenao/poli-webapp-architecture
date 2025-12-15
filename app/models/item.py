from typing import Optional
from sqlmodel import Field, SQLModel

class ItemBase(SQLModel):
    title: str
    description: Optional[str] = None

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None