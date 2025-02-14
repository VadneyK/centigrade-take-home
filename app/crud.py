from sqlalchemy.orm import Session
from . import models, schemas, auth
from fastapi import HTTPException, status

def get_customer(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    if get_customer_by_email(db, customer.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(customer.password)
    db_customer = models.Customer(
        email=customer.email,
        hashed_password=hashed_password,
        full_name=customer.full_name
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def create_order(db: Session, order: schemas.OrderCreate):
    # Verify customer exists
    customer = get_customer(db, order.customer_id)
    
    # Create order
    db_order = models.Order(
        customer_id=order.customer_id,
        total_amount=order.total_amount
    )
    db.add(db_order)
    db.flush()  # Flush to get the order ID
    
    # Add products to order
    for product_id in order.product_ids:
        product = get_product(db, product_id)
        db_order.products.append(product)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def authenticate_user(db: Session, email: str, password: str):
    user = get_customer_by_email(db, email)
    if not user:
        return False
    if not auth.verify_password(password, user.hashed_password):
        return False
    return user 