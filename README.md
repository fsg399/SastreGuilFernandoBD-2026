# SastreGuilFernandoBD-2026
# Biblioteca REST API

API REST para la gestión de una biblioteca, desarrollada con **FastAPI** y **MySQL**, 
desplegada con **Docker** (Uvicorn en puerto 8000, MySQL en puerto 3306).

## Tecnologías

- Python 3.11
- FastAPI
- MySQL 8.0
- Docker + Docker Compose
- Uvicorn

## Instalación y puesta en marcha

1. Clona el repositorio:
   git clone [https://github.com/tuusuario/biblioteca-restapi.git](https://github.com/fsg399/SastreGuilFernandoBD-2026.git)

2. Renombra el archivo de entorno:
   cp setup-environment/.env.example setup-environment/.env
   (edita los valores de contraseña)

3. Arranca los contenedores:
   cd setup-environment
   docker-compose up -d

4. Importa la base de datos en MySQL Workbench:
   - biblioteca-schema.sql
   - biblioteca-datos.sql

5. Crea el usuario de base de datos:
   CREATE USER biblioteca@'%' IDENTIFIED BY 'biblioteca123';
   GRANT ALL PRIVILEGES ON PrestamosBiblioteca.* TO biblioteca@'%';
   FLUSH PRIVILEGES;

6. La API estará disponible en: http://localhost:8000
   Documentación Swagger: http://localhost:8000/docs

---

## Endpoints

### 📚 Libros

---

#### GET /books/
Devuelve la lista completa de libros.

**Petición:**
curl http://localhost:8000/books/

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "titulo": "El Quijote",
    "autor": "Miguel de Cervantes",
    "editorial": "Editorial A",
    "publicadoEn": 1605,
    "categoria": "Ficción"
  },
  {
    "id": 2,
    "titulo": "Cien años de soledad",
    "autor": "Gabriel García Márquez",
    "editorial": "Editorial B",
    "publicadoEn": 1967,
    "categoria": "Ficción"
  }
]
```

---

#### GET /books/{id}
Devuelve un libro por su ID.

**Petición:**
curl http://localhost:8000/books/1

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "titulo": "El Quijote",
  "autor": "Miguel de Cervantes",
  "editorial": "Editorial A",
  "publicadoEn": 1605,
  "categoria": "Ficción"
}
```

**Respuesta si no existe (404):**
```json
{ "detail": "Book not found" }
```

---

#### POST /books/
Crea un nuevo libro.

**Petición:**
curl -X POST http://localhost:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Don Quijote",
    "autor": "Cervantes",
    "editorial": "Espasa",
    "publicadoEn": 1605,
    "categoria": "Ficción"
  }'

**Respuesta (201 Created):**
```json
{
  "id": 18,
  "titulo": "Don Quijote",
  "autor": "Cervantes",
  "editorial": "Espasa",
  "publicadoEn": 1605,
  "categoria": "Ficción"
}
```

---

#### PUT /books/{id}
Actualiza un libro existente por su ID.

**Petición:**
curl -X PUT http://localhost:8000/books/18 \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Don Quijote de la Mancha",
    "autor": "Miguel de Cervantes",
    "editorial": "Espasa Calpe",
    "publicadoEn": 1605,
    "categoria": "Ficción"
  }'

**Respuesta (200 OK):**
```json
{
  "id": 18,
  "titulo": "Don Quijote de la Mancha",
  "autor": "Miguel de Cervantes",
  "editorial": "Espasa Calpe",
  "publicadoEn": 1605,
  "categoria": "Ficción"
}
```

**Respuesta si no existe (404):**
```json
{ "detail": "Book not found" }
```

---

#### DELETE /books/{id}
Elimina un libro por su ID.

**Petición:**
curl -X DELETE http://localhost:8000/books/18

**Respuesta:** 204 No Content (sin cuerpo)

**Respuesta si tiene ejemplares asociados (409):**
```json
{ "detail": "No se puede eliminar: el libro tiene ejemplares o reseñas asociados" }
```

---

### 🔄 Préstamos

---

#### POST /loans/
Crea un nuevo préstamo de un ejemplar.

**Petición:**
curl -X POST http://localhost:8000/loans/ \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "inventoryNumber": "EJ001"
  }'

**Respuesta (200 OK):**
```json
{ "message": "Préstamo creado correctamente" }
```

**Respuesta si el ejemplar no está disponible (400):**
```json
{ "detail": "El ejemplar no está disponible" }
```

---

#### POST /loans/return
Registra la devolución de un ejemplar prestado.

**Petición:**
curl -X POST http://localhost:8000/loans/return \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "inventoryNumber": "EJ001"
  }'

**Respuesta (200 OK):**
```json
{ "message": "Devolución registrada correctamente" }
```

**Respuesta si no hay préstamo activo (404):**
```json
{ "detail": "No se encontró un préstamo activo para ese ejemplar y usuario" }
```
