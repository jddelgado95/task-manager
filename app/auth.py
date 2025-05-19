#set token expiration times.
from datetime import datetime, timedelta
#jwt is used to encode/decode JWT tokens.
#JWTError helps catch token-related exceptions
from jose import JWTError, jwt
#Depends is for dependency injection.
#HTTPException is for raising custom error responses.
#status provides readable HTTP status codes.
from fastapi import Depends, HTTPException, status
#Provides a token-based dependency to extract the Authorization: Bearer <token> from requests.
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import database, crud, utils, schemas
import os

#These define how the JWT token will be signed, which algorithm to use, and how long it will last
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
#Token extractor: 
#his creates a dependency that expects the client to send a token in the Authorization header.It’s used to automatically pull tokens from requests for protected routes.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

#Token generator: 
def create_access_token(data: dict):
    #Starts by copying the user's info (data)
    to_encode = data.copy()
    #Sets the expiry time by adding x minutes to the current time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #Adds the expiry to the payload, which will be encoded in the toke
    to_encode.update({"exp": expire})
    #Returns the final JWT token, signed with your secret key
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#User authenticator
#This function checks if a user exists and the password is correct
def authenticate_user(username: str, password: str, db: Session = Depends(database.get_db)):
    #Tries to fetch the user from the DB
    user = crud.get_user_by_username(username, db)
    #Returns error if the user doesn’t exist or the password is wrong
    if not user or not utils.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    #If valid, generates a JWT token with sub (subject) set to username
    access_token = create_access_token(data={"sub": user.username})
    #Returns the token to the client
    return {"access_token": access_token, "token_type": "bearer"}

#Token verifier
#This function is used by protected routes to extract and verify the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        ##Decodes the token using your secret key and algorithm.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #Extracts username from the token’s sub claim. If missing, it’s invalid.
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    #If decoding fails (expired or tampered), return an error.
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user_by_username(username, db)
    #Makes sure the user still exists in the DB.
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    #Returns the authenticated user object to the protected route
    return user