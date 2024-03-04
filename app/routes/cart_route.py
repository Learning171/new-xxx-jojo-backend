from fastapi import APIRouter, Depends, HTTPException
from app.services.db_service import db_dependency
from app.services.cart_services import (
    add_to_cart,
    get_user_cart,
    update_cart_item_quantity,
    remove_from_cart,
)
from app.validations.cart_validations import CartCreate
from typing import Annotated
from app.routes.auth_routes import (
    check_customer_privilege,
)

cutomer_required = Annotated[str, Depends(check_customer_privilege)]

cart_router = APIRouter(tags=["Shopping Cart"])


@cart_router.post("/cart/")
def add_item_to_cart(
    cart_create: CartCreate, db: db_dependency, user:cutomer_required):
    return add_to_cart(db, cart_create)


@cart_router.get("/cart/")
def get_cart_items(db: db_dependency, user:cutomer_required):
    return get_user_cart(db)


@cart_router.put("/cart/{cart_id}")
def update_cart_quantity(cart_id: int, new_quantity: int, db: db_dependency, user:cutomer_required):
    cart_item = update_cart_item_quantity(db, cart_id, new_quantity)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item


@cart_router.delete("/cart/{cart_id}")
def remove_item_from_cart(cart_id: int, db: db_dependency, user:cutomer_required):
    cart_item = remove_from_cart(db, cart_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item
