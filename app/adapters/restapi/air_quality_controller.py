from datetime import datetime

from typing import Optional

from app.adapters.restapi.dependecies import get_measurement_repository
from app.domain.mapper import to_air_quality
from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.model.measurement_entity import MeasurementEntity
from app.persistance.repositories.measurement_repository import MeasurementRepository
from app.domain.openaq_service import OpenAQAirQualityService
from app.persistance.sensor_metadata_loader import load_sensor_metadata

from fastapi import APIRouter, Depends, Response, status, Query
from typing import List

router = APIRouter()

@router.get("/air/measurements", response_model=List[AirQualityMeasurement])
def get_air_quality(
    city: str = "Warsaw",
    repo=Depends(get_measurement_repository)
):
    use_case = OpenAQAirQualityService(measurement_repo=repo)
    new_measurements = use_case.get_latest_measurements(city)
    if not new_measurements:
        # ✅ Return an *empty* 204 response properly
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return new_measurements


@router.get("/air/measurements/chart-data", response_model=List[AirQualityMeasurement])
def get_chart_data(
    start_date: Optional[datetime] = Query(None, description="Filter start date (ISO)"),
    end_date: Optional[datetime] = Query(None, description="Filter end date (ISO)"),
    parameter: Optional[List[str]] = Query([], description="Filter by parameter. Use multiple times: ?parameter=pm25&parameter=no2"),
    sort_by: Optional[List[str]] = Query(
        ["timestamp:asc"],
        description="Sorting fields, e.g. ?sort_by=timestamp:asc&sort_by=city:desc",
    ),
    repo: MeasurementRepository = Depends(get_measurement_repository),
):
    items = repo.get_chart_data(
        start_date=start_date,
        end_date=end_date,
        parameters=parameter,
        sort_by=sort_by,
    )
    return items

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