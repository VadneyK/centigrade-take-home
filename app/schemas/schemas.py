from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    email: str
    full_name: str

class CustomerCreate(CustomerBase):
    password: str

class Customer(CustomerBase):
    id: int
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_id: int
    total_amount: float

class OrderCreate(OrderBase):
    product_ids: List[int]

class Order(OrderBase):
    id: int
    order_date: datetime
    products: List[Product]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 