from datetime import datetime
from pydantic import BaseModel

class AirQualityMeasurement(BaseModel):
    id: str
    city: str
    parameter: str
    value: float
    unit: str
    timestamp: datetime