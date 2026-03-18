from pydantic import BaseModel, Field

class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="identificador de usuario")
    nombre:str= Field(...,min_length=3, max_length=50, example="Joohn Doe")
    edad:int=Field(...,gt=1,le=125,description="edad valida entre 1 y 125")