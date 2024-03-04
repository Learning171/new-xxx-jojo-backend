from app.services.db_service import db_dependency
from app.models.product_model import Product, Image
from app.validations.product_validations import ProductCreate
from app.validations.product_validations import ProductCategory
from fastapi import UploadFile, HTTPException
from uuid import uuid4
import os

from sqlalchemy.orm import joinedload


def get_all_products(db: db_dependency, skip: int = 0, limit: int = 10):
    return (
        db.query(Product)
        .options(joinedload(Product.images))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_products_by_category(
    db: db_dependency, category: ProductCategory, skip: int = 0, limit: int = 10
):
    return (
        db.query(Product)
        .options(joinedload(Product.images))
        .filter(Product.category == category)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_product(db: db_dependency, product_create: ProductCreate):
    db_product = Product(**product_create.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: db_dependency, product_id: int, product_update: ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product_update.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: db_dependency, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


def save_image(file: UploadFile) -> str:
    # Generate a unique filename
    filename = f"{uuid4()}{os.path.splitext(file.filename)[1]}"
    with open(os.path.join("static/images", filename), "wb") as f:
        f.write(file.file.read())
    return filename


def create_image_record(db: db_dependency, product_id: int, filename: str):
    db_image = Image(url=f"/static/images/{filename}", product_id=product_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def update_image_record(db: db_dependency, image_id: int, filename: str) -> Image:
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")

    db_image.url = f"/static/images/{filename}"
    db.commit()
    db.refresh(db_image)
    return db_image


def validate_image_extension(file_name: str):
    allowed_extensions = {".png", ".jpg", ".jpeg", ".gif"}
    ext = os.path.splitext(file_name)[1]
    if ext.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension. Allowed extensions are: .png, .jpg, .jpeg, .gif",
        )
