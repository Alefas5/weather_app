from dotenv import load_dotenv
import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# Load environment variables from the .env file
load_dotenv()

# Secret key for signing JWTs
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

# Algorithm used for signing JWTs
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Schema that retrieves the token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to create a JWT token
def create_access_token(data: dict):
    to_encode = data.copy()         # Make a copy of the data to encode
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  
    return encoded_jwt

# Function to verify a JWT token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
