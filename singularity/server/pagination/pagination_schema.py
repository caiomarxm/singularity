from typing import List
from pydantic import BaseModel, computed_field
from typing import TypeVar, Generic

T = TypeVar("T")


class PaginationMetadata(BaseModel):
    page: int
    per_page: int
    total_count: int

    @computed_field(return_type=int)
    @property
    def total_pages(self) -> int:
        return (self.total_count // self.per_page) + (
            1 if self.total_count % self.per_page > 0 else 0
        )


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    metadata: PaginationMetadata
