#importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel,Field


class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="identificador de usuario")
    nombre:str= Field(...,min_length=3, max_length=50, example="Joohn Doe")
    edad:int=Field(...,gt=1,le=125,description="edad valida entre 1 y 125")

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
@app.get("/v1/ParametroOP/", tags=["Parametro Opcional"]) 
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
     


@app.get("/v1/Usuarios/", tags=["Crud HTTP"]) 
async def consultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "Usuarios":usuarios
    }

@app.post("/v1/usuarios/",tags=['CRUD HTTP'])  
async def agregar_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400, 
                  detail="el id ya existe"
            )
    usuarios.append(usuario.dict())
    return{
        "mensaje":"usuario agregado",
        "Usuario" :usuario,
        "status":"200"
    }
    

@app.put("/v1/usuario/", tags=["Crud HTTP"])
async def Actualizar_usuario(usuario_actualizado: dict, id: Optional[int] = None):
    if id is None:
        raise HTTPException(status_code=400, detail="Proporcionar un ID para actualizar")

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": "Usuario actualizado correctamente",
                "usuario": usuario_actualizado,
                "status": 200
            }
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")



@app.delete("/v1/usuario/", tags=["Crud HTTP"])
async def Eliminar_usuario(id: Optional[int] = None):
    if id is None:
        raise HTTPException(status_code=400, detail="Proporciona una ID para eliminar")

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": 200
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

#activar entorno del uvicor:  cd MYAPI Y despues python -m uvicorn main:app --reload