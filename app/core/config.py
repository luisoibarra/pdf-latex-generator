from pydantic import AnyHttpUrl

class Settings:
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "PDF Latex Generator"
    PROJECT_NAME: str = "PDF Latex Generator"

settings = Settings()
