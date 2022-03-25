from pydantic import BaseModel, EmailStr
from datetime import datetime


#This is the pydantic model:defines the structure of a request & response
#ensures that a created or updated post has this (required) fields
class Post(BaseModel):
    title: str  # expected input type
    content: str
    published: bool
    owner: str
    

class PostResponse(Post): #Manages the response sent as output
    id: int
    class Config:
        orm_mode = True
        

class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str
    
