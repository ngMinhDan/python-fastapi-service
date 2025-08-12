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



│   │   ├── __init__.py
│   │   └── v1/              # API version 1
│   │       ├── __init__.py
│   │       └── user.py      # User endpoints (register, login, profile)
│   ├── core/                # Core functionality and utilities
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration settings
│   │   ├── security.py      # JWT tokens, password hashing
│   │   └── validate.py      # Input validation utilities
│   ├── models/              # Database models (Beanie ODM)
│   │   ├── __init__.py
│   │   └── user.py          # User document model
│   ├── schemas/             # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication schemas
│   │   └── user.py          # User request/response schemas
│   └── services/            # Business logic layer
│       ├── __init__.py
│       └── user_service.py  # User business logic
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_api.py          # API endpoint tests
│   ├── test_models.py       # Database model tests
│   ├── test_schemas.py      # Schema validation tests
│   └── test_validate.py     # Validation utility tests
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Application container
├── requirements.txt         # Python dependencies
├── pytest.ini             # Test configuration
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB 4.4+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-fastapi-service
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start MongoDB** (if not using Docker)
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   
   # Or install MongoDB locally
   # https://docs.mongodb.com/manual/installation/
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Using Docker Compose

```bash
# Start all services (app + MongoDB)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔗 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/users/register` | Register new user | ❌ |
| POST | `/users/login` | User login | ❌ |
| GET | `/users/me` | Get current user profile | ✅ |
| GET | `/users/` | List users (admin only) | ✅ |

### Example Requests

**Register User**
```bash
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john.doe@example.com",
    "password": "SecurePass123!"
  }'
```

**Login User**
```bash
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123!"
  }'
```

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/test_validate.py -v

# API tests only
pytest tests/test_api.py -v

# With coverage
pytest --cov=app tests/
```

### Test Structure

- **`test_validate.py`**: Validation utility tests
- **`test_schemas.py`**: Pydantic schema tests
- **`test_models.py`**: Database model tests
- **`test_api.py`**: API endpoint integration tests

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=fastapi_service

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=FastAPI Service
APP_VERSION=1.0.0
DEBUG=false

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

## 🔒 Security Features

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character
- No common weak patterns

### Account Security
- Account locking after 5 failed login attempts
- JWT token-based authentication
- Password hashing with bcrypt
- Email validation with deliverability checks

### Input Validation
- Comprehensive Pydantic schemas
- Custom validation functions
- SQL injection prevention
- XSS protection

## 🏗️ Architecture

### Clean Architecture Principles

1. **Separation of Concerns**: Clear separation between API, business logic, and data layers
2. **Dependency Inversion**: High-level modules don't depend on low-level modules
3. **Single Responsibility**: Each module has a single, well-defined purpose
4. **Open/Closed Principle**: Open for extension, closed for modification

### Layer Responsibilities

- **API Layer** (`app/api/`): HTTP request/response handling, routing
- **Schema Layer** (`app/schemas/`): Data validation and serialization
- **Service Layer** (`app/services/`): Business logic and orchestration
- **Model Layer** (`app/models/`): Data persistence and database operations
- **Core Layer** (`app/core/`): Shared utilities and configuration

## 📊 Database Schema

### User Document
```python
{
  "_id": ObjectId,
  "name": str,
  "email": str,  # Unique, indexed
  "hashed_password": str,
  "active": bool,
  "role": str,
  "created_at": datetime,
  "updated_at": datetime,
  "last_login": datetime,
  "login_attempts": int,
  "locked_until": datetime,
  "phone": str,
  "address": str,
  "profile_picture_url": str,
  "cover_picture_url": str
}
```

### Indexes
- `email`: Unique index for fast user lookup
- `active`: Index for filtering active users
- `role`: Index for role-based queries
- `created_at`: Index for sorting by creation date

## 🚀 Deployment

### Production Checklist

- [ ] Set strong `SECRET_KEY` in production
- [ ] Configure proper MongoDB connection string
- [ ] Set `DEBUG=false`
- [ ] Configure CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure logging levels
- [ ] Set up monitoring and health checks
- [ ] Configure backup strategy

### Docker Production Deployment

```bash
# Build production image
docker build -t fastapi-service:latest .

# Run with production settings
docker run -d \
  --name fastapi-service \
  -p 8000:8000 \
  --env-file .env.production \
  fastapi-service:latest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Maintain test coverage above 90%
- Use meaningful variable and function names

## 📝 Development Notes

### Adding New Endpoints

1. Create schema in `app/schemas/`
2. Add business logic in `app/services/`
3. Create API endpoint in `app/api/v1/`
4. Write tests in `tests/`
5. Update documentation

### Database Migrations

For schema changes:
1. Update model in `app/models/`
2. Create migration script if needed
3. Test with sample data
4. Update tests

## 🐛 Troubleshooting

### Common Issues

**MongoDB Connection Issues**
```bash
# Check if MongoDB is running
docker ps | grep mongo

# Check connection
mongo mongodb://localhost:27017
```

**Import Errors**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Test Failures**
```bash
# Run tests with verbose output
pytest -v

# Run specific test
pytest tests/test_api.py::TestUserRegistrationAPI::test_successful_registration -v
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Beanie ODM Documentation](https://roman-right.github.io/beanie/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [pytest Documentation](https://docs.pytest.org/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- MongoDB team for the robust database
- Python community for excellent libraries

---

**Built with ❤️ using FastAPI, MongoDB, and Python**
