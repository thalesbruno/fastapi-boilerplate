from fastapi import FastAPI
from app.api.routers import items, users
from app.core.config import settings


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users"
    },
    {
        "name": "items",
        "description": "Operations with items"
    },
    {
        "name": "admin",
        "description": "Admin operations"
    },
    {
        "name": "auth",
        "description": "Authenticate operations"
    }
]

app = FastAPI(
    title=settings.APP_NAME,
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.0.1",
    openapi_tags=tags_metadata
)


app.include_router(items.router)
app.include_router(users.router)
