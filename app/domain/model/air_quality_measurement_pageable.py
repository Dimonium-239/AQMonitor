from typing import List

from pydantic import BaseModel

from app.domain.model.air_quality import AirQualityMeasurement


class AirQualityMeasurementPageable(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[AirQualityMeasurement]