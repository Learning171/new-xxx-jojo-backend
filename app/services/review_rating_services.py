from app.services.db_service import db_dependency
from app.models.reating_review_model import Review
from app.validations.review_rating_validations import ReviewCreate


def get_all_reviews_for_product(db: db_dependency, product_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_review_for_product(db: db_dependency, product_id: int, review_id: int):
    return (
        db.query(Review)
        .filter(Review.product_id == product_id, Review.id == review_id)
        .first()
    )


def create_review_for_product(db: db_dependency, review_create: ReviewCreate):
    db_review = Review(**review_create.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
