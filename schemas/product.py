from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    """
    Base schema for product-related operations.
    Fields:
    - name: The name of the product.
    - description: A brief description of the product, optional.
    - price: The price of the product.
    - quantity: The available quantity of the product in stock.
    """
    name: str
    description: str | None = None
    price: float
    quantity: int

class ProductCreate(ProductBase):
    """
    Schema for creating a new product.
    Inherits all fields from ProductBase.
    """
    pass

class ProductUpdate(ProductBase):
    """
    Schema for updating product details.
    All fields are optional to allow partial updates.
    Fields:
    - name: Optional updated name of the product.
    - description: Optional updated description of the product.
    - price: Optional updated price of the product.
    - quantity: Optional updated quantity of the product in stock.
    """
    name: Optional[str] = None  # Fields are optional for updates
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class ProductResponse(ProductBase):
    """
    Schema for product responses, used to return product details.
    Fields:
    - id: The unique identifier of the product.
    - seller_id: The ID of the seller who owns the product.
    - All fields from ProductBase are also included.
    
    Configuration:
    - orm_mode: Enables compatibility with SQLAlchemy ORM objects.
    """
    id: int
    seller_id: int

    class Config:
        orm_mode = True
