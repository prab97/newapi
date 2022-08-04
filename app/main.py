

from typing import  List
from fastapi import FastAPI, Depends
from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, users, auth, vote
from .config import setting
from fastapi.middleware.cors import CORSMiddleware



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome "}



'''my_list = [ {'title': 'funny guy', 
             'content' : 'This is title1',
             'id' : 1
            },
            {
                'title': 'Absolut',
                'content': 'This is title 2',
                'id': 2
            }

]'''



'''@app.get("/testing")
def test_db(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {'data': posts}'''
 
'''
@app.get("/posts", response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    #cursor.execute("""SELECT * FROM social_media""") # selecting from table in the DB
    #posts = cursor.fetchall() # to fetch all row
    return  posts  # to post through get request.

'''
'''
@app.post("/create_posts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_posts" : f"title : {payload['title']}' content : {payload['content']}"  }  '''
'''
def show_post(id): #reading post 
    for item in my_list:
        if item['id'] == id:
            return item'''



'''
def find_index(id):
    for index, items in enumerate(my_list):
        if items['id'] == id:
            return index

'''
