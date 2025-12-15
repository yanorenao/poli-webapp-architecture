from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item, ItemCreate, ItemUpdate

class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item_data: ItemCreate) -> Item:
        db_item = Item.from_orm(item_data)
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item

    async def get_all(self) -> list[Item]:
        result = await self.session.execute(select(Item))
        return result.scalars().all()

    async def get_by_id(self, item_id: int) -> Item | None:
        return await self.session.get(Item, item_id)

    async def update(self, item_id: int, item_data: ItemUpdate) -> Item | None:
        db_item = await self.get_by_id(item_id)
        if not db_item:
            return None
        
        item_dict = item_data.dict(exclude_unset=True)
        for key, value in item_dict.items():
            setattr(db_item, key, value)
            
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item

    async def delete(self, item_id: int) -> bool:
        db_item = await self.get_by_id(item_id)
        if not db_item:
            return False
        await self.session.delete(db_item)
        await self.session.commit()
        return True