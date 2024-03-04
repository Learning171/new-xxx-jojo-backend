from app.services.db_service import db_dependency
from app.models.cart_model import Cart
from app.models.product_model import Product
from app.validations.cart_validations import CartCreate


def add_to_cart(db: db_dependency, cart_create: CartCreate):
    existing_cart_item = (
        db.query(Cart).filter(Cart.product_id == cart_create.product_id).first()
    )
    existing_product_price = (
        db.query(Product).filter(Product.id == cart_create.product_id).first()
    )

    if existing_cart_item:
        # If the item already exists, you can choose whether to update or raise an error
        raise ValueError(
            "Item already exists in the cart. Update the quantity if needed."
        )

    total_price = existing_product_price.price * cart_create.quantity
    db_cart = Cart(**cart_create.dict(), total_price=total_price)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def get_user_cart(db: db_dependency):
    return db.query(Cart).all()


def update_cart_item_quantity(db: db_dependency, cart_id: int, new_quantity: int):
    db_cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    existing_product_price = (
        db.query(Product).filter(Product.id == db_cart_item.product_id).first()
    )

    if db_cart_item:
        db_cart_item.quantity = new_quantity
        db_cart_item.total_price = existing_product_price.price * new_quantity
        db.commit()
        db.refresh(db_cart_item)
        return db_cart_item


def remove_from_cart(db: db_dependency, cart_id: int):
    db_cart_item = db.query(Cart).filter(Cart.id == cart_id).first()

    if db_cart_item:
        db.delete(db_cart_item)
        db.commit()

    return db_cart_item
