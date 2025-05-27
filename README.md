# TalentLabs Backend Assignment

This is the backend implementation of the TalentLabs Full Stack Assignment.  
It is a Job Platform API built using **Django**, **Django Ninja**, and **JWT authentication**.  
It supports job management with search, filtering, pagination, and role-based authentication.

## Tech Stack

- **Python 3.12**
- **Django 5.2**
- **Django Ninja** (async-ready API framework)
- **Ninja JWT** (authentication)
- **PostgreSQL** (with TimescaleDB)
- **Pydantic v2**
- **Pytest** for testing
- **Docker + Docker Compose** for deployment

## Features

* JWT authentication (`/api/auth/pair`, `/api/auth/me`)  
* CRUD API for jobs (`/api/job`)  
* Filter jobs by status, location, skills  
* Search by title, description, or company name  
* Pagination and sorting (by posting/expiration date)  
* Protected update rules (company name is immutable)  
* Async service/repository design pattern  
* Schema validation via Pydantic v2  
* OpenAPI docs auto-generated (`/api/docs`)  
* Seed command: admin user + 10 dummy jobs  
* Docker support for local development  
* Fully tested with Pytest, including positive/negative/unit cases

## How to Run the Project

### 1. Local Python Environment

Ensure PostgreSQL is running locally and matches the credentials in `res/config.yml`.

```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run DB migrations and seed data
python manage.py migrate
python manage.py seed

# Start development server
python manage.py runserver
```

### 2. Docker Compose

```bash
docker compose up --build
```

This will:

* Start the TimescaleDB container
* Start the Django API container
* Run migrations
* Seed the admin user and 10 sample jobs

Access the app at:
* [http://localhost:8000](http://localhost:8000)
* [http://0.0.0.0:8000](http://0.0.0.0:8000)

### 3. Quick Start Script

```bash
./bin/run_api_servcer_local_entrypoint.sh
```

This script:

* Applies migrations
* Seeds data
* Starts dev server at `0.0.0.0:8000`

## Seeded Admin Account

After seeding (via `manage.py seed` or Docker), this account is available:

```
Username: admin
Password: admin123
```

An access token is also printed in the terminal for quick testing.
### Auto-generated JWT Token
When the app is seeded, an access token is automatically generated and printed to the console.

Example output:
```txt
Access Token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Example curl test:
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5..." http://localhost:8000/api/job/
```
This token can be used to directly test authenticated endpoints without logging in manually.

## API Documentation

OpenAPI docs available at:

[http://localhost:8000/api/docs](http://localhost:8000/api/docs)
[http://0.0.0.0:8000/api/docs](http://0.0.0.0:8000/api/docs)

### How to Use Auth in Swagger UI

1. Go to `POST /api/auth/pair`
2. Click **Try it out**, enter:

   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
3. Click **Execute**
4. Copy the `access` token
5. Click **Authorize** (top-right), paste: `Bearer <your_token>`
6. You're now authenticated and can test all endpoints

## Running Tests

```bash
pytest
```

Or with verbose output:

```bash
pytest -v --disable-warnings
```

## Project Structure

```text
.
├── bin/                           # Shell scripts
│   ├── run_api_servcer_local_entrypoint.sh     # Local dev script
│   └── web_api_server_entrypoint.sh            # Docker entrypoint
│
├── res/                         # Configuration files
│   ├── config.yml               # Local settings
│   └── config.docker.yml        # Docker-specific overrides
│
├── docker-compose.yml           # Compose config for API + DB
├── Dockerfile                   # Django API Docker image
├── manage.py                    # Django CLI
├── requirements.txt             # Python dependencies
├── pyproject.toml               # PEP 621 + build config
│
└── src/
    ├── authentication/
    │   └── handler.py           # JWT route handler
    │
    ├── job/
    │   ├── handler.py           # Job API routes
    │   ├── schema.py            # Pydantic request/response schemas
    │   ├── service.py           # Business logic
    │   ├── repository.py        # Data access
    │   ├── model.py             # ORM model
    │   ├── enum_type.py         # Enums for job status and sorting
    │   ├── exception.py         # Custom exceptions
    │   ├── middleware.py        # Service injection
    │   └── test/                # Test suite
    │       ├── handler/
    │       ├── service/
    │       └── utils/
    │
    ├── job_platform/            # Django project core (settings, ASGI, etc.)
```

> All route logic is placed in `handler.py` across modules, following the `handler → service → repository` layering convention.

## Design Philosophy

* Follows Clean Architecture principles (modular, testable)
* Avoids fat views by layering responsibilities
* Makes full use of Pydantic 2.0 features (field validation, `extra="forbid"`)
* Configuration decoupled using `config.yml` for easy Docker overrides
* Emphasizes developer experience: quick setup, live docs, seeded tokens, and testable layers

## License
```
MIT – for assignment evaluation only.
```