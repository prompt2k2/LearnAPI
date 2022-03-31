from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" #"postgresql://user:password@ip-address/hostname/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        


# # to connect to actual DB install psycopg2 first
# while True:  # checks if connection is successful
#     try:
#         conn = psycopg2.connect("dbname=postgres user=postgres password=admin")
#         cursor = conn.cursor()
#         print("######################################")
#         print("#   Database Connection Successful   #")
#         print("######################################")
#         break  # break the while. continues program is connection is successful else retries connection

#     except Exception as error:
#         print("######################################")
#         print("#    Connection to Database failed   #")
#         print("######################################")
#         print("Error: ", error)
#         print("######################################")

#         print("trying again...")
#         time.sleep(5)  # retry connection after 5 seconds
