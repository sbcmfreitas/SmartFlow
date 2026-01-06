import uuid
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.types import TypeDecorator, CHAR
from app.database import Base
from datetime import datetime

# GUID handling for SQLite compatibility
class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            from sqlalchemy.dialects.postgresql import UUID
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    # Storing hashed password
    hashed_password = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"

    # We use GUID as requested
    transaction_id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    device_id = Column(String, index=True)
    entity_id = Column(String, index=True)
    user_id = Column(Integer, nullable=True) # Optional link to user who initiated if applicable, or device
    
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    
    interval_seconds = Column(Float, nullable=True)
    interval_formatted = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
