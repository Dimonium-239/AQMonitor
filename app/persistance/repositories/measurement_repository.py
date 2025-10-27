from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.model.measurement_entity import MeasurementEntity


class MeasurementRepository(ABC):
    @abstractmethod
    def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        parameters: Optional[List[str]] = None,
        paginated: bool = True
    ) -> tuple[List["AirQualityMeasurement"], int]:
        """
        Fetch measurements from storage.

        Args:
            page: Page number (ignored if paginated=False).
            page_size: Number of results per page (ignored if paginated=False).
            start_date: Filter lower bound for timestamp.
            end_date: Filter upper bound for timestamp.
            parameters: Optional list of parameter names to include.
            paginated: Whether to apply pagination or return all filtered results.

        Returns:
            A tuple of (measurements, total_count)
        """
        pass


    @abstractmethod
    def get_by_id(self, measurement_id: str) -> Optional[MeasurementEntity]:
        pass

    @abstractmethod
    def add(self, measurement: MeasurementEntity) -> MeasurementEntity:
        pass
