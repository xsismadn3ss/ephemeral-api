from typing import Any, Mapping, Protocol


class CachePort(Protocol):
    def get(self, key: str) -> Any:
        ...

    def set(self, key: str, value: Any, ex: int | None = 10) -> None:
        ...

    def delete(self, key: str) -> None:
        ...


class ProductRepositoryPort(Protocol):
    def list(self) -> list[dict]:
        ...

    def get(self, product_id: str) -> dict | None:
        ...

    def create(self, product: dict) -> str:
        ...

    def update(self, product_id: str, product: dict) -> int:
        ...

    def delete(self, product_id: str) -> int:
        ...

    def mark_as_sold(self, product_id: str) -> int:
        ...

    def ensure_indexes(self) -> None:
        ...

    def get_indexes(self) -> Mapping[str, Any]:
        ...


class ReceiptRepositoryPort(Protocol):
    def list(self) -> list[dict]:
        ...

    def get(self, receipt_id: str) -> dict | None:
        ...

    def create(self, receipt: dict) -> str:
        ...
