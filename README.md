# Scalable FastAPI Backend 🚀

Este proyecto es un backend **robusto, modular y escalable**, construido con **Python (FastAPI)** y **PostgreSQL**, siguiendo principios de **Clean Architecture**, **Separation of Concerns** y el **Patrón Repositorio**. La arquitectura está diseñada para permitir la evolución hacia otros protocolos de comunicación (GraphQL, gRPC, mensajería) sin reescribir la lógica de negocio.

---

## 🏗️ Arquitectura del Proyecto

La aplicación se organiza en capas claramente desacopladas para maximizar mantenibilidad, testabilidad y escalabilidad.

### 1. Capa de Presentación (API REST)

**Ruta:** `app/api`

* Expone los endpoints HTTP REST.
* Orquesta los casos de uso sin contener lógica de negocio.
* Valida y serializa datos de entrada/salida mediante **Pydantic**.
* Actúa como una *puerta de entrada* a la aplicación.

> En caso de incorporar GraphQL o gRPC, se crearían nuevas capas de entrada (`app/graphql`, `app/grpc`) reutilizando íntegramente los repositorios.

### 2. Capa de Repositorios (Dominio / Acceso a Datos)

**Ruta:** `app/repositories`

* Encapsula la lógica de acceso a datos y operaciones CRUD.
* Implementa el **Patrón Repositorio**.
* Aísla el ORM del resto de la aplicación.
* Garantiza independencia de la infraestructura.

### 3. Capa de Modelos y Core

**Rutas:** `app/models`, `app/core`

* Define las entidades persistentes usando **SQLModel**.
* Centraliza la configuración de base de datos y variables de entorno.
* Proporciona el motor asíncrono y la sesión de base de datos.

---

## 📁 Estructura de Directorios

```text
.
├── app/
│   ├── api/            # Endpoints REST (Controladores)
│   ├── core/           # Configuración y conexión a la base de datos
│   ├── models/         # Modelos SQLModel / Esquemas
│   ├── repositories/   # Lógica de negocio y acceso a datos
│   └── main.py         # Punto de entrada FastAPI
├── alembic/            # Migraciones de base de datos
├── tests/              # Pruebas unitarias e integración
├── docker-compose.yml  # Orquestación de servicios
├── Dockerfile          # Imagen de la aplicación
├── alembic.ini         # Configuración Alembic
└── requirements.txt    # Dependencias
```

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.11+
* **Framework Web:** FastAPI
* **ORM:** SQLModel (SQLAlchemy + Pydantic)
* **Base de Datos:** PostgreSQL 15
* **Migraciones:** Alembic
* **Driver Asíncrono:** asyncpg
* **Containerización:** Docker & Docker Compose
* **Testing:** Pytest

---

## 🚀 Despliegue con Docker

### 1. Prerrequisitos

Asegúrate de tener instalados:

* Docker
* Docker Compose
* Git

### 2. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

### 3. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (recomendado):

```ini
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/mydatabase
```

> Los valores por defecto permiten ejecutar el proyecto directamente con Docker Compose.

### 4. Construir y Levantar los Servicios

```bash
docker-compose up -d --build
```

Esto iniciará:

* PostgreSQL en el puerto `5432`.
* FastAPI en el puerto `8000`.

La aplicación espera automáticamente a que la base de datos esté disponible y ejecuta las migraciones.

### 5. Verificar Logs

```bash
docker-compose logs -f web
```

Deberías observar:

```text
Application startup complete.
```

---

## 🗄️ Gestión de Base de Datos (Alembic)

Todos los comandos deben ejecutarse dentro del contenedor `web`.

### Crear una Nueva Migración

```bash
docker-compose exec web alembic revision --autogenerate -m "Descripción del cambio"
```

### Aplicar Migraciones

```bash
docker-compose exec web alembic upgrade head
```

---

## ✅ Ejecución de Pruebas

El proyecto incluye pruebas unitarias y de integración.

```bash
docker-compose exec web pytest
```

---

## 📚 Documentación de la API

Una vez en ejecución:

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Ejemplo de Endpoints CRUD

* `POST   /api/v1/items/` – Crear un item
* `GET    /api/v1/items/` – Listar items
* `GET    /api/v1/items/{id}` – Obtener un item
* `PATCH  /api/v1/items/{id}` – Actualizar un item
* `DELETE /api/v1/items/{id}` – Eliminar un item

---

## 🔮 Escalabilidad Futura

La lógica de negocio está completamente desacoplada del protocolo de comunicación.

* **GraphQL:** Integración con Strawberry o Ariadne reutilizando los repositorios.
* **gRPC:** Implementación de servicios `.proto` llamando a la misma capa de dominio.
* **Mensajería:** Posible integración con Kafka, RabbitMQ o eventos asincrónicos.

---

## 🧪 Buenas Prácticas Aplicadas

* Clean Architecture
* Dependency Inversion
* Repository Pattern
* Async I/O end-to-end
* Infraestructura desacoplada
* Testing automatizado

---

**Hecho con ❤️ Python y FastAPI.**
