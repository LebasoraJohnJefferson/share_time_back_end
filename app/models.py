from datetime import timezone
from sqlalchemy import Integer,Column,String,TIMESTAMP,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database.con_db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,nullable=False,primary_key=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    profile = Column(String,nullable=True)
    created_at  = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))

class Store(Base):
    __tablename__ = "store"
    id=Column(Integer,nullable=False,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'))
    store_name = Column(String,nullable=False)
    store_profile = Column(String,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)
