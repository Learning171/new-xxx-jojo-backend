from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.db_config import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    rating = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="reviews")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="reviews")
