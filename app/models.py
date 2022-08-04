from datetime import timezone
from enum import unique
from itertools import product
from sqlalchemy.orm import relationship
from xmlrpc.client import Boolean
from sqlalchemy import TIMESTAMP, ForeignKey, Integer,String, Column, Boolean, text
from .database import Base
from sqlalchemy.sql.expression import null 

class Post(Base):
    __tablename__ = "socialmedia"

    id = Column(Integer, primary_key= True, nullable = False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default= 'TRUE', nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), server_default= text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable=False)   #creating foreing key in sqlalchemy
    owner = relationship("Users")  #to make relations with Users class.



class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key= True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone= True), server_default= text('now()'), nullable=False)
    phone_no = Column(String)

class Vote(Base):
    __tablename__ = "votes"
    user_id  = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("socialmedia.id", ondelete="CASCADE"), primary_key= True)

   
