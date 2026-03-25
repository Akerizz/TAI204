from fastapi import APIRouter, status, HTTPException,Depends
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion
from typing import Optional

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB

router = APIRouter(
    prefix= "/v1/usuarios",tags=["Crud HTTP"]
)

@router.get("/{id}") 
async def leer_uasuarios(db: Session = Depends(get_db)):

    queryUsuario = db.query(UsuarioDB).all()
    return{
        "status":"200",
        "total": len(usuariosDB),
        "Usuarios":usuariosDB
    }

@router.post("/",status_code=status.HTTP_201_CREATED)  
async def crear_usuario(usuarioP:crear_usuario, db: Session = Depends(get_db)):
    uasuarionuevo = UsuarioDB(nombre = usuarioP.nombre, edad = usuarioP.edad)
    db.add(uasuarionuevo)
    db.commit()
    db.refresh(uasuarionuevo)

    return{
        "mensaje":"usuario agregado",
        "Usuario" :usuarioP,
        
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