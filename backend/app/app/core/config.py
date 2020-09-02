from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Boilerplate"

    POSTGRES_USER: str = "app"
    POSTGRES_PASSWORD: str = "app"
    POSTGRES_SERVER: str = "db"
    POSTGRES_DB: str = "app"


settings = Settings()
