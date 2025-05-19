#Import FastAPI class to create the web API app.
#Depends is used for dependency injection — automatically providing required dependencies (like database sessions) to path operations.
#HTTPException lets you raise HTTP errors with custom status codes and messages.

from fastapi import FastAPI, Depends, HTTPException

#Import the SQLAlchemy Session class, which is used to interact with the database.
from sqlalchemy.orm import Session
#Import my own app modules:
# ->models contains your SQLAlchemy ORM models (DB tables).
# ->schemas contains your Pydantic models (data validation/serialization).
# ->crud contains functions that handle DB operations (Create, Read, Update, Delete).
from . import models, schemas, crud, auth
#SessionLocal is a SQLAlchemy session factory to create DB sessions.
#engine is the SQLAlchemy engine connected to your database.
#Base is the base class for your ORM models.
from .database import SessionLocal, engine, Base
from .schemas import UserCreate, User
#Creates all tables in the database that are defined by my ORM models if they don’t exist yet.
#Uses the engine (DB connection) to execute this.
Base.metadata.create_all(bind=engine)

#Creates a FastAPI application instance called app.
#This object will be used to define API routes.
app = FastAPI()

# Dependency to get DB session
#Creates a new DB session with SessionLocal().
#yields the session to the caller (e.g., an API route).
#Ensures the DB session is closed after the request is done, no matter what (with finally).
#This pattern helps manage DB connections cleanly and efficiently per request.

#Using yield in this context allows FastAPI to:
#Inject the dependency: FastAPI can provide the database session to path operations and other dependencies.
#Handle cleanup: After the request is completed, FastAPI ensures that the code following the yield statement is executed, which is essential for closing the database session.
#This pattern is particularly useful for managing resources that need to be cleaned up after use, such as database connections.
def get_db():
    #This creates a new SQLAlchemy session. It's configured in database.py.
    db = SessionLocal()
    try:
        #Instead of returning the session, we yield it. This allows FastAPI to handle the session as a dependency, ensuring that the code after the yield runs after the request is completed
        yield db
    #This ensures that the database session is properly closed after the request is handled, preventing potential database connection leaks    
    finally:
        db.close()

#Defines a POST API endpoint at /tasks/.
#Expects a request body of type schemas.TaskCreate (a Pydantic model validating input).
@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    #Automatically gets a DB session injected via Depends(get_db).
    #Calls the crud.create_task function passing DB session and task data.
    #Returns the created task serialized by schemas.TaskResponse.
    return crud.create_task(db, task)

#Defines a GET API endpoint at /tasks/ to fetch all tasks.
@app.get("/tasks/", response_model=list[schemas.TaskResponse])
#Injects a DB session.
#Calls crud.get_tasks to query all tasks from DB.
#Returns a list of tasks, serialized with schemas.TaskResponse.
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

#Defines a GET endpoint at /tasks/{task_id} where task_id is a path parameter.
@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    #Gets a single task by its ID.
    #If task not found, raises a 404 HTTP error with a message.
    #Otherwise, returns the task serialized as TaskResponse.
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

#Defines a PUT endpoint at /tasks/{task_id} to update an existing task.
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
#Receives the task ID in the URL, the new task data in the request body, and the DB session.
#Calls the crud.update_task function to perform the update.
#Returns the updated task serialized.
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task(db, task_id, task)

#Defines a DELETE endpoint at /tasks/{task_id}.
#Deletes the task with the given ID from the database.
#Returns the deleted task (or nothing) as confirmation.
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_task(db, task_id)

#User Registration Endpoint
#@app.post("/register") → This defines a POST route at /register.
#response_model=User → The response returned will be validated & shaped like the User schema (without password).
#user: UserCreate → FastAPI expects a JSON body with username and password (validated using the UserCreate schema).
#crud.create_user(user) → Calls your DB logic to hash the password and store the new user in the database.
@app.post("/register", response_model=User)
def register(user: UserCreate):
    return crud.create_user(user)

# Login Endpoint (JWT)
#POST request to /login.
#Expects a JSON body with username and password.
#Calls auth.authenticate_user() to:
#Fetch the user from the database.
#Verify the password using bcrypt.
#If valid, return a JWT access token like:
#{
#  "access_token": "eyJhbGciOi...",
#  "token_type": "bearer"
#}
@app.post("/login")
def login(user: UserCreate):
    return auth.authenticate_user(user.username, user.password)

#Protected Route (JWT Required)
#GET request to /protected.
#Requires a valid JWT token in the Authorization header:
#Authorization: Bearer <token>
#Depends(auth.get_current_user):
#Decodes the token.
#Fetches the user from the DB.
#Raises 401 if invalid.
#If token is valid, it returns a greeting with the current username.
@app.get("/protected")
def protected(current_user: User = Depends(auth.get_current_user)):
    return {"message": f"Hello, {current_user.username}"}