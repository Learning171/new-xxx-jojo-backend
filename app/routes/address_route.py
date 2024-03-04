from fastapi import APIRouter, Depends, HTTPException, status
from app.services.db_service import db_dependency
from app.models.auth_model import Address
from typing import Annotated
from app.validations.auth_validations import AddressCreate, AddressResponse, AddressList
from app.routes.auth_routes import (
    check_customer_privilege,
)

cutomer_required = Annotated[str, Depends(check_customer_privilege)]

address_router = APIRouter(tags=["Addresses"])

# Address routes

@address_router.post("/addresses/", response_model=AddressResponse)
def create_address(address: AddressCreate, db: db_dependency, user: cutomer_required):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


@address_router.get("/addresses/{address_id}", response_model=AddressResponse)
def read_address(address_id: int, db: db_dependency, user: cutomer_required):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@address_router.put("/addresses/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int, address: AddressCreate, db: db_dependency, user: cutomer_required):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    for key, value in address.dict().items():
        setattr(db_address, key, value)

    db.commit()
    db.refresh(db_address)
    return db_address


@address_router.delete("/addresses/{address_id}", response_model=AddressResponse)
def delete_address(address_id: int, db: db_dependency, user: cutomer_required):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(db_address)
    db.commit()
    return db_address


@address_router.get("/addresses/", response_model=AddressList)
def list_addresses(db: db_dependency, user: cutomer_required):
    addresses = db.query(Address).all()
    total = db.query(Address).count()
    return {"items": addresses, "total": total}
