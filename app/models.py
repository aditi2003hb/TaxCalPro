# app/models.py
from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    uuid = Column(String, unique=True, index=True)

class ProductEntry(Base):
    __tablename__ = "product_entries"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    uuid = Column(String)
    type = Column(String)
    product = Column(String)
    quantity = Column(Integer)
    weight = Column(Integer)
    pre_tax = Column(Float)
    vat1 = Column(Float)
    vat2 = Column(Float)
    final_tax = Column(Float)
