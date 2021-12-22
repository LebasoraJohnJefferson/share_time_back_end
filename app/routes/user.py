from fastapi import APIRouter,Depends,HTTPException,status
from starlette.responses import Response
from ..database.con_db import get_db
from .. import models
from ..script import utils
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
    password = payload.password
    payload.password = password
    if (res_user != None):
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail=f'email already taken')
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)