from fastapi import FastAPI, Response, status, Depends, HTTPException, APIRouter
from app.schemas import User, UserResponse
from app.utils import hasher
from app import models
from app.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['Users'])

@router.post("/createuser", status_code=201, response_model = UserResponse)
def create_user(c_user: User, db: Session = Depends(get_db)):  # receive post content from the defined BaseModel
    
    #hash the password
    hashed_password = hasher(c_user.password)
    c_user.password = hashed_password
    
    new_user = models.User(**c_user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    

@router.get("/user/{id}", response_model = UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):  # converts the id to interger type
    user = db.query(models.User).get(id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail =f"User with id: {id} not found o")
    return user
    