# FastAPI Catalog API

API de catálogos con FastAPI con generación automática de JSON.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

O con uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Características

- CRUD completo para Lines, Categories, Subcategories, Brands y Catalogs
- Generación automática de JSON en `/sync/catalogs.json` cada vez que se modifica la BD
- Endpoint manual de sincronización: `POST /sync/catalogs`
- CORS habilitado para frontend
- Base de datos SQLite

## Endpoints principales

- `/lines` - CRUD de líneas
- `/categories` - CRUD de categorías  
- `/subcategories` - CRUD de subcategorías
- `/brands` - CRUD de marcas
- `/catalogs` - CRUD de catálogos
- `/sync/catalogs` - Regenerar JSON manualmente
- `/sync/catalogs.json` - Descargar JSON generado

