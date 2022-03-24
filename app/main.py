from multiprocessing import synchronize
from fastapi import FastAPI, Response, status, Depends, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str  # expected input type
    content: str
    published: bool
    owner: str

# to connect to actual DB install psycopg2 first
while True:  # checks if connection is successful
    try:
        conn = psycopg2.connect("dbname=postgres user=postgres password=admin")
        cursor = conn.cursor()
        print("######################################")
        print("#   Database Connection Successful   #")
        print("######################################")
        break  # break the while. continues program is connection is successful else retries connection

    except Exception as error:
        print("######################################")
        print("#    Connection to Database failed   #")
        print("######################################")
        print("Error: ", error)
        print("######################################")

        print("trying again...")
        time.sleep(5)  # retry connection after 5 seconds


def load_post_id(id):
    for p in cursor:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(cursor):
        if p['id'] == id:
            return i  # returns the index of the post

#Testing Session with SQLALCHEMY which automatically created the table in db
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    
    post = db.query(models.Post).all()
    return {"data": post}


@app.get("/")
async def read_root():
    return {"Hello James, Welcome to the Games of Throne"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):  # receive post content from the defined BaseModel
    #new_post = models.Post(title=post.title, content=post.content, published=post.published, owner=post.owner) replace this with models.Post(**post.dict())
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"result": new_post}


@app.get("/posts/{id}")
def get_single(id: int, db: Session = Depends(get_db)):  # converts the id to interger type
    post = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail =f"Item with id: {id} not found o")
    return{"data_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)
        
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}")
    db.delete(post)    
    db.commit()

    return {"message": f"Post with id {id} successfully deleted"}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, u_post: Post, db: Session = Depends(get_db)):  # makes sure the update follows the POST schema
    
    post_q = db.query(models.Post).filter(models.Post.id == id)
    post = post_q.first() 
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with that Id, {id}")
    
    post_q.update(u_post.dict(), synchronize_session=False)   
    db.commit()     
    print(u_post)            

    return {"data": u_post}
