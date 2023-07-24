from pydantic import BaseModel, Field
from typing import Optional, Annotated
from annotated_types import Gt


class ProductSchemas(BaseModel):
    code: str = Field(..., max_length=20, min_length=5)
    name: str = Field(..., max_length=20, min_length=5)
    description: str = Field(..., min_length=5)
    price: int = Annotated[int, Gt(0)]
    stock: Optional[int]
    mark_model: Optional[int]
    category: int = Annotated[int, Gt(0)]
    images: list[str]
    profit: Optional[int]
    transmission: Optional[str]
