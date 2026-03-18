#importaciones
from fastapi import FastAPI, APIRouter
from app.routers import usuarios, varios





#instancias
app = FastAPI(
    title="Mi primer API",
    description="Jorge Armando Lopez Morales",
    version="1.0"
) #preparacion de la app


app.include_router(usuarios.router) #incluir el router de usuarios
app.include_router(varios.routerV) #incluir el router de varios








