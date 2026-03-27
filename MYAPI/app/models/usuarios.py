from pydantic import BaseModel, Field
from typing import Optional

class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="panchito Doe")
    edad: int = Field(..., gt=1, le=125, description="edad valida entre 1 y 125")

class actualizar_usuario(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50)
    edad: Optional[int] = Field(None, gt=1, le=125)
    edad:int = Field(...,gt=1, le=125, description="edad valida entre 1 y 125")