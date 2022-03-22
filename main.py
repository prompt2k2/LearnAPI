from re import I
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str  # expected input type
    content: str
    published: bool = True
    rating: Optional[int] = None


post_db = [{"title": "Post", "content": "Aye o pe meji", "id": 3}, {
    "title": "About food", "content": "I love Egusi soup", "id": 6}]


def load_post_id(id):
    for p in post_db:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(post_db):
        if p['id'] == id:
            return i  # returns the index of the post


@app.get("/")
async def read_root():
    return {"Hello James, Welcome to the Games of Throne"}


@app.get("/posts")
def get_posts():
    return {"data": post_db}


# creates an entry to the post_db array
@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):  # receive post content
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000000)
    post_db.append(post_dict)
    # post_db.append(post.dict())
    return {"result": post_dict}


@app.get("/posts/{id}")
def get_single(id: int, response: Response):  # converts the id to interger type
    single_post = load_post_id(id)
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            message="Item with id {id} not found")
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
