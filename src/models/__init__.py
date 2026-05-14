from typing import Any, Callable, Literal

from pydantic import BaseModel, Field
from pydantic.main import IncEx


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
    password: str = Field()
    cart: Cart = Field()

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
        polymorphic_serialization: bool | None = None,
    ) -> dict[str, Any]:
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            exclude_computed_fields=exclude_computed_fields,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
            polymorphic_serialization=polymorphic_serialization,
        )
        # eliminar clave password
        data.pop("password", None)
        return data
