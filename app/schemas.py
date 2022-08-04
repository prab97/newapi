
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional 



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
      pass



class Users(BaseModel):
    email  : EmailStr
    password : str
    class Config:
        orm_mode=True

class UsersResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UsersResponse   #pydantic model has been used to give characters of UserResponse class
    class Config:
       orm_mode = True


class createLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id : int
    dir: conint(le=1)
