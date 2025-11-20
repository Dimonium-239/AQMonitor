from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from datetime import datetime

from app.adapters.restapi.dependecies import get_measurement_repository
from app.domain.mapper import to_air_quality
from app.domain.model.air_quality import AirQualityMeasurement
from app.domain.openaq_service import OpenAQAirQualityService
from app.persistance.model.measurement_entity import MeasurementEntity
from app.persistance.repositories.measurement_repository import MeasurementRepository
from app.persistance.sensor_metadata_loader import load_sensor_metadata

router = APIRouter()

def assert_city_supported(city: str):
    if city.lower() != "warsaw":
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"City '{city}' is not implemented. Only Warsaw is supported."
        )


@router.get(
    "/air/measurements",
    response_model=List[AirQualityMeasurement],
    summary="Fetch latest air quality measurements from OpenAQ or cache",
    responses={
        200: {"description": "List of latest measurements"},
        204: {"description": "No measurements found for the given city"},
        400: {"description": "Invalid city parameter"},
        500: {"description": "Internal server error"},
        501: {"description": "City not implemented"},
    },
)
def get_air_quality(
    city: str = Query("Warsaw", description="City name, e.g. Warsaw"),
    repo: MeasurementRepository = Depends(get_measurement_repository),
):
    assert_city_supported(city)

    try:
        service = OpenAQAirQualityService(measurement_repo=repo)
        new_measurements = service.get_latest_measurements(city)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not new_measurements:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return new_measurements


@router.get(
    "/air/measurements/chart-data",
    response_model=List[AirQualityMeasurement],
    summary="Retrieve measurement data filtered for chart rendering",
    responses={
        200: {"description": "Filtered measurement list"},
        400: {"description": "Invalid filter parameters"},
        500: {"description": "Internal server error"},
        501: {"description": "City not implemented"},
    },
)
def get_chart_data(
    city: str = Query("Warsaw", description="City name, e.g. Warsaw"),
    start_date: Optional[datetime] = Query(None, description="Filter start date (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Filter end date (ISO format)"),
    parameter: Optional[List[str]] = Query(
        [], description="Filter by parameter. Repeat parameter for multiple values, e.g. ?parameter=pm25&parameter=no2"
    ),
    sort_by: Optional[List[str]] = Query(
        ["timestamp:asc"],
        description="Sorting directives, e.g. ?sort_by=timestamp:asc&sort_by=city:desc",
    ),
    repo: MeasurementRepository = Depends(get_measurement_repository),
):
    assert_city_supported(city)

    try:
        items = repo.get_chart_data(
            start_date=start_date,
            end_date=end_date,
            parameters=parameter,
            sort_by=sort_by,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return items


@router.post(
    "/air/measurements",
    response_model=AirQualityMeasurement,
    summary="Manually insert a new measurement",
    responses={
        201: {"description": "Measurement created"},
        400: {"description": "Invalid input"},
        404: {"description": "City or sensor not found"},
        500: {"description": "Internal server error"},
        501: {"description": "City not implemented"},
    },
    status_code=201,
)
def add_manual_measurement(
    city: str = Query(..., example="Warsaw", description="City name"),
    sensor_id: int = Query(..., example=36161, description="Sensor identifier"),
    value: float = Query(..., example=18.4, description="Measured numeric value"),
    repo: MeasurementRepository = Depends(get_measurement_repository),
):
    assert_city_supported(city)

    try:
        sensor_metadata = load_sensor_metadata()
        if not sensor_metadata:
            raise HTTPException(
                status_code=500,
                detail="Sensor metadata could not be loaded"
            )

        city_data = sensor_metadata.get(city)
        if not city_data:
            raise HTTPException(
                status_code=501,
                detail=f"City '{city}' is not implemented. Only Warsaw is supported."
            )

        sensor_info = city_data.get(sensor_id)
        if not sensor_info:
            raise HTTPException(
                status_code=404,
                detail=f"Sensor ID {sensor_id} not found for city '{city}'",
            )

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

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/air/measurements/{measurement_id}",
    response_model=AirQualityMeasurement,
    summary="Update an existing measurement",
    responses={
        200: {"description": "Measurement updated"},
        400: {"description": "Invalid request data"},
        404: {"description": "Measurement not found"},
        500: {"description": "Server error"},
    },
)
def update_measurement(
    measurement_id: str,
    city: Optional[str] = Query(None, description="Optional city name"),
    parameter: Optional[str] = Query(None, description="Optional parameter"),
    value: Optional[float] = Query(None, description="Optional updated numeric value"),
    timestamp: Optional[datetime] = Query(None, description="Optional updated timestamp"),
    repo: MeasurementRepository = Depends(get_measurement_repository),
):
    try:
        existing = repo.get_by_id(measurement_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Measurement not found")

        updated = MeasurementEntity(
            id=existing.id,
            city=city or existing.city,
            parameter=parameter or existing.parameter,
            value=value if value is not None else existing.value,
            unit=existing.unit,
            timestamp=timestamp or existing.timestamp,
        )

        saved = repo.update(measurement_id, updated)
        return to_air_quality(saved)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/air/measurements/{measurement_id}",
    status_code=204,
    summary="Delete a measurement",
    responses={
        204: {"description": "Measurement deleted"},
        404: {"description": "Measurement not found"},
        500: {"description": "Server error"},
    },
)
def delete_measurement(
    measurement_id: str,
    repo: MeasurementRepository = Depends(get_measurement_repository),
):
    try:
        deleted = repo.delete(measurement_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Measurement not found")

        return  # FastAPI automatically sends 204

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
