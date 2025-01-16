from pydantic import BaseModel # type: ignore
from typing import Optional
from enum import Enum

class OrderCreate(BaseModel):
    """
    Schema for creating a new order.
    Fields:
    - product_id: The ID of the product being ordered.
    - customer_id: The ID of the customer placing the order.
    - quantity: The number of items being ordered.
    - status: The status of the order, defaults to 'pending'.
    
    Configuration:
    - orm_mode: Enables compatibility with SQLAlchemy ORM objects.
    """
    product_id: int
    customer_id: int
    quantity: int
    status: Optional[str] = 'pending'  # Default status as 'pending'

    class Config:
        orm_mode = True


class OrderResponse(BaseModel):
    """
    Schema for order responses, used to return order details.
    Fields:
    - id: The unique identifier of the order.
    - product_id: The ID of the product in the order.
    - quantity: The quantity of the product ordered.
    - status: The current status of the order.
    
    Configuration:
    - orm_mode: Enables compatibility with SQLAlchemy ORM objects.
    """
    id: int
    product_id: int
    quantity: int
    status: str

    class Config:
        orm_mode = True


class OrderStatus(str, Enum):
    """
    Enumeration for order status values.
    Enum Values:
    - pending: The order has been placed but not yet processed.
    - processing: The order is being prepared.
    - shipped: The order has been shipped.
    - delivered: The order has been delivered to the customer.
    - canceled: The order has been canceled.
    """
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"

class OrderUpdateStatus(BaseModel):
    """
    Schema for updating the status of an order.
    Fields:
    - status: The new status of the order, selected from the OrderStatus enumeration.
    """
    status: OrderStatus