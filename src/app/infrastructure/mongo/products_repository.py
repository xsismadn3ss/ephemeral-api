from datetime import datetime, timedelta
from typing import Any, Mapping

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pymongo.database import Database


class MongoProductRepository:
    def __init__(self, db: Database):
        self._db = db

    def ensure_indexes(self) -> None:
        self._db.products.create_index(
            "expiresAt",
            expireAfterSeconds=60 * 3,
            name="products_expiresAt_ttl",
            partialFilterExpression={"sold": True},
        )

    def get_indexes(self) -> Mapping[str, Any]:
        return self._db.products.index_information()

    def list(self) -> list[dict]:
        products = self._db.products.find()
        data = []
        for product in products:
            product["_id"] = str(product["_id"])
            data.append(product)
        return data

    def get(self, product_id: str) -> dict | None:
        try:
            object_id = ObjectId(product_id)
        except InvalidId:
            return None

        product = self._db.products.find_one({"_id": object_id})
        if product:
            product["_id"] = str(product["_id"])
        return product

    def create(self, product: dict) -> str:
        result = self._db.products.insert_one(product)
        return str(result.inserted_id)

    def update(self, product_id: str, product: dict) -> int:
        try:
            object_id = ObjectId(product_id)
        except InvalidId:
            return 0

        result = self._db.products.update_one({"_id": object_id}, {"$set": product})
        return result.modified_count

    def mark_as_sold(self, product_id: str) -> int:
        try:
            object_id = ObjectId(product_id)
        except InvalidId:
            return 0

        result = self._db.products.update_one(
            {"_id": object_id},
            {"$set": {"sold": True, "expiresAt": datetime.now() + timedelta(minutes=3)}},
        )
        return result.modified_count

    def delete(self, product_id: str) -> int:
        try:
            object_id = ObjectId(product_id)
        except InvalidId:
            return 0

        result = self._db.products.delete_one({"_id": object_id})
        return result.deleted_count
