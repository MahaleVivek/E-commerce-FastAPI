from pydantic import BaseModel # type: ignore
from typing import Optional

class CustomerCreate(BaseModel):
    """
    Schema for creating a new customer.
    Fields:
    - name: The full name of the customer.
    - email: The email address of the customer.
    - password: The customer's password (hashed before storing).
    """
    name: str
    email: str
    password: str  # We'll hash the password before storing it

class CustomerLogin(BaseModel):
    """
    Schema for customer login.
    Fields:
    - email: The email address of the customer.
    - password: The customer's password.
    """
    email: str
    password: str

class CustomerResponse(BaseModel):
    """
    Schema for customer response, used for returning customer data.
    Fields:
    - id: The unique identifier of the customer.
    - name: The full name of the customer.
    - email: The email address of the customer.
    
    Configuration:
    - orm_mode: Enables compatibility with SQLAlchemy ORM objects.
    """
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
