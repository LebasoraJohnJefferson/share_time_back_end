from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database.con_db import get_db
from .. import models
from ..script import oauth2,utils
from ..schemas import user


router = APIRouter(tags=['authentication'])

@router.post("/login",response_model=user.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    #check if user exist if not then raise the exception
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='INVALID CREDENTIALS')
    #check if password is same in hast password from database if not then raise the exception
    if not utils.verifying(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='INVALID CREDENTIALS')
    #if all data is validated, create token
    access_token = oauth2.create_access_token(data = {'user_id':user.id})
    return {"access_token":access_token, "token_type":"bearer"}


