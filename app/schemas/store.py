from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Store(BaseModel):
    id:int
    user_id:int
    store_name:str
    store_profile:Optional[str] = None
    create_at:datetime
    class Config:
        orm_mode = True

class CreateStore(BaseModel):
    store_name:str
    store_profile:Optional[str] =None
    class Config:
        orm_mode = True
