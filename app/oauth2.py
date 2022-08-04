from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models, database
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .config import setting   #from config.py file


oath2_scheme = OAuth2PasswordBearer(tokenUrl= '/login')


SECRET_KEY = setting.secret_key  # look at the config.py for detailed expressions.
ALGORITHM =setting.algorithm                #TAKEN FROM oauth documentation.
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes    #in minutes




def create_user_login(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

         id  : str = payload.get('user_id')
         if id is None:
             raise credentials_exception
         token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data 
    
def get_current_user(token : str = Depends(oath2_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail=f'could not validate', headers= {'WWW-AUTHENTICATE': "Bearer"}) 
    token = verify_access_token(token, credentials_exception) 
    user  = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user