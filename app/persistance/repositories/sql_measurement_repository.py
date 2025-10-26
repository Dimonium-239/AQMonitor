import uuid
from typing import Optional, cast
from sqlalchemy.orm import Session

from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.database import MeasurementDB
from app.persistance.entity_mapper import to_domain, to_entity
from app.persistance.model.measurement_entity import MeasurementEntity
from app.persistance.repositories.measurement_repository import MeasurementRepository

class SQLMeasurementRepository(MeasurementRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[AirQualityMeasurement]:
        db_items = self.db.query(MeasurementDB).all()
        return [to_domain(i) for i in db_items]

    def get_by_id(self, measurement_id: str) -> Optional[MeasurementEntity]:
        db_item = self.db.query(MeasurementDB).filter(MeasurementDB.id == measurement_id).first()
        if db_item:
            return to_entity(db_item)
        return None

    def add(self, measurement: MeasurementEntity) -> MeasurementEntity:
        if not measurement.id:
            measurement.id = str(uuid.uuid4())

        db_item = MeasurementDB(
            id=measurement.id,
            city=measurement.city,
            parameter=measurement.parameter,
            value=measurement.value,
            unit=measurement.unit,
            timestamp=measurement.timestamp
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return to_entity(db_item)
