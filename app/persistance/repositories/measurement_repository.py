from abc import ABC, abstractmethod
from typing import List, Optional

from app.persistance.model.measurement_entity import MeasurementEntity


class MeasurementRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[MeasurementEntity]:
        pass

    @abstractmethod
    def get_by_id(self, measurement_id: str) -> Optional[MeasurementEntity]:
        pass

    @abstractmethod
    def add(self, measurement: MeasurementEntity) -> MeasurementEntity:
        pass
