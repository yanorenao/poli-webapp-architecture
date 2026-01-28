import strawberry
from typing import List, Optional
from strawberry.types import Info

from app.models.item import Producto, ProductoCreate, ProductoUpdate
from app.repositories.producto_repository import ProductoRepository
from app.graphql.types import ProductoType

@strawberry.type
class Query:
    @strawberry.field
    async def get_productos(self, info: Info) -> List[ProductoType]:
        session = info.context["session"]
        repo = ProductoRepository(session)
        productos = await repo.get_all()
        return [ProductoType.from_pydantic(p) for p in productos]

    @strawberry.field
    async def get_producto(self, info: Info, id: int) -> Optional[ProductoType]:
        session = info.context["session"]
        repo = ProductoRepository(session)
        producto = await repo.get_by_id(id)
        if producto:
            return ProductoType.from_pydantic(producto)
        return None

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_producto(
        self, 
        info: Info, 
        nombre: str, 
        precio: float, 
        descripcion: Optional[str] = None
    ) -> ProductoType:
        session = info.context["session"]
        repo = ProductoRepository(session)
        
        producto_in = ProductoCreate(
            nombre=nombre, 
            precio=precio, 
            descripcion=descripcion
        )
        nuevo_producto = await repo.create(producto_in)
        return ProductoType.from_pydantic(nuevo_producto)

    @strawberry.mutation
    async def update_producto(
        self, 
        info: Info, 
        id: int, 
        nombre: Optional[str] = None, 
        precio: Optional[float] = None, 
        descripcion: Optional[str] = None
    ) -> Optional[ProductoType]:
        session = info.context["session"]
        repo = ProductoRepository(session)
        
        # 1. Crear diccionario solo con los valores que NO son None
        update_data = {}
        if nombre is not None:
            update_data["nombre"] = nombre
        if precio is not None:
            update_data["precio"] = precio
        if descripcion is not None:
            update_data["descripcion"] = descripcion
            
        # 2. Pasar los datos desempaquetados al modelo
        # Esto asegura que Pydantic marque los campos como "set" solo si venían en la petición
        producto_data = ProductoUpdate(**update_data)
        
        updated = await repo.update(id, producto_data)
        if updated:
            return ProductoType.from_pydantic(updated)
        return None

    @strawberry.mutation
    async def delete_producto(self, info: Info, id: int) -> bool:
        session = info.context["session"]
        repo = ProductoRepository(session)
        return await repo.delete(id)

schema = strawberry.Schema(query=Query, mutation=Mutation)