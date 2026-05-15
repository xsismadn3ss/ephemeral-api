from enum import Enum
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from src.app.models import Product, ProductInput
from src.app.services import cache
from src.app.services import products as products_service
from src.app.utils.mongo import Database, get_db
from src.app.utils.redis import Redis, get_redis

router = APIRouter(prefix="/products", tags=["products"])


class CacheKeys(Enum):
    ALL_PRODUCTS = "products:all"
    PRODUCT = "products:{id}"


@router.get("/")
async def list_products(
    db: Annotated[Database, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    # Intentar obtener productos desde la caché
    products = cache.get(CacheKeys.ALL_PRODUCTS.value, redis)
    if products:
        return products["products"]
    # Obtener productos desde la base de datos
    products = products_service.list_products(db)
    # Guardar productos en la caché
    cache.set(CacheKeys.ALL_PRODUCTS.value, {"products": products}, redis)

    return products


# obtener producto por id
@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: str,
    db: Annotated[Database, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    # Intentar obtener producto desde la caché
    product = cache.get(CacheKeys.PRODUCT.value.format(id=product_id), redis)
    if product:
        return product
    # Obtener producto desde la base de datos
    product = products_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    # Guardar producto en la caché
    cache.set(CacheKeys.PRODUCT.value.format(id=product_id), product, redis)
    return product


@router.post("/")
async def add_product(
    product: ProductInput,
    db: Annotated[Database, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    # Agregar producto a la base de datos
    reference = products_service.create_product(db, product.model_dump())
    # Eliminar productos en caché para forzar actualización
    cache.delete(CacheKeys.ALL_PRODUCTS.value, redis)
    cache.delete(CacheKeys.PRODUCT.value.format(id=reference), redis)
    # Enviar producto agregado
    return {"message": "Product added successfully", "product_id": str(reference)}


# Editar producto por id
@router.put("/{product_id}")
async def update_product(
    product_id: str,
    product: ProductInput,
    db: Annotated[Database, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    result = products_service.update_product(db, product_id, product.model_dump())
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    # Eliminar productos en caché para forzar actualización
    cache.delete(CacheKeys.ALL_PRODUCTS.value, redis)
    cache.delete(CacheKeys.PRODUCT.value.format(id=product_id), redis)

    #  Obtenemos el producto actualizado
    return {"message": "Product updated successfully"}


# eliminar producto por id
@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    db: Annotated[Database, Depends(get_db)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    result = products_service.delete_product(db, product_id)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Eliminar productos en caché para forzar actualización
    cache.delete(CacheKeys.ALL_PRODUCTS.value, redis)
    cache.delete(CacheKeys.PRODUCT.value.format(id=product_id), redis)

    return {"message": "Product deleted successfully"}
