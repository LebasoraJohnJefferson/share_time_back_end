from fastapi import APIRouter,Depends,HTTPException,status
from starlette.responses import Response
from starlette.status import HTTP_403_FORBIDDEN
from ..database.con_db import get_db
from .. import models
from ..script import utils,oauth2
from ..schemas import user
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(tags=['users'],prefix='/users')

@router.get("/",response_model=List[user.User_Created])
def get_user(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/",status_code=status.HTTP_201_CREATED)
def register_user(payload:user.User,db:Session = Depends(get_db)):
    isUserExist = db.query(models.User).filter(models.User.email == payload.email)
    res_user = isUserExist.first()
    password = utils.hash(payload.password)
    payload.password = password
    if (res_user != None):
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail=f'email already taken')
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)

@router.put("/")
def update_user(payload:user.User,db:Session = Depends(get_db),user_id:int= Depends(oauth2.get_current_user)):
    payload_email = db.query(models.User).filter(models.User.email == payload.email).first()
    current_user = db.query(models.User).filter(models.User.id == user_id.id)
    user_auth = current_user.first()
    hash_pass = utils.hash(payload.password)
    payload.password = hash_pass
    #check if email not exist
    if(payload_email != None):
        #if already exist check if the email belong to owner
        if(payload_email.email != user_auth.email):
            raise HTTPException(status_code=HTTP_403_FORBIDDEN,detail=f'email {payload.email} already in used')
    if user_auth == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    current_user.update(payload.dict(),synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)
    




