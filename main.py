from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello James, Welcome to the Games of Throne"}


@app.get("/posts")
def get_posts():
    return {"data:" "These are your posts"}


@app.post("/createpost")
def create_posts(payload: dict = Body(...)):  # receive post content
    print(payload)
    return {"New Entry": f"title {payload['title']} content: {payload['content']}"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
