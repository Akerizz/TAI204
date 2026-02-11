#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional


#instancias
app = FastAPI(
    title="Mi primer API",
    description="Jorge Armando Lopez Morales",
    version="1.0"
) #preparacion de la app


#TB ficticia
usuarios=[
    {"id":1, "nombre":"Jorge", "edad":21},
    {"id":2, "nombre":"Maria", "edad":28},
    {"id":3, "nombre":"Betito", "edad":30}
   
]
#Endpoints
@app.get("/", tags=["Inicio"]) 
async def Bienvenidos():
    return {"mensaje": "Bienvenidos a FastAPI amor"}

@app.get("/HolaMundo", tags=["Asincronia"])
async def Hola():
    await asyncio.sleep(5) #peticion,consultaDB,Archivos
    return {
        "mensaje": "Hola Mundo FastAPI",
        "status": 200 #
    }

@app.get("/v1/usuario/{id}", tags=["Parametro Oblogatorio"]) 
async def Consultauno(id:int):
    return {"mensaje": "Usuario encontrado",
            "usuario":id,
            "status": 200}

#debe de tenero otro nombre porque el anrerior tambuen era get y no nececita las llaves porque es opcional
@app.get("/v1/usuarios/", tags=["Parametro Opcional"]) 
async def Consultatodos(id:Optional[int]=None):
    if id is not None:
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return{"mensaje": "Usuario encontrado",
                        "usuario": usuariok,
                        "status": 200}
        return{"mensaje": "Usuario no encontrado",
                "status": 200}   
    return{"mensaje":"no se proporciono id",
            "status": 200}
     


#activar entorno del uvicor:  cd MYAPI Y despues python -m uvicorn main:app --reload