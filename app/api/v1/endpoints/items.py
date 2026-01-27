from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.models.item import Producto, ProductoCreate, ProductoUpdate
from app.repositories.producto_repository import ProductoRepository

router = APIRouter()

@router.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def create_item(item: ProductoCreate, session: AsyncSession = Depends(get_session)):
    # Se actualizó ItemRepository por ProductoRepository
    repo = ProductoRepository(session)
    return await repo.create(item)

@router.get("/", response_model=list[Producto])
async def read_items(session: AsyncSession = Depends(get_session)):
    repo = ProductoRepository(session)
    return await repo.get_all()

@router.get("/{item_id}", response_model=Producto)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    repo = ProductoRepository(session)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@router.patch("/{item_id}", response_model=Producto)
async def update_item(item_id: int, item_update: ProductoUpdate, session: AsyncSession = Depends(get_session)):
    repo = ProductoRepository(session)
    updated_item = await repo.update(item_id, item_update)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    repo = ProductoRepository(session)
    success = await repo.delete(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None