from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto",bcrypt__truncate_error=False)

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password,hashed_passeword):
    return pwd_context.verify(plain_password,hashed_passeword)