from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from helper_functions import goes_module as gm
from helper_functions import helper
from helper_functions import login
from helper_functions import noes_module as nm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import snowflake.connector
from snowflake.connector import DictCursor, ProgrammingError
from fastapi.requests import Request

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str 


class User(BaseModel):
    USERNAME: str
    FULL_NAME: str 
    TIER:str
    HASHED_PASSWORD:str
    DISABLED: bool 

class UserInDB(User):
    HASHED_PASSWORD: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

# print(pwd_context.hash("dummy"))

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.HASHED_PASSWORD):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(user_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.DISABLED:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def test_authenticate_user():
    # Test with valid credentials
    user = authenticate_user(fake_db, "johndoe", "password123")
    assert user is not False

    # Test with invalid credentials
    user = authenticate_user(fake_db, "johndoe", "wrongpassword")
    assert user is False
