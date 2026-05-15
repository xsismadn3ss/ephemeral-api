from dataclasses import dataclass

from src.app.domain.ports import CachePort, ProductRepositoryPort


@dataclass
class ProductAppService:
    repository: ProductRepositoryPort
    cache: CachePort

    ALL_PRODUCTS_KEY: str = "products:all"
    PRODUCT_KEY_TEMPLATE: str = "products:{id}"

    def list_products(self):
        cached = self.cache.get(self.ALL_PRODUCTS_KEY)
        if cached:
            return cached["products"]

        products = self.repository.list()
        self.cache.set(self.ALL_PRODUCTS_KEY, {"products": products})
        return products

    def get_product(self, product_id: str):
        cache_key = self.PRODUCT_KEY_TEMPLATE.format(id=product_id)
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        product = self.repository.get(product_id)
        if product is None:
            return None

        self.cache.set(cache_key, product)
        return product

    def create_product(self, product: dict) -> str:
        reference = self.repository.create(product)
        self.cache.delete(self.ALL_PRODUCTS_KEY)
        self.cache.delete(self.PRODUCT_KEY_TEMPLATE.format(id=reference))
        return reference

    def update_product(self, product_id: str, product: dict) -> int:
        result = self.repository.update(product_id, product)
        if result:
            self.cache.delete(self.ALL_PRODUCTS_KEY)
            self.cache.delete(self.PRODUCT_KEY_TEMPLATE.format(id=product_id))
        return result

    def delete_product(self, product_id: str) -> int:
        result = self.repository.delete(product_id)
        if result:
            self.cache.delete(self.ALL_PRODUCTS_KEY)
            self.cache.delete(self.PRODUCT_KEY_TEMPLATE.format(id=product_id))
        return result
