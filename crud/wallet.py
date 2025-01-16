from sqlalchemy.orm import Session
from models.wallet import Wallet
from schemas.wallet import WalletCreate

def get_wallet_by_customer(db: Session, customer_id: int):
    """
    Retrieve a wallet by customer ID.
    """
    # Query the Wallet table to find the wallet associated with the customer
    return db.query(Wallet).filter(Wallet.customer_id == customer_id).first()

def create_wallet(db: Session, wallet: WalletCreate):
    """
    Create a new wallet for a customer with an initial balance of zero.
    """
    # Initialize a new wallet with the provided customer ID and a balance of 0
    db_wallet = Wallet(customer_id=wallet.customer_id, balance=0)
    db.add(db_wallet)     # Add the wallet to the session
    db.commit()           # Commit the transaction to save the wallet
    db.refresh(db_wallet)    # Refresh the session to include the newly created wallet
    return db_wallet

def update_wallet_balance(db: Session, wallet_id: int, amount: int):
    """
    Update the balance of a wallet by a specified amount.
    """
    # Retrieve the wallet by its ID
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        return None

    wallet.balance += amount
    db.commit()
    db.refresh(wallet)
    return wallet
