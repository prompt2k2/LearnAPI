from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor


app = FastAPI()


class Post(BaseModel):
    title: str  # expected input type
    content: str
    published: bool = True


# to connect to actual DB install psycopg2 first
while True:  # checks if connection is successful
    try:
        conn = psycopg2.connect("dbname=FastAPI user=admin password=admin")
        cursor = conn.cursor()
        print("######################################")
        print("#   Database Connection Successful    #")
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


post_db = [{"title": "Post", "content": "Aye o pe meji", "id": 3}, {
    "title": "About food", "content": "I love Egusi soup", "id": 6}]


def load_post_id(id):
    for p in cursor:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(cursor):
        if p['id'] == id:
            return i  # returns the index of the post


@app.get("/")
async def read_root():
    return {"Hello James, Welcome to the Games of Throne"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM public."Post" """)
    posts = cursor.fetchall()
    return {"data": posts}


# creates an entry to the post_db array
@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_posts(po: Post):  # receive post content
    cursor.execute("""INSERT INTO public."Post" (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (po.title, po.content, po.published))

    new_post = cursor.fetchall()

    conn.commit()  # save to Database

    return {"result": new_post}


@app.get("/posts/{id}")
def get_single(id: int):  # converts the id to interger type
    cursor.execute(
        """SELECT * from public."Post" WHERE id = %s """, (str(id), ))
    single_post = cursor.fetchone()

    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Item with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"Item with id {id} not found"}
    return{"data_detail": single_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}")

    post_db.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):  # makes sure the update follows the POST schema
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            message=f"No post with id {id}")

    post_dict = post.dict()
    post_dict['id'] = id
    post_db[index] = post_dict

    return {"data": post_dict}
