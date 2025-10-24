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
    db: str = "mock"

