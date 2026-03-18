from fastapi import APIRouter, FastAPI, status, HTTPException,Depends
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion
from typing import Optional


router = APIRouter(
    prefix= "/v1/usuarios",tags=["Crud HTTP"]
)

@router.get("/{id}") 
async def consultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "Usuarios":usuarios
    }

@router.post("/")  
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
    

@router.put("/")
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



@router.delete("/")
async def Eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    if id is None:
        raise HTTPException(status_code=400, detail="Proporciona una ID para eliminar")

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado correctamente {usuarioAuth}",
                "status": 200
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

#activar entorno del uvicor:  cd MYAPI Y despues python -m uvicorn main:app --reload