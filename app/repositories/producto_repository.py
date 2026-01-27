from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Producto, ProductoCreate, ProductoUpdate 

class ProductoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, producto_data: ProductoCreate) -> Producto:
        db_producto = Producto.from_orm(producto_data)
        self.session.add(db_producto)
        await self.session.commit()
        await self.session.refresh(db_producto)
        return db_producto

    async def get_all(self) -> list[Producto]:
        result = await self.session.execute(select(Producto))
        return result.scalars().all()

    async def get_by_id(self, producto_id: int) -> Producto | None:
        return await self.session.get(Producto, producto_id)

    async def update(self, producto_id: int, producto_data: ProductoUpdate) -> Producto | None:
        db_producto = await self.get_by_id(producto_id)
        if not db_producto:
            return None
        
        producto_dict = producto_data.dict(exclude_unset=True)
        for key, value in producto_dict.items():
            setattr(db_producto, key, value)
            
        self.session.add(db_producto)
        await self.session.commit()
        await self.session.refresh(db_producto)
        return db_producto

    async def delete(self, producto_id: int) -> bool:
        db_producto = await self.get_by_id(producto_id)
        if not db_producto:
            return False
        await self.session.delete(db_producto)
        await self.session.commit()
        return True