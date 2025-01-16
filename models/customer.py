from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    """
    Represents a customer entity in the database.
    """
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)
    phone = Column(String)

    orders = relationship("Order", back_populates="customer")  # Establish relationship with orders
    wallet = relationship("Wallet", back_populates="customer", uselist=False)

    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name}, email={self.email})>"
