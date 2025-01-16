from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Wallet(Base):
    """
    Represents a wallet entity in the database.
    """
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), unique=True, nullable=False)
    balance = Column(Integer, default=0, nullable=False)

    customer = relationship("Customer", back_populates="wallet")
