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
from typing import Optional

app = FastAPI()
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "b6033f6c2ecf769b8f9dc310302c6f3401e82e657cab28759b34937c469f98e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user_db = login.get_users()
    user = get_user(user_db, username)
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
    user_db = login.get_users()
    user = get_user(user_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.DISABLED:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.USERNAME}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
###########################################################################################
async def get_user_info(user: User):
    return {"username": user.USERNAME, "tier": user.TIER, "hashed_password": user.HASHED_PASSWORD}

async def get_user_password(user: User):
            return {"username": user.USERNAME, "hashed_password": user.HASHED_PASSWORD}

###########################################################################################
#API for Creating a new user
@app.post("/create_user/")
async def create_user(user: User):
    #Check if the user already exists
    check_user = login.check_user_exists(user.USERNAME)
    if check_user == True:
        return {"status":"User already exists"}
    else:
        login.create_user(full_name = user.FULL_NAME, username = user.USERNAME, hashed_password = user.HASHED_PASSWORD, tier = user.TIER)
        return {"status":"User created successfully"}

# #API for updating a user
# @app.post("/update_user/")
# async def update_user(user: User):
#     #Field to be updated

#API for Deleting a user
@app.post("/delete_user/")
async def delete_user(user: User):
    #Check if the user exists
    if login.check_user_exists(user):
        return login.delete_user(user)
    else:
        return {"status":"User does not exists"}

#API for Updating a user
@app.post("/update_user/")
async def update_user(old_password: str, new_password: str,current_user: User = Depends(get_current_active_user)):
    user_details = await get_user_info(current_user)
    new_password_hash = pwd_context.hash(new_password)
    if new_password == old_password:
        return {"status":False, "response": "New password and old password can't be same"}
    else:
        if verify_password(old_password, user_details["hashed_password"]):
            response = login.update_user_password(new_password_hash,current_user.USERNAME)
            if response:
                return {"status":True, "response": "Password updated successfully"}    
        else:
                return {"status":False, "response": "Old password doesn't match"}

#API for getting the list of users
@app.get("/get_users/")
async def get_users(current_user: User = Depends(get_current_active_user)):
    return login.get_users()


#API to get the filtered hours 
@app.get("/get_hours_goes/{year}/{month}/{day}")
async def get_hours_goes_api(year, month, day, current_user: User = Depends(get_current_active_user)):
    return {"hours":gm.get_hours(year, month, day)}


#API to get the list of files GOES  
@app.get("/get_files_goes/{year}/{month}/{day}/{hour}")
async def get_files_goes_api(year, month, day, hour, current_user: User = Depends(get_current_active_user)):
    if current_user.DISABLED:
        raise HTTPException(status_code=400, detail="Inactive user")
    user_details = await get_user_info(current_user)
    try:
        response = login.count_api_calls(user_details['username'], user_details['tier'])
        if response == True:
            login.add_api_call(user_details['username'], user_details['tier'])
            return {"list_of_files":gm.get_files_goes(year, month, day, hour)}
        else:
            raise HTTPException(status_code=429, detail="API limit exceeded")
    except Exception as e:
        return e

# #POST API to copy files to s3   
@app.post("/copy_to_s3/") 
async def copy_to_s3_goes(src_file_key, src_bucket_name, dst_bucket_name, dataset, current_user: User = Depends(get_current_active_user)):
    urls = helper.copy_to_s3(src_file_key, src_bucket_name, dst_bucket_name, dataset)
    return {"url": urls}


@app.get("/map_visualization/{station}")
async def plot_map_viz(station, current_user: User = Depends(get_current_active_user)):
    name, lat, lon = helper.map_viz(station)
    return {"name": name, "lat": lat, "lon": lon}

@app.get("/get_stations/{year}/{month}/{day}")
async def get_stations_api(year, month, day, current_user: User = Depends(get_current_active_user)):
    return {"stations" : nm.get_stations(year, month, day)}
        

@app.get("/get_files_noaa/{station}/{year}/{month}/{day}/{hour}")
async def get_files_noaa_api(station, year, month, day, hour, current_user: User = Depends(get_current_active_user)):
    return {"list of files": nm.get_files_noaa(station, year, month, day, hour)}

    
@app.get("/get_url_nexrad_original/{filename}")
async def get_url_nexrad_original(filename, current_user: User = Depends(get_current_active_user)):
    return {"original url": nm.get_url_nexrad_original(filename)}


@app.get("/get_url_goes_original/{filename}")
async def get_url_goes_original(filename, current_user: User = Depends(get_current_active_user)):
    return {"original url": gm.get_url_goes_original(filename)}










    




 






    



