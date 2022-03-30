from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import Vote
from app.database import get_db
from app.models import Post, User, Votes
from . import auth


router = APIRouter(tags=['Vote'])

@router.post("/vote", status_code=201)
def vote(vote: Vote, db: Session = Depends(get_db), get_current_user: int = Depends(auth.get_current_user)): #Vote here is the Pydantic
    
    post = db.query(Votes).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} not found ")
    
    vote_query = db.query(Votes).filter(Votes.post_id == vote.post_id, Votes.user_id == get_current_user.id) #checks if the same user has voted
    found_vote = vote_query.first()
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {get_current_user.id} has already voted on post {vote.post_id}")
        new_vote = Votes(post_id = vote.post_id, user_id = get_current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"message": "Voted successfully"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session = False)
        db.commit()
        
        return {"message": "Successfully undo the vote"}