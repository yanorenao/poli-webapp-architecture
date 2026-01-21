import strawberry
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info

from app.graphql.types import ItemType
from app.repositories.item_repository import ItemRepository

@strawberry.type
class Query:
    @strawberry.field
    async def items(self, info: Info) -> List[ItemType]:
        # Obtenemos la sesión de base de datos desde el contexto
        session: AsyncSession = info.context["session"]
        
        # Reutilizamos tu lógica de negocio existente
        repo = ItemRepository(session)
        items_db = await repo.get_all()
        
        # Convertimos los modelos de SQLModel a Tipos de Strawberry
        return [
            ItemType(
                id=item.id, 
                title=item.title, 
                description=item.description
            ) for item in items_db
        ]

schema = strawberry.Schema(query=Query)