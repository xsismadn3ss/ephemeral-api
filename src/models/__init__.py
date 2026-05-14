from pydantic import BaseModel, Field


class ProductProperty(BaseModel):
    name: str = Field()
    value: str = Field()


class Product(BaseModel):
    id: str = Field()
    name: str = Field()
    description: str = Field()
    price: float = Field()
    properties: list[ProductProperty] = Field()


class CartItem(BaseModel):
    id: str = Field()
    product_id: str = Field()
    quantity: int = Field()


class Cart(BaseModel):
    id: str = Field()
    items: list[CartItem] = Field()


class Order(BaseModel):
    id: str = Field()
    cart_id: str = Field()
    total: float = Field(gt=0)
    status: str = Field()
    items: list[CartItem] = Field()


class Billing(BaseModel):
    id: str = Field()
    order: Order = Field()
    amount: float = Field(gt=0)
    status: str = Field()


class User(BaseModel):
    id: str = Field()
    name: str = Field()
    email: str = Field()
    cart: Cart = Field()
