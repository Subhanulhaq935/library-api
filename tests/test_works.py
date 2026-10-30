from fastapi import status
from models.work import Work


def test_create_work_success(
    client,
    create_test_user,
    get_token_for_user,
    db_session,
):
    user = create_test_user(
        username="author1",
        email="author1@example.com",
        password="password123",
    )

    token = get_token_for_user(
        email="author1@example.com",
        password="password123",
    )

    payload = {
        "title": "Clean Architecture in Practice",
        "description": "A comprehensive guide to software design",
        "content": "Detailed chapters on domain models, repositories, and services.",
    }

    response = client.post(
        "/works/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["content"] == payload["content"]
    assert data["artist_id"] == user.id
    assert "id" in data

    # Verify work is saved in the test database
    saved_work = db_session.query(Work).filter_by(id=data["id"]).first()
    assert saved_work is not None
    assert saved_work.title == payload["title"]
    assert saved_work.artist_id == user.id


def test_unauthorized_user_cannot_update_work(
    client,
    create_test_user,
    get_token_for_user,
    db_session,
):
    # 1. Create User A
    create_test_user(
        username="usera",
        email="usera@example.com",
        password="password123",
    )

    # 2. Create User B
    create_test_user(
        username="userb",
        email="userb@example.com",
        password="password123",
    )

    # 3. Authenticate as User A
    token_a = get_token_for_user(
        email="usera@example.com",
        password="password123",
    )

    # 4. User A creates a work
    create_resp = client.post(
        "/works/",
        json={
            "title": "Original Title by User A",
            "description": "Original Description",
            "content": "Original Content",
        },
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert create_resp.status_code == status.HTTP_201_CREATED
    work_id = create_resp.json()["id"]

    # 5. Authenticate as User B
    token_b = get_token_for_user(
        email="userb@example.com",
        password="password123",
    )

    # 6. User B attempts to update User A's work using PUT
    update_resp = client.put(
        f"/works/{work_id}",
        json={"title": "Hacked Title Attempt"},
        headers={"Authorization": f"Bearer {token_b}"},
    )

    # 7. Verify API returns HTTP 403 Forbidden
    assert update_resp.status_code == status.HTTP_403_FORBIDDEN
    assert update_resp.json()["detail"] == "You are not allowed to update this work"

    # 8. Verify that the original work remains unchanged in the database
    db_session.expire_all()
    work_in_db = db_session.query(Work).filter_by(id=work_id).first()
    assert work_in_db is not None
    assert work_in_db.title == "Original Title by User A"

