from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.models.item import Item, ItemCreate, ItemUpdate
from app.repositories.item_repository import ItemRepository

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    return await repo.create(item)

@router.get("/", response_model=list[Item])
async def read_items(session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    return await repo.get_all()

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.patch("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemUpdate, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    updated_item = await repo.update(item_id, item_update)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    success = await repo.delete(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None