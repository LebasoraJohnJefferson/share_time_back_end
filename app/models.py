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
    created_at  = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))
