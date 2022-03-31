from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas import Vote, VoteResponse
from app.database import get_db
from app.models import Post, User, Votes
from app import models
from . import auth
from typing import Optional, List


router = APIRouter(tags=['Vote'])

@router.post("/vote", status_code=201)
def vote(vote: Vote, db: Session = Depends(get_db), get_current_user: int = Depends(auth.get_current_user)): #Vote here is the Pydantic
    
    post = db.query(Votes).filter(Post.id == Votes.post_id).first()
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
    
    

@router.get("/vote_result", response_model = List[VoteResponse]) #List ensure the retiurn of response in List format
def get_votes(db: Session = Depends(get_db), search: Optional[str] = " " , limit: int = 10, skip: int = 0): #0 means not skipping any by default
    results = db.query(models.Post, 
                       func.count(models.Votes.post_id).label("votes")).join(
                           models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
                               models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results