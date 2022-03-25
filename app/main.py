from multiprocessing import synchronize
from fastapi import FastAPI, Response, status, Depends, HTTPException
from fastapi.params import Body
from .schemas import Post, PostResponse, User, UserResponse
from typing import Optional, List
from random import randrange
import psycopg2
from .utils import hasher
import time
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def read_root():
    return {"Hello James, Welcome to the Games of Throne"}




    
    