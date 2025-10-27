import uuid
from datetime import datetime
from select import select
from typing import Optional, cast, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.database import MeasurementDB
from app.persistance.entity_mapper import to_domain, to_entity
from app.persistance.model.measurement_entity import MeasurementEntity
from app.persistance.repositories.measurement_repository import MeasurementRepository

class SQLMeasurementRepository(MeasurementRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(
            self,
            page: int = 1,
            page_size: int = 10,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            parameters: Optional[List[str]] = None,
            paginated: bool = True
    ):
        query = self.db.query(MeasurementDB)

        # Apply date filter
        if start_date and end_date:
            query = query.filter(
                MeasurementDB.timestamp.between(start_date, end_date)
            )

        # Apply parameter filter
        if parameters and len(parameters) > 0:
            query = query.filter(MeasurementDB.parameter.in_(parameters))

        # Total count before pagination
        total = query.count()

        # Apply pagination
        if paginated:
            query = query.offset((page - 1) * page_size).limit(page_size)

        db_items = query.all()
        return [to_domain(i) for i in db_items], total


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
