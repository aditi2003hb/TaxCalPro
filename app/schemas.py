# app/schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

class UserLogin(BaseModel):
    username: str
    uuid: str

class ProductInput(BaseModel):
    username: str
    uuid: str
    type: str
    product: str
    quantity: int
    weight: int
