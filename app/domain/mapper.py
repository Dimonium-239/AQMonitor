from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.model.measurement_entity import MeasurementEntity


def to_air_quality(m: MeasurementEntity) -> AirQualityMeasurement:
    return AirQualityMeasurement(
        id=m.id or "",
        city=m.city,
        parameter=m.parameter,
        value=m.value,
        unit=m.unit,
        timestamp=m.timestamp,
    )
