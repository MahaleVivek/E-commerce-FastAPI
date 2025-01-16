from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Order(Base):
    """
    Represents a order entity in the database.
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default='pending')  # Example statuses: 'pending', 'shipped', 'delivered'
    created_at = Column(Float, server_default=func.now())

    product = relationship('Product', back_populates='orders')
    seller = relationship('Seller', back_populates='orders')
    customer = relationship('Customer', back_populates='orders')

    def __repr__(self):
        return f"<Order(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, status={self.status})>"
