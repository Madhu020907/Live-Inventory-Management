from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- SQL DATABASE CONFIGURATION ---
DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DATABASE MODEL (How data looks in the SQL tables) ---
class DBProduct(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer)

# Create the database tables automatically
Base.metadata.create_all(bind=engine)

# --- FASTAPI APP SETTINGS ---
app = FastAPI(title="Production E-Commerce Backend")

# Database Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- DATA VALIDATION MODELS (Pydantic) ---
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

# --- API ENDPOINTS ---

# 1. CREATE: Add a new validated product directly into SQL
@app.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product: ProductBase, db: Session = Depends(get_db)):
    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero.")
    if product.stock < 0:
        raise HTTPException(status_code=400, detail="Stock levels cannot be negative.")
    
    db_product = DBProduct(name=product.name, price=product.price, stock=product.stock)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 2. READ ALL: Fetch all active inventory data records from SQL
@app.get("/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(DBProduct).all()

# 3. DELETE: Remove an item using its unique identifier
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    db.delete(db_product)
    db.commit()
    return None