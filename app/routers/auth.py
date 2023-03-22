from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
#88888888888888888888888888888888888888888888888888888888888888888888888888888888 Nebuvo from
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #if hashes do not match
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create token
    #return token

    #data we want to put in payload (dictionary), where providing only user_id, it was just decided like that, can be passed other parameters, like user role etc.
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return{"access_token": access_token, "token_type": "bearer"}