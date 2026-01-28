# 🚀 Backend Híbrido: REST + GraphQL + gRPC

Este proyecto implementa una arquitectura de backend moderna, escalable y desacoplada que expone **tres interfaces de comunicación simultáneas** sobre una misma lógica de negocio y una única base de datos:

1. **REST API** (FastAPI)
2. **GraphQL** (Strawberry)
3. **gRPC** (Google Remote Procedure Call)

La solución está diseñada siguiendo principios de **Clean Architecture**, **Dependency Inversion** y el **Patrón Repositorio**, garantizando mantenibilidad, testabilidad y evolución tecnológica sin reescritura del core.

---

## 🏗️ Arquitectura del Proyecto

La aplicación se organiza en capas claramente desacopladas. Cada protocolo actúa como una *capa de entrada* independiente que reutiliza la misma lógica de negocio y acceso a datos.

### 1. Capa de Presentación (REST / GraphQL / gRPC)

**Rutas:**

* `app/api` – REST API (FastAPI)
* `app/graphql` – GraphQL (Strawberry)
* `app/grpc` – gRPC (Protobuf + grpcio)

Responsabilidades:

* Exponer contratos de comunicación.
* Orquestar casos de uso sin lógica de negocio.
* Validar y serializar datos de entrada/salida.
* Delegar toda la lógica a la capa de dominio.

---

### 2. Capa de Repositorios (Dominio / Acceso a Datos)

**Ruta:** `app/repositories`

* Implementa el **Repository Pattern**.
* Encapsula operaciones CRUD y consultas complejas.
* Aísla completamente el ORM del resto del sistema.
* Permite cambiar PostgreSQL, SQLModel u ORM sin impacto en la capa superior.

---

### 3. Capa de Modelos y Core

**Rutas:** `app/models`, `app/core`

* Define entidades persistentes con **SQLModel**.
* Centraliza configuración, variables de entorno y settings.
* Gestiona motor asíncrono, sesiones y dependencias de base de datos.

---

## 📁 Estructura de Directorios

```text
.
├── app/
│   ├── api/              # Endpoints REST (FastAPI)
│   ├── graphql/          # Esquemas y resolvers GraphQL
│   ├── grpc/             # Servicios gRPC y archivos .proto
│   ├── core/             # Configuración y base de datos
│   ├── models/           # Modelos SQLModel
│   ├── repositories/     # Lógica de dominio y acceso a datos
│   └── main.py           # Punto de entrada unificado
├── alembic/              # Migraciones de base de datos
├── tests/                # Pruebas unitarias e integración
├── docker-compose.yml    # Orquestación de servicios
├── Dockerfile            # Imagen de la aplicación
├── alembic.ini           # Configuración Alembic
└── requirements.txt      # Dependencias
```

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.11+
* **Framework Web:** FastAPI
* **ORM:** SQLModel (SQLAlchemy + Pydantic)
* **Base de Datos:** PostgreSQL 15
* **Migraciones:** Alembic
* **Driver Asíncrono:** asyncpg
* **GraphQL:** Strawberry (schema-first)
* **gRPC:** grpcio + Protobuf
* **Testing:** Pytest
* **Containerización:** Docker & Docker Compose

---

## 🚀 Despliegue con Docker

### 1. Prerrequisitos

* Docker
* Docker Compose
* Git

---

### 2. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

---

### 3. Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```ini
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/mydatabase
```

> Los valores por defecto permiten ejecutar el proyecto directamente con Docker Compose.

---

### 4. Construir y Levantar Servicios

```bash
docker-compose up -d --build
```

Servicios expuestos:

* PostgreSQL → `5432`
* FastAPI → `8000`
* gRPC → `50051`

La aplicación espera automáticamente la base de datos y ejecuta migraciones.

---

### 5. Verificar Logs

```bash
docker-compose logs -f web
```

Salida esperada:

```text
Application startup complete.
```

---

## 🗄️ Gestión de Base de Datos (Alembic)

Ejecutar siempre dentro del contenedor `web`.

### Crear Migración

```bash
docker-compose exec web alembic revision --autogenerate -m "Descripción del cambio"
```

### Aplicar Migraciones

```bash
docker-compose exec web alembic upgrade head
```

---

## ✅ Ejecución de Pruebas

```bash
docker-compose exec web pytest
```

Incluye:

* Pruebas unitarias de repositorios.
* Pruebas de integración para REST, GraphQL y gRPC.

---

## 📡 Endpoints y Servicios

| Protocolo | URL / Dirección                                                | Descripción |
| --------- | -------------------------------------------------------------- | ----------- |
| REST API  | [http://localhost:8000/docs](http://localhost:8000/docs)       | Swagger UI  |
| GraphQL   | [http://localhost:8000/graphql](http://localhost:8000/graphql) | GraphiQL    |
| gRPC      | localhost:50051                                                | RPC binario |

---

### Ejemplo REST CRUD

* `POST   /api/v1/items/`
* `GET    /api/v1/items/`
* `GET    /api/v1/items/{id}`
* `PATCH  /api/v1/items/{id}`
* `DELETE /api/v1/items/{id}`

---

## 🕸️ Ejemplo GraphQL

```graphql
mutation {
  createProducto(
    nombre: "Teclado Mecánico"
    precio: 120.50
    descripcion: "Switch Cherry MX Blue"
  ) {
    id
    nombre
  }
}
```

---

## ⚡ Cómo probar gRPC

El servidor escucha en el puerto `50051`.

Archivo `.proto`:

```
app/grpc/producto.proto
```

### Usando Postman

1. New gRPC Request.
2. URL: `localhost:50051`.
3. Importar archivo `.proto`.
4. Ejecutar `CreateProducto`:

```json
{
  "nombre": "Monitor gRPC",
  "descripcion": "Test desde Postman",
  "precio": 300.00
}
```

---

## 🔮 Escalabilidad Futura

* Reutilización total del dominio para nuevos protocolos.
* Integración con mensajería (Kafka, RabbitMQ).
* Separación futura en microservicios sin refactor del core.

---

## 🧪 Buenas Prácticas Aplicadas

* Clean Architecture
* Dependency Inversion Principle
* Repository Pattern
* Async I/O end-to-end
* Infraestructura desacoplada
* Testing automatizado

---

**Hecho con ❤️ usando Python y FastAPI.**