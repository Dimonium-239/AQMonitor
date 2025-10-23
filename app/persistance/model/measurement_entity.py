from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class MeasurementEntity(BaseModel):
    id: Optional[str] = None  # will be filled by repo
    city: str
    parameter: str
    value: float
    unit: str
    timestamp: datetime