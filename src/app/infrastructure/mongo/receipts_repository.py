from bson.errors import InvalidId
from bson.objectid import ObjectId
from pymongo.database import Database


class MongoReceiptRepository:
    def __init__(self, db: Database):
        self._db = db

    def list(self) -> list[dict]:
        receipts = self._db.receipts.find()
        data = []
        for receipt in receipts:
            receipt["_id"] = str(receipt["_id"])
            data.append(receipt)
        return data

    def get(self, receipt_id: str) -> dict | None:
        try:
            object_id = ObjectId(receipt_id)
        except InvalidId:
            return None

        receipt = self._db.receipts.find_one({"_id": object_id})
        if receipt:
            receipt["_id"] = str(receipt["_id"])
        return receipt

    def create(self, receipt: dict) -> str:
        result = self._db.receipts.insert_one(receipt)
        return str(result.inserted_id)
