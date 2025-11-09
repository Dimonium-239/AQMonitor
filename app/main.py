from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.adapters.restapi.air_quality_controller import router as air_router
from app.domain.model.config import load_config
from app.persistance.model.measurement_entity import init_db

config = load_config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if config.repository_type != "mock":
        print("Checking/creating tables in database...")
        init_db()
        print("Tables ready")
    yield

app = FastAPI(title="Hexagonal FastAPI Example", lifespan=lifespan)
app.include_router(air_router, prefix="/api", tags=["Air Quality"])

from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:5173",
           "https://aq-monitor-fe.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running"}