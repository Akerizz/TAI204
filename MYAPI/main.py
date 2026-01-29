#importaciones
from fastapi import FastAPI
import asyncio

#instancias
app = FastAPI() #preparacion de la app

#Endpoints
@app.get("/") 
async def Bienvenidos():
    return {"mensaje": "Bienvenidos a mi API con FastAPI"}

@app.get("/HolaMundo")
async def Hola():
    await asyncio.sleep(1) 
    return {
        "mensaje": "Hola Mundo FastAPI",
        "status": 200 #
    }
