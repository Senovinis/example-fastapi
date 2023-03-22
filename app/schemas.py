from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

#For validation using basemodel - what kind of data front end should send

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#extending above class PostBase, which in this case inherits fields
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# #defining what will pe provided on response for users or front end
# class Post(BaseModel):
#     id: int
#     title: str
#     content: str
#     published: bool
#     created_at: datetime

#Same as above "class Post(BaseModel):", just inherited from other class
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

#Pydantic deos not know what to do with sqlalchemy model, it only knows how to work with dictionaries, 
# so we are telling to Pydantic model to read data even it is not a dictiorary, but an ORM model (or any other arbitrary model with attributes)
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)