# Task Manager

Basic Task Manager API project with Python. This is a backend project that covers real-world concepts like routing, databases, and RESTful CRUD operations.

## Requirements

### psycopg2-binary

Purpose: PostgreSQL database driver

- Allows SQLAlchemy to connect to a PostgreSQL database.
- Binary version is precompiled for convenience (no need to build from source).
  Help to use PostgreSQL with SQLAlchemy in a Docker environment.

### python-jose

Purpose: JSON Web Token (JWT) handling
Encodes and decodes JWT tokens securely.
Used for authentication:

- Create access tokens (jwt.encode)
- Verify and extract payload (jwt.decode)
  Powers the login and protected route logic in auth.py.

### passlib bcrypt

Purpose: Secure password hashing

- passlib provides a clean API for password hashing. -[bcrypt] installs the bcrypt hashing algorithm, which is strong and widely used.

### python-dotenv

Purpose: Load environment variables from .env files

- Helps keep secrets and config out of source code.
  Ensures secure and flexible config management, especially in Dockerized apps

### pytest-asyncio

plugin for pytest that lets you write and run async def test functions

- FastAPI has async routes

### httpx

An HTTP client (like requests) that supports both synchronous and asynchronous HTTP calls.
Works good with FastAPI for testing async endpoints
Allows sending requests to your API in unit/integration tests

## Run instructions:

```bash
$ pip install -r requirements.txt
```

## Run the project:

Use a virtual environment (optional):

```bash
$ pip install virtualenv
$ python -m venv venv_name
$ source venv/bin/activate
$ uvicorn app.main:app --reload
```

To run it using Docker:

```bash
$ cd <task-manager>
$ docker-compose up --build
```

To test it:

```bash
$ curl -X POST http://localhost:8000/register \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass"}'
```

Or use Postman.

## Troubleshooting

When testing:

```
ERROR tests/test_auth.py - sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not translate host name "db" to address: nodename nor servname provided, or not known
```

### Option 1:

Override the DB host in local .env or test config
Edit your local .env to use localhost instead:

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskdb
Or add a separate .env.test or test override logic for local testing.

### Option 2:

Use SQLite or mock DB for unit tests

### To run pytest without docker:

```python
database.py
SQLALCHEMY_DATABASE_URL = "sqlite:///.tasks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

```

```bash
$PYTHONPATH=. pytest

$uvicorn app.main:app --reload
```

### OUTPUT log of testing:

```bash
latform darwin -- Python 3.13.3, pytest-8.3.5, pluggy-1.6.0
rootdir: /Users/juandiegodelgado/learning-sw/python/task-manager
plugins: anyio-4.9.0, asyncio-0.26.0
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 2 items

tests/test_auth.py . [ 50%]
tests/test_main.py . [100%]

============================================================================================ 2 passed in 0.37s =============================================================================================
```
