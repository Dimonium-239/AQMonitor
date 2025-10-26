from app.domain.model.config import load_config
from app.persistance.repositories.in_memory_measurement_repository import InMemoryMeasurementRepository
from app.persistance.repositories.sql_measurement_repository import SQLMeasurementRepository
from app.persistance.database import SessionLocal

configs = load_config()
_in_memory_repo = InMemoryMeasurementRepository()

def get_measurement_repository():
    if configs.repository_type == "mock":
        try:
            yield _in_memory_repo
        finally:
            return _in_memory_repo
    elif configs.repository_type == "postgres":
        db = SessionLocal()
        try:
            yield SQLMeasurementRepository(db)
        finally:
            db.close()
            return db
    yield None
    return None