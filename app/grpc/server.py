import asyncio
import logging
import grpc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# Importaciones de los archivos generados por protoc

import app.grpc.producto_pb2 as pb2
import app.grpc.producto_pb2_grpc as pb2_grpc

# Importaciones de tu lógica de negocio
from app.repositories.producto_repository import ProductoRepository
from app.core.database import engine
from app.models.item import ProductoCreate, ProductoUpdate

# Configuración de sesión local
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class ProductoServicer(pb2_grpc.ProductoServiceServicer):
    """Implementación de los servicios CRUD definidos en el archivo .proto"""

    async def CreateProducto(self, request, context):
        async with SessionLocal() as session:
            repo = ProductoRepository(session)
            try:
                p_in = ProductoCreate(
                    nombre=request.nombre,
                    precio=request.precio,
                    descripcion=request.descripcion
                )
                p = await repo.create(p_in)
                return pb2.ProductoResponse(
                    id=p.id,
                    nombre=p.nombre,
                    descripcion=p.descripcion or "",
                    precio=p.precio
                )
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, f"Error al crear producto: {str(e)}")

    async def GetProducto(self, request, context):
        async with SessionLocal() as session:
            repo = ProductoRepository(session)
            p = await repo.get_by_id(request.id)
            if not p:
                context.abort(grpc.StatusCode.NOT_FOUND, f"Producto con ID {request.id} no encontrado")
            
            return pb2.ProductoResponse(
                id=p.id,
                nombre=p.nombre,
                descripcion=p.descripcion or "",
                precio=p.precio
            )

    async def GetAllProductos(self, request, context):
        async with SessionLocal() as session:
            repo = ProductoRepository(session)
            productos = await repo.get_all()
            
            responses = [
                pb2.ProductoResponse(
                    id=p.id,
                    nombre=p.nombre,
                    descripcion=p.descripcion or "",
                    precio=p.precio
                ) for p in productos
            ]
            return pb2.ProductoListResponse(productos=responses)

    async def UpdateProducto(self, request, context):
        async with SessionLocal() as session:
            repo = ProductoRepository(session)
            p_update = ProductoUpdate(
                nombre=request.nombre if request.nombre else None,
                precio=request.precio if request.precio > 0 else None,
                descripcion=request.descripcion if request.descripcion else None
            )
            
            updated_p = await repo.update(request.id, p_update)
            if not updated_p:
                context.abort(grpc.StatusCode.NOT_FOUND, f"No se pudo actualizar: Producto {request.id} no existe")
            
            return pb2.ProductoResponse(
                id=updated_p.id,
                nombre=updated_p.nombre,
                descripcion=updated_p.descripcion or "",
                precio=updated_p.precio
            )

    async def DeleteProducto(self, request, context):
        async with SessionLocal() as session:
            repo = ProductoRepository(session)
            success = await repo.delete(request.id)
            if not success:
                context.abort(grpc.StatusCode.NOT_FOUND, f"No se pudo eliminar: Producto {request.id} no existe")
            
            return pb2.DeleteResponse(success=True)

async def serve():
    server = grpc.aio.server()
    pb2_grpc.add_ProductoServiceServicer_to_server(ProductoServicer(), server)
    
    # Puerto estandar para gRPC definido en la arquitectura
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    
    logging.info(f"Servidor gRPC iniciado en {listen_addr}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        pass