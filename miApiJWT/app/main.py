#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta


SECRET_KEY = "leprechaun"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="identificador de usuario")
    nombre:str= Field(...,min_length=3, max_length=50, example="Joohn Doe")
    edad:int=Field(...,gt=1,le=125,description="edad valida entre 1 y 125")

#instancias
app = FastAPI(
    title="Mi primer API JWT",
    description="Jorge Armando Lopez Morales",
    version="1.0"
) 

#TB ficticia
usuarios=[
    {"id":1, "nombre":"Jorge", "edad":21},
    {"id":2, "nombre":"Maria", "edad":28},
    {"id":3, "nombre":"Betito", "edad":30}
]

# b. Generación de Tokens (incluir limite max 30 minutos)
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login", tags=["Autenticación"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "Marron" or form_data.password != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# c. Implementar validación de tokens
async def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

#Endpoints
@app.get("/", tags=["Inicio"]) 
async def Bienvenidos():
    return {"mensaje": "Bienvenidos a FastAPI amor"}

@app.get("/HolaMundo", tags=["Asincronia"])
async def Hola():
    await asyncio.sleep(5) 
    return {
        "mensaje": "Hola Mundo FastAPI",
        "status": 200 
    }

@app.get("/v1/usuario/{id}", tags=["Parametro Oblogatorio"]) 
async def Consultauno(id:int):
    return {"mensaje": "Usuario encontrado",
            "usuario":id,
            "status": 200}

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

@app.post("/v1/usuarios/",tags=['Crud HTTP'])  
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

# d. Protección de endpoints (PUT y DELETE)
@app.put("/v1/usuario/", tags=["Crud HTTP"])
async def Actualizar_usuario(usuario_actualizado: dict, id: Optional[int] = None, current_user: str = Depends(verificar_token)):
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
async def Eliminar_usuario(id: int, current_user: str = Depends(verificar_token)):
    if id is None:
        raise HTTPException(status_code=400, detail="Proporciona una ID para eliminar")

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado correctamente por {current_user}",
                "status": 200
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

#activar entorno del uvicor:  cd MYAPI Y despues python -m uvicorn main:app --reload