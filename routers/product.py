from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.product import Product
from models.seller import Seller
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from database import get_db
from authentication import get_current_seller

router = APIRouter(prefix="/products", tags=["Products"])

# Create a product
@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_seller: Seller = Depends(get_current_seller)
):
    """
    Endpoint to create a product. Only available to logged-in sellers.
    """
    try:
        db_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            seller_id=current_seller.id,
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

# Retrieve all products
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """
    Retrieve all products in the database.
    """
    try:
        return db.query(Product).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {str(e)}")


# Retrieve a specific product
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific product by its ID.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Update a product
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_seller: Seller = Depends(get_current_seller)
    ):
    """
    Update a product. Only available to the seller who created it.
    """
    db_product = db.query(Product).filter(Product.id == product_id, Product.seller_id == current_seller.id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found or unauthorized")

    try:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

# Delete a product
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_seller: Seller = Depends(get_current_seller)
    ):
    """
    Delete a product. Only available to the seller who created it.
    """
    db_product = db.query(Product).filter(Product.id == product_id, Product.seller_id == current_seller.id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found or unauthorized")

    try:
        db.delete(db_product)
        db.commit()
        return {"detail": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")
