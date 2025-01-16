from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext # type: ignore
from database import get_db
from datetime import datetime, timedelta
from jose import JWTError, jwt # type: ignore
from models.customer import Customer
from models.order import Order
from schemas.customer import CustomerCreate, CustomerResponse, CustomerLogin
from schemas.order import OrderResponse
from typing import List
from authentication import get_current_customer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/register/", response_model=CustomerResponse)
def register_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new customer.
    """
    # Check if the email already exists
    existing_customer = db.query(Customer).filter(Customer.email == customer.email).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        # Hash the password before saving
        hashed_password = pwd_context.hash(customer.password)

        new_customer = Customer(
            name=customer.name,
            email=customer.email,
            password=hashed_password
        )

        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        return new_customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering customer: {str(e)}")


SECRET_KEY = "your_secret_key_here"  # Change this to a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Utility to create access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login/")
def login(customer: CustomerLogin, db: Session = Depends(get_db)):
    """
    Endpoint to log in a customer.
    """
    try:
        # Fetch customer by email
        customer_db = db.query(Customer).filter(Customer.email == customer.email).first()

        # Validate credentials
        if not customer_db or not pwd_context.verify(customer.password, customer_db.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Generate access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": customer_db.email}, expires_delta=access_token_expires)

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging in: {str(e)}")


@router.get("/customer/orders", response_model=List[OrderResponse])
def get_customer_orders(
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer)
    ):
    """
    Retrieve the order history for the logged-in customer.
    """
    orders = db.query(Order).filter(Order.customer_id == current_customer.id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this customer.")
    return orders