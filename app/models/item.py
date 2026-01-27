from typing import Optional
from sqlmodel import Field, SQLModel

# Clase base con los atributos requeridos 
class ProductoBase(SQLModel):
    nombre: str  
    descripcion: Optional[str] = None  
    precio: float  

# Entidad para la base de datos 
class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Esquema para la creación de productos
class ProductoCreate(ProductoBase):
    pass

# Esquema para actualizaciones 
class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None