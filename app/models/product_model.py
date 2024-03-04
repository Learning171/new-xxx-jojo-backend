from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.db_config import Base
from app.validations.product_validations import ProductCategory


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(Enum(ProductCategory), index=True)
    # subcategory = Column(Enum(ProductSubcategory), nullable=True)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    seller_id = Column(Integer, ForeignKey("users.id"))
    seller = relationship("User", back_populates="products")
    orders = relationship("Order", back_populates="product")
    cart_items = relationship("Cart", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    images = relationship("Image", back_populates="product")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="images")
