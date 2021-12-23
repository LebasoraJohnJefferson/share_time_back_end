from fastapi import APIRouter
from sqlalchemy import schema
from sqlalchemy.orm.session import Session
from ..database.con_db import get_db
from typing import List
from fastapi import HTTPException,status,Depends
from .. import models
from ..schemas import store
from ..script import oauth2


router = APIRouter(tags=['stores'],prefix='/stores')

@router.get('/',response_model=List[store.Store])
def get_all_store(db:Session = Depends(get_db),limit:int=5,skip:int=1):
    stores = db.query(models.Store).offset(skip).limit(limit).all()
    return stores

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=store.CreateStore)
def create_store(payload:store.CreateStore,db:Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    isUserHadStore = db.query(models.Store).filter(models.Store.user_id == user_id.id).first()
    if isUserHadStore != None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Already have Store')
    payload_update = payload.dict()
    payload_update.update({"user_id":user_id.id})
    new_store = models.Store(**payload_update)
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    print(payload_update)
    return  new_store

