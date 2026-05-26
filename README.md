# SastreGuilFernandoBD-2026 - Biblioteca REST API

API REST para la gestión de una biblioteca, desarrollada con **FastAPI** y **MySQL**. Proporciona la conexión con una base de datos local y permite realizar operaciones CRUD sobre el catálogo de libros y gestionar préstamos. Expone endpoints de salud, documentación interactiva y recursos de datos.

## Tecnologías
- **Python 3.11**
- **FastAPI** & **Uvicorn**
- **MySQL 8.0**
- **Docker** & **Docker Compose**

---

## Arquitectura

```mermaid
flowchart LR

fastapi["🐍 FastAPI (8000)<br/>Uvicorn"]
mysql["🗄️ MySQL 8 (3306)"]

fastapi -->|SQL| mysql
