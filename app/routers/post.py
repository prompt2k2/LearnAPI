from multiprocessing import synchronize
from fastapi import FastAPI, Response, status, APIRouter, Depends, HTTPException
from fastapi.params import Body
from sqlalchemy import func
from app.schemas import Post, PostResponse, VoteResponse
from typing import Optional, List
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from app import models, schemas, utils
from . import auth


router = APIRouter(tags=['Posts'])

@router.get("/posts", response_model = List[PostResponse]) #List ensure the retiurn of response in List format
def get_posts(db: Session = Depends(get_db), search: Optional[str] = " " , limit: int = 10, skip: int = 0): #0 means not skipping any by default
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #offset use to skip post (pagination)

    return posts


@router.get("/myposts", response_model = List[PostResponse]) #List ensure the retiurn of response in List format
def get_myposts(db: Session = Depends(get_db), get_current_user:int = Depends(auth.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == get_current_user.id).all()
   
    return posts

@router.post("/createpost", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: Post, db: Session = Depends(get_db), get_current_user:int = Depends(auth.get_current_user)):  # receive post content from the defined BaseModel
    #new_post = models.Post(title=post.title, content=post.content, published=post.published, owner=post.owner) replace this with models.Post(**post.dict())
    new_post = models.Post(owner_id=get_current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/posts/{id}", response_model = PostResponse)
def get_single(id: int, db: Session = Depends(get_db), get_current_user:int = Depends(auth.get_current_user)):  # converts the id to interger type
    post = db.query(models.Post).get(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail =f"Item with id: {id} not found o")
    
    if post.owner_id != get_current_user.id:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"You are not authorize for this action"
        )
    return post


@router.get("/votepost/{id}", response_model = VoteResponse)
def get_votepostsingle(id: int, db: Session = Depends(get_db), get_current_user:int = Depends(auth.get_current_user)):  # converts the id to interger type
    
    post = db.query(models.Post, 
                       func.count(models.Votes.post_id).label("votes")).join(
                           models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail =f"Item with id: {id} not found o")
        
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user:int = Depends(auth.get_current_user)):
    post = db.query(models.Post).get(id)
        
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}")
        
    if post.owner_id != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"You are not authorize for this action"
        )
    db.delete(post)    
    db.commit()

    return {"message": f"Post with id {id} successfully deleted"}


@router.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, u_post: Post, db: Session = Depends(get_db), get_current_user:int = Depends(auth.get_current_user)):  # makes sure the update follows the POST schema
    
    post_q = db.query(models.Post).filter(models.Post.id == id)
    post = post_q.first() 

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with that Id, {id}")
    
    if post.owner_id != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"You are not authorize for this action"
        )
    post_q.update(u_post.dict(), synchronize_session=False)   
    db.commit()     

    return u_post

