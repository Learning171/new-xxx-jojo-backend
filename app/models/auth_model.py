from datetime import datetime
from app.config.db_config import Base
from sqlalchemy.orm import relationship
from app.validations.auth_validations import UserRole
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("Cart", uselist=False, back_populates="user")
    products = relationship("Product", back_populates="seller")
    reviews = relationship("Review", back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="addresses")
    username = Column(String)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    orders = relationship("Order", back_populates="address")

