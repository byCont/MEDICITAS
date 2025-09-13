import os
import json
from sqlalchemy.orm import Session
from sqlalchemy import text

# CORRECCIÓN: Se usa una importación relativa (.main) porque seeds.py está en el mismo paquete que main.py
from .main import (Base, User, Line, Category, Subcategory, Brand, Catalog,
                   engine, SessionLocal, pwd_context)

def run_initial_setup():
    """
    Función principal para recrear la BD y poblarla con datos iniciales.
    """
    db = SessionLocal()
    try:
        # 1. Recrear la base de datos
        print("🗑️  Eliminando y recreando todas las tablas...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos recreada exitosamente.")

        # 2. Crear usuarios iniciales
        print("\n👤 Creando usuarios administradores...")
        users_data = [
            {"email": "admin@example.com", "password": "adminpassword"},
            {"email": "user1@example.com", "password": "user1password"},
            {"email": "user2@example.com", "password": "user2password"},
        ]
        for user_data in users_data:
            if not db.query(User).filter(User.email == user_data["email"]).first():
                hashed_password = pwd_context.hash(user_data["password"])
                db_user = User(email=user_data["email"], password_hash=hashed_password)
                db.add(db_user)
        db.commit()
        print(f"✅ Creados {len(users_data)} usuarios.")

        # 3. Poblar desde el JSON autocontenido
        print("\n🌱 Poblando la base de datos con los datos de catálogos...")
        lines_data = [
    {
        "id": 4,
        "name": "ABRASIVOS",
        "categories": [
            {"id": 27, "name": "Abrasivos recubiertos"},
            {"id": 28, "name": "Discos abrasivos"},
            {"id": 30, "name": "Grados de alambre"},
            {"id": 29, "name": "Productos aglomerados"}
        ]
    },
    {
        "id": 11,
        "name": "CUBIERTOS",
        "categories": [
            {"id": 55, "name": "Cubiertos"}
        ]
    },
    {
        "id": 9,
        "name": "EMBELLECIMIENTO AUTOMOTRIZ",
        "categories": [
            {"id": 45, "name": "Accesorios"},
            {"id": 47, "name": "Cerámicas"},
            {"id": 44, "name": "Cremas"},
            {"id": 46, "name": "Revitalizadores"}
        ]
    },
    {
        "id": 12,
        "name": "ESTRUCTURA LIVIANA",
        "categories": [
            {"id": 57, "name": "Perfileria libiana"},
            {"id": 56, "name": "Placa"}
        ]
    },
    {
        "id": 10,
        "name": "HERRAJERÍA, CERRAJERÍA, TORNILLERÍA",
        "categories": [
            {"id": 54, "name": "Accesorios"},
            {"id": 52, "name": "Clavos y puntillas"},
            {"id": 51, "name": "Drywal"},
            {"id": 48, "name": "Grapas y clavillos"},
            {"id": 50, "name": "Herrrajes"},
            {"id": 49, "name": "Productos de seguridad"},
            {"id": 53, "name": "Remaches"}
        ]
    },
    {
        "id": 5,
        "name": "HERRAMIENTA ELÉCTRICA Y MANUAL",
        "categories": [
            {"id": 34, "name": "Accesorios"},
            {"id": 32, "name": "Herramienta de medición"},
            {"id": 33, "name": "Herramienta manual"},
            {"id": 31, "name": "Herrramienta eléctrica"},
            {"id": 35, "name": "Hidrolavadoras y aspiradoras"}
        ]
    },
    {
        "id": 1,
        "name": "MATERIAL DE EMPAQUE",
        "categories": [
            {
                "id": 6, "name": "Accesorios"
            },
            {
                "id": 1, "name": "Cintas",
                "subcategories": [
                    {"id": 3, "name": "elec"},
                    {
                        "id": 2, "name": "empaque"
                    },
                    {"id": 1, "name": "enmarcar"}
                ]
            },
            {"id": 5, "name": "Plásticos (identias y bolsas)", "subcategories": [{"id": 4, "name": "subca"}]},
            {"id": 2, "name": "Strech"},
            {"id": 4, "name": "Zurchos metálicos y grapadora metálica"},
            {"id": 3, "name": "Zurchos y grapadora"}
        ]
    },
    {
        "id": 13,
        "name": "PRODUCTOS KO",
        "categories": [
            {"id": 60, "name": "Cintas"},
            {"id": 58, "name": "Lavaplatos"},
            {"id": 59, "name": "Seguridad industrial"},
            {"id": 61, "name": "Valvulas PVC"}
        ]
    },
    {
        "id": 3,
        "name": "QUÍMICOS, PINTURA Y PROD. LIMPIEZA",
        "categories": [
            {"id": 25, "name": "Accesorios de pintura"},
            {"id": 23, "name": "Adhesivos y sellantes"},
            {"id": 24, "name": "Aerosoles"},
            {"id": 20, "name": "Aquitectónica"},
            {"id": 21, "name": "Automotriz"},
            {"id": 26, "name": "Impermeables"},
            {"id": 19, "name": "Lubricantes"},
            {"id": 22, "name": "Paños de limpieza"}
        ]
    },
    {
        "id": 2,
        "name": "SEGURIDAD INDUSTRIAL",
        "categories": [
            {"id": 18, "name": "Calzado"},
            {"id": 9, "name": "Dotacion"},
            {"id": 8, "name": "Ergonomia"},
            {"id": 12, "name": "Prototipo auditivo"},
            {"id": 13, "name": "Prototipo cabeza"},
            {"id": 16, "name": "Prototipo corporal"},
            {"id": 15, "name": "Prototipo facial"},
            {"id": 14, "name": "Prototipo manual"},
            {"id": 11, "name": "Prototipo respiratorio"},
            {"id": 10, "name": "Prototipo visual"},
            {
                "id": 7, "name": "Señalización-editada"
            },
            {"id": 17, "name": "Trabajo de altura"}
        ]
    },
    {
        "id": 6,
        "name": "TUBERÍA Y GRIFERÍA",
        "categories": [
            {"id": 36, "name": "HCC"},
            {"id": 37, "name": "HCC accesorios"}
        ]
    },
    {
        "id": 8,
        "name": "USO AGRÍCOLAS",
        "categories": [
            {"id": 41, "name": "Herramientas"},
            {"id": 42, "name": "Plastico"},
            {"id": 43, "name": "Polisombras y telas"}
        ]
    },
    {
        "id": 7,
        "name": "VARIOS",
        "categories": [
            {"id": 40, "name": "Cintas especiales"},
            {"id": 39, "name": "Izaje de carga"},
            {
                "id": 62, "name": "otros varios",
                "brands": [{"id": 1, "name": "VariousBrand"}]
            },
            {"id": 38, "name": "Ruedas y rodachines"}
        ],
        "brands": [{"id": 2, "name": "braVR"}]
    }
]

        for line_data in lines_data:
            db_line = Line(id=line_data['id'], name=line_data['name'])
            db.add(db_line)
            db.flush()
 
            if 'brands' in line_data:
                for brand_data in line_data['brands']:
                    db_brand = Brand(id=brand_data['id'], name=brand_data['name'], line_id=db_line.id)
                    db.add(db_brand)

            if 'categories' in line_data:
                for category_data in line_data['categories']:
                    db_category = Category(id=category_data['id'], name=category_data['name'], line_id=db_line.id)
                    db.add(db_category)
                    db.flush()

                    if 'brands' in category_data:
                        for brand_data in category_data['brands']:
                            db_brand = Brand(id=brand_data['id'], name=brand_data['name'], category_id=db_category.id)
                            db.add(db_brand)
                    
                    if 'subcategories' in category_data:
                        for sub_data in category_data['subcategories']:
                            db_sub = Subcategory(id=sub_data['id'], name=sub_data['name'], category_id=db_category.id)
                            db.add(db_sub)
                            db.flush()

                            if 'brands' in sub_data:
                                for brand_data in sub_data['brands']:
                                    db_brand = Brand(id=brand_data['id'], name=brand_data['name'], subcategory_id=db_sub.id)
                                    db.add(db_brand)

        db.commit()
        print("✅ Datos de catálogos poblados exitosamente.")

        # --- INICIO DE LA CORRECCIÓN ---
        # 4. Actualizar las secuencias de IDs en PostgreSQL
        if engine.dialect.name == "postgresql":
            print("\n🔄 Actualizando secuencias de IDs para PostgreSQL...")
            table_names = ["users", "lines", "categories", "subcategories", "brands", "catalogs"]
            for table in table_names:
                try:
                    # Este comando SQL reinicia el contador del ID al valor máximo actual en la tabla
                    sequence_name = f"{table}_id_seq"
                    db.execute(text(f"SELECT setval('{sequence_name}', (SELECT MAX(id) FROM {table}));"))
                    print(f"  - Secuencia para '{table}' actualizada.")
                except Exception as seq_e:
                    print(f"  - ⚠️  No se pudo actualizar la secuencia para '{table}': {seq_e}")
            db.commit()
            print("✅ Secuencias actualizadas.")
        # --- FIN DE LA CORRECCIÓN ---

    except Exception as e:
        print(f"❌ Ocurrió un error durante la configuración: {e}")
        db.rollback()
    finally:
        db.close()

