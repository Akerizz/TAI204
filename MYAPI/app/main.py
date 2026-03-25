#importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios
from app.data.db import engine
from app.data import usuario


usuario.base.metadata.create_all(bind=engine) #creacion de tablas en la base de datos


#instancias
app = FastAPI(
    title="Mi primer API",
    description="Jorge Armando Lopez Morales",
    version="1.0"
) #preparacion de la app


app.include_router(usuarios.router) #incluir el router de usuarios
app.include_router(varios.routerV) #incluir el router de varios








