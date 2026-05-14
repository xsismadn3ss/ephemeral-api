from datetime import datetime
from typing import Annotated

from bson.objectid import ObjectId
from fastapi import Depends
from pymongo.database import Database

from src.app.models import ReceiptInput
from src.app.services import crypt
from src.app.services import products as products_service
from src.app.utils.mongo import get_db


def list(db: Annotated[Database, Depends(get_db)]):
    receipts = db.receipts.find()
    data = []
    for receipt in receipts:
        receipt["_id"] = str(receipt["_id"])
        data.append(receipt)
    return data


def get(db: Annotated[Database, Depends(get_db)], receipt_id: str):
    receipt = db.receipts.find_one({"_id": ObjectId(receipt_id)})
    if receipt:
        receipt["_id"] = str(receipt["_id"])
    return receipt


def create(
    db: Annotated[Database, Depends(get_db)],
    receipt: ReceiptInput,
):
    # Eliminar las propiedades de los productos
    p_cleaned = []
    total = 0.0
    for p in receipt.products:
        p.clean_properties()
        products_service.set_as_sold(db, p.id)
        p_dict = p.model_dump()
        p_dict.pop("expiresAt")
        p_cleaned.append(p_dict)
        total += p.price

    # Crear cifrado de los productos
    encrypted = crypt.base64_encode({"products": p_cleaned})
    data_dict = receipt.model_dump(by_alias=True)

    # Eliminar llave products
    data_dict.pop("products")
    data_dict["products_data"] = encrypted
    data_dict["total"] = total
    data_dict["data"] = datetime.now()
    data_dict["hash"] = None

    result = db.receipts.insert_one(data_dict)

    return {
        "receipt_id": str(result.inserted_id),
        "total": total,
        "total_products": len(p_cleaned),
    }
