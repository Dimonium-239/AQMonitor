from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.model.measurement_entity import MeasurementEntity


class MeasurementRepository(ABC):
    @abstractmethod
    def get_all(self, page: int = 1, page_size: int = 10) -> tuple[List[AirQualityMeasurement], int]:
        pass

    @abstractmethod
    def get_by_id(self, measurement_id: str) -> Optional[MeasurementEntity]:
        pass

    @abstractmethod
    def add(self, measurement: MeasurementEntity) -> MeasurementEntity:
        pass
