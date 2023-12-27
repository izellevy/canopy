# test_auth.py
from fastapi.testclient import TestClient
from main import app
from canopy_server.auth.token_manager import create_jwt_token
from datetime import timedelta

client = TestClient(app)

def test_protected_route_with_valid_token():
    # Generate a JWT token
    token_subject = "test_user"
    token_expiration = timedelta(minutes=15)
    jwt_token = create_jwt_token(token_subject, token_expiration)

    # Test accessing the protected route with a valid token
    response = client.get("/protected", headers={"Authorization": f"Bearer {jwt_token}"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data and "current_user" in data
    assert data["current_user"] == token_subject

def test_protected_route_with_expired_token():
    # Generate an expired JWT token
    token_subject = "expired_user"
    expired_jwt_token = create_jwt_token(token_subject, timedelta(seconds=-1))

    # Test accessing the protected route with an expired token
    response = client.get("/protected", headers={"Authorization": f"Bearer {expired_jwt_token}"})
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data and "Token has expired" in data["detail"]

def test_protected_route_with_invalid_token():
    # Generate a JWT token with an invalid signature
    invalid_jwt_token = "invalid_token"

    # Test accessing the protected route with an invalid token
    response = client.get("/protected", headers={"Authorization": f"Bearer {invalid_jwt_token}"})
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data and "Could not validate credentials" in data["detail"]

def test_protected_route_without_token():
    # Test accessing the protected route without a token when authorization is enabled
    response = client.get("/protected")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data and "current_user" in data
    assert data["current_user"] == "dummy_user"

def test_protected_route_without_token_when_auth_disabled():
    # Test accessing the protected route without a token when authorization is disabled
    response = client.get("/protected", headers={"Authorization": "Bearer "})  # Empty token
    assert response.status_code == 200
    data = response.json()
    assert "message" in data and "current_user" in data
    assert data["current_user"] == "dummy_user"