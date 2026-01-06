from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str

# Transaction Schemas
class TransactionBase(BaseModel):
    device_id: str
    entity_id: str
    start_time: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionFinish(BaseModel):
    end_time: Optional[datetime] = None

class TransactionOut(TransactionBase):
    transaction_id: UUID
    end_time: Optional[datetime] = None
    interval_seconds: Optional[float] = None
    interval_formatted: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TransactionFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    device_id: Optional[str] = None
    transaction_id: Optional[UUID] = None
