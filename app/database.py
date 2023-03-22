from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#prisijungimui prie postgress duombazes ir kursoriaus valfymui (komandoms)
import psycopg
from psycopg import connect, ClientCursor
#timeoutams
import time

from .config import settings

#sqlalchemy formatas prisijungimui prie duombazes, connection string
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

# #Pries environment variables
# SQLALCHEMY_DATABASE_URL = 'postgresql://auj:Slaptazodis04@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#create engine, responsible for establishing connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for ORM, session to database, opens and closes everytime request is sent to API endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# #connecting to database using regular Postgress driver (we are no nonger using this, raw sql). Insted we are using sqlalchemy
# while True:
#     try:
#         conn = psycopg.connect(host='localhost', dbname='fastapi', user='auj', password='Slaptazodis04', cursor_factory=ClientCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(10)