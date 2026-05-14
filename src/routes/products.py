from typing import List

from fastapi import APIRouter, HTTPException, status

from src.config import APP_Config
from src.models import Product, ProductInput
from src.services import products as products_service
from src.utils.mongo import get_db

router = APIRouter(prefix="/products")


@router.get("/", response_model=List[Product])
async def list_products():
    config = APP_Config()
    db = get_db(config)
    return products_service.list_products(db)


# obtener producto por id
@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    config = APP_Config()
    db = get_db(config)

    product = products_service.get_product(db, product_id)
    print(product)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post("/")
async def add_product(product: ProductInput):
    config = APP_Config()
    db = get_db(config)

    # Agregar producto a la base de datos
    reference = products_service.create_product(db, product.model_dump())
    print(reference)
    # Enviar producto agregado
    return {"message": "Product added successfully", "product_id": str(reference)}


# Editar producto por id
@router.put("/{product_id}")
async def update_product(product_id: str, product: ProductInput):
    config = APP_Config()
    db = get_db(config)

    result = products_service.update_product(db, product_id, product.model_dump())
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    #  Obtenemos el producto actualizado
    return {"message": "Product updated successfully"}


# eliminar producto por id
@router.delete("/{product_id}")
async def delete_product(product_id: str):
    config = APP_Config()
    db = get_db(config)

    result = products_service.delete_product(db, product_id)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return {"message": "Product deleted successfully"}
