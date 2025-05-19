#Base image: This uses the official Python 3.10 image, in its slimmed-down version (smaller size, fewer tools).
#It contains Python but minimal extras, which makes your image lightweight.
#Good for production — faster builds, smaller image size.
FROM python:3.10-slim

#Sets the working directory inside the container to /app.
#All subsequent commands will run relative to this directory.
#Think of this as cd /app inside the container.
#Keeps your app organized in a standard location.
WORKDIR /app

#Copies the requirements.txt file from your local machine into the container at /app/requirements.txt.
#Helps Docker cache dependencies and avoid reinstalling them unless requirements.txt changes
COPY requirements.txt .

#Installs the Python dependencies listed in requirements.txt.
#--no-cache-dir ensures that pip doesn't store any downloaded packages, keeping the image clean and small.
RUN pip install --no-cache-dir -r requirements.txt

#Copies everything in your current project folder (the .) into the container’s /app directory (also .).
#Now the rest of your app’s code (e.g., main.py, models.py, schemas.py) is inside the container.
#This step comes after installing dependencies to take advantage of Docker layer caching.
COPY . .

#This defines the default command that runs when the container starts.
#This starts your FastAPI server automatically when the container runs
#--host 0.0.0.0 → listens on all network interfaces (required for Docker access)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]