from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.db_config import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="cart_items")
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="cart_items")
