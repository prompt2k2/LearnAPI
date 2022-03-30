from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


#This is the pydantic model:defines the structure of a request & response
#ensures that a created or updated post has this (required) fields
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
    

class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[int] = None

class Post(BaseModel):
    title: str  # expected input type
    content: str
    published: bool
    
    

class PostResponse(Post): #Manages the response sent as output
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        orm_mode = True
        

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #Direction to show if liking on unliking/ le means less than or equal to
    