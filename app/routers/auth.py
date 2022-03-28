from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.schemas import UserLogin, TokenData, Token
from app import models
from app.utils import verify
from jose import JWTError, jwt
from datetime import datetime,timedelta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') #points to the login url


router = APIRouter(tags = ['Authentication'])

#TOKEN CREATION
#SECRET_KEY, #ALGORITHM, #EXPIRATION TIME

SECRET_KEY = "myproblemisthatitoosabi,andyouwahalaisthatyounosabi.thankyoutoburnaboy"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 120

def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp":expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt #The Token returned

def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exceptions
        token_data = TokenData(id = id)
        
    except JWTError:
        raise credentials_exceptions
    
    return token_data

@router.post('/login' )#response_model=Token
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #OAuth2PasswordRequestForm = Depends() user input is expected in form-data not JSON
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = create_access_token(data = {"user_id" : user.id, "username" : user.username})
    return {"token": access_token, "token_type":"bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={"Authorization":"Bearer"})
    
    return verify_access_token(token, credentials_exceptions)