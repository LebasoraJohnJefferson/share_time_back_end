from fastapi import Depends,HTTPException,status
from jose import jwt,JWSError
from datetime import datetime,timedelta
from ..schemas import user
from fastapi.security import OAuth2AuthorizationCodeBearer
from ..config import setting

ouath_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='authorized',tokenUrl="login")

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt


def verify_access_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = user.TokenData(id=id)
    except JWSError:
        raise credential_exception
    return token_data

def get_current_user(token:str = Depends(ouath_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"could not validate credentials",headers={"WWW-authenticate":"Bearer"})
    return verify_access_token(token,credential_exception)