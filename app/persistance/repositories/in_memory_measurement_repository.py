import uuid
from typing import List, Optional

from app.domain.mapper import to_air_quality
from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.model.measurement_entity import MeasurementEntity
from app.persistance.repositories.measurement_repository import MeasurementRepository


class InMemoryMeasurementRepository(MeasurementRepository):
    def __init__(self):
        self.measurement = {}

    def get_all(self) -> list[AirQualityMeasurement]:
        return [to_air_quality(m) for m in self.measurement.values()]

    def get_by_id(self, item_id: str) -> Optional[MeasurementEntity]:
        return self.measurement.get(item_id)

    def add(self, measurement: MeasurementEntity) -> MeasurementEntity:
        if not measurement.id:
            measurement.id = str(uuid.uuid4())
        self.measurement[measurement.id] = measurement
        return measurement
