import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database import Base, get_db
from core.security import hash_password
from main import app
from models.user import User
import models  # Ensures all models (User, Work, Support) are registered on Base.metadata

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError(
        "CRITICAL ERROR: 'TEST_DATABASE_URL' is missing from the environment. "
        "Automated tests must run exclusively against the isolated test database "
        "and will never fall back to DATABASE_URL."
    )

dev_db_url = os.getenv("DATABASE_URL")
if dev_db_url and TEST_DATABASE_URL == dev_db_url:
    raise ValueError(
        "CRITICAL ERROR: 'TEST_DATABASE_URL' matches 'DATABASE_URL'. "
        "Tests must use a separate test database to avoid data loss in development."
    )

test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(scope="session", autouse=True)
def init_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    test_engine.dispose()


@pytest.fixture(autouse=True)
def clean_database():
    with test_engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()

    yield

    with test_engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def create_test_user(db_session):
    def _create_user(
        username: str = "testuser",
        email: str = "test@example.com",
        password: str = "password123",
    ) -> User:
        hashed = hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _create_user


@pytest.fixture
def get_token_for_user(client):
    def _get_token(
        email: str = "test@example.com",
        password: str = "password123",
    ) -> str:
        response = client.post(
            "/auth/login",
            data={"email": email, "password": password},
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        return response.json()["access_token"]

    return _get_token

