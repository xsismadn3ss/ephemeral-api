from bson.objectid import ObjectId
from pymongo.database import Database


def list_products(db: Database) -> list:
    products = db.products.find()
    data = []
    for product in products:
        product["_id"] = str(product["_id"])
        data.append(product)
    return data


def get_product(db: Database, product_id: str):
    product = db.products.find_one({"_id": ObjectId(product_id)})
    if product:
        product["_id"] = str(product["_id"])
    return product


def create_product(db: Database, product: dict):
    result = db.products.insert_one(product)
    return result.inserted_id


def update_product(db: Database, product_id: str, product: dict):
    result = db.products.update_one({"_id": ObjectId(product_id)}, {"$set": product})
    return result.modified_count


def delete_product(db: Database, product_id: str):
    result = db.products.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count
