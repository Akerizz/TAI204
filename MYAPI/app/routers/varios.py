import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

routerV= APIRouter(tags=["Inicio"])


#Endpoints
@routerV.get("/", tags=["Inicio"]) 
async def Bienvenidos():
    return {"mensaje": "Bienvenidos a FastAPI amor"}

@routerV.get("/HolaMundo", tags=["Asincronia"])
async def Hola():
    await asyncio.sleep(5) #peticion,consultaDB,Archivos
    return {
        "mensaje": "Hola Mundo FastAPI",
        "status": 200 #
    }

@routerV.get("/v1/usuario/{id}", tags=["Parametro Oblogatorio"]) 
async def Consultauno(id:int):
    return {"mensaje": "Usuario encontrado",
            "usuario":id,
            "status": 200}

#debe de tenero otro nombre porque el anrerior tambuen era get y no nececita las llaves porque es opcional
@routerV.get("/v1/ParametroOP/", tags=["Parametro Opcional"]) 
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