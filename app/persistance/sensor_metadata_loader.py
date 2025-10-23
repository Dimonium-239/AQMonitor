import yaml
from pathlib import Path

def load_sensor_metadata() -> dict:
    metadata_path = Path(__file__).resolve().parent.parent.parent / "sensor_metadata.yaml"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Sensor metadata file not found: {metadata_path}")

    with open(metadata_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)