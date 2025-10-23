from sqlalchemy.orm import Session

from app.persistance.config_loader import load_config
from app.persistance.database import SessionLocal
from app.persistance.repositories.in_memory_measurement_repository import InMemoryMeasurementRepository
from app.persistance.repositories.sql_measurement_repository import SQLMeasurementRepository

configs = load_config()

_in_memory_repo = InMemoryMeasurementRepository()  # persistent singleton in memory

def get_measurement_repository():
    if configs.db == "in_memory":
        return _in_memory_repo
    elif(configs.db == "mock"):
        db: Session = SessionLocal()
        try:
            yield SQLMeasurementRepository(db)
        finally:
            db.close()