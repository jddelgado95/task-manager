#Import SQLAlchemy Column Types: importing data types and column constructor used to define database fields.
#Column: Used to define each field/column.
#Integer: For numeric columns.
#String: For text fields.
#Date: For storing date values.
#Boolean: For storing True/False.
from sqlalchemy import Column, Integer, String, Date, Boolean

#Import the Base Class: This Base is the base class all ORM models will inherit from so SQLAlchemy can recognize them and map them to tables.
from .database import Base
#Class will map to a database table. 
#By inheriting from Base, it tells SQLAlchemy this is a model
class Task(Base):
    #This tells SQLAlchemy the name of the actual table in the database will be "tasks"
    __tablename__ = "tasks"
    #Define Columns
    #id: A unique integer for each task (usually auto-incremented).
    # -> primary_key=True: Makes it the unique identifier for the table.
    # -> index=True: Adds an index to speed up lookups by this column.
    id = Column(Integer, primary_key=True, index=True)
    #title: A short text for the task.
    # -> index=True: Optimizes searching/filtering by title.
    title = Column(String, index=True)
    #description: A longer text field
    description = Column(String)
    #due_date: Stores a calendar date for when the task is due
    due_date = Column(Date)
    #status: Tracks whether a task is "pending" or "done".
    # -> default="pending": New tasks default to "pending" status.
    status = Column(String, default="pending")  # pending / done