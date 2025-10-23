from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.persistance.config_loader import load_config
from app.adapters.restapi.air_quality_controller import router as air_router
from app.persistance.database import Base, engine

config = load_config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup logic ---
    if config.db != "in_memory":  # Only create tables if using real DB
        print("Checking/creating tables in database...")
        Base.metadata.create_all(bind=engine)  # Only creates tables if not exist
        print("✅ Tables ready")
    yield
    # --- Shutdown logic (optional) ---

# Pass lifespan to FastAPI
app = FastAPI(title="Hexagonal FastAPI Example", lifespan=lifespan)

# Include routes
app.include_router(air_router, prefix="/api", tags=["Air Quality"])

@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running"}