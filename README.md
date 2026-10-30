# Library API

A RESTful backend API built with **Python**, **FastAPI**, and **PostgreSQL (Neon)**. The platform enables creators to publish text-based literary works (such as stories, essays, and poetry) while allowing registered users to browse works and financially support their favorite authors.

---

## 🌐 Live Deployment

The API is deployed and accessible on Render:

- **Live Base URL**: [https://library-api-blta.onrender.com](https://library-api-blta.onrender.com)
- **Interactive API Documentation (Swagger UI)**: [https://library-api-blta.onrender.com/docs](https://library-api-blta.onrender.com/docs)

---

## 🛠️ Technologies Used

- **Language**: Python 3.10+
- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) (high performance, automatic OpenAPI / Swagger generation)
- **ORM & Database Toolkit**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) hosted serverless on [Neon](https://neon.tech/)
- **Database Driver**: `psycopg2-binary`
- **Data Validation & Settings**: [Pydantic v2](https://docs.pydantic.dev/)
- **Security & Authentication**:
  - `python-jose` for JWT (JSON Web Tokens)
  - `passlib[bcrypt]` for secure password hashing
- **Testing**:
  - [pytest](https://docs.pytest.org/)
  - [HTTPX](https://www.python-httpx.org/) (for FastAPI `TestClient`)
- **Server**: [Uvicorn](https://www.uvicorn.org/) (ASGI web server)

---

## ✨ Features

### 1. Authentication & Security
- **User Registration**: Create a new account with validation for unique email, unique username, and minimum password length.
- **User Login**: Authenticate via standard credentials and receive a signed JWT access token.
- **Password Hashing**: Secure salted password storage using bcrypt.
- **Protected Routes**: Granular endpoint protection using FastAPI dependencies and OAuth2 Bearer token authentication.

### 2. Works Management
- **Publish Works**: Authenticated users can create new works with titles, descriptions, and full text content.
- **List Works**: Browse all published works with pagination (`skip` and `limit`) and filtering by `author_id`.
- **Get Work by ID**: View detailed information about any individual work.
- **Author Ownership & Control**: Only the original creator can update (`PUT`) or delete (`DELETE`) their work. Unauthorized modifications return `403 Forbidden`.

### 3. Financial Support System
- **Support a Work**: Authenticated users can support creators by contributing a custom monetary amount (`amount > 0`).
- **Input Validation**: Rejects invalid, zero, or negative amounts with `422 Unprocessable Entity`.
- **Supporter Traceability**: The supporter ID is automatically extracted from the authenticated JWT session and cannot be spoofed.
- **Work Support History**: Publicly view all support contributions received for a specific work.
- **User Support History**: Publicly retrieve all contributions made by a specific user.

### 4. Work Details with Aggregated Support
- **Single Joined Query**: High-performance SQL query combining the work, author details, and total financial support received.
- **Zero-Support Resilient**: Utilizes `LEFT OUTER JOIN` and `COALESCE(SUM(amount), 0)` to guarantee works with no contributions return `total_support: 0` rather than `null`.

### 5. Automated Pytest Test Suite
- Comprehensive automated test suite with **8 tests passing**:
  - `test_user_registration_success`
  - `test_user_registration_duplicate_email`
  - `test_user_login_success`
  - `test_user_login_invalid_credentials`
  - `test_create_work_success`
  - `test_unauthorized_user_cannot_update_work` (403 Forbidden check)
  - `test_work_details_with_total_support` (Aggregation verification)
  - `test_work_details_with_zero_support` (Zero-support baseline)

---

## 🏛️ Project Architecture

The project adheres to a clean, decoupled **Layered Architecture**:

```text
HTTP Request
     │
     ▼
┌──────────────┐
│    Router    │  Validates HTTP requests, handles status codes & response schemas
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Service    │  Encapsulates core business logic, permissions & entity verification
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Repository  │  Executes SQLAlchemy queries & database persistence
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Database   │  PostgreSQL (Neon)
└──────────────┘
```

### Layer Responsibilities
- **`routers/`**: Exposes API endpoints, defines routes, tags, parameter extraction, and status codes.
- **`services/`**: Coordinates workflows, enforces business constraints (e.g. ownership authorization, duplicate checks), and raises appropriate `HTTPException` errors.
- **`repositories/`**: Isolates all database operations (queries, joins, aggregations, commits) from business logic.
- **`models/`**: SQLAlchemy declarative models defining database table schemas and relationships.
- **`schemas/`**: Pydantic schemas validating inbound request payloads and serializing outbound responses.
- **`dependencies/`**: Shared FastAPI dependency injection providers (e.g., token decoding and current user resolution).
- **`core/`**: Centralized engine configuration, session generators (`get_db`), and cryptographic helpers.

---

## 📂 Project Directory Structure

```text
library-api/
├── core/
│   ├── database.py              # Engine, SessionLocal, and get_db dependency
│   └── security.py              # Password hashing and JWT generation/decoding
├── dependencies/
│   ├── __init__.py
│   └── auth.py                  # OAuth2 Bearer get_current_user dependency
├── models/
│   ├── __init__.py              # Model exports
│   ├── support.py               # Support SQLAlchemy model
│   ├── user.py                  # User SQLAlchemy model
│   └── work.py                  # Work SQLAlchemy model
├── repositories/
│   ├── __init__.py
│   ├── support_repository.py    # Support persistence and queries
│   ├── user_repository.py       # User persistence and lookups
│   └── work_repository.py       # Work CRUD and joined aggregation queries
├── routers/
│   ├── __init__.py
│   ├── auth.py                  # Registration and login endpoints
│   ├── users.py                 # User profile and user support history endpoints
│   └── works.py                 # Work CRUD, work details, and work support endpoints
├── schemas/
│   ├── __init__.py
│   ├── support.py               # SupportCreate and SupportResponse schemas
│   ├── user.py                  # UserCreate, UserResponse, UserLogin, Token schemas
│   └── work.py                  # WorkCreate, WorkUpdate, WorkResponse, WorkDetailResponse schemas
├── services/
│   ├── __init__.py
│   ├── auth_service.py          # Registration and login business logic
│   ├── support_service.py       # Support logic and existence validation
│   └── work_service.py          # Work business logic and permission enforcement
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures, test DB engine, and isolation
│   ├── test_auth.py             # Auth & user registration tests
│   ├── test_support.py          # Support & aggregated details tests
│   └── test_works.py            # Work creation and authorization tests
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore specifications
├── create_tables.py             # Table creation utility script
├── main.py                      # FastAPI application entry point
├── README.md                    # Project documentation
├── requirements.txt             # Project dependencies
└── test_db.py                   # Database connection verification script
```

---

## 🚀 Installation & Local Setup

Follow these steps to set up and run the project locally on **Windows (PowerShell)**:

### 1. Clone the Repository
```powershell
git clone https://github.com/Subhanulhaq935/library-api.git
cd library-api
```

### 2. Create and Activate a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root directory by copying the `.env.example` template:

```powershell
Copy-Item .env.example .env
```

Open `.env` and fill in your configuration:

```env
# Primary PostgreSQL Database (e.g. Neon)
DATABASE_URL=postgresql+psycopg2://<username>:<password>@<ep-host>.neon.tech/library_db?sslmode=require

# Dedicated Test Database for Pytest
TEST_DATABASE_URL=postgresql+psycopg2://<username>:<password>@<ep-host>.neon.tech/library_test_db?sslmode=require

# JWT Configuration
SECRET_KEY=your_secure_random_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> [!NOTE]
> **Neon PostgreSQL Setup**:
> 1. Sign up or log in at [Neon.tech](https://neon.tech/).
> 2. Create a new project and copy the connection string.
> 3. Create a second database in the Neon console (e.g. `library_test_db`) for automated testing.
> 4. Ensure the connection strings use `postgresql+psycopg2://` with `?sslmode=require`.

### 5. Initialize Database Tables
Run the database initialization script to create tables in your primary database:

```powershell
python create_tables.py
```

---

## 💻 Running the Application

Start the local development server with Uvicorn:

```powershell
uvicorn main:app --reload
```

Once running:
- **Base URL**: `http://127.0.0.1:8000/`
- **Interactive Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | Health check endpoint | No |
| **Authentication** | | | |
| `POST` | `/auth/register` | Register a new user | No |
| `POST` | `/auth/login` | Authenticate with email & password; returns JWT | No |
| `POST` | `/auth/token` | OAuth2-compatible token endpoint | No |
| **Users** | | | |
| `GET` | `/users/me` | Retrieve the authenticated user's profile | **Yes** |
| `GET` | `/users/{user_id}/support` | View all support contributions made by a specific user | No |
| **Works** | | | |
| `POST` | `/works/` | Create and publish a new work | **Yes** |
| `GET` | `/works/` | List all works (supports `author_id`, `skip`, `limit`) | No |
| `GET` | `/works/{work_id}` | Retrieve details of a single work by ID | No |
| `GET` | `/works/{work_id}/details` | Retrieve work details, author profile, and total support | No |
| `PUT` | `/works/{work_id}` | Update an existing work (author/owner only) | **Yes** |
| `DELETE` | `/works/{work_id}` | Delete a work (author/owner only) | **Yes** |
| **Support** | | | |
| `POST` | `/works/{work_id}/support` | Support a work with a monetary amount | **Yes** |
| `GET` | `/works/{work_id}/support` | List all support contributions received by a work | No |

---

## 🔐 Authentication Guide

The API uses **JWT (JSON Web Token)** bearer tokens for authentication.

### How to Authenticate
1. Send a `POST` request to `/auth/login` with your registered credentials (`email` and `password`).
2. The response will return an access token:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```
3. Include this token in the `Authorization` header for protected endpoints:
   ```http
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```

### Authorizing in Swagger UI (`/docs`)
1. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
2. Click the green **Authorize** button at the top right.
3. In the dialog, enter your registered credentials in the username/password fields, or directly paste your bearer token.
4. Click **Authorize** and then **Close**. All protected endpoints will now send the token automatically.

---

## 🧪 Automated Testing

Automated tests are built with **pytest** and **HTTPX**. Tests run in complete isolation against a dedicated PostgreSQL test database.

### Running the Entire Test Suite
```powershell
pytest -v
```

### Running Individual Test Suites
```powershell
# Run Authentication tests
pytest tests/test_auth.py -v

# Run Works Management and Authorization tests
pytest tests/test_works.py -v

# Run Support System and Aggregated Details tests
pytest tests/test_support.py -v
```

> [!WARNING]
> **Database Safety**: Tests use `TEST_DATABASE_URL` exclusively. The test suite automatically cleans and tears down test data before and after each test. **Never** point `TEST_DATABASE_URL` to your production or development database.

---

## 🗄️ Database & Migrations

- **PostgreSQL on Neon**: Production and development environments connect to a hosted Neon PostgreSQL database with SSL enabled.
- **Initial Table Creation**: Tables were generated using the declarative metadata via `create_tables.py`.
- **Database Migrations**: While `alembic` is present as a dependency, migrations are not yet configured or applied. Schema management is planned as a future improvement.

---

## 🔮 Future Improvements

- [ ] **Alembic Database Migrations**: Implement automated version-controlled schema migrations.
- [ ] **Expanded Test Coverage**: Add edge-case and performance tests for concurrent support requests.
- [ ] **Rate Limiting**: Add rate-limiting middleware to protect authentication endpoints from brute-force attacks.
- [ ] **Enhanced Filtering & Search**: Support full-text search across work titles and content.
- [ ] **Observability & Logging**: Introduce structured JSON logging and health monitoring.
