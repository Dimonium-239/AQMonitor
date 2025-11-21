import uuid
from datetime import datetime, time, timezone
from typing import Optional, List

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.domain.mapper import to_air_quality, to_entity
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
        query = self.db.query(MeasurementEntity)

        if start_date:
            start_date = datetime.combine(start_date.date(), time.min)

        if end_date:
            end_date = datetime.combine(end_date.date(), time.max)

        if start_date and end_date:
            query = query.filter(MeasurementEntity.timestamp.between(start_date, end_date))
        elif start_date:
            query = query.filter(MeasurementEntity.timestamp >= start_date)
        elif end_date:
            query = query.filter(MeasurementEntity.timestamp <= end_date)

        if parameters:
            query = query.filter(MeasurementEntity.parameter.in_(parameters))

        if sort_by:
            sort_columns = []
            for sort_item in sort_by:
                try:
                    field, direction = sort_item.split(":")
                    column = getattr(MeasurementEntity, field, None)
                    if column is not None:
                        sort_columns.append(asc(column) if direction.lower() == "asc" else desc(column))
                except ValueError:
                    continue

            if sort_columns:
                query = query.order_by(*sort_columns)
        else:
            query = query.order_by(MeasurementEntity.timestamp.asc())

        db_items = query.all()
        return [to_air_quality(i) for i in db_items]


    def get_by_id(self, measurement_id: str) -> Optional[MeasurementEntity]:
        db_item = self.db.query(MeasurementEntity).filter(MeasurementEntity.id == measurement_id).first()
        if db_item:
            return to_entity(db_item)
        return None

    def add(self, measurement: MeasurementEntity) -> MeasurementEntity:
        if not measurement.id:
            measurement.id = str(uuid.uuid4())
        ts = measurement.timestamp
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)

        if ts.tzinfo is None:
            ts = ts.astimezone(timezone.utc)
        else:
            ts = ts.astimezone(timezone.utc)

        db_item = MeasurementEntity(
            id=measurement.id,
            city=measurement.city,
            parameter=measurement.parameter,
            value=measurement.value,
            unit=measurement.unit,
            timestamp=ts,  # always UTC now
        )

        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return to_entity(db_item)

    def measurement_exists(self, city: str, parameter: str, timestamp: datetime) -> bool:
        exists = (
            self.db.query(MeasurementEntity)
            .filter(
                MeasurementEntity.city == city,
                MeasurementEntity.parameter == parameter,
                MeasurementEntity.timestamp == timestamp
            )
            .first()
        )
        return exists is not None

    def update(self, measurement_id: str, updated_data: MeasurementEntity) -> Optional[MeasurementEntity]:
        db_item = self.db.query(MeasurementEntity).filter(
            MeasurementEntity.id == measurement_id
        ).first()

        if not db_item:
            return None

        # Update fields
        db_item.city = updated_data.city
        db_item.parameter = updated_data.parameter
        db_item.value = updated_data.value
        db_item.unit = updated_data.unit
        db_item.timestamp = updated_data.timestamp

        self.db.commit()
        self.db.refresh(db_item)
        return to_entity(db_item)

    def delete(self, measurement_id: str) -> bool:
        db_item = self.db.query(MeasurementEntity).filter(
            MeasurementEntity.id == measurement_id
        ).first()

        if not db_item:
            return False

        self.db.delete(db_item)
        self.db.commit()
        return True
