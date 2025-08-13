from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/combos", tags=["Combos"])

@router.get("/", response_model=list[schemas.Combo])
def listar_combos(db: Session = Depends(get_db)):
    return db.query(models.Combo).filter(models.Combo.activo == True).all()

@router.post("/", response_model=schemas.Combo)
def crear_combo(combo: schemas.ComboCreate, db: Session = Depends(get_db)):
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.id == combo.creado_por, models.Usuario.activo == True)
        .first()
    )
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario creador no encontrado o inactivo")

    nuevo_combo = models.Combo(**combo.dict())
    db.add(nuevo_combo)
    db.commit()
    db.refresh(nuevo_combo)
    return nuevo_combo
