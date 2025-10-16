import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_id = Column(String, index=True)
    query_text = Column(String)
    query_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    response_text = Column(String)
    response_timestamp = Column(DateTime)
    source_references = Column(String) # Storing as JSON string
