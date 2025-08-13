from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import combos, usuarios

# Crea tablas si no existen (no migra cambios)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Combos")

# CORS (ajusta a tu frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Healthcheck
@app.get("/health")
def health():
    return {"api": "funcionando"}

# Rutas
app.include_router(usuarios.router)
app.include_router(combos.router)
