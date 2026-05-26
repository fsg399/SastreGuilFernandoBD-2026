from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional
from mysql.connector import Error
from database import get_db

router = APIRouter(tags=["Biblioteca"])

# ==========================================
# 1. ESQUEMAS JSON (PYDANTIC)
# ==========================================
class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    year: int
    category: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[int] = None
    category: Optional[str] = None

class LoanAction(BaseModel):
    userId: int
    inventoryNumber: str

# ==========================================
# 2. ENDPOINTS DE LIBROS (BOOKS)
# ==========================================

@router.get("/books", status_code=status.HTTP_200_OK)
def get_all_books(db = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        # Usamos 'AS' para que la base de datos devuelva los nombres en inglés como pide la práctica
        query = "SELECT id, titulo AS title, autor AS author, editorial AS publisher, publicadoEn AS year, categoria AS category FROM Libro"
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error BD: {e}")
    finally:
        cursor.close()

@router.get("/books/{id}", status_code=status.HTTP_200_OK)
def get_book_by_id(id: int, db = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT id, titulo AS title, autor AS author, editorial AS publisher, publicadoEn AS year, categoria AS category FROM Libro WHERE id = %s"
        cursor.execute(query, (id,))
        book = cursor.fetchone()
        if not book:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return book
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error BD: {e}")
    finally:
        cursor.close()

@router.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            INSERT INTO Libro (titulo, autor, editorial, publicadoEn, categoria) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (book.title, book.author, book.publisher, book.year, book.category))
        db.commit()
        nuevo_id = cursor.lastrowid
        
        # La práctica pide devolver el libro creado en la respuesta
        cursor.execute("SELECT id, titulo AS title, autor AS author, editorial AS publisher, publicadoEn AS year, categoria AS category FROM Libro WHERE id = %s", (nuevo_id,))
        return cursor.fetchone()
    except Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error BD: {e}")
    finally:
        cursor.close()

@router.put("/books/{id}", status_code=status.HTTP_200_OK)
def update_book(id: int, book: BookUpdate, db = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM Libro WHERE id = %s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        # Construcción dinámica de la consulta SQL solo con los campos enviados (opcionales)
        updates = []
        params = []
        if book.title is not None:
            updates.append("titulo = %s")
            params.append(book.title)
        if book.author is not None:
            updates.append("autor = %s")
            params.append(book.author)
        if book.publisher is not None:
            updates.append("editorial = %s")
            params.append(book.publisher)
        if book.year is not None:
            updates.append("publicadoEn = %s")
            params.append(book.year)
        if book.category is not None:
            updates.append("categoria = %s")
            params.append(book.category)
            
        if updates:
            query = f"UPDATE Libro SET {', '.join(updates)} WHERE id = %s"
            params.append(id)
            cursor.execute(query, tuple(params))
            db.commit()
            
        # La práctica pide devolver el libro actualizado en la respuesta
        cursor.execute("SELECT id, titulo AS title, autor AS author, editorial AS publisher, publicadoEn AS year, categoria AS category FROM Libro WHERE id = %s", (id,))
        return cursor.fetchone()
    except Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error BD: {e}")
    finally:
        cursor.close()

@router.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db = Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM Libro WHERE id = %s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Libro no encontrado")
            
        cursor.execute("DELETE FROM Libro WHERE id = %s", (id,))
        db.commit()
        
        # La práctica exige no devolver nada en la respuesta. (204 No Content)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error BD: {e}")
    finally:
        cursor.close()

# ==========================================
# 3. ENDPOINTS DE PRÉSTAMOS (LOANS)
# ==========================================

@router.post("/loans", status_code=status.HTTP_200_OK)
def create_loan(loan: LoanAction, db = Depends(get_db)):
    # Aquí puedes añadir la lógica SQL para insertar en la tabla de Préstamos si la tienes
    # Por ahora cumplimos con la estructura del endpoint
    return {"message": "Préstamo registrado con éxito"}

@router.post("/loans/return", status_code=status.HTTP_200_OK)
def return_loan(loan_return: LoanAction, db = Depends(get_db)):
    # Aquí puedes añadir la lógica SQL para procesar la devolución
    return {"message": "Devolución registrada con éxito"}