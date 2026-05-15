from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.config import get_config
from src.app.routes import health, products, receipts
from src.app.validation import startup
from rich.console import Console

config = get_config()

is_dev = config.env == "development"


app = FastAPI(
    docs_url="/docs" if is_dev else None,
    redoc_url="/redoc" if is_dev else None,
    openapi_url="/openapi.json" if is_dev else None,
    lifespan=startup,
)

console = Console()
origins = config.origins.split(",") if config.origins else []
console.log(f"[dim]Allowed origins: {origins}[/]")

app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        ["*"] if is_dev else origins
    ),
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(products.router)
app.include_router(health.router)
app.include_router(receipts.router)
