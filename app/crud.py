# app/crud.py
from sqlalchemy.orm import Session
from app import models
import uuid as uuid_lib

def create_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return None
    new_uuid = str(uuid_lib.uuid4())
    new_user = models.User(username=username, uuid=new_uuid)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, uuid: str):
    return db.query(models.User).filter(models.User.username == username, models.User.uuid == uuid).first()

def save_product_entry(db: Session, data):
    rate = 10  # per kg
    pre_tax = data.weight * rate
    vat1 = data.quantity * 5
    vat2 = pre_tax * 0.01
    final_tax = pre_tax + vat1 + vat2

    entry = models.ProductEntry(
        username=data.username,
        uuid=data.uuid,
        type=data.type,
        product=data.product,
        quantity=data.quantity,
        weight=data.weight,
        pre_tax=pre_tax,
        vat1=vat1,
        vat2=vat2,
        final_tax=final_tax
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {
        "pre_tax": pre_tax,
        "vat1": vat1,
        "vat2": vat2,
        "final_tax": final_tax
    }
