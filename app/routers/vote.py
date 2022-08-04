from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2, database

router = APIRouter(
    prefix = "/vote",
    tags = ['Votes']
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def get_votes(votes: schemas.Vote, db : Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user) ):
    vote_check = db.query(models.Post).filter(models.Post.id == votes.post_id).first()
    if not vote_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {votes.post_id} does not exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == votes.post_id, models.Vote.user_id == current_user.id)
    found_votes = vote_query.first()
    if (votes.dir == 1):
        if found_votes:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'{current_user.id} has already registerd vot by {votes.post_id}')
    
        new_vote = models.Vote(post_id = votes.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully voted"}

    else: 
        if not found_votes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"Vote deleted successfully"}
