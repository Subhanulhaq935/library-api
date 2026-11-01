from decimal import Decimal
from fastapi import status


def test_work_details_with_total_support(
    client,
    create_test_user,
    get_token_for_user,
):
    author = create_test_user(
        username="bookauthor",
        email="author@example.com",
        password="authorpassword",
    )
    author_token = get_token_for_user(
        email="author@example.com",
        password="authorpassword",
    )

    work_resp = client.post(
        "/works/",
        json={
            "title": "Supported Masterpiece",
            "description": "A popular book with community support",
            "content": "Story and chapters.",
        },
        headers={"Authorization": f"Bearer {author_token}"},
    )
    assert work_resp.status_code == status.HTTP_201_CREATED
    work_id = work_resp.json()["id"]

    
    create_test_user(
        username="supporter1",
        email="supporter1@example.com",
        password="supporterpassword",
    )
    supporter_token = get_token_for_user(
        email="supporter1@example.com",
        password="supporterpassword",
    )

    support_amounts = [100, 200, 300]
    for amt in support_amounts:
        support_resp = client.post(
            f"/works/{work_id}/support",
            json={"amount": amt},
            headers={"Authorization": f"Bearer {supporter_token}"},
        )
        assert support_resp.status_code == status.HTTP_201_CREATED

    
    details_resp = client.get(f"/works/{work_id}/details")
    assert details_resp.status_code == status.HTTP_200_OK
    details = details_resp.json()

    assert details["id"] == work_id
    assert details["title"] == "Supported Masterpiece"
    assert details["description"] == "A popular book with community support"
    assert details["content"] == "Story and chapters."
    assert details["artist_id"] == author.id

    # 6. Verify author information
    assert details["author"]["id"] == author.id
    assert details["author"]["username"] == "bookauthor"
    assert details["author"]["email"] == "author@example.com"

    assert Decimal(str(details["total_support"])) == Decimal("600.00")


def test_work_details_with_zero_support(
    client,
    create_test_user,
    get_token_for_user,
):
    author = create_test_user(
        username="newauthor",
        email="newauthor@example.com",
        password="authorpassword",
    )
    author_token = get_token_for_user(
        email="newauthor@example.com",
        password="authorpassword",
    )

    work_resp = client.post(
        "/works/",
        json={
            "title": "Unfunded Work",
            "description": "No supports yet",
            "content": "Work in progress.",
        },
        headers={"Authorization": f"Bearer {author_token}"},
    )
    assert work_resp.status_code == status.HTTP_201_CREATED
    work_id = work_resp.json()["id"]

    # Call details endpoint on work with no supports
    details_resp = client.get(f"/works/{work_id}/details")
    assert details_resp.status_code == status.HTTP_200_OK
    details = details_resp.json()

    # Verify total_support is 0
    assert Decimal(str(details["total_support"])) == Decimal("0")
    assert details["author"]["id"] == author.id

