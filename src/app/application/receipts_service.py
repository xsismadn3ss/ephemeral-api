from dataclasses import dataclass
from datetime import datetime

from src.app.domain.ports import CachePort, ProductRepositoryPort, ReceiptRepositoryPort
from src.app.models import ProductMinified, ReceiptInput


@dataclass
class ReceiptAppService:
    receipt_repository: ReceiptRepositoryPort
    product_repository: ProductRepositoryPort
    cache: CachePort

    ALL_RECEIPTS_KEY: str = "receipts:all"
    RECEIPT_KEY_TEMPLATE: str = "receipts:{id}"

    def list_receipts(self):
        cached = self.cache.get(self.ALL_RECEIPTS_KEY)
        if cached:
            return cached["receipts"]

        receipts = self.receipt_repository.list()
        self.cache.set(self.ALL_RECEIPTS_KEY, {"receipts": receipts})
        return receipts

    def get_receipt(self, receipt_id: str):
        cache_key = self.RECEIPT_KEY_TEMPLATE.format(id=receipt_id)
        cached = self.cache.get(cache_key)
        if cached:
            return cached["receipt"]

        receipt = self.receipt_repository.get(receipt_id)
        if receipt is None:
            return None

        self.cache.set(cache_key, {"receipt": receipt}, ex=60 * 3)
        return receipt

    def create_receipt(self, receipt: ReceiptInput):
        products_data = []
        total = 0.0

        for product in receipt.products:
            result = self.product_repository.mark_as_sold(product.id)
            if result:
                product_dict = product.model_dump(by_alias=True)
                products_data.append(
                    ProductMinified(**product_dict).model_dump(by_alias=True)
                )
                total += product.price

        receipt_dict = receipt.model_dump(by_alias=True)
        receipt_dict.pop("products")
        receipt_dict["products_data"] = products_data
        receipt_dict["total"] = total
        receipt_dict["date"] = datetime.now()
        receipt_dict["hash"] = None

        receipt_id = self.receipt_repository.create(receipt_dict)
        self.cache.delete(self.ALL_RECEIPTS_KEY)

        created_receipt = self.receipt_repository.get(receipt_id)
        if created_receipt is not None:
            self.cache.set(
                self.RECEIPT_KEY_TEMPLATE.format(id=receipt_id),
                {"receipt": created_receipt},
                ex=60 * 3,
            )

        return {
            "receipt_id": receipt_id,
            "total": total,
            "total_products": len(products_data),
        }
