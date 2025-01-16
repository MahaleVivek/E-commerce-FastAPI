from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt # type: ignore
from sqlalchemy.orm import Session
from models.seller import Seller
from models.customer import Customer
from database import get_db

# Secret key and algorithm for JWT
SECRET_KEY = "your_secret_key_here"  # Replace with a strong secret key
ALGORITHM = "HS256"

def get_current_seller(token: str, db: Session = Depends(get_db)):
    """
    Decodes the JWT token to get the current authenticated seller.

    Args:
        token (str): The JWT token provided in the Authorization header.
        db (Session): SQLAlchemy session for database queries.

    Returns:
        Seller: The authenticated seller.

    Raises:
        HTTPException: If the token is invalid or the seller does not exist.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    seller = db.query(Seller).filter(Seller.email == email).first()
    if seller is None:
        raise HTTPException(status_code=401, detail="Seller not found")
    return seller


#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="customer/login/")

def get_current_customer(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        customer = db.query(Customer).filter(Customer.email == email).first()
        if customer is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return customer
    except:
        raise HTTPException(status_code=401, detail="Invalid token")