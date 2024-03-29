from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str 
    database_password: str 
    database_name: str
    #database_name2: str
    secret_key: str
    algorithm: str
    ACCESS_TOKEN_EXPIRE_MINUTE: int
    
    class Config:
        env_file = ".env"
    
settings = Settings()