from fastapi import status
from models.user import User


def test_user_registration_success(client, db_session):
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword123",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data

    # Verify password is not exposed in the response
    assert "password" not in data
    assert "password_hash" not in data

    # Verify user is saved in the test database
    saved_user = db_session.query(User).filter_by(email=payload["email"]).first()
    assert saved_user is not None
    assert saved_user.username == payload["username"]
    assert saved_user.password_hash != payload["password"]


def test_user_registration_duplicate_email(client):
    payload1 = {
        "username": "userone",
        "email": "duplicate@example.com",
        "password": "password123",
    }
    first_resp = client.post("/auth/register", json=payload1)
    assert first_resp.status_code == status.HTTP_201_CREATED

    payload2 = {
        "username": "usertwo",
        "email": "duplicate@example.com",
        "password": "password456",
    }
    second_resp = client.post("/auth/register", json=payload2)

    assert second_resp.status_code == status.HTTP_409_CONFLICT
    assert second_resp.json()["detail"] == "Email is already registered"


def test_user_login_success(client, create_test_user):
    create_test_user(
        username="loginuser",
        email="loginuser@example.com",
        password="mypassword123",
    )

    response = client.post(
        "/auth/login",
        data={
            "email": "loginuser@example.com",
            "password": "mypassword123",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"].lower() == "bearer"
    assert len(data["access_token"]) > 0


def test_user_login_invalid_credentials(client, create_test_user):
    create_test_user(
        username="validuser",
        email="valid@example.com",
        password="correctpassword",
    )

    # Wrong password
    response_wrong_pw = client.post(
        "/auth/login",
        data={
            "email": "valid@example.com",
            "password": "wrongpassword",
        },
    )
    assert response_wrong_pw.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_wrong_pw.json()["detail"] == "Invalid email or password"

    # Non-existent email
    response_no_user = client.post(
        "/auth/login",
        data={
            "email": "nonexistent@example.com",
            "password": "correctpassword",
        },
    )
    assert response_no_user.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_no_user.json()["detail"] == "Invalid email or password"

