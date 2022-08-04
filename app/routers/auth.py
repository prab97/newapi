
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from .. import schemas, utils, models, oauth2

router = APIRouter(
     tags=["Authentication"]
)

@router.post("/login", status_code= status.HTTP_201_CREATED, response_model= schemas.Token)
#def createLogin(user_credential: schemas.createLogin , db : Session = Depends(get_db)):\
def createLogin(user_credential: OAuth2PasswordRequestForm = Depends()  , db : Session = Depends(get_db)):
    """"After Oauth2Passwrodrequestform there will be no field called email 
         but username such as  { "username" :
                                 "password": }"""
    user = db.query(models.Users).filter(models.Users.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    result = utils.verify(user_credential.password, user.password)
    if not result:
           raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Invalid credential")

    access_token = oauth2.create_user_login(data = {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
