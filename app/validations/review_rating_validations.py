from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class ReviewBase(BaseModel):
    content: str
    rating: float = Field(gt=0, le=5)
    product_id: int
    user_id: int


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class ReviewList(BaseModel):
    items: List[ReviewResponse]
    total: int
