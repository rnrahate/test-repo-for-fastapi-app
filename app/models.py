from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.expression import text   

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True,nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(DateTime(timezone=True),
                        server_default=text('now()'), nullable=False)
    phone_number = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)

    owner = relationship("User")
    

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True,nullable=False, index=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False,unique=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=text('now()'), nullable=False)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.user_id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)

