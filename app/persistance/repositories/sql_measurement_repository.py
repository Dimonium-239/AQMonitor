import uuid
from typing import List, Optional, cast
from sqlalchemy.orm import Session

from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.database import MeasurementDB
from app.persistance.model.measurement_entity import MeasurementEntity
from app.persistance.repositories.measurement_repository import MeasurementRepository


def _to_entity(db_item: MeasurementDB) -> MeasurementEntity:
    return MeasurementEntity(
        id=db_item.id,
        city=db_item.city,
        parameter=db_item.parameter,
        value=db_item.value,
        unit=db_item.unit,
        timestamp=db_item.timestamp
    )

def _to_domain(db_item: MeasurementDB) -> AirQualityMeasurement:
    return AirQualityMeasurement(
        id=db_item.id,
        city=db_item.city,
        parameter=db_item.parameter,
        value=db_item.value,
        unit=db_item.unit,
        timestamp=db_item.timestamp
    )

class SQLMeasurementRepository(MeasurementRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[AirQualityMeasurement]:
        db_items = self.db.query(MeasurementDB).all()
        return [_to_domain(i) for i in db_items]

    def get_by_id(self, measurement_id: str) -> Optional[MeasurementEntity]:
        db_item = self.db.query(MeasurementDB).filter(MeasurementDB.id == measurement_id).first()
        if db_item:
            return _to_entity(db_item)
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
        return _to_entity(db_item)
