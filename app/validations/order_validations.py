from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List


class OrderStatus(str, Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderBase(BaseModel):
    product_id: int
    user_id: int
    address_id: int
    quantity: int
    status: OrderStatus = OrderStatus.PENDING


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class OrderList(BaseModel):
    items: List[OrderResponse]
    total: int
