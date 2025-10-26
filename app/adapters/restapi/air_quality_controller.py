from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List

from app.adapters.restapi.dependecies import get_measurement_repository
from app.domain.mapper import to_air_quality
from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.model.measurement_entity import MeasurementEntity
from app.persistance.repositories.measurement_repository import MeasurementRepository
from app.domain.openaq_service import OpenAQAirQualityService
from app.persistance.sensor_metadata_loader import load_sensor_metadata

router = APIRouter()

@router.get("/air/measurements", response_model=List[AirQualityMeasurement])
def get_air_quality(city: str = "Warsaw", repo=Depends(get_measurement_repository)) -> List[AirQualityMeasurement]:
    use_case = OpenAQAirQualityService(measurement_repo=repo)
    return use_case.get_latest_measurements(city)

@router.get("/air/measurements/persisted", response_model=List[AirQualityMeasurement])
def list_items(repo: MeasurementRepository = Depends(get_measurement_repository)):
    print("HERE controller")
    return  repo.get_all()

@router.post("/air/measurements", response_model=AirQualityMeasurement)
def add_manual_measurement(
    city: str = Query(..., example="Warsaw"),
    sensor_id: int = Query(..., example=36161),
    value: float = Query(..., example=18.4),
    repo: MeasurementRepository = Depends(get_measurement_repository),
):
    sensor_metadata = load_sensor_metadata()
    city_data = sensor_metadata.get(city)
    if not city_data:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found in metadata")
    sensor_info = city_data.get(sensor_id)
    if not sensor_info:
        raise HTTPException(status_code=404, detail=f"Sensor ID {sensor_id} not found for city '{city}'")

    parameter = sensor_info.get("parameter", "unknown")
    unit = sensor_info.get("unit", "unknown")

    measurement = MeasurementEntity(
        city=city,
        parameter=parameter,
        value=value,
        unit=unit,
        timestamp=datetime.utcnow(),
    )

    saved = repo.add(measurement)
    return to_air_quality(saved)