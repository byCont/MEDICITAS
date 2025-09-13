#!/usr/bin/env python3
"""
Script para ejecutar las semillas de la base de datos de Catálogos.
"""
# Se importa la función principal desde el módulo correcto: app.seeds
from app.seeds import run_initial_setup

if __name__ == "__main__":
    print("🚀 Iniciando el proceso de configuración inicial de la base de datos...")
    run_initial_setup()
    print("\n✅ Proceso finalizado. Ya puedes iniciar la API con 'uvicorn main:app --reload'")

