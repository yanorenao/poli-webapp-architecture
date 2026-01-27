import strawberry
from typing import Optional
from app.models.item import Producto # Asegúrate de que el nombre del archivo sea correcto

@strawberry.experimental.pydantic.type(model=Producto, all_fields=True)
class ProductoType:
    """
    Representación de GraphQL del modelo Producto.
    'all_fields=True' mapea automáticamente id, nombre, descripcion y precio. 
    """
    pass