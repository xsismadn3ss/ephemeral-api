from fastapi import FastAPI

from src.app.routes import health, products

app = FastAPI()

app.include_router(products.router)
app.include_router(health.router)
