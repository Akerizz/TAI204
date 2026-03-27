from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario
from app.models.usuarios import crear_usuario, actualizar_usuario


router = APIRouter(
    prefix="/v1/usuarios", tags=["Crud HTTP"]
)

@router.get("/") 
async def consulta_todos(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return {
        "status": "200",
        "total": len(usuarios),
        "Usuarios": usuarios
    }

@router.get("/{id}")
async def consulta_uno(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"status": "200", "Usuario": usuario}

@router.post("/")  
async def agregar_usuario(usuario: crear_usuario, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario.id).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="el id ya existe")
    
    nuevo_usuario = Usuario(id=usuario.id, nombre=usuario.nombre, edad=usuario.edad)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {
        "mensaje": "usuario agregado",
        "Usuario": nuevo_usuario,
        "status": "200"
    }
    
@router.put("/{id}")
async def actualizar_usuario_completo(id: int, usuario_actualizado: crear_usuario, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.id = usuario_actualizado.id
    usuario.nombre = usuario_actualizado.nombre
    usuario.edad = usuario_actualizado.edad
    
    db.commit()
    db.refresh(usuario)
    return {
        "mensaje": "Usuario actualizado correctamente",
        "usuario": usuario,
        "status": 200
    }

@router.patch("/{id}")
async def actualizar_usuario_parcial(id: int, usuario_actualizado: actualizar_usuario, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if usuario_actualizado.nombre is not None:
        usuario.nombre = usuario_actualizado.nombre
    if usuario_actualizado.edad is not None:
        usuario.edad = usuario_actualizado.edad
        
    db.commit()
    db.refresh(usuario)
    return {
        "mensaje": "Usuario actualizado parcialmente",
        "usuario": usuario,
        "status": 200
    }

@router.delete("/{id}")
async def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {
        "mensaje": "Usuario eliminado correctamente",
        "status": 200
    }