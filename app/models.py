from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.db import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    hashed_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)