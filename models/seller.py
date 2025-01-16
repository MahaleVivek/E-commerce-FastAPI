from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Seller(Base):
    """
    Represents a seller entity in the database.
    """
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Store hashed password
    store_name = Column(String, nullable=False)
    business_location = Column(String, nullable=True)
    niche = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    # Relationship with the Order model (one-to-many relationship)
    orders = relationship('Order', back_populates='seller')
    products = relationship("Product", back_populates="seller")


