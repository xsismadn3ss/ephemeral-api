from typing import Optional, Union

from pydantic import BaseModel, Field


class ProductProperty(BaseModel):
    name: str = Field()
    value: Union[str, bool] = Field()


class Product(BaseModel):
    id: str = Field(alias="_id")
    name: str = Field()
    description: str = Field()
    price: float = Field()
    properties: list[ProductProperty] = Field()
    sold: bool = Field(default=False)


class ProductInput(BaseModel):
    name: str = Field()
    description: str = Field()
    price: float = Field()
    properties: list[ProductProperty] = Field()
    sold: bool = Field(default=False)


class Receipt(BaseModel):
    id: str = Field(alias="_id")
    products: list[Product] = Field()
    total: float = Field()
    date: str = Field()
    hash: Optional[str] = Field(
        description="Hash de la factura, hash generado en una blockchain"
    )
