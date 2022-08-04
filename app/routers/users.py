
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. database import  get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils

router = APIRouter(
    prefix = "/user",
    tags = ["Users"]
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.UsersResponse)
def createruser(new_user: schemas.Users, db: Session = Depends(get_db)):
   hashed = utils.hashed(new_user.password)
   new_user.password = hashed
   new_posts =models.Users(**new_user.dict()) # to unpack post data into dictionary format.
   db.add(new_posts)
   db.commit() 
   db.refresh(new_posts)
   return  new_posts

@router.get("/{id}" ,response_model= schemas.UsersResponse)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'id: {id} does not exist')
    
    return user