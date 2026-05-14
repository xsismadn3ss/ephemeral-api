from fastapi import FastAPI

from src.app.config import get_config
from src.app.routes import health, products

config = get_config()

is_dev = config.env == "development"

app = FastAPI(
    docs_url="/docs" if is_dev else None,
    redoc_url="/redoc" if is_dev else None,
    openapi_url="/openapi.json" if is_dev else None,
)

app.include_router(products.router)
app.include_router(health.router)
