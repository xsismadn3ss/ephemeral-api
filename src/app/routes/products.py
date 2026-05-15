from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from src.app.config import APP_Config
from src.app.models import Product, ProductInput
from src.app.services import products as products_service
from src.app.utils.mongo import Database, get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[Product])
async def list_products(db: Annotated[Database, Depends(get_db)]):
    return products_service.list_products(db)


# obtener producto por id
@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str, db: Annotated[Database, Depends(get_db)]):
    product = products_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post("/")
async def add_product(product: ProductInput, db: Annotated[Database, Depends(get_db)]):
    # Agregar producto a la base de datos
    reference = products_service.create_product(db, product.model_dump())
    # Enviar producto agregado
    return {"message": "Product added successfully", "product_id": str(reference)}


# Editar producto por id
@router.put("/{product_id}")
async def update_product(
    product_id: str, product: ProductInput, db: Annotated[Database, Depends(get_db)]
):
    result = products_service.update_product(db, product_id, product.model_dump())
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    #  Obtenemos el producto actualizado
    return {"message": "Product updated successfully"}


# eliminar producto por id
@router.delete("/{product_id}")
async def delete_product(product_id: str, db: Annotated[Database, Depends(get_db)]):
    result = products_service.delete_product(db, product_id)
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return {"message": "Product deleted successfully"}
