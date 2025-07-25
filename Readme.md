### to build something cool quickly and go to production in some hours


### 🧠 From a basic to advanced thinking only register user

| Area                   | Focus                                                |
| ---------------------- | ---------------------------------------------------- |
| **Edge cases**         | Re-registering with same email, missing fields       |
| **Security**           | Rate limiting, CAPTCHA, timing attacks               |
| **Scalability**        | Async DB writes, background tasks for emails         |
| **Maintainability**    | Is your logic testable and reusable?                 |
| **Clean architecture** | Are you separating layers (API, service, DB)?        |
| **Error handling**     | Are you raising proper exceptions with status codes? |
| **Auditing**           | Should you log registrations? Add metrics?           |



Skill	Practice
Clean Code	Layered structure (schema, router, service, repo)
Async	Use async def and motor with MongoDB
Security	Password hashing, no plain-text storage
Testing	Pytest: test service and router layers
Type hints	Always type input/output clearly
Scaling	Learn FastAPI Dependency Injection, background jobs, etc.

## Which solution is used?


## How to run this project?

By manual:
- Clone this repository
- Install dependencies: `pip install -r requirements.txt`
- Set environment variables: `cp .env.example .env`
- Run the app: `uvicorn app.main:app --reload`

By docker:
- Clone this repository
- Run docker compose: `docker compose up -d`


## FastAPI Project Structure
my_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance & startup logic
│   ├── api/                 # Routers grouped by feature
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── auth.py
│   ├── core/                # App-wide logic (config, settings, auth utils)
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── models/              # Pydantic & DB models
│   │   ├── __init__.py
│   │   ├── user.py
│   ├── db/                  # Database connections & repos
│   │   ├── __init__.py
│   │   ├── mongodb.py
│   │   └── repositories/
│   │       ├── user_repository.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   ├── external/            # Clients to external APIs
│   │   ├── __init__.py
│   │   └── payment_client.py
│   └── schemas/             # Pydantic schemas (request/response)
│       ├── __init__.py
│       ├── user.py
│
├── tests/                   # Unit and integration tests
├── .env
├── requirements.txt
└── README.md
