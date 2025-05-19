# task-manager

Basic Task Manager API project with Python. This is a backend project that covers real-world concepts like routing, databases, and RESTful CRUD operations.

psycopg2-binary
Purpose: PostgreSQL database driver
-Allows SQLAlchemy to connect to a PostgreSQL database.
-binary version is precompiled for convenience (no need to build from source).
Help to use PostgreSQL with SQLAlchemy in a Docker environment.

python-jose
Purpose: JSON Web Token (JWT) handling
Encodes and decodes JWT tokens securely.
Used for authentication:
-Create access tokens (jwt.encode)
-Verify and extract payload (jwt.decode)
Powers the login and protected route logic in auth.py.

passlib[bcrypt]
Purpose: Secure password hashing
-passlib provides a clean API for password hashing. -[bcrypt] installs the bcrypt hashing algorithm, which is strong and widely used.

python-dotenv
Purpose: Load environment variables from .env files
-Helps keep secrets and config out of source code.
Ensures secure and flexible config management, especially in Dockerized apps

To run requirements:
$ pip install -r requirements.txt

To run the project:
Use a virtual environment (optional):
$ pip install virtualenv
$ python -m venv venv_name
$ source venv/bin/activate
$ uvicorn app.main:app --reload

To run it using Docker:
$ cd <task-manager>
$ docker-compose up --build

To test it:
$ curl -X POST http://localhost:8000/register \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass"}'

Or use Postman.
