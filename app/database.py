#Imports create_engine from SQLAlchemy.
#create_engine() is used to initialize the connection to your database.
#Think of it as the "dialer" that connects your Python app to the database

#An ORM (Object-Relational Mapping) is a programming technique that allows you to interact with a relational database (like PostgreSQL, MySQL, SQLite) using the objects and classes of your programming language—instead of writing raw SQL queries. It maps database tables to Python classes and rows to instances of those classes.

#Without ORM: SELECT * FROM users WHERE id = 1;
#With ORM (e.g., SQLAlchemy or Django ORM in Python): user = session.query(User).get(1)

#sessionmaker: a factory function that creates new database sessions (used to interact with the DB).
#declarative_base: a base class from which all your ORM models will inherit. It keeps track of tables and classes for SQLAlchemy.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
#os lets you access environment variables.
#load_dotenv() loads the .env file so environment variables like DATABASE_URL can be used
import os
from dotenv import load_dotenv

#Loads variables from .env into your environment so os.getenv("DATABASE_URL") will work
load_dotenv()
# This defines the database connection URL.
#"sqlite:///.tasks.db" means:Use SQLite. and ./tasks.db is the local file where the DB is stored.
#If it were PostgreSQL, it might look like: "postgresql://user:password@localhost/dbname"
#set the DB variable as an environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///.tasks.db")
#use this without docker
#SQLALCHEMY_DATABASE_URL = "sqlite:///.tasks.db"

#Gets the PostgreSQL connection string from the .env file.
#Use with docker: 
#todo: add logic to run pytest with docker
#SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

#Creates a SQLAlchemy engine instance using the DB URL.
#connect_args={"check_same_thread": False} is specific to SQLite:It disables SQLite's "single-thread rule" (SQLite is usually restricted to one thread).This is needed when using the database in web frameworks like FastAPI, which uses multiple threads.
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

#Establishes the connection to the database.
#The engine is the low-level component that talks to the DB.
#Use with docker: 
#engine = create_engine(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Creates a local session factory. Every time you need a DB session, you'll call SessionLocal().
#Parameters:
#autocommit=False: You must explicitly commit transactions.
#autoflush=False: SQLAlchemy won’t automatically flush changes to the DB until you commit.
#bind=engine: Binds this session factory to the engine created above.

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

#Creates a base class Base that all your ORM models will inherit from. It tells SQLAlchemy: "Any class that inherits from me is a table in the database."
Base = declarative_base()

#This function is a FastAPI dependency (used with Depends(get_db)).
#It:
#Creates a DB session.
#yields it to the route handler or function that needs it.
#Closes the session afterward — avoids DB leaks or uncommitted connections.
#The try/finally ensures the database session is always closed — even if there's an error or exception.
#Prevents connection leaks that can happen if you forget to close the session manually.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()