from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"
    shop_owner = "shop_owner"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.customer


class UserCreate(UserBase):
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: Optional[bool] = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UserLogin(BaseModel):
    email : EmailStr
    password: str

class TokenData(BaseModel):
    email: str | None = None


class AddressBase(BaseModel):
    user_id: int
    username : str
    street: str
    city: str
    state: str
    zip_code: str


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class AddressList(BaseModel):
    items: List[AddressResponse]
    total: int
