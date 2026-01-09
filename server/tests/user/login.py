import requests

BASE_URL = "http://localhost:8000/user"

def test_login_success():
    payload = {
        "email": "john@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/login", json=payload, params={"remember": False})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] is not None

def test_login_failure():
    payload = {
        "email": "john@example.com",
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=payload, params={"remember": False})
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_login_missing_fields():
    payload = {
        "email": "john@example.com"
        # Missing password field
    }
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data