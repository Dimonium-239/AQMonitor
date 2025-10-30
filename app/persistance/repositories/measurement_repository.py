from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.model.measurement_entity import MeasurementEntity


class MeasurementRepository(ABC):
    @abstractmethod
    def get_chart_data(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        parameters: Optional[List[str]] = None,
        sort_by: Optional[List[str]] = None,
    ) -> tuple[List["AirQualityMeasurement"], int]:
        pass


    @abstractmethod
    def get_by_id(self, measurement_id: str) -> Optional[MeasurementEntity]:
        pass

    @abstractmethod
    def add(self, measurement: MeasurementEntity) -> MeasurementEntity:
        pass

    @abstractmethod
    def measurement_exists(self, city: str, parameter: str, timestamp: datetime) -> bool:
        pass
