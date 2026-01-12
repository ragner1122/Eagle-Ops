from backend.app.auth import hash_password
from backend.app.models import User


def test_login_success(client, db_session):
    user = User(
        email="auth@eagleops.io",
        hashed_password=hash_password("AuthPass123"),
        role="Admin",
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "auth@eagleops.io", "password": "AuthPass123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]


def test_login_invalid_password(client, db_session):
    user = User(
        email="authfail@eagleops.io",
        hashed_password=hash_password("RightPass123"),
        role="Analyst",
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "authfail@eagleops.io", "password": "WrongPass"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"
