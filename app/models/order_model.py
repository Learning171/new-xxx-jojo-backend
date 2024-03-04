from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.db_config import Base
from app.validations.order_validations import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="orders")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")
    address_id = Column(Integer, ForeignKey("addresses.id"))
    address = relationship("Address", back_populates="orders")
