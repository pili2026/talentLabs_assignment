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

### API Integration Testing with Docker

This project includes a full api integration test environment using Docker and TimescaleDB:

```bash
./run_tests.sh
```

This script will:

- Start the TimescaleDB test container (`docker-compose.test.yml`)
- Wait until the database is fully ready (not just TCP ready)
- Run Django migrations
- Execute all tests using `pytest`
- Automatically clean up the test database container and volume

You can run specific test functions with:

```bash
./bin/run_api_integration_test.sh -k test_job_api_integration
```

### Test Coverage Report

To run tests with a code coverage summary:

```bash
pytest --cov=job --cov-config=.coveragerc --cov-report=term --cov-report=html
```

* This will show a terminal summary of test coverage
* A full HTML report will be generated at `htmlcov/index.html`

You can open it in your browser with:

```bash
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

#### Sample Output:

```
Name                    Stmts   Miss  Cover
-------------------------------------------
src/job/repository.py      67      9    87%
src/job/model.py           21      2    90%
TOTAL                     236     16    93%
```

> To achieve 100% coverage, be sure to test all conditional branches and exception cases in repository methods.

### .coveragerc Configuration

The `.coveragerc` file helps exclude boilerplate and test-only code from coverage calculations:

```ini
[run]
omit =
    */__init__.py
    */migrations/*
    */test/*
    manage.py
    */asgi.py
    */wsgi.py
    */settings.py

[report]
exclude_lines =
    pragma: no cover
    if __name__ == .__main__.:
    raise NotImplementedError
    except ImportError

show_missing = true
skip_covered = true
```

## Project Structure

```
.
├── bin/                                        # Shell scripts
|   ├── run_api_integration_test.sh             # Shell script to run api integration tests
│   ├── run_api_servcer_local_entrypoint.sh     # Local dev script
│   └── web_api_server_entrypoint.sh            # Docker entrypoint
│
├── res/                         # Configuration files
│   ├── config.yml               # Local settings
|   ├── config.test.yml          # API Integration test settings
│   └── config.docker.yml        # Docker-specific overrides
│
├── docker-compose.yml           # Compose config for API + DB
├── docker-compose.test.yml      # Compose config for integration testing
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

## Design Decisions & Tradeoffs

Several assumptions were made to handle under-specified behaviors in the original prompt.  
Where requirements were vague or incomplete, reasonable defaults and tradeoffs were applied to ensure a robust and testable backend implementation.

Key examples include:

### 1. Salary Range Type

The assignment allowed `salary_range` to be a `string or object`. To handle both cases:

- Defined a Pydantic `SalaryRange` object with `min` and `max`
- Allowed string fallback (e.g., `"90k-110k"`) during parsing and DB storage
- Tradeoff: sacrificed some schema strictness for flexibility and backward compatibility

### 2. Job Status Enum Validation

- Used a `StrEnum` (`JobStatusEnum`) to constrain allowed values (`active`, `expired`, `scheduled`)
- Added request-time schema validation to prevent invalid input
- Tradeoff: strict typing may lead to 422 errors if clients use wrong casing

### 3. Search & Filter Logic

- `search` field is applied to `title`, `description`, and `company_name`
- `skills` filter uses `__contains` for partial array match
- Tradeoff: easier to implement and test, but suboptimal for large-scale datasets (e.g., no full-text index)

### 4. Immutable Company Name

- Enforced rule that `company_name` cannot be updated after creation
- Implemented via service-layer validation logic
- Tradeoff: avoids side effects and keeps business rules outside schema layer

### 5. JWT Authentication Strategy

- Used `django-ninja-jwt` for seamless integration with Ninja and async handlers
- Automatically seeded an admin user and printed JWT token for quick testing
- Tradeoff: no token refresh support in this prototype (would add in production)

### 6. Mock-Based Repository Testing

- Repository methods are tested using `pytest-mock` and `AsyncMock`, rather than hitting the DB
- Tradeoff: test coverage is higher and faster, though full ORM behavior is assumed, not verified

### 7. Three-Layer Architecture: Handler → Service → Repository

The app uses a layered design:

- **Handler**: API routes and schema validation
- **Service**: business rules (e.g., immutable fields)
- **Repository**: DB access and query abstraction

This structure improves testability, clarity, and modularity—at the cost of some initial complexity, which is justified for scalable projects.

> These decisions aim to balance clarity, developer experience, and testability under real-world constraints.

## License

```
MIT – for assignment evaluation only.
```
