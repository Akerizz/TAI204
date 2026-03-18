from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta

app = FastAPI(
    title="API Sistema de Turnos Bancarios Digital",
    description="Sistema para gestión de turnos en banco",
    version="1.0"
)

turnos_db = []
consultar_db = []

SECRET_KEY = "leprechaun"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class CrearUsuario(BaseModel):
    id: int = Field(..., gt=0, description="identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="John Doe")
    edad: int = Field(..., gt=1, le=125, description="edad valida entre 1 y 125")

# GENERACIÓN DE TOKEN
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# LOGIN
@app.post("/login", tags=["Autenticación"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "banco" or form_data.password != "2468":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# VALIDAR TOKEN
async def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return username

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# MODELOS
class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2)
    correo: EmailStr

class Turno(BaseModel):
    id: int
    nombre: str = Field(..., min_length=2, max_length=100)
    tipo_servicio: str
    estado: str = Field(default="disponible")

class ConsultaTurno(BaseModel):
    id_consulta: int
    id_turno: int
    usuario: Usuario

# CREAR TURNO
@app.post("/v1/crear_turno/", status_code=status.HTTP_201_CREATED)
def registrar_turno(turno: Turno):
    turnos_db.append(turno.model_dump())
    return {"mensaje": "Turno registrado"}

# LISTAR TURNOS DISPONIBLES
@app.get("/v1/turnos/disponibles")
def listar_turnos_disponibles():
    return [t for t in turnos_db if t["estado"] == "disponible"]

# BUSCAR TURNO
@app.get("/v1/turnos/buscar")
def consultar_turno(nombre: str):
    return [t for t in turnos_db if nombre.lower() in t["nombre"].lower()]

# REGISTRAR CONSULTA DE TURNO
@app.post("/v1/consultar_turnos/")
def registrar_consulta(turno: ConsultaTurno):

    for t in turnos_db:
        if t["id"] == turno.id_turno:

            if t["estado"] == "atendido":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El turno ya fue atendido"
                )

            t["estado"] = "atendido"
            consultar_db.append(turno.model_dump())

            return {"mensaje": "Turno atendido"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turno no encontrado")

# MARCAR TURNO COMO ATENDIDO
@app.put("/v1/marcar_atendido/{id_turno}", status_code=status.HTTP_200_OK)
def marcar_como_atendido(id_turno: int):

    for turno in turnos_db:

        if turno["id"] == id_turno:
            turno["estado"] = "atendido"
            return {"mensaje": "Turno marcado como atendido"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turno no encontrado")

# ELIMINAR TURNO
@app.delete("/v1/turno/{id_turno}")
def eliminar_turno(id_turno: int, current_user: str = Depends(verificar_token)):

    for index, turno in enumerate(turnos_db):

        if turno["id"] == id_turno:

            turnos_db.pop(index)

            return {
                "mensaje": f"Turno eliminado correctamente por {current_user}",
                "status": 200
            }

    raise HTTPException(status_code=404, detail="Turno no encontrado")