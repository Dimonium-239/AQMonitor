from fastapi import APIRouter, Depends
from typing import List

from app.adapters.restapi.dependecies import get_measurement_repository
from app.domain.model.air_quality import AirQualityMeasurement
from app.persistance.repositories.measurement_repository import MeasurementRepository
from app.persistance.repositories.openaq_repository import OpenAQAirQualityRepository

router = APIRouter()

@router.get("/air/measurements", response_model=List[AirQualityMeasurement])
def get_air_quality(city: str = "Warsaw", repo=Depends(get_measurement_repository)) -> List[AirQualityMeasurement]:
    use_case = OpenAQAirQualityRepository(measurement_repo=repo)
    return use_case.get_latest_measurements(city)

@router.get("/air/measurements/persisted", response_model=List[AirQualityMeasurement])
def list_items(repo: MeasurementRepository = Depends(get_measurement_repository)):
    return  repo.get_all()