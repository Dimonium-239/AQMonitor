from app.domain.model.config import load_config
from app.persistance.model.measurement_entity import SessionLocal
from app.persistance.repositories.sql_measurement_repository import SQLMeasurementRepository

configs = load_config()

def get_measurement_repository():
    if configs.repository_type == "postgres":
        db = SessionLocal()
        try:
            yield SQLMeasurementRepository(db)
        finally:
            db.close()
    else:
        yield None