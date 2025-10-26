import yaml
from pydantic import BaseModel
from typing import Optional

class OpenAQConfig(BaseModel):
    base_url: str
    api_key: str

class AppConfig(BaseModel):
    name: str = "Web app"
    environment: str = "dev"
    repository_type: str = "in_memory"
    openaq: Optional[OpenAQConfig] = None

def load_config() -> AppConfig:
    try:
        """Load YAML config and return a validated AppConfig instance"""
        config_path = "./config.yaml"
        with open(config_path, "r") as f:
            raw_cfg = yaml.safe_load(f)
        app_cfg = raw_cfg.get("app", {})

        return AppConfig(**app_cfg)
    except Exception:
        return AppConfig()  # fallback to defaults
