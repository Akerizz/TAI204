from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#Definir URL de la conecxion

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost:5432/mydatabase"
    )

#2 creamos motor de conexion
engine = create_engine(DATABASE_URL)

#3 creamos gestion de sesiones
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

#4 Base declarativa para modelo
base = declarative_base()

#5 funcion que trabaja sesiones con las peticiones
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    