from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Post(Base):
    ___tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)