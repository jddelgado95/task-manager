#Imports CryptContext from the passlib library.
#CryptContext lets you configure how passwords are hashed and verified — it abstracts away hashing algorithms like bcrypt, argon2, etc.
from passlib.context import CryptContext

#Password Hasher Configuration
#Creates a password hashing context using the bcrypt algorithm.
#"bcrypt" is a secure and well-tested algorithm ideal for storing passwords.
#"deprecated='auto'" ensures old algorithms (if used) can be flagged or migrated automatically.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Securely Hashes Plain Text Passwords
#Takes a plain-text password (e.g., from registration).
#Returns a hashed version of that password.
#This is what you store in the database — never store raw passwords!
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#Compares Raw Input to Hashed Password
#plain_password → input from login form
#hashed_password → stored hash from the database
#Verifies if the input matches the hash.
#Returns True if they match, False otherwise.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)