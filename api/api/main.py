# from routes import base and books
from routes import base, books
from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI(
    title="Products API",
    description="API for managing products using FastAPI and MySQL",
    version="1.0.0"
)

app.include_router(base.router)
app.include_router(books.router)
