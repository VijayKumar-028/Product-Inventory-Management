from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from sqlalchemy.orm import Session

import database_models
from database import SessionLocal, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


database_models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try: 
        yield db
    finally:
        db.close()

products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

def init_db():
    db=SessionLocal()

    existing_count=db.query(database_models.Product).count()
    if existing_count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
        print("DataBase initilazed with sample products")
    db.close()
init_db()

@app.get("/products")
def get_all_products(db: Session= Depends(get_db)):
    products=db.query(database_models.Product).all()
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session= Depends(get_db) ):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product

    return "product not found bro"

@app.post("/products")
def add_product(product: Product, db: Session= Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session= Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not Found")

    db_product.name=product.name # type: ignore
    db_product.description=product.description  # type: ignore
    db_product.price=product.price  # type: ignore
    db_product.quantity=product.quantity  # type: ignore
    db.commit()
    db.refresh(db_product)
    return {"message": "Product Updated Successfully", "product":db_product}

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_models.Product)
        .filter(database_models.Product.id == id)
        .first()
    )

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(db_product)
    db.commit()

    return {"message": "Product deleted successfully"}