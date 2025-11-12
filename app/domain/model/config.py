import os
import yaml
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

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
        config_path = "./config.yaml"

        with open(config_path, "r") as f:
            raw_yaml = f.read()

        resolved_yaml = os.path.expandvars(raw_yaml)

        raw_cfg = yaml.safe_load(resolved_yaml)
        app_cfg = raw_cfg.get("app", {})

        return AppConfig(**app_cfg)

    except Exception as e:
        print(f"Config load failed: {e}")
        return AppConfig()

