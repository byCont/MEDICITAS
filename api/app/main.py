import os
import uvicorn
from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import Base, engine
from app.routers import login, usuarios, especialidades, doctores, citas
from app.middlewares import authenticate

# Crear las tablas en la base de datos (solo si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MediCitas API",
    description='"Especialistas para ti, cuando lo necesitas."'
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"))

# Middlewares
@app.middleware("http")
async def authenticate_middleware(request: Request, next: Callable):
    return await authenticate(request, next)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, se recomienda restringir esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(login.router, prefix="/api")
app.include_router(system.router, prefix="/api")
app.include_router(usuarios.router, prefix="/api")
app.include_router(especialidades.router, prefix="/api")
app.include_router(doctores.router, prefix="/api")
app.include_router(citas.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de MediCitas"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)