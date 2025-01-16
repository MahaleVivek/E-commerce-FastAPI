from pydantic import BaseModel # type: ignore

class WalletBase(BaseModel):
    """
    Base schema for wallet operations.
    Fields:
    - balance: The current balance in the wallet.
    """
    balance: int

class WalletCreate(BaseModel):
    """
    Schema for creating a new wallet.
    Fields:
    - customer_id: The unique identifier of the customer who owns the wallet.
    """
    customer_id: int

class WalletResponse(WalletBase):
    """
    Schema for responding with wallet details.
    Inherits from WalletBase and adds:
    - id: The unique identifier of the wallet.
    
    Configuration:
    - orm_mode: Ensures compatibility with SQLAlchemy models.
    """
    id: int

    class Config:
        orm_mode = True
