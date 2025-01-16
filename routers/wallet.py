from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.wallet import WalletResponse, WalletCreate
from crud.wallet import get_wallet_by_customer, create_wallet, update_wallet_balance
from models.customer import Customer
from database import get_db
from authentication import get_current_customer

router = APIRouter()

@router.get("/wallet/", response_model=WalletResponse)
def get_wallet_balance(
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer),
    ):
    """
    Retrieve the wallet balance for the current customer.
    """
    wallet = get_wallet_by_customer(db, current_customer.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.post("/wallet/create/")
def create_wallet_for_customer(
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer),
    ):
    """
    Create a wallet for the current customer.
    """
    existing_wallet = get_wallet_by_customer(db, current_customer.id)
    if existing_wallet:
        raise HTTPException(status_code=400, detail="Wallet already exists")
    wallet_data = WalletCreate(customer_id=current_customer.id)
    wallet = create_wallet(db, wallet_data)
    return {"detail": "Wallet created successfully"}

@router.put("/wallet/credit/")
def credit_wallet(
    amount: int,
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer),
    ):
    """
    Credit the wallet with a specified amount.
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")
    
    wallet = get_wallet_by_customer(db, current_customer.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    updated_wallet = update_wallet_balance(db, wallet.id, amount)
    return {"detail": "Wallet credited successfully", "balance": updated_wallet.balance}

@router.put("/wallet/debit/")
def debit_wallet(
    amount: int,
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer),
    ):
    """
    Debit the wallet by a specified amount.
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    wallet = get_wallet_by_customer(db, current_customer.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    updated_wallet = update_wallet_balance(db, wallet.id, -amount)
    return {"detail": "Wallet debited successfully", "balance": updated_wallet.balance}
