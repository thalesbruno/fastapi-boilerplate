from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Boilerplate"
    EMAIL_SENDER: str = "no-reply@app.com"
    SMTP_SERVER: str = "your_stmp_server_here"

    POSTGRES_USER: str = "app"
    POSTGRES_PASSWORD: str = "app"
    POSTGRES_SERVER: str = "db"
    POSTGRES_DB: str = "app"


settings = Settings()
