# app/main.py
# aplicacion principal
#!/usr/bin/env python3
"""
Sistema de Autenticación para MediCitas API
Aplicación principal
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .config import settings
from .database import engine, Base
from .routers import auth, users, doctors, appointments, public

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Incluir routers (orden importante: públicos primero)
app.include_router(public.router)
app.include_router(doctors.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(appointments.router)

# Middleware de manejo de errores
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)