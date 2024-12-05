# Django Todo API

A RESTful API for managing todo items built with Django REST Framework. Features include user authentication, CRUD operations for todos, and comprehensive API documentation.

## Features

- Token-based authentication
- CRUD operations for todo items
- User-specific todo lists
- Swagger/OpenAPI documentation
- Automated tests
- Audit fields (created_at, updated_at, created_by, updated_by)

## Prerequisites

* Python 3.10 or higher
* pip (Python package manager)
* Virtual environment (recommended) 

## Installation

1. Clone the repository

```bash
git clone https://github.com/khaido2209/todo_BE.git
cd <project-directory>
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Apply database migrations

```bash
python manage.py migrate
```
5. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

## Running the Development Server

```bash
python manage.py runserver
```
The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## Authentication

To use the API, you need to obtain an authentication token:

```bash
curl -X POST http://localhost:8000/api-token-auth/ \
-H "Content-Type: application/json" \
-d '{"username": "your_username", "password": "your_password"}'
```

Use the returned token in subsequent requests:

```bash
curl http://localhost:8000/api/todos/ \
-H "Authorization: Token your_token_here"
```

## API Endpoints

- `POST /api-token-auth/` - Obtain authentication token
- `GET /api/todos/` - List all todos for current user
- `POST /api/todos/` - Create a new todo
- `GET /api/todos/{id}/` - Retrieve a specific todo
- `PUT /api/todos/{id}/` - Update a todo
- `PATCH /api/todos/{id}/` - Partially update a todo
- `DELETE /api/todos/{id}/` - Delete a todo

## Running Tests

```bash
python manage.py test
```