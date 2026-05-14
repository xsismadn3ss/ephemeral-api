from pydantic import BaseModel, Field


class ProductProperty(BaseModel):
    id: str = Field()
    name: str = Field()
    value: str = Field()


class Product(BaseModel):
    id: str = Field()
    name: str = Field()
    description: str = Field()
    price: float = Field()
    properties: list[ProductProperty] = Field()
