#!/usr/bin/env python3
"""
Script para ejecutar las semillas de la base de datos MediCitas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.seeds import crear_semillas_completas

def main():
    """Función principal para ejecutar las semillas"""
    print("🌱 Iniciando creación de semillas para MediCitas...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Configuración de la base de datos
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("❌ Error: No se encontró la URL de la base de datos")
        sys.exit(1)
    
    try:
        # Crear conexión a la base de datos
        print("📡 Conectando a la base de datos...")
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Probar la conexión
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Conexión exitosa a la base de datos")
        
        # Ejecutar las semillas
        with SessionLocal() as db:
            crear_semillas_completas(db)
        
        print("🎉 ¡Semillas ejecutadas exitosamente!")
        print("\n📋 Datos de prueba disponibles:")
        print("   • Usuarios de prueba (pacientes, doctores, administradores)")
        print("   • Especialidades médicas")
        print("   • Citas de ejemplo")
        print("   • Reseñas y notificaciones")
        print("\n💡 Para probar la API, ejecuta:")
        print("   uvicorn app.main:app --reload")
        print("   Y ve a: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error al ejecutar las semillas: {str(e)}")
        print(f"📝 Detalles del error: {type(e).__name__}")
        sys.exit(1)

if __name__ == "__main__":
    main()