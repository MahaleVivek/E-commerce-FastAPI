from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.order import OrderCreate, OrderResponse, OrderUpdateStatus
from crud.order import create_order, get_orders_by_customer, get_order_by_id
from models.product import Product
from models.customer import Customer
from models.order import Order
from models.seller import Seller
from authentication import get_current_customer, get_current_seller
from database import get_db
router = APIRouter()

@router.post("/create/")
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new order.
    """
    # Check if the product and customer exist (optional)
    product = db.query(Product).filter(Product.id == order.product_id).first()
    customer = db.query(Customer).filter(Customer.id == order.customer_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    try:
        # Create the order and update product stock
        return create_order(db=db, order=order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

@router.get("/orders/{customer_id}/")
def get_orders(customer_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get all orders by a specific customer.
    """
    try:
        orders = get_orders_by_customer(db=db, customer_id=customer_id)
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this customer")
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve orders: {str(e)}")

@router.get("/order/{order_id}/")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a specific order by its ID.
    """
    try:
        order = get_order_by_id(db=db, order_id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve order: {str(e)}")

# @router.post("/place/", response_model=OrderResponse)
# def place_order(order: OrderCreate, db: Session = Depends(get_db), customer: Customer = Depends(get_current_customer)):
#     # Check if the product exists
#     product = db.query(Product).filter(Product.id == order.product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     # Create the order
#     new_order = Order(
#         product_id=order.product_id,
#         seller_id=product.seller_id,  # Assuming seller is linked to the product
#         customer_id=customer.id,
#         quantity=order.quantity
#     )
    
#     db.add(new_order)
#     db.commit()
#     db.refresh(new_order)
    
#     return new_order

@router.put("/order/{order_id}/status", response_model=dict)
def update_order_status(
    order_id: int,
    order_update: OrderUpdateStatus,
    db: Session = Depends(get_db),
    current_seller: Seller = Depends(get_current_seller),
    ):
    """
    Update the status of an existing order. Only the seller of the product can update its status.
    """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.seller_id != current_seller.id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this order")

    # Update the status
    order.status = order_update.status
    db.commit()
    db.refresh(order)

    return {"detail": "Order status updated successfully"}