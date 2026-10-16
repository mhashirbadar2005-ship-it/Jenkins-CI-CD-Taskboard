# Task Board: Jenkins CI/CD Pipeline Demo

A small full-stack app (HTML/JavaScript frontend, FastAPI backend, PostgreSQL database) used to practice building an automated CI/CD pipeline with Jenkins. Built as a DevOps internship task.

## What it demonstrates

- A `Jenkinsfile` pipeline that checks out code, lints it, runs unit tests, builds a Docker image and deploys it
- Static analysis with `flake8` and unit tests with `pytest`, with test results published on the Jenkins dashboard
- A multi-stage Docker image that runs as a non-root user
- Database credentials supplied at deploy time from the Jenkins credential store, never from the repo
- AWS RDS (PostgreSQL) as the production database

## Project structure

```
.
├── app/
│   ├── main.py            # FastAPI routes and startup logic
│   ├── database.py        # Database connection (reads DATABASE_URL)
│   ├── models.py          # Task table definition
│   ├── schemas.py         # Request/response validation
│   └── static/index.html  # Frontend
├── tests/                 # pytest unit tests (in-memory SQLite)
├── Jenkinsfile            # The pipeline definition
├── Dockerfile             # Multi-stage image
├── docker-compose.yml     # Local app + PostgreSQL
├── requirements.txt       # Runtime dependencies
├── requirements-dev.txt   # Test and lint tools
├── .flake8                # Lint settings
└── pytest.ini             # Test settings
```

## Run the checks locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
flake8 app tests
pytest
```

## Run the app locally with Docker Compose

```bash
cp .env.example .env
docker compose up --build -d
```

Open `http://localhost:8000`. Stop it with `docker compose down`.

## Configuration

| Variable       | Purpose                                                           |
|----------------|-------------------------------------------------------------------|
| `DATABASE_URL` | Database connection string (SQLite by default, PostgreSQL on RDS) |
| `APP_NAME`     | Optional name shown in the API docs and health check              |

## API

| Method | Path              | Description                    |
|--------|-------------------|--------------------------------|
| GET    | `/health`         | Checks the database connection |
| GET    | `/api/tasks`      | Lists tasks                    |
| POST   | `/api/tasks`      | Creates a task                 |
| PATCH  | `/api/tasks/{id}` | Marks a task done or not done  |
| DELETE | `/api/tasks/{id}` | Deletes a task                 |

## Pipeline stages

1. Checkout: pull the latest commit
2. Lint: `flake8` static analysis
3. Unit tests: `pytest`, results published to Jenkins
4. Build image: Docker build, tagged with the build number
5. Deploy: run the new container against RDS and wait for `/health`

