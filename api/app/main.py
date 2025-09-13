#!/usr/bin/env python3
"""
API de Catálogos - Versión de Producción
Maneja la subida y servicio de archivos estáticos, con CRUD completo.
"""
import os
import logging
import json
import secrets
import shutil
from datetime import datetime
from typing import List, Optional

import jwt
from dotenv import load_dotenv
from fastapi import (FastAPI, Depends, HTTPException, status, Request,
                     BackgroundTasks, UploadFile, File, Form)
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import (create_engine, Column, Integer, String, Text,
                        DateTime, ForeignKey)
from sqlalchemy.orm import sessionmaker, Session, relationship, joinedload, declarative_base
from sqlalchemy.sql import func
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# --- Configuración Inicial ---
load_dotenv()

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_in_env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./catalog_prod.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuración del limitador de velocidad
limiter = Limiter(key_func=get_remote_address)

# Paths para archivos
JSON_OUTPUT_PATH = "sync/catalog.json"
STATIC_DIR = "static"
CATALOGS_DIR = os.path.join(STATIC_DIR, "catalogs")

# --- Modelos SQLAlchemy (Flexibles) ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Line(Base):
    __tablename__ = "lines"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    brands = relationship("Brand", back_populates="line", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="line", cascade="all, delete-orphan")
    catalogs = relationship("Catalog", back_populates="line", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    line_id = Column(Integer, ForeignKey("lines.id"), nullable=False)
    line = relationship("Line", back_populates="categories")
    subcategories = relationship("Subcategory", back_populates="category", cascade="all, delete-orphan")
    brands = relationship("Brand", back_populates="category", cascade="all, delete-orphan")
    catalogs = relationship("Catalog", back_populates="category", cascade="all, delete-orphan")

class Subcategory(Base):
    __tablename__ = "subcategories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="subcategories")
    brands = relationship("Brand", back_populates="subcategory", cascade="all, delete-orphan")
    catalogs = relationship("Catalog", back_populates="subcategory", cascade="all, delete-orphan")

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    line_id = Column(Integer, ForeignKey("lines.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=True)
    line = relationship("Line", back_populates="brands")
    category = relationship("Category", back_populates="brands")
    subcategory = relationship("Subcategory", back_populates="brands")
    catalogs = relationship("Catalog", back_populates="brand", cascade="all, delete-orphan")

class Catalog(Base):
    __tablename__ = "catalogs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    file_path = Column(String(255), nullable=True)
    line_id = Column(Integer, ForeignKey("lines.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    line = relationship("Line", back_populates="catalogs")
    category = relationship("Category", back_populates="catalogs")
    subcategory = relationship("Subcategory", back_populates="catalogs")
    brand = relationship("Brand", back_populates="catalogs")

# --- Modelos Pydantic (Schemas) ---

# Schemas para el JSON público
class CatalogPublic(BaseModel):
    id: int
    name: str
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    class Config: from_attributes = True

class BrandPublic(BaseModel):
    id: int
    name: str
    catalogs: List[CatalogPublic] = []
    class Config: from_attributes = True

class SubcategoryPublic(BaseModel):
    id: int
    name: str
    brands: List[BrandPublic] = []
    catalogs: List[CatalogPublic] = []
    class Config: from_attributes = True

class CategoryPublic(BaseModel):
    id: int
    name: str
    subcategories: List[SubcategoryPublic] = []
    brands: List[BrandPublic] = []
    catalogs: List[CatalogPublic] = []
    class Config: from_attributes = True

class LinePublic(BaseModel):
    id: int
    name: str
    categories: List[CategoryPublic] = []
    brands: List[BrandPublic] = []
    catalogs: List[CatalogPublic] = []
    class Config: from_attributes = True

# Schemas para Autenticación
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Schemas para CRUD (Entrada)
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    line_id: int

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class SubcategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int

class SubcategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class BrandCreate(BaseModel):
    name: str
    description: Optional[str] = None
    line_id: Optional[int] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None

class BrandUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CatalogUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Schemas para CRUD (Respuesta)
class CatalogResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    line_id: Optional[int] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    brand_id: Optional[int] = None
    class Config: from_attributes = True

class BrandResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    line_id: Optional[int] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    class Config: from_attributes = True
    
class SubcategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category_id: int
    class Config: from_attributes = True

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    line_id: int
    class Config: from_attributes = True

# --- Inicialización de FastAPI ---
app = FastAPI(
    title="API de Catálogos",
    description="Una API para gestionar un sistema de catálogos jerárquico, con CRUD completo.",
    version="3.1.0"
)

# Montar directorio estático
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount(f"/{STATIC_DIR}", StaticFiles(directory=STATIC_DIR), name="static")


# Middlewares
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependencias ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(HTTPBearer()), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- Lógica de Negocio ---
def generate_public_json(db: Session, request: Request):
    logger.info("Iniciando la generación del archivo catalog.json...")
    try:
        lines = db.query(Line).options(
            joinedload(Line.catalogs),
            joinedload(Line.brands).joinedload(Brand.catalogs),
            joinedload(Line.categories).joinedload(Category.catalogs),
            joinedload(Line.categories).joinedload(Category.brands).joinedload(Brand.catalogs),
            joinedload(Line.categories).joinedload(Category.subcategories).joinedload(Subcategory.catalogs),
            joinedload(Line.categories).joinedload(Category.subcategories).joinedload(Subcategory.brands).joinedload(Brand.catalogs)
        ).order_by(Line.id).all()
        
        validated_lines = [LinePublic.model_validate(line) for line in lines]
        
        def build_urls(item: dict):
            if "file_path" in item and item["file_path"]:
                item["file_url"] = str(request.base_url.replace(path=item["file_path"]))
            
            for key, value in item.items():
                if isinstance(value, list):
                    for sub_item in value:
                        if isinstance(sub_item, dict):
                            build_urls(sub_item)

        result_lines = [line.model_dump() for line in validated_lines]
        for line_dict in result_lines:
            build_urls(line_dict)

        os.makedirs(os.path.dirname(JSON_OUTPUT_PATH), exist_ok=True)
        
        with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump({"lines": result_lines}, f, indent=4, ensure_ascii=False)
        
        logger.info(f"✅ Archivo {JSON_OUTPUT_PATH} generado exitosamente.")
    except Exception as e:
        logger.error(f"❌ Error al generar el JSON público: {e}")

# --- Endpoints ---

# Endpoints Públicos
@app.get("/", tags=["General"])
@limiter.limit("10/minute")
def read_root(request: Request):
    return {"message": "Bienvenido a la API de Catálogos"}

@app.get("/health", tags=["General"])
@limiter.limit("10/minute")
def health_check(request: Request, db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error de base de datos: {e}")

@app.get("/catalog.json", tags=["General"])
@limiter.limit("20/minute")
def get_public_catalog(request: Request):
    if not os.path.exists(JSON_OUTPUT_PATH):
        db = SessionLocal()
        try:
            generate_public_json(db, request)
        finally:
            db.close()
        
        if not os.path.exists(JSON_OUTPUT_PATH):
             raise HTTPException(status_code=404, detail="El archivo de catálogo no pudo ser generado.")

    with open(JSON_OUTPUT_PATH, "r", encoding="utf-8") as f:
        content = json.load(f)
    return JSONResponse(content=content)

# Endpoints de Autenticación
@app.post("/auth/login", response_model=Token, tags=["Autenticación"])
@limiter.limit("5/minute")
def login_for_access_token(request: Request, form_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrecta",
        )
    access_token = jwt.encode(
        {"sub": user.email}, SECRET_KEY, algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- START: CRUD Endpoints Protegidos ---

# CRUD para Líneas (Solo lectura)
@app.get("/lines", response_model=List[LinePublic], tags=["Administración - Líneas"])
def get_lines(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Line).all()

@app.get("/lines/{line_id}", response_model=LinePublic, tags=["Administración - Líneas"])
def get_line(line_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_line = db.query(Line).filter(Line.id == line_id).first()
    if not db_line:
        raise HTTPException(status_code=404, detail="Línea no encontrada")
    return db_line

# CRUD para Categorías
@app.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, tags=["Administración - Categorías"])
def create_category(category: CategoryCreate, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    background_tasks.add_task(generate_public_json, db, request)
    return db_category

@app.get("/categories", response_model=List[CategoryResponse], tags=["Administración - Categorías"])
def get_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Category).all()

@app.get("/categories/{category_id}", response_model=CategoryResponse, tags=["Administración - Categorías"])
def get_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_category

@app.put("/categories/{category_id}", response_model=CategoryResponse, tags=["Administración - Categorías"])
def update_category(category_id: int, category_data: CategoryUpdate, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for key, value in category_data.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    background_tasks.add_task(generate_public_json, db, request)
    return db_category

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Administración - Categorías"])
def delete_category(category_id: int, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_category)
    db.commit()
    background_tasks.add_task(generate_public_json, db, request)
    return

# CRUD para Subcategorías
@app.post("/subcategories", response_model=SubcategoryResponse, status_code=status.HTTP_201_CREATED, tags=["Administración - Subcategorías"])
def create_subcategory(subcategory: SubcategoryCreate, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_subcategory = Subcategory(**subcategory.model_dump())
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    background_tasks.add_task(generate_public_json, db, request)
    return db_subcategory

@app.get("/subcategories", response_model=List[SubcategoryResponse], tags=["Administración - Subcategorías"])
def get_subcategories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Subcategory).all()

@app.get("/subcategories/{subcategory_id}", response_model=SubcategoryResponse, tags=["Administración - Subcategorías"])
def get_subcategory(subcategory_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if not db_subcategory:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    return db_subcategory

@app.put("/subcategories/{subcategory_id}", response_model=SubcategoryResponse, tags=["Administración - Subcategorías"])
def update_subcategory(subcategory_id: int, subcategory_data: SubcategoryUpdate, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if not db_subcategory:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    for key, value in subcategory_data.model_dump(exclude_unset=True).items():
        setattr(db_subcategory, key, value)
    db.commit()
    db.refresh(db_subcategory)
    background_tasks.add_task(generate_public_json, db, request)
    return db_subcategory

@app.delete("/subcategories/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Administración - Subcategorías"])
def delete_subcategory(subcategory_id: int, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if not db_subcategory:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    db.delete(db_subcategory)
    db.commit()
    background_tasks.add_task(generate_public_json, db, request)
    return

# CRUD para Marcas
@app.post("/brands", response_model=BrandResponse, status_code=status.HTTP_201_CREATED, tags=["Administración - Marcas"])
def create_brand(brand: BrandCreate, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not any([brand.line_id, brand.category_id, brand.subcategory_id]):
        raise HTTPException(status_code=400, detail="La marca debe estar asociada al menos a una línea, categoría o subcategoría.")
    db_brand = Brand(**brand.model_dump())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    background_tasks.add_task(generate_public_json, db, request)
    return db_brand

@app.get("/brands", response_model=List[BrandResponse], tags=["Administración - Marcas"])
def get_brands(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Brand).all()

@app.get("/brands/{brand_id}", response_model=BrandResponse, tags=["Administración - Marcas"])
def get_brand(brand_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return db_brand

@app.put("/brands/{brand_id}", response_model=BrandResponse, tags=["Administración - Marcas"])
def update_brand(brand_id: int, brand_data: BrandUpdate, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    for key, value in brand_data.model_dump(exclude_unset=True).items():
        setattr(db_brand, key, value)
    db.commit()
    db.refresh(db_brand)
    background_tasks.add_task(generate_public_json, db, request)
    return db_brand

@app.delete("/brands/{brand_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Administración - Marcas"])
def delete_brand(brand_id: int, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    db.delete(db_brand)
    db.commit()
    background_tasks.add_task(generate_public_json, db, request)
    return

# CRUD para Catálogos
@app.post("/upload/catalog", response_model=CatalogResponse, tags=["Administración - Catálogos"])
@limiter.limit("10/minute")
async def upload_catalog(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    line_id: Optional[int] = Form(None),
    category_id: Optional[int] = Form(None),
    subcategory_id: Optional[int] = Form(None),
    brand_id: Optional[int] = Form(None),
):
    if not any([line_id, category_id, subcategory_id, brand_id]):
        raise HTTPException(status_code=400, detail="Debe asociar el catálogo al menos a una línea, categoría, subcategoría o marca.")

    os.makedirs(CATALOGS_DIR, exist_ok=True)
    safe_filename = f"{secrets.token_hex(8)}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join(CATALOGS_DIR, safe_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    new_catalog = Catalog(
        name=name,
        description=description,
        file_path=file_path.replace("\\", "/"),
        line_id=line_id,
        category_id=category_id,
        subcategory_id=subcategory_id,
        brand_id=brand_id,
    )
    db.add(new_catalog)
    db.commit()
    db.refresh(new_catalog)
    
    background_tasks.add_task(generate_public_json, db, request)
    
    return new_catalog

@app.get("/catalogs", response_model=List[CatalogResponse], tags=["Administración - Catálogos"])
def get_catalogs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Catalog).all()

@app.get("/catalogs/{catalog_id}", response_model=CatalogResponse, tags=["Administración - Catálogos"])
def get_catalog(catalog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_catalog = db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if not db_catalog:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    return db_catalog

@app.put("/catalogs/{catalog_id}", response_model=CatalogResponse, tags=["Administración - Catálogos"])
def update_catalog(catalog_id: int, catalog_data: CatalogUpdate, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_catalog = db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if not db_catalog:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    for key, value in catalog_data.model_dump(exclude_unset=True).items():
        setattr(db_catalog, key, value)
    db.commit()
    db.refresh(db_catalog)
    background_tasks.add_task(generate_public_json, db, request)
    return db_catalog

@app.delete("/catalogs/{catalog_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Administración - Catálogos"])
def delete_catalog(catalog_id: int, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_catalog = db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if not db_catalog:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    
    file_path_to_delete = db_catalog.file_path
    
    db.delete(db_catalog)
    db.commit()

    if file_path_to_delete and os.path.exists(file_path_to_delete):
        try:
            os.remove(file_path_to_delete)
            logger.info(f"Archivo {file_path_to_delete} eliminado del servidor.")
        except OSError as e:
            logger.error(f"Error al eliminar el archivo {file_path_to_delete}: {e}")

    background_tasks.add_task(generate_public_json, db, request)
    return

@app.post("/sync/catalog", tags=["Administración - General"])
@limiter.limit("5/minute")
def sync_catalog_manually(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    background_tasks.add_task(generate_public_json, db, request)
    return {"message": "La sincronización del catálogo ha comenzado en segundo plano."}

# --- END: CRUD Endpoints Protegidos ---