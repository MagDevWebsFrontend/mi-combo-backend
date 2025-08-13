import os

# Carpetas base
folders = [
    "app",
    "app/routers",
    "app/core",
    "scripts"
]

# Archivos y su contenido inicial
files_content = {
    "requirements.txt": """fastapi
uvicorn[standard]
SQLAlchemy
psycopg2-binary
python-dotenv
passlib[bcrypt]
python-jose[cryptography]
pydantic
""",
    ".env.example": """DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/combos_db
JWT_SECRET=CAMBIA_ESTE_SECRETO_LARGO
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
CORS_ORIGINS=http://localhost:3000
""",
    "app/__init__.py": "",
    "app/main.py": """from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import combos

# Crear tablas en la BD
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Rutas
app.include_router(combos.router)

@app.get("/")
def root():
    return {"message": "API de Combos funcionando"}
""",
    "app/database.py": """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
    "app/models.py": """from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255))
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"))
    categoria = relationship("Categoria", back_populates="productos")
    items_combo = relationship("ItemCombo", back_populates="producto")

class Combo(Base):
    __tablename__ = "combos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    precio_total = Column(Float, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    items = relationship("ItemCombo", back_populates="combo")

class ItemCombo(Base):
    __tablename__ = "items_combo"
    id = Column(Integer, primary_key=True, index=True)
    combo_id = Column(Integer, ForeignKey("combos.id", ondelete="CASCADE"))
    producto_id = Column(Integer, ForeignKey("productos.id", ondelete="CASCADE"))
    cantidad = Column(Integer, nullable=False)
    combo = relationship("Combo", back_populates="items")
    producto = relationship("Producto", back_populates="items_combo")
""",
    "app/schemas.py": """from pydantic import BaseModel
from typing import List, Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int

class ProductoCreate(ProductoBase):
    categoria_id: Optional[int] = None

class Producto(ProductoBase):
    id: int
    class Config:
        orm_mode = True

class ComboBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_total: float

class ComboCreate(ComboBase):
    pass

class Combo(ComboBase):
    id: int
    class Config:
        orm_mode = True
""",
    "app/routers/__init__.py": "",
    "app/routers/combos.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from typing import List

router = APIRouter(prefix="/combos", tags=["Combos"])

@router.get("/", response_model=List[schemas.Combo])
def listar_combos(db: Session = Depends(get_db)):
    return db.query(models.Combo).all()

@router.post("/", response_model=schemas.Combo)
def crear_combo(combo: schemas.ComboCreate, db: Session = Depends(get_db)):
    nuevo_combo = models.Combo(**combo.dict())
    db.add(nuevo_combo)
    db.commit()
    db.refresh(nuevo_combo)
    return nuevo_combo
""",
    "scripts/__init__.py": ""
}

# Crear carpetas
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Crear archivos con contenido
for path, content in files_content.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Proyecto FastAPI creado con estructura y código base listo.")
