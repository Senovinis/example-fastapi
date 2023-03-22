
from fastapi import FastAPI
#CORS - susisnekejimui su API tarp domenu
from fastapi.middleware.cors import CORSMiddleware
# #for providing particular post format. Title and body for example, nothing more
# from pydantic import BaseModel
# Portui keist
import uvicorn
# #ID generuot
# from random import randrange

# #For ORM to operate (additional models.py and database.py files were createdtoo)
# from sqlalchemy.orm import Session

#from . import models 111111111111111111111111111111111111111111111111111111111111111111111111111111 import models
from . import models
#from .database import engine, SessionLocal 22222222222222222222222222222222222222222222222222222222 tasko nebuvo
from .database import engine
#importing routers from new folder "routers" 3333333333333333333333333333333333333333333333333333333 tasko nebuvo
from .routers import post, user, auth, vote
# from config import settings
# 1000000000000000000000000000000000000000000000000000000000000000000000000000000000 nebuvo tasko    
from .config import settings

print(settings.database_username)



# models.Base.metadata.create_all(bind=engine)


origins = ["https://www.google.com"]

#Call FastAPI function
app = FastAPI()
#CORS susisnekejimui tarp domenu, origins nurodau domenus. Methods nurodau kokius metodus leidziu naudot - GET, PUT
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#using get method pointung to root URL in this case
@app.get("/")
#Specific path operation function - can be called root or any other name
def root():
    return {"message": "wawaweewa"}



# #variable aray containing whole bunch of posts objects. each post is dictionary. ID is needed to fetch data and update data
# my_posts = [{"title": "title of p1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "Ilike pizza", "id": 2}]

# #below 2 functions were needed before stated working with databases
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     #i - specific index, individual posts -p
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#For port change, paleidziama su: python app/main.py , bet suvaro appso paleidima velesniuose etapuose
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8001)