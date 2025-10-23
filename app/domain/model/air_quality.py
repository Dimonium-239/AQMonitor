from dataclasses import dataclass
from datetime import datetime

@dataclass
class AirQualityMeasurement:
    id: str
    city: str
    parameter: str
    value: float
    unit: str
    timestamp: datetime