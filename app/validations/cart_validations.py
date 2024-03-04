from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
 
class CartBase(BaseModel):
    product_id: int
    user_id : int
    quantity: int = Field(gt=0)

 
class CartCreate(CartBase):
    pass
 
class CartResponse(CartBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
 
class CartList(BaseModel):
    items: List[CartResponse]
    total: int