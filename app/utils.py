#passwordu hashinimi po instaliavimo pip install passlib[bcrypt]
from passlib.context import CryptContext
#Telling passlib what is the hashing algorythm (we want to use bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

#comparing provided pas with hashed pass in database (hashing provided pass)
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)