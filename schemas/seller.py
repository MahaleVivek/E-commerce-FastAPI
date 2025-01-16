from pydantic import BaseModel, EmailStr

class SellerBase(BaseModel):
    """
    Base schema for seller-related operations.
    Fields:
    - name: The name of the seller.
    - email: The email address of the seller.
    - store_name: The name of the seller's store.
    - phone: The contact phone number of the seller, optional.
    - business_location: The location of the seller's business.
    - niche: The business niche or category the seller operates in.
    """
    name: str
    email: EmailStr
    store_name: str
    phone: str | None = None
    business_location: str
    niche: str

class SellerCreate(SellerBase):
    """
    Schema for creating a new seller.
    Inherits all fields from SellerBase and adds:
    - password: The password for seller authentication during registration.
    """
    password: str  # Include password during registration

class SellerResponse(SellerBase):
    """
    Schema for seller responses, used to return seller details.
    Fields:
    - id: The unique identifier of the seller.
    - All fields from SellerBase are also included.
    
    Configuration:
    - orm_mode: Enables compatibility with SQLAlchemy ORM objects.
    """
    id: int

    class Config:
        orm_mode = True
