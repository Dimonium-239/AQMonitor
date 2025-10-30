import uuid
from abc import ABC
from datetime import datetime
from select import select
from typing import Optional, cast, List

from sqlalchemy import func, asc, desc
from sqlalchemy.orm import Session

from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.database import MeasurementDB
from app.persistance.entity_mapper import to_domain, to_entity
from app.persistance.model.measurement_entity import MeasurementEntity
from app.persistance.repositories.measurement_repository import MeasurementRepository

class SQLMeasurementRepository(MeasurementRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_chart_data(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        parameters: Optional[List[str]] = None,
        sort_by: Optional[List[str]] = None,
    ):
        query = self.db.query(MeasurementDB)

        if start_date and end_date:
            query = query.filter(MeasurementDB.timestamp.between(start_date, end_date))
        elif start_date:
            query = query.filter(MeasurementDB.timestamp >= start_date)
        elif end_date:
            query = query.filter(MeasurementDB.timestamp <= end_date)

        # Apply parameter filter
        if parameters:
            query = query.filter(MeasurementDB.parameter.in_(parameters))

        # Sorting logic
        if sort_by:
            sort_columns = []
            for sort_item in sort_by:
                try:
                    field, direction = sort_item.split(":")
                    column = getattr(MeasurementDB, field, None)
                    if column is not None:
                        sort_columns.append(asc(column) if direction.lower() == "asc" else desc(column))
                except ValueError:
                    # Skip invalid format
                    continue

            if sort_columns:
                query = query.order_by(*sort_columns)
        else:
            query = query.order_by(MeasurementDB.timestamp.asc())

        db_items = query.all()
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

    def measurement_exists(self, city: str, parameter: str, timestamp: datetime) -> bool:
        exists = (
            self.db.query(MeasurementDB)
            .filter(
                MeasurementDB.city == city,
                MeasurementDB.parameter == parameter,
                MeasurementDB.timestamp == timestamp
            )
            .first()
        )
        return exists is not None
