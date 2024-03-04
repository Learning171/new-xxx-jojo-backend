from app.services.db_service import db_dependency
from app.models.order_model import Order
from app.models.product_model import Product
from app.validations.order_validations import OrderCreate


def create_order(db: db_dependency, order_create: OrderCreate):
    product = db.query(Product).filter(Product.id == order_create.product_id).first()
    if product:
        if product.stock_quantity < order_create.quantity:
            raise ValueError("Insufficient stock for the ordered quantity")
        product.stock_quantity -= order_create.quantity
        total_price = product.price * order_create.quantity
        db.commit()
        db_order = Order(**order_create.dict(), total_price=total_price)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    else:
        raise ValueError("Product not found in the database")


def get_order(db: db_dependency, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: db_dependency, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()
