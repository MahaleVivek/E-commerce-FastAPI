from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.order import Order
from models.product import Product
from schemas.order import OrderCreate

def create_order(db: Session, order: OrderCreate):
    """
    Creates a new order, updates the product stock, and saves the order to the database.
    """
    # Fetch the product details
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    

    # Check product stock
    if product.quantity < order.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stock for product {product.name}. Only {product.stock} items available."
        )

    # Deduct stock
    product.quantity -= order.quantity
    db.add(product)

    db_order = Order(
        product_id=order.product_id,
        seller_id=product.seller_id,
        customer_id=order.customer_id,
        quantity=order.quantity,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders_by_customer(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of orders for a specific customer with optional pagination.
    """
    return db.query(Order).filter(Order.customer_id == customer_id).offset(skip).limit(limit).all()

def get_order_by_id(db: Session, order_id: int):
    """
    Retrieves the details of a specific order by its ID.
    """
    return db.query(Order).filter(Order.id == order_id).first()
