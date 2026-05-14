from datetime import datetime, timedelta
from typing import List, Optional, Union

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
    expiresAt: Optional[datetime] = Field(
        default=datetime.now() + timedelta(weeks=52 * 10)
    )


class ProductMinified(BaseModel):
    id: str = Field(alias="_id")
    name: str = Field()
    price: float = Field()


class ProductInput(BaseModel):
    name: str = Field()
    description: str = Field()
    price: float = Field()
    properties: list[ProductProperty] = Field()
    # Los productos expiran 10 años
    expiresAt: Optional[datetime] = Field(
        default=datetime.now() + timedelta(weeks=52 * 10)
    )


class Receipt(BaseModel):
    id: str = Field(alias="_id")
    products_data: List[ProductMinified] = Field()
    total: float = Field()
    date: datetime = Field()
    hash: Optional[str] = Field(
        description="Hash de la factura, hash generado en una blockchain"
    )


class ReceiptInput(BaseModel):
    """Input para generar una factura"""

    products: list[Product] = Field()
