from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Boilerplate"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "db"
    POSTGRES_DB: str = "app"


settings = Settings()
