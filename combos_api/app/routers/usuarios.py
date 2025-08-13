from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar nombre único
    existente = db.query(models.Usuario).filter(models.Usuario.nombre_usuario == usuario.nombre_usuario).first()
    if existente:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    # Hash de contraseña
    hashed = pwd_context.hash(usuario.contraseña)

    nuevo_usuario = models.Usuario(
        nombre_usuario=usuario.nombre_usuario,
        contraseña=hashed,
        rol=usuario.rol,
        activo=usuario.activo if usuario.activo is not None else True,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/", response_model=list[schemas.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()
