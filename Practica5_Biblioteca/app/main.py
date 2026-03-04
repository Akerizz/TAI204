from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

app = FastAPI(title="API Biblioteca Digital")

libros_db = []
prestamos_db = []

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2)
    correo: EmailStr

class Libro(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    anio: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: str = Field(default="disponible", pattern="^(disponible|prestado)$")

class Prestamo(BaseModel):
    id_prestamo: int
    id_libro: int
    usuario: Usuario

@app.post("/v1/libros/", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    libros_db.append(libro.model_dump())
    return {"mensaje": "Libro registrado"}

@app.get("/v1/libros/disponibles")
def listar_disponibles():
    return [l for l in libros_db if l["estado"] == "disponible"]

@app.get("/v1/libros/buscar")
def buscar_libro(nombre: str):
    return [l for l in libros_db if nombre.lower() in l["nombre"].lower()]

@app.post("/v1/prestamos/")
def registrar_prestamo(prestamo: Prestamo):
    for libro in libros_db:
        if libro["id"] == prestamo.id_libro:
            if libro["estado"] == "prestado":
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya está prestado")
            libro["estado"] = "prestado"
            prestamos_db.append(prestamo.model_dump())
            return {"mensaje": "Préstamo registrado"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")

@app.put("/v1/prestamos/devolver/{id_libro}", status_code=status.HTTP_200_OK)
def devolver_libro(id_libro: int):
    for i, prestamo in enumerate(prestamos_db):
        if prestamo["id_libro"] == id_libro:
            for libro in libros_db:
                if libro["id"] == id_libro:
                    libro["estado"] = "disponible"
            prestamos_db.pop(i)
            return {"mensaje": "Libro devuelto"}
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro de préstamo ya no existe")

@app.delete("/v1/prestamos/{id_prestamo}")
def eliminar_prestamo(id_prestamo: int):
    for i, prestamo in enumerate(prestamos_db):
        if prestamo["id_prestamo"] == id_prestamo:
            prestamos_db.pop(i)
            return {"mensaje": "Préstamo eliminado"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado")