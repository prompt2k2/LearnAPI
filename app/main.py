from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor


app = FastAPI()


class Products(BaseModel):
    title: str  # expected input type
    content: str
    published: bool = True


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
    cursor.execute("""SELECT * FROM public."Products" """)
    product = cursor.fetchall()
    return {"data": product}


# creates an entry to the post_db array
@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_posts(po: Products):  # receive post content from the defined BaseModel
    cursor.execute("""INSERT INTO public."Products" (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (po.title, po.content, po.published))

    new_product = cursor.fetchall()
    conn.commit()  # save to Database
    return {"result": new_product}


@app.get("/posts/{id}")
def get_single(id: int):  # converts the id to interger type
    cursor.execute(
        """SELECT * from public."Products" WHERE id = %s """, (str(id), ))
    product = cursor.fetchone()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail =f"Item with id: {id} not found o")
    return{"data_detail": product}


@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM public."Products" WHERE id = %s RETURNING * """, (str(id), ))
    deleted_product = cursor.fetchall()
    conn.commit()

    if deleted_product == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Products):  # makes sure the update follows the POST schema
    cursor.execute("""UPDATE public."Products" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id),))
    updated_product = cursor.fetchone()
    conn.commit()

    if updated_product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not product with that Id, {id}")
        #                     

    return {"data": updated_product}
