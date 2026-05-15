from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from src.app.application.products_service import ProductAppService
from src.app.models import Product, ProductInput
from src.app.dependencies import get_product_app_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[Product])
async def list_products(
    service: Annotated[ProductAppService, Depends(get_product_app_service)],
):
    return service.list_products()


# obtener producto por id
@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: str,
    service: Annotated[ProductAppService, Depends(get_product_app_service)],
):
    product = service.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post("/")
async def add_product(
    product: ProductInput,
    service: Annotated[ProductAppService, Depends(get_product_app_service)],
):
    reference = service.create_product(product.model_dump())
    return {"message": "Product added successfully", "product_id": str(reference)}


# Editar producto por id
@router.put("/{product_id}")
async def update_product(
    product_id: str,
    product: ProductInput,
    service: Annotated[ProductAppService, Depends(get_product_app_service)],
):
    result = service.update_product(product_id, product.model_dump())
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return {"message": "Product updated successfully"}


# eliminar producto por id
@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    service: Annotated[ProductAppService, Depends(get_product_app_service)],
):
    result = service.delete_product(product_id)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return {"message": "Product deleted successfully"}
