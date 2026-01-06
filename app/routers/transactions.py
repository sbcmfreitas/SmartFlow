from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import uuid
from app import database, models, schemas, auth

router = APIRouter(
    prefix="/transaction",
    tags=["Transactions"]
)

import logging
logger = logging.getLogger(__name__)

@router.post("/start", response_model=uuid.UUID)
def start_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    # If start_time is not provided, use server time
    start_time = transaction.start_time or datetime.utcnow()
    
    # Ensure start_time is naive for consistency
    if start_time.tzinfo is not None:
        start_time = start_time.replace(tzinfo=None)

    logger.info(f"Transaction started by user {current_user.username} for device {transaction.device_id}")
    
    db_transaction = models.Transaction(
        device_id=transaction.device_id,
        entity_id=transaction.entity_id,
        user_id=current_user.id,
        start_time=start_time
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction.transaction_id

@router.post("/finish", response_model=schemas.TransactionOut)
def finish_transaction(
    transaction_id: uuid.UUID,
    transaction_data: schemas.TransactionFinish,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).first()
    if not db_transaction:
        logger.warning(f"Attempt to finish non-existent transaction {transaction_id}")
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if db_transaction.end_time:
        logger.warning(f"Attempt to finish already finished transaction {transaction_id}")
        raise HTTPException(status_code=400, detail="Transaction already finished")
    
    end_time = transaction_data.end_time or datetime.utcnow()
    
    # Ensure end_time is naive for consistency
    if end_time.tzinfo is not None:
        end_time = end_time.replace(tzinfo=None)
    
    if end_time < db_transaction.start_time:
         logger.error(f"Invalid transaction finish: End time {end_time} before start time {db_transaction.start_time}")
         raise HTTPException(status_code=400, detail="End time cannot be before start time")

    interval = (end_time - db_transaction.start_time).total_seconds()
    
    hours, remainder = divmod(interval, 3600)
    minutes, seconds = divmod(remainder, 60)
    interval_formatted = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    db_transaction.end_time = end_time
    db_transaction.interval_seconds = interval
    db_transaction.interval_formatted = interval_formatted
    
    db.commit()
    db.refresh(db_transaction)
    
    logger.info(f"Transaction {transaction_id} finished. Duration: {interval_formatted}")
    return db_transaction

@router.get("/search", response_model=List[schemas.TransactionOut])
def search_transactions(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    device_id: Optional[str] = None,
    transaction_id: Optional[uuid.UUID] = None,
    limit: int = 10,
    offset: int = 0,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Transaction)

    if transaction_id:
        query = query.filter(models.Transaction.transaction_id == transaction_id)
    
    if device_id:
        query = query.filter(models.Transaction.device_id == device_id)
        
    if start_date:
        query = query.filter(models.Transaction.start_time >= start_date)
        
    if end_date:
        query = query.filter(models.Transaction.start_time <= end_date)

    transactions = query.order_by(desc(models.Transaction.start_time)).offset(offset).limit(limit).all()
    return transactions
