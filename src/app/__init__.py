from dotenv import load_dotenv
from fastapi import FastAPI

from src.app.routes import products

load_dotenv()

app = FastAPI()

app.include_router(products.router)
