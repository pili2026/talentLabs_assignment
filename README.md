# TalentLabs Backend Assignment

This is the backend implementation of the TalentLabs Full Stack Assignment. It is a job platform API built using Django, Django Ninja, and JWT authentication. It supports job management, search, filtering, pagination, and authentication.


## Tech Stack

- Python 3.12
- Django 5.2
- Django Ninja + Ninja JWT
- PostgreSQL (TimescaleDB)
- Pydantic v2
- Pytest
- Docker + Docker Compose


## How to Run the Project

### 1. Local Python Environment

Make sure PostgreSQL is running locally and matches the configuration in `res/config.yml`.

```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and seed data
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
* Seed the admin user and 10 random job records

The server will be available at: [http://localhost:8000](http://localhost:8000) or [http://0.0.0.0:8000](http://0.0.0.0:8000)

### 3. Quick Start Script (Optional)

You can also use the following shell script to quickly run the project locally:

```bash
./bin/run_api_servcer_local_entrypoint.sh
```
This script will:

* Apply migrations
* Seed the database (admin + 10 jobs)
* Start the development server at 0.0.0.0:8000


## Seeded Admin Account

After running python manage.py seed or launching via Docker, the following user is created:

```txt
Username: admin  
Password: admin123
```
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

Interactive API docs are available at:

> [http://localhost:8000/api/docs](http://localhost:8000/api/docs) or [http://0.0.0.0:8000/api/docs](http://0.0.0.0:8000/api/docs)

### How to Test API via Swagger UI:

1. Go to `/api/auth/pair`
2. Click **Try it out**, and enter:

   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
3. Click **Execute**
4. Copy the `access` token
5. Click **Authorize** in the top right
6. Paste the token: `Bearer <your_token>`
7. Now you can test all authorized endpoints


## Features

* JWT authentication (`/auth/pair`, `/auth/me`)
* CRUD API for jobs (`/api/job`)
* Filter by job status (Active, Expired, Scheduled)
* Search by title, description, and company name
* Pagination and sorting (posting/expiration date)
* Async service + repository pattern
* Schema validation with Pydantic v2
* Auto-generated API documentation
* Seed command: creates admin user and job data
* Docker support for easy deployment

## Running Tests

```bash
pytest
```

Or for verbose output:

```bash
pytest -v --disable-warnings
```

## License

MIT – for assignment evaluation use only.

