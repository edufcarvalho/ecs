import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from datetime import datetime

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())

    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    credit_limits = relationship("CreditLimit", back_populates="user", order_by="CreditLimit.updated_at")
    emotional_data = relationship("EmotionalData", uselist=False, back_populates="user")

    @property
    def credit_limit(self):
        if self.credit_limits:
            return self.credit_limits[-1]
        return None

# Transaction Model
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.now())

    # Relationship back to User
    user = relationship("User", back_populates="transactions")

# Credit Limit Model
class CreditLimit(Base):
    __tablename__ = 'credit_limits'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    credit_limit = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.now())

    # Relationship back to User
    user = relationship("User", back_populates="credit_limits")

# Emotional Data Model
class EmotionalData(Base):
    __tablename__ = 'emotional_data'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    emotion = Column(String, nullable=False)
    thought = Column(String, nullable=False)

    # Relationship back to User
    user = relationship("User", back_populates="emotional_data")