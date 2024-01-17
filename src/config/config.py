import secrets

from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api_v1"
    MONGODB_URL: str
    MONGODB_DATABASE: str
    MONGODB_COLLECTION: str

    class Config:
        case_sensitive = True


settings = Settings()
