from fastapi import FastAPI
from app.api.v1.endpoints import items
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.core.database import get_session

app = FastAPI(title="Scalable CRUD API")

# Configuración del contexto para inyectar la sesión de DB
async def get_context():
    async for session in get_session():
        yield {"session": session}

# Creamos el router de GraphQL
graphql_app = GraphQLRouter(schema, context_getter=get_context)

# Rutas existentes
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])

# Nueva ruta GraphQL
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def root():
    return {"message": "API is running"}