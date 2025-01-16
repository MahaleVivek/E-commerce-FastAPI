from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.order import OrderResponse
from schemas.seller import SellerCreate, SellerResponse
from models.seller import Seller
from models.order import Order
from models.product import Product
from database import get_db
from passlib.hash import bcrypt # type: ignore
from passlib.context import CryptContext # type: ignore
from jose import JWTError, jwt # type: ignore
from datetime import datetime, timedelta
from authentication import get_current_seller
from typing import List

router = APIRouter(prefix="/sellers", tags=["Sellers"])

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret and algorithm
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Hash the password
def hash_password(password: str) -> str:
    """
    Hash a plain password.
    """
    return pwd_context.hash(password)

# Verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Create a JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token with the specified data and expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Login endpoint
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Authenticate the seller using email and password and return a JWT token.
    """
    seller = db.query(Seller).filter(Seller.email == email).first()
    if not seller or not verify_password(password, seller.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT token
    access_token = create_access_token(data={"sub": seller.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=SellerResponse)
def register_seller(seller: SellerCreate, db: Session = Depends(get_db)):
    """
    Create a new seller account.
    """
    # Check if email is already registered
    existing_seller = db.query(Seller).filter(Seller.email == seller.email).first()
    if existing_seller:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before saving
    hashed_password = hash_password(seller.password)

    # Create a new seller instance and save to the database
    new_seller = Seller(
        name=seller.name,
        email=seller.email,
        password=hashed_password,
        store_name=seller.store_name,
        phone=seller.phone,
        business_location=seller.business_location,
        niche=seller.niche
    )
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
    
    #return create_seller(db, seller)


@router.get("/me", response_model=SellerResponse)
def get_seller_profile(current_seller: Seller = Depends(get_current_seller)):
    """
    Retrieve the profile information of the currently authenticated seller.
    """
    return current_seller

@router.get("/seller/orders", response_model=List[OrderResponse])
def get_seller_orders(
    db: Session = Depends(get_db),
    current_seller: Seller = Depends(get_current_seller)
):
    """
    Retrieve the order history for the logged-in seller.
    """
    orders = db.query(Order).join(Product).filter(Product.seller_id == current_seller.id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this seller.")
    return orders
