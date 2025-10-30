import requests
from datetime import datetime
from typing import List

from app.domain.mapper import to_air_quality
from app.domain.model.air_quality import AirQualityMeasurement
from app.domain.model.config import load_config
from app.persistance.model.measurement_entity import MeasurementEntity
from app.persistance.repositories.measurement_repository import MeasurementRepository
from app.persistance.sensor_metadata_loader import load_sensor_metadata

class OpenAQAirQualityService:
    """Repository fetching air quality data for Warsaw from OpenAQ API (v3)."""

    def __init__(self, measurement_repo: MeasurementRepository):
        self.config = load_config()
        self.base_url = self.config.openaq.base_url
        self.api_key = self.config.openaq.api_key
        self.sensor_metadata = load_sensor_metadata()
        self.measurement_repo = measurement_repo

    def get_latest_measurements(self, city: str) -> List[AirQualityMeasurement]:
        location_id = self.sensor_metadata.get(city).get("id")
        url = f"{self.base_url}/locations/{location_id}/latest"
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        results = []
        city_metadata = self.sensor_metadata.get(city, {})
        for m in data.get("results", []):
            sensor_id = m.get("sensorsId")
            param_info = city_metadata.get(sensor_id, {"parameter": "unknown", "unit": "unknown"})

            timestamp = datetime.fromisoformat(m["datetime"]["utc"].replace("Z", "+00:00"))
            parameter = param_info["parameter"]
            value = m["value"]

            exists = self.measurement_repo.measurement_exists(city=city, parameter=parameter, timestamp=timestamp)
            if exists:
                continue  # skip if already in DB

            # Otherwise save new one
            measurement = MeasurementEntity(
                city=city,
                parameter=parameter,
                value=value,
                unit=param_info["unit"],
                timestamp=timestamp,
            )
            saved = self.measurement_repo.add(measurement)
            results.append(to_air_quality(saved))

        return results


