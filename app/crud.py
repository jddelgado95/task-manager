#Session: SQLAlchemy’s session object to talk to the database.
#.models: Your database models (like Task).
#.schemas: Your Pydantic schemas (like TaskCreate, TaskUpdate) used for validation.
from sqlalchemy.orm import Session
from . import models, schemas

#Return a list of all tasks.
#db.query(models.Task): Ask the DB for all Task entries.
#.all(): Convert the query into a list of actual results.
def get_tasks(db: Session):
    return db.query(models.Task).all()

# Fetch one task by ID.
#.filter(...): Add condition (where id == task_id).
#.first(): Get the first matching record (or None if not found).
#Adds a condition: "Only consider rows where the id column matches the task_id passed to the function.".
# first()→ Fetch the first (and usually only) result that matches the filter condition.
#In most databases, each record has a unique id, which serves as the primary key. So when you're trying to fetch, update, or delete a specific task, you use its id to identify it.
#If task_id = 3, this line:
#db.query(models.Task).filter(models.Task.id == 3).first()
#will fetch the task with ID 3 from the tasks table.

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

#Create a new task in the database.
#task.dict(): Converts the Pydantic object into a dictionary.
#Why do we do this conversion?
#Pydantic models are not plain dicts:
#They are special classes with extra validation, parsing, and type-checking features.
#SQLAlchemy models expect keyword arguments:
#When you create a SQLAlchemy model instance like models.Task(...), it expects its fields as regular Python keyword arguments or a dictionary unpacked into keyword arguments.
#task.dict() gives you a clean dictionary of field names and values:
#So **task.dict() unpacks that dictionary into named arguments for the SQLAlchemy model constructor.
#**task.dict(): Unpacks it into models.Task(...).

# Say task has this data:
#task.title = "Learn SQLAlchemy"
#task.description = "Understand how to integrate Pydantic with SQLAlchemy"
#task.due_date = date(2025, 5, 17)
#task.status = "pending"

#task.dict() returns:
#{
#  "title": "Learn SQLAlchemy",
#  "description": "Understand how to integrate Pydantic with SQLAlchemy",
#  "due_date": date(2025, 5, 17),
#  "status": "pending"
#}
#Then:
#models.Task(**task.dict())

#Is equivalent to:
#models.Task(
#  title="Learn SQLAlchemy",
#  description="Understand how to integrate Pydantic with SQLAlchemy",
#  due_date=date(2025, 5, 17),
#  status="pending"
#)


#db.add(): Adds the task to the session.
#db.commit(): Saves the changes to the DB.
#db.refresh(): Updates the object with its final DB state (like the auto-generated id).
#return db_task: Return the created task.
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

#Update a task’s fields if it exists.

#get_task(...): Find the task first.
#task.dict().items(): Loop over all fields provided in the update.
#setattr(...): Update each field dynamically.
#db.commit(): Save the updates.
#db.refresh(): Refresh from DB.
#Return updated task, or None if not found.
def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

#Delete a task if it exists.
#get_task(...): Find it first.
#db.delete(...): Mark for deletion.
#db.commit(): Apply changes.
#Return the deleted task (or None if not found).
def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task