
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from .. database import  get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database
from typing import  List, Optional
import psycopg2


router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)



@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # Creating a post
    #cursor.execute("""INSERT INTO social_media (title, content, published) VALUES(%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
   # new_posts = cursor.fetchone()
   # conn.commit()
   # print('done')
  # new_posts = models.Post(title=post.title, content=post.content, published=post.published)
   print(current_user.email)
   new_posts =models.Post(owner_id = current_user.id, **post.dict()) # to unpack post data into dictionary format.
   db.add(new_posts)
   db.commit() 
   db.refresh(new_posts)
   return  new_posts

'''@router.get('/posts/latest')
def latest_post():
    post = my_list[len(my_list)-1]
    return  post'''


@router.get("/", response_model=List[schemas.Post])
def get_post_all(db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    print(limit)                              #offest is used to skip the results mentioned by the user.

    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  #limt the result to user response. used in pagination.
    #posts = db.query(models.Post).all()   
    #title.contains(search) - to search about the items
    results = db.query(models.Post, func.count(models.Vote.post_id)).label("votes").join(models.Vote, models.Vote,post_id == models.Post.id, isouter= True).group_by(models.Post.id).all()
    print(results)

    
   # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    #if not posts:
      #  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=' not found.')
    
    return posts
    


@router.get("/{id}", response_model = schemas.Post) 
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # reading a post.
    #cursor.execute(""" SELECT * FROM social_media WHERE id = %s """, (str(id)))
    #post = cursor.fetchone() 
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail = f'{id} is not found.')
       # response.status_code = status.HTTP_404_NOT_FOUND
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requested action cannot be performed.")
    return posts

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute("""DELETE FROM social_media WHERE id = %s RETURNING *""", (str(id),))
   # deleted_post = cursor.fetchone()
   # conn.commit()
   post_query = db.query(models.Post).filter(models.Post.id == id) 
   posts = post_query.first()
   
   if posts == None:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'{id} not found.')
   
   if posts.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requested action cannot be performed.")

   posts.delete(synchronize_session = False)
   db.commit()
   return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE social_media SET title = %s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published, str(id)))
   # updated_post = cursor.fetchone()
   # conn.commit()
   
   query_update = db.query(models.Post).filter(models.Post.id == id)
   posts = query_update.first()
   
   if posts == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'{id} not found.')
    
  # query_update.update({'title': 'Rihanna', 'content': 'This is the greatest'} , synchronize_session=False)
   if posts.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requested action cannot be performed.")
   db.commit()
   return query_update.first()
