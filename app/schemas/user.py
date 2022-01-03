from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime

class User(BaseModel):
    email:EmailStr
    password:str

class User_Created(BaseModel):
    email:EmailStr
    profile:Optional[str]
    created_at:datetime
    class Config:
        orm_mode = True

class User_profile(BaseModel):
    profile:str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id:Optional[str] = None

class Token(BaseModel):
    access_token:str
    token_type:str
    