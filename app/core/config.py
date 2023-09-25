from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "PDF Latex Generator"
    PROJECT_NAME: str = "PDF Latex Generator"

settings = Settings()
