from fastapi import APIRouter, Depends, HTTPException
from app.services.db_service import db_dependency
from app.services.review_rating_services import (
    create_review_for_product,
    get_review_for_product,
    get_all_reviews_for_product,
)
from app.validations.review_rating_validations import ReviewCreate
from typing import Annotated
from app.routes.auth_routes import (
    check_customer_privilege,
)

cutomer_required = Annotated[str, Depends(check_customer_privilege)]

review_router = APIRouter(tags=["Review"])


@review_router.post("/reviews/{product_id}")
def create_new_review_for_product(review_create: ReviewCreate, db: db_dependency, user: cutomer_required):
    return create_review_for_product(db, review_create)


@review_router.get("/reviews/{product_id}")
def read_all_reviews_for_product(
    product_id: int, db: db_dependency, user: cutomer_required, skip: int = 0, limit: int = 10
):
    return get_all_reviews_for_product(db, product_id, skip=skip, limit=limit)


@review_router.get("/reviews/{product_id}/{review_id}")
def read_review_for_product(product_id: int, review_id: int, db: db_dependency, user: cutomer_required):
    review = get_review_for_product(db, product_id, review_id)
    if review is None:
        raise HTTPException(
            status_code=404,
            detail=f"Review with id {review_id} for product {product_id} not found",
        )
    return review
