from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.database import MeasurementDB
from app.persistance.model.measurement_entity import MeasurementEntity


def to_entity(db_item: MeasurementDB) -> MeasurementEntity:
    return MeasurementEntity(
        id=db_item.id,
        city=db_item.city,
        parameter=db_item.parameter,
        value=db_item.value,
        unit=db_item.unit,
        timestamp=db_item.timestamp
    )

def to_domain(db_item: MeasurementDB) -> AirQualityMeasurement:
    return AirQualityMeasurement(
        id=db_item.id,
        city=db_item.city,
        parameter=db_item.parameter,
        value=db_item.value,
        unit=db_item.unit,
        timestamp=db_item.timestamp
    )
